# Read a netlist from a spice-like text file; create a list of lists

import comp_constants as COMP                             # Get the constants needed for lists
from sys import exit                                      # Needed to exit on error

def read_netlist():                                       # Read a netlist - no input argument!
    filename = input("enter netlist text file name: ")    # Ask for the netlist
    fh = open(filename,"r")                               # Open the file
    lines = fh.readlines()                                # Read the file
    fh.close()                                            # Close the file

    netlist = []                                          # Initialize our list
    for line in lines:                                    # For each component
        line = line.strip()                               # Strip CR/LF
        if line:                                          # Skip empty lines

            # reads: name, from, to, value
            # so we need to insert the node type at the start of the list
            props = line.split(" ")                       # Parse properties delimited by spaces

            if props[COMP.TYPE][0] == COMP.RESIS:         # is it a resistor?
                props.insert(COMP.TYPE,COMP.R)            # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                netlist.append(props)                     # add to our netlist

            elif props[COMP.TYPE][0:2] == COMP.V_SRC:     # a voltage source?
                props.insert(COMP.TYPE,COMP.VS)           # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                netlist.append(props)                     # add to our netlist

            elif props[COMP.TYPE][0:2] == COMP.I_SRC:     # a current source?
                props.insert(COMP.TYPE,COMP.IS)           # insert type
                props[COMP.I]   = int(props[COMP.I])      # convert from string
                props[COMP.J]   = int(props[COMP.J])      # convert from string
                props[COMP.VAL] = float(props[COMP.VAL])  # convert from string
                netlist.append(props)                     # add to our netlist

            else:                                         # Unknown component!
                print("Unknown component type:\n",line)   # Bad data!
                exit()                                    # Bail!

    return netlist