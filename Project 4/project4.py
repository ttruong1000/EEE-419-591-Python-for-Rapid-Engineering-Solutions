# Driving hspice to find the optimal high-to-low propagation delay for an inverter train of increasing integer fan size 

import numpy as np                                                                                                                                                    # For extracting data from .csv files
import subprocess                                                                                                                                                     # For running subprocesses
import shutil                                                                                                                                                         # For copying files
import sys                                                                                                                                                            # For obtaining the maximum integer value that Python can print

optimal_num_inverters = 0                                                                                                                                             # Initialize the number of inverters used in the inverter train
optimal_fan_size = 0                                                                                                                                                  # Initialize the base fan size of each inverter
optimal_tphl = sys.maxsize                                                                                                                                            # Initialize the high-to-low propagation delay as a maximum value to spot the minimum easier
num_internal_inverters = 1                                                                                                                                            # Set the initial number of internal inverters to 1 (2 inverters are already placed at the beginning and end of the inverter train)
while num_internal_inverters < 13:                                                                                                                                    # While the number of internal inverters is less than 2(6) + 1 = 13
    fan_size = 2                                                                                                                                                      # Set the initial base fan size of the inverter to 2
    while fan_size < 10:                                                                                                                                              # While the fan size is less than 10
        shutil.copy("InvChainTemplate.sp", "InvChain.sp")                                                                                                             # Copy the templated hspice file to a file that will be manipulated
        hspice_file = open("InvChain.sp", "a")                                                                                                                        # Open this copied hspice file
        index = 0                                                                                                                                                     # Set the index to 0
        hspice_file.write(".param fan = " + str(fan_size) + "\n")                                                                                                     # Insert the fan size line
        hspice_file.write("Xinv1 a b inv M=1" + "\n")                                                                                                                 # Insert the first inverter in the inverter train
        while index < num_internal_inverters:                                                                                                                         # For each (index)-th internal inverters (index = 0)
            hspice_file.write("Xinv" + str(index + 2) + " " + chr(ord("a") + index + 1) + " " + chr(ord("a") + index + 2) + " inv M=fan**" + str(index + 1) + "\n")   # Insert the (i + 1)-internal inverter in the inverter train
            index += 1                                                                                                                                                # Increase the index (number of internal inverters) by 1
        hspice_file.write("Xinv" + str(index + 2) + " " + chr(ord("a") + index + 1) + " z inv M=fan**" + str(index + 1) + "\n")                                       # Insert the last inverter in the inverter train
        hspice_file.write(".end")                                                                                                                                     # End the hspice file
        hspice_file.close()                                                                                                                                           # Close the hspice file
        proc = subprocess.Popen(["hspice", "InvChain.sp"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)                                                        # Run hspice on the completed copied file
        output, err = proc.communicate()                                                                                                                              # Communicate with this subprocess (hspice) to produce a .csv file of desired values
        data = np.recfromcsv("InvChain.mt0.csv", comments = "$", skip_header = 3)                                                                                     # Extract the data from the hspice output
        tphl = data["tphl_inv"]                                                                                                                                       # Extract the high-to-low propagation delay from the hspice output
        print(f"Number of Inverters = {num_internal_inverters + 2}") 
        print(f"Integer Fan Size = {fan_size}")
        print(f"High-to-Low Propagation Delay, tphl = {tphl}\n")
        if tphl < optimal_tphl:                                                                                                                                       # If the high-to-low propagation delay found from the current hspice output is less than that for preivous iterations
            optimal_num_inverters = num_internal_inverters + 2                                                                                                        # Set the optimal number of inverters to be the number of inverters that give this minimum high-to-low propagation delay
            optimal_fan_size = fan_size                                                                                                                               # Set the optimal fan size to be the fan size of the inverter that give this minimum high-to-low propagation delay
            optimal_tphl = tphl                                                                                                                                       # Set the optimal high-to-low propagation delay to be this value
        fan_size += 1                                                                                                                                                 # Increase the fan size by 1 for the next iteration with the same number of internal inverters
    num_internal_inverters += 2                                                                                                                                       # Increase the number of internal inverters by 2 for the next iteration (so that a high-to-low propagation delay exists)
print(f"Optimal Number of Inverters = {optimal_num_inverters}")
print(f"Optimal Integer Fan Size = {optimal_fan_size}")
print(f"Optimal High-to-Low Propagation Delay, tphl = {optimal_tphl}")