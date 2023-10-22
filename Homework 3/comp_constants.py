# Constants for solving resistor networks with voltage and/or current sources

# Define some constants we'll use to reference things
RESIS = 'R'      # A resistor
V_SRC = 'VS'     # A voltage source
I_SRC = 'IS'     # A current source

# Define the list data structure that we'll use to hold components:
# [ Type, Name, i, j, Value ]; set up an index for each component's property
TYPE = 0         # A voltage source or resistor
NAME = 1         # The name of the component
I    = 2         # The "from" node of the component 
J    = 3         # The "to" node of the component
VAL  = 4         # The value of the component

# Define the different types of component
R    = 0         # A resistor
VS   = 1         # An independent voltage source
IS   = 2         # An independent current source