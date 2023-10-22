# Wealth After 70 Years Calculator using PySimpleGUI

import numpy as np                                                                                                                        # For extracting methods for arrays
import matplotlib.pyplot as plt                                                                                                           # For extracting plotting functions
import locale                                                                                                                             # For extracting US currency formatting
import PySimpleGUI as sg                                                                                                                  # For extracting high-level GUI functions

MAX_YEARS = 70                                                                                                                            # Maximum number of years used for wealth analysis

FN_MEAN_RETURN         = 'Mean Return (%)'                                                                                                # Field name for mean return
FN_STD_DEV_RETURN      = 'Standard Deviation Return (%)'                                                                                  # Field name for the standard deviaion of return
FN_YEARLY_CONTRIB      = 'Yearly Contribution ($)'                                                                                        # Field name for yearly contribution
FN_NUM_YEARS_CONTRIB   = 'Number of Years of Contribution'                                                                                # Field name for number of years of contribution
FN_NUM_YEARS_RETIRE    = 'Number of Years to Retirement'                                                                                  # Field name for number of years to retirement
FN_ANNUAL_RETIRE_SPEND = 'Annual Retirement Spending ($)'                                                                                 # Field name for annual retirement spending

FIELD_NAMES = [FN_MEAN_RETURN, FN_STD_DEV_RETURN, FN_YEARLY_CONTRIB, 
               FN_NUM_YEARS_CONTRIB, FN_NUM_YEARS_RETIRE, FN_ANNUAL_RETIRE_SPEND]                                                         # Field names list layout

B_QUIT = 'Quit'                                                                                                                           # Instantiate the name for the quit button
B_CALCULATE = 'Calculate'                                                                                                                 # Instantiate the name for the calculate button

NUM_FIELDS = 6                                                                                                                            # Number of fields in the field names list

# Once the calculate button is pressed, run this function to do the wealth analysis 10 times, calculate the average wealth after retirement, and plot each of the analyses on one graph
def calculate_and_plot_wealth(window, entries):
    sum_wealth_at_retirement = 0                                                                                                          # Instantiate a variable that takes the running sum of the wealth after retirement for each of the 10 analyses
    for i in range(1, 11):                                                                                                                # For each n-th analysis, up to 10 analyses
        noise = float(entries[FN_STD_DEV_RETURN]) / 100 * np.random.randn(MAX_YEARS)                                                      # Instantiate a noise list of 70 (MAX_YEARS) values of random values to demonstrate randomness in wealth across 70 (MAX_YEARS) years
        wealth_by_year = [0]                                                                                                              # Keep track of the amount of wealth earned each year, which resets per analysis
        for year in range(1, MAX_YEARS + 1):                                                                                              # For each year i, up to 70 (MAX_YEARS) years
            wealth_by_year.append(calculate_next_wealth(wealth_by_year[year - 1], year, noise, entries))                                  # Calculate the wealth earned at the i-th year
            if year == int(entries[FN_NUM_YEARS_RETIRE]):                                                                                 # If year i reaches the number of years to retirement
                sum_wealth_at_retirement += wealth_by_year[year - 1]                                                                      # Add the wealth earned the immediate year before retirement to the running sum of the wealth after retirement
            if wealth_by_year[year] < 0:                                                                                                  # If the wealth at the i-th year is less than $0
                wealth_by_year[year] = 0.0                                                                                                # Assign the wealth at the i-th year to $0, as the wealth cannot be below $0
                break                                                                                                                     # Break from the n-th analysis
        wealth_plot(wealth_by_year)                                                                                                       # Once each n-th analysis is done, up to 10 analyses, graph the wealth across all valid years where a non-negative wealth was recorded
    plt.xlabel("Year")
    plt.ylabel("Wealth")
    plt.title("Wealth Over 70 Years")
    plt.show()
    locale.setlocale(locale.LC_ALL, '')                                                                                                   # Set the locale for all categories (for currency formatting)
    window['OUTPUT'].update("Wealth After Retirement: " + locale.currency(sum_wealth_at_retirement / 10, grouping = True))                # Update the GUI console with the output text for the average wealth after retirement in the proper US currency formatting

# Calculate the wealth earned in the next year based off of wealth earned in the previous year (recursive, but the recursion is taken care of in the for-loop in the calculate_and_plot_wealth function)
def calculate_next_wealth(current_wealth, year, noise, entries):
    if year <= int(entries[FN_NUM_YEARS_CONTRIB]):                                                                                        # If the year is less than the number of years of contribution
        return current_wealth * (1 + float(entries[FN_MEAN_RETURN]) / 100 + noise[year - 1]) + float(entries[FN_YEARLY_CONTRIB])          # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), noise at that year, and the yearly contribution
    elif year > int(entries[FN_NUM_YEARS_CONTRIB]) and year < int(entries[FN_NUM_YEARS_RETIRE]):                                          # If the year is greater than the number of years of contribution and less than the number of years to retirement
        return current_wealth * (1 + float(entries[FN_MEAN_RETURN]) / 100 + noise[year - 1])                                              # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), and noise at that year
    else:                                                                                                                                 # Otherwise, retirement occurs until 70 (MAX_YEARS) years is reached
        return current_wealth * (1 + float(entries[FN_MEAN_RETURN]) / 100 + noise[year - 1]) - float(entries[FN_ANNUAL_RETIRE_SPEND])     # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), noise at that year, and the annual retirement spending

# After each analysis of wealth after 70 (MAX_YEARS) years, graph the wealth across all valid years where a non-negative wealth was recorded 
def wealth_plot(wealth_by_year):
    years = np.arange(1, len(wealth_by_year) + 1)                                                                                         # Generate the valid years in which the wealth values per year is nonnegative
    return plt.plot(years, wealth_by_year)                                                                                                # Return the plot of wealth against years, up to 70 (MAX_YEARS) years

layout = []                                                                                                                               # Start with an empty layout list for the PySimpleGUI GUI
for index in range(NUM_FIELDS):                                                                                                           # For each of the 6 (NUM_ENTRIES) field entries to create
    layout.append([sg.Text(FIELD_NAMES[index],size = (30,1)), sg.InputText(key = FIELD_NAMES[index],size = (10,1))])                      # Add the field name text name and the corresponding entry box from the fields name layout list
layout.append([sg.Text("", size=(30, 1), key = 'OUTPUT')])                                                                                # Add an output label returning the average wealth after retirement in the correct currency formatting
layout.append([sg.Button(B_QUIT), sg.Button(B_CALCULATE)])                                                                                # Add the quit and calculate buttons

window = sg.Window('Wealth After 70 Years', layout)                                                                                       # Start the GUI

while True:                                                                                                                               # While the GUI is running
    event, values = window.read()                                                                                                         # Continuously read the events happening in the window and values inputted in the entry boxes corresponding to the field name labels
    if event == sg.WIN_CLOSED or event == B_QUIT:                                                                                         # If the console window is closed or the 'Quit' button has been pressed
        break                                                                                                                             # The GUI stops running and closes out of the window; jump to window.close()
    if event == B_CALCULATE:                                                                                                              # If the console window spots that the 'Calculate' button has been pressed
        calculate_and_plot_wealth(window, values)                                                                                         # Calculate the average wealth at retirement and plot the wealth accumulated per year for 10 analyses

window.close()                                                                                                                            # Once the console window is closed or the 'Quit' button has been pressed, end the program

########################################################################################################################################################################################################################################################################################################
# Wealth After 70 Years Calculator using tkinter

# import numpy as np                                                                                                                                  # For extracting methods for arrays
# import matplotlib.pyplot as plt                                                                                                                     # For extracting plotting functions
# import locale                                                                                                                                       # For extracting US currency formatting
# from tkinter import *                                                                                                                               # For extracting low-level GUI functions

# MAX_YEARS = 70                                                                                                                                      # Maximum number of years used for wealth analysis

# FIELD_NAMES = ['Mean Return (%)', 'Standard Deviation Return (%)', 'Yearly Contribution ($)', 
#                'Number of Years of Contribution', 'Number of Years to Retirement', 'Annual Retirement Spending ($)']                                # List of field names in the GUI

# F_MEAN_RETURN         = 0                                                                                                                           # Index for mean return in the field names list
# F_STD_DEV_RETURN      = 1                                                                                                                           # Index for standard deviation of return in the field names list
# F_YEARLY_CONTRIB      = 2                                                                                                                           # Index for yearly contribution in the field names list
# F_NUM_YEARS_CONTRIB   = 3                                                                                                                           # Index for number of years of contribution in the field names list
# F_NUM_YEARS_RETIRE    = 4                                                                                                                           # Index for number of years to retirement in the field names list
# F_ANNUAL_RETIRE_SPEND = 5                                                                                                                           # Index for annual retirement spending in the field names list

# NUM_FIELDS = 6                                                                                                                                      # Number of fields in the field names list

# Once the calculate button is pressed, run this function to do the wealth analysis 10 times, calculate the average wealth after retirement, and plot each of the analyses on one graph
# def calculate_and_plot_wealth(entries):
#     sum_wealth_at_retirement = 0                                                                                                                    # Instantiate a variable that takes the running sum of the wealth after retirement for each of the 10 analyses
#     for i in range(1, 11):                                                                                                                          # For each n-th analysis, up to 10 analyses
#         noise = float(entries[F_STD_DEV_RETURN].get()) / 100 * np.random.randn(MAX_YEARS)                                                           # Instantiate a noise list of 70 (MAX_YEARS) values of random values to demonstrate randomness in wealth across 70 (MAX_YEARS) years
#         wealth_by_year = [0]                                                                                                                        # Keep track of the amount of wealth earned each year, which resets per analysis
#         for year in range(1, MAX_YEARS + 1):                                                                                                        # For each year i, up to 70 (MAX_YEARS) years
#             wealth_by_year.append(calculate_next_wealth(wealth_by_year[year - 1], year, noise, entries))                                            # Calculate the wealth earned at the i-th year
#             if year == int(entries[F_NUM_YEARS_RETIRE].get()):                                                                                      # If year i reaches the number of years to retirement
#                 sum_wealth_at_retirement += wealth_by_year[year - 1]                                                                                # Add the wealth earned the immediate year before retirement to the running sum of the wealth after retirement
#             if wealth_by_year[year] < 0:                                                                                                            # If the wealth at the i-th year is less than $0
#                 wealth_by_year[year] = 0.0                                                                                                          # Assign the wealth at the i-th year to $0, as the wealth cannot be below $0
#                 break                                                                                                                               # Break from the n-th analysis
#         wealth_plot(wealth_by_year)                                                                                                                 # Once each n-th analysis is done, up to 10 analyses, graph the wealth across all valid years where a non-negative wealth was recorded
#     plt.xlabel("Year")
#     plt.ylabel("Wealth")
#     plt.title("Wealth Over 70 Years")
#     plt.show()
#     locale.setlocale(locale.LC_ALL, '')                                                                                                             # Set the locale for all categories (for currency formatting)
#     outputLabel.configure(text = "Wealth After Retirement: " + locale.currency(sum_wealth_at_retirement / 10, grouping = True))                     # Update the GUI console with the output text for the average wealth after retirement in the proper US currency formatting

# Calculate the wealth earned in the next year based off of wealth earned in the previous year (recursive, but the recursion is taken care of in the for-loop in the calculate_and_plot_wealth function)
# def calculate_next_wealth(current_wealth, year, noise, entries):
#     if year <= int(entries[F_NUM_YEARS_CONTRIB].get()):                                                                                             # If the year is less than the number of years of contribution
#         return current_wealth * (1 + float(entries[F_MEAN_RETURN].get()) / 100 + noise[year - 1]) + float(entries[F_YEARLY_CONTRIB].get())          # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), noise at that year, and the yearly contribution
#     elif year > int(entries[F_NUM_YEARS_CONTRIB].get()) and year < int(entries[F_NUM_YEARS_RETIRE].get()):                                          # If the year is greater than the number of years of contribution and less than the number of years to retirement
#         return current_wealth * (1 + float(entries[F_MEAN_RETURN].get()) / 100 + noise[year - 1])                                                   # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), and noise at that year
#     else:                                                                                                                                           # Otherwise, retirement occurs until 70 (MAX_YEARS) years is reached
#         return current_wealth * (1 + float(entries[F_MEAN_RETURN].get()) / 100 + noise[year - 1]) - float(entries[F_ANNUAL_RETIRE_SPEND].get())     # Return the next year's wealth in terms of the previous year's wealth, mean return (rate), noise at that year, and the annual retirement spending

# After each analysis of wealth after 70 (MAX_YEARS) years, graph the wealth across all valid years where a non-negative wealth was recorded
# def wealth_plot(wealth_by_year):
#     years = np.arange(1, len(wealth_by_year) + 1)                                                                                                   # Generate the valid years in which the wealth values per year is nonnegative
#     return plt.plot(years, wealth_by_year)                                                                                                          # Return the plot of wealth against years, up to 70 (MAX_YEARS) years

# Create and embed the fields for the GUI
# def makeform(root):
#     entries = []                                                                                                                                    # Start with an empty entries list for the GUI
#     for index in range(NUM_FIELDS):                                                                                                                 # For each of the 6 (NUM_ENTRIES) field entries to create
#         row = Frame(root)                                                                                                                           # Get the row in the GUI
#         label = Label(row, width = 30, text = FIELD_NAMES[index], anchor='w')                                                                       # Create the label at that row
#         entry = Entry(row)                                                                                                                          # Create the entry box for the label
#         row.pack(side=TOP, fill = X, padx = 5, pady =5 )                                                                                            # Place the row in the GUI
#         label.pack(side = LEFT)                                                                                                                     # Place the label in the GUI
#         entry.pack(side = RIGHT, expand = YES, fill = X)                                                                                            # Place the entry box in the GUI
#         entries.append(entry)                                                                                                                       # Add the entry box input to the entries list
#     return entries                                                                                                                                  # Return the entries list

# root = Tk()                                                                                                                                         # Create a tkinter GUI
# entries = makeform(root)                                                                                                                            # Create and embed the fields for the GUI

# outputRow = Frame(root)                                                                                                                             # Instantiate an output row above the Quit and Calculate buttons but below the input entry area to return the average wealth after retirement in the correct currency formatting
# outputRow.pack(side = TOP, fill = X, padx = 5, pady = 5)                                                                                            # Add an output row above the Quit and Calculate buttons but below the input entry area to return the average wealth after retirement in the correct currency formatting
# outputLabel = Label(outputRow, width = 30)                                                                                                          # Instantiate an output label returning the average wealth after retirement in the correct currency formatting
# outputLabel.pack(side = LEFT, expand = YES, fill = X)                                                                                               # Add this output label to the GUI

# button1 = Button(root, text = 'Quit', command = root.destroy)                                                                                       # Instantiate a quit button, embedding it with its proper default function
# button1.pack(side = LEFT, padx = 5, pady = 5)                                                                                                       # Add the quit button to the GUI

# button2 = Button(root, text = 'Calculate', command = (lambda e = entries: calculate_and_plot_wealth(e)))                                            # Instantiate a calculate button, embedding it with the calculate_and_plot_wealth function
# button2.pack(side = RIGHT, padx=5, pady=5)                                                                                                          # Add the calculate button to the GUI

# root.mainloop()                                                                                                                                     # Start executing the GUI; end the program when the 'Quit' button is pressed or the 'X' button is pressed on the top right corner of the console
########################################################################################################################################################################################################################################################################################################