# Determine I-V characteristics for a diode and optimize parameters for a diode to match given diode data

import numpy as np                                                                                                                                               # For extracting methods for arrays
import matplotlib.pyplot as plt                                                                                                                                  # For extracting plotting functions
from scipy import optimize                                                                                                                                       # For extracting the function solver (fsolve, root solver) and least squares (leastsq, minimization) optimization functions

# Problems 1 and 2 Shared Parameters
I_S = 1e-9                                                                                                                                                       # Saturation current (A)
Q = 1.6021766208e-19                                                                                                                                             # Elementary charge of an electron (C)
K_B = 1.3806452e-23                                                                                                                                              # Boltzmann constant (J/K)
V_STEP = 0.1                                                                                                                                                     # Voltage step and initial guess for the voltage of the diode (V)

# Problem 1 Distinct Parameters
N_IDEALITY_P1 = 1.7                                                                                                                                              # Ideality constant n for Problem 1
T_P1 = 350                                                                                                                                                       # Temperature constant (K) for Problem 1
R_P1 = 11e3                                                                                                                                                      # Resistance constant (Ohms) for Problem 1

# Problem 2 Distinct Parameters
A = 1e-8                                                                                                                                                         # Cross-sectional area constant of the diode (in m^2) for Problem 2
T_P2 = 375                                                                                                                                                       # Temperature constant (in Kelvins) for Problem 2
PHI = 0.8                                                                                                                                                        # Initial guess for the built-in diode potential phi (V) for Problem 2
N_IDEALITY_P2 = 1.5                                                                                                                                              # Initial guess for the ideality constant n for Problem 2
R_P2 = 10e3                                                                                                                                                      # Initial guess for the resistance R (Ohms) for Problem 2

# Problem 1
# Compute the voltage of the diode at a particular source voltage and diode voltage iteratively
def compute_V_diode(V_diode, R, V_source, I_s, n_ideality, T):
    return V_diode / R - V_source / R + I_s*(np.exp((Q * V_diode) / (n_ideality * K_B * T)) - 1)

# Compute the current of the diode at a particular diode voltage iteratively
def compute_I_diode(I_s, V_diode, n_ideality, T):
    return I_s * (np.exp((Q * V_diode) / (n_ideality * K_B * T)) - 1)

# Compute the current and voltage of the diode over a range of source voltages and an initial diode voltage
def compute_V_I_diode_estimate(V_diode, R, V_source, I_s, n_ideality, T):
    V_diode_estimate = np.zeros_like(V_source)                                                                                                                   # Set up the diode voltages array
    I_diode_estimate = np.zeros_like(V_source)                                                                                                                   # Set up the diode currents array
    for index in range(len(V_source)):                                                                                                                           # For each entry in the range of source voltages
        V_diode = optimize.fsolve(compute_V_diode, V_diode, (R, V_source[index], I_s, n_ideality, T), xtol = 1e-12)[0]                                           # Calculate the diode voltage at the indexed source voltage
        V_diode_estimate[index] = V_diode                                                                                                                        # Put this diode voltage in the diode voltages array
        I_diode = compute_I_diode(I_s, V_diode, n_ideality, T)                                                                                                   # Calculate the diode current at the diode voltage at the indexed source voltage
        I_diode_estimate[index] = I_diode                                                                                                                        # Put this diode current in the diode currents array
    return V_diode_estimate, I_diode_estimate                                                                                                                    # Return both the estimated diode voltages and currents

V_source = np.arange(V_STEP, 2.5 + V_STEP, V_STEP)                                                                                                               # Set up the source voltage sweep array (from 0.1 V to 2.5 V with steps of 0.1 V)
V_diode_estimate, I_diode_estimate = compute_V_I_diode_estimate(V_STEP, R_P1, V_source, I_S, N_IDEALITY_P1, T_P1)                                                # Compute the estimated diode voltage and currents
plt.plot(V_source, I_diode_estimate, label = "log(Diode Current) vs. Source Voltage")                                                                            # Plot the estimated diode current against the source voltage
plt.plot(V_diode_estimate, I_diode_estimate, label = "log(Diode Current) vs. Diode Voltage")                                                                     # Plot the estimated diode current against the estimated diode voltage
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.yscale("log")
plt.title('I-V Characteristics for a Diode - Source and Diode Voltage')
plt.legend()
plt.show()

# Problem 2
# Optimize the value of phi
def optimize_phi(phi, n_ideality, R, V_source, I_diode_estimate):
    I_s = A * T_P2**2 * np.exp(-(phi * Q) / (K_B * T_P2))                                                                                                        # Calculate the (new) reverse bias saturation current with a new phi value
    V_diode, I_actual = compute_V_I_diode_estimate(V_STEP, R, V_source, I_s, n_ideality, T_P2)                                                                   # Calculate the new diode voltage and current with a new phi value
    return (I_diode_estimate - I_actual)/(I_diode_estimate + I_actual + 1e-15)                                                                                   # Return the normalized residual error between the previous current and the calculated current with a new phi value

# Optimize the value of the ideality constant n
def optimize_n_ideality(n_ideality, phi, R, V_source, I_diode_estimate):
    I_s = A * T_P2**2 * np.exp(-(phi * Q) / (K_B * T_P2))                                                                                                        # Calculate the reverse bias saturation current with a new ideality constant value
    V_diode, I_actual = compute_V_I_diode_estimate(V_STEP, R, V_source, I_s, n_ideality, T_P2)                                                                   # Calculate the new diode voltage and current with a new ideality constant value
    return (I_diode_estimate - I_actual)/(I_diode_estimate + I_actual + 1e-15)                                                                                   # Return the normalized residual error between the previous current and the calculated current with a new ideality constant value

# Optimize the value of the resistance R
def optimize_R(R, n_ideality, phi, V_source, I_diode_estimate):
    I_s = A * T_P2**2 * np.exp(-(phi * Q) / (K_B * T_P2))                                                                                                        # Calculate the reverse bias saturation current with a new resistance value
    V_diode, I_actual = compute_V_I_diode_estimate(V_STEP, R, V_source, I_s, n_ideality, T_P2)                                                                   # Calculate the new diode voltage and current with a new resistance value
    return (I_diode_estimate - I_actual)/(I_diode_estimate + I_actual + 1e-15)                                                                                   # Return the normalized residual error between the previous current and the calculated current with a new resistance value

DiodeIV = np.loadtxt('DiodeIV.txt', dtype = 'float64')                                                                                                           # Extract the text file of data
V_source_DiodeIV, I_diode_DiodeIV = DiodeIV[:,0], DiodeIV[:,1]                                                                                                   # Assign the diode voltages and currents from the text file of the data
optimal_phi = PHI                                                                                                                                                # Assign an initial guess for the optimal value of phi
optimal_n_ideality = N_IDEALITY_P2                                                                                                                               # Assign an initial guess for the optimal value of the ideality constant n
optimal_R = R_P2                                                                                                                                                 # Assign an initial guess for the optimal value of the resistance
iterations = 1                                                                                                                                                   # Set iteration counter
not_optimizing = False                                                                                                                                           # Set condition to start and stop optimizing

# Order of optimization matters! R is optimized first, then the ideality constant, and then the phi value.
while(not not_optimizing):                                                                                                                                       # Start optimizing; for each iteration that does not reach the desired error (tolerance)
    print(f"Iteration {iterations}")
    optimal_R = optimize.leastsq(optimize_R, optimal_R, args = (optimal_n_ideality, optimal_phi, V_source_DiodeIV, I_diode_DiodeIV))[0][0]                       # Optimize the value of the resistance R by minimizing the least squares difference of the residuals in the optimize_R output
    print(f"Optimal R = {optimal_R} Ohms")
    optimal_n_ideality = optimize.leastsq(optimize_n_ideality, optimal_n_ideality, args = (optimal_phi, optimal_R, V_source_DiodeIV, I_diode_DiodeIV))[0][0]     # Optimize the value of the ideality constant by minimizing the least squares difference of the residuals in the optimize_n_ideality output
    print(f"Optimal Ideality n = {optimal_n_ideality}")
    optimal_phi = optimize.leastsq(optimize_phi, optimal_phi, args = (optimal_n_ideality, optimal_R, V_source_DiodeIV, I_diode_DiodeIV))[0][0]                   # Optimize the value of phi by minimizing the least squares difference of the residuals in the optimize_phi output
    print(f"Optimal phi = {optimal_phi} V")
    residuals_R = optimize_R(optimal_R, optimal_n_ideality, optimal_phi, V_source_DiodeIV, I_diode_DiodeIV)                                                      # Find the residuals (accumulated errors matrix at each source voltage and diode current) for the resistance (R) values
    residuals_n_ideality = optimize_n_ideality(optimal_n_ideality, optimal_phi, optimal_R, V_source_DiodeIV, I_diode_DiodeIV)                                    # Find the residuals (accumulated errors matrix at each source voltage and diode current) for the ideality constant (n) values
    residuals_phi = optimize_phi(optimal_phi, optimal_n_ideality, optimal_R, V_source_DiodeIV, I_diode_DiodeIV)                                                  # Find the residuals (accumulated errors matrix at each source voltage and diode current) for the phi values
    average_error_R = sum(abs(residuals_R)) / len(residuals_R)                                                                                                   # Find the average error of the resistance  R via taking the average of the residual matrix for R
    average_error_n_ideality = sum(abs(residuals_n_ideality)) / len(residuals_n_ideality)                                                                        # Find the average error of the ideality constant n via taking the average of the residual matrix for n
    average_error_phi = sum(abs(residuals_phi)) / len(residuals_phi)                                                                                             # Find the average error of phi via taking the average of the residual matrix for phi
    print(f"Average Residual Error for R = {average_error_R} Ohms")
    print(f"Average Residual Error for Ideality n = {average_error_n_ideality}")
    print(f"Average Residual Error for phi = {average_error_phi} V\n")
    if(average_error_R < 1e-8 and average_error_n_ideality < 1e-8 and average_error_phi < 1e-8):                                                                 # If the average residual error for the resistance, the ideality constant, and phi is less than 1e-8
        not_optimizing = True                                                                                                                                    # Stop optimizing
    else:                                                                                                                                                        # Otherwise,
        iterations += 1                                                                                                                                          # Perform another iteration of optimization

optimal_I_s = A * T_P2**2 * np.exp(-(optimal_phi * Q) / (K_B * T_P2))                                                                                            # Use the optimized phi value to find the new optimized reverse saturation current bias I_s
V_diode_estimate, I_diode_estimate = compute_V_I_diode_estimate(V_STEP, optimal_R, V_source_DiodeIV, optimal_I_s, optimal_n_ideality, T_P2)                      # Use the optimized I_s, 
plt.plot(V_source_DiodeIV, I_diode_DiodeIV, label = "log(I_diode) vs. V_source, From DiodeIV", marker = 'x')                                                     # Plot the diode current against the source voltage with the DiodeIV.txt
plt.plot(V_source_DiodeIV, I_diode_estimate, label = "log(I_diode) vs. V_source, Optimized Parameters", marker = 'o')                                            # Plot the estimated diode current with optimized parameters against the source voltage
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
plt.yscale("log")
plt.title('IV Characteristics for a Diode - Real Data and Optimized Parameters')
plt.legend()
plt.show()