# Program to solve resister networks with voltage and/or current sources using nodal analysis

# Import necessary packages for calculations
import numpy as np                                                                               # For extracting methods for arrays
from numpy.linalg import solve                                                                   # For extracting methods needed to solve systems of equations using matrices
from read_netlist import read_netlist                                                            # Supplied function to read the netlist
import comp_constants as COMP                                                                    # For extracting common constants

# Obtain the dimensions of the initial admittance matrix based on the number of nodes in the circuit defined by the netlist
def get_dimensions(netlist):
    node_cnt = 0                                                                                 # Intialize a count for the number of nodes in the circuit netlist
    for component in range(len(netlist)):                                                        # For each component in the netlist
        if netlist[component][COMP.I] > node_cnt:                                                # If the component's node i is greater than the count
            node_cnt = netlist[component][COMP.I]                                                # Update this count
        elif netlist[component][COMP.J] > node_cnt:                                              # Else, if the component's node j is greater than the count
            node_cnt = netlist[component][COMP.J]                                                # Update this count
    return node_cnt                                                                              # Return the node count (ASSUMPTION: All nodes are nonnegative integers from 0 to N, where N is the number of nodes in the matrix)
                                                                                                 # Note that node 0 is ground, which is omitted in the matrix and the matrix dimension. Therefore, all nontrivial nodes are positive integers from 1 to N.

# Stamp each component in the circuit (resistors and independent voltage/current sources) under the correct matrix (admittance and current matrices)
def stamper(netlist, admittances, currents):
    for component in netlist:                                                                    # For each component in the netlist
        i, j = component[COMP.I] - 1, component[COMP.J] - 1                                      # Adjust the i, j index to deal with Python arrays starting at index 0
        # Resistors have positive voltage if the nodes i, j connecting each resistor form a circular nodal link
        # Example: (node 1 < node 2 < node 3 < node 4 < node 5 < ... < node k) and (node k > node 0) is a circular nodal link if each resistor is connected by taking consecutive pairs in the chained inequality,
        #          where (node 0 < node 1) would be an independent voltage/current source
        if component[COMP.TYPE] == COMP.R:                                                       # If the component is a resistor
            if i >= 0:                                                                           # If i is at least 0
                admittances[i, i] += 1.0/component[COMP.VAL]                                     # Stamp the positive admittance of the resistor at (i, i)
            if j >= 0:                                                                           # If j is at least 0
                admittances[j, j] += 1.0/component[COMP.VAL]                                     # Stamp the positive admittance of the resistor at (j, j)
            if i >= 0 and j >= 0:                                                                # If both i and j is at least 0
                admittances[i, j] -= 1.0/component[COMP.VAL]                                     # Stamp the negative admittance of the resistor at (i, j)
                admittances[j, i] -= 1.0/component[COMP.VAL]                                     # Stamp the negative admittance of the resistor at (j, i)
        # Independent voltage sources between node i and node j
        elif component[COMP.TYPE] == COMP.VS:                                                    # If the component is an independent voltage source
            rows = len(admittances)                                                              # Count the current number of rows in the admittance matrix
            admittances = np.hstack((admittances, np.atleast_2d(np.zeros(rows, float)).T))       # Add a row of zeros in the admittance matrix to increase the row dimension of the admittance matrix by 1
            admittances = np.vstack((admittances, np.atleast_2d(np.zeros(rows + 1, float))))     # Add a column of zeros in the admittance matrix to increase the column dimension of the admittance matrix by 1
            currents = np.resize(currents, rows + 1)                                             # Add another row (of one zero) in the current matrix to increase the row dimension of the current matrix by 1
            if i >= 0:                                                                           # If i is at least 0
                admittances[rows, i], admittances[i, rows] = 1, 1                                # Stamp the admittance matrix with 1 at (rows, i), (i, rows)
            if j >= 0:                                                                           # If j is at least 0
                admittances[rows, j], admittances[j, rows] = -1, -1                              # Stamp the admittance matrix with -1 at (rows, j), (j, rows)
            currents[rows] += component[COMP.VAL]                                                # Stamp the current matrix with the value of the voltage source
                                                                                                 # With an independent voltage source, the voltage matrix will solve for both the voltages at all of the nodes and currents flowing through each independent voltage source
        # Independent current sources flow from node i to node j
        elif component[COMP.TYPE] == COMP.IS:                                                    # If the component is an independent current source
            if i >= 0:                                                                           # If i is at least 0
                currents[i] -= component[COMP.VAL]                                               # Stamp the current matrix with the negative independent current source value at node i
            if j >= 0:                                                                           # If j is at least 0
                currents[j] += component[COMP.VAL]                                               # Stamp the current matrix with the negative independent current source value at node j
    return admittances, currents                                                                 # Return the updated admittance matrix and current matrix

netlist = read_netlist()                                                                         # Read the netlist
node_cnt = get_dimensions(netlist)                                                               # Obtain the initial dimensions of the (square) matrix by counting the number of nodes in the circuit netlist
admittances, currents = np.zeros((node_cnt, node_cnt), float), np.zeros(node_cnt, float)         # Initialize the admittance matrix and current matrix with zeros
admittances, currents = stamper(netlist, admittances, currents)                                  # Stamp the admittance matrix and current matrix with their proper values based off of the netlist contents
print(solve(admittances, currents))                                                              # Solve for the voltage matrix, which may include
                                                                                                 #      (1) only voltages
                                                                                                 #           - given at least one independent current source
                                                                                                 #      (2) both voltages and currents 
                                                                                                 #           - given at least one independent voltage source 
                                                                                                 #           - given at least one independent voltage source and at least one current source