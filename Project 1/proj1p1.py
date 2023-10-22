# Conduct a data analysis on the heart1.csv data

import numpy as np                                                                        # For extracting methods for arrays
import matplotlib.pyplot as plt                                                           # For extracting plotting functions
import pandas as pd                                                                       # For extracting CSV files
import seaborn as sns                                                                     # For extracting methods for the pair plot

heart_data = pd.read_csv('heart1.csv')                                                    # Extract the CSV file

heart_correlation = heart_data.corr().abs()                                               # Obtain the absolute value of the correlation matrix for the data
print(heart_correlation)                                                                  # Print the entire (symmetric) correlation matrix for the data
heart_correlation *= np.tri(*heart_correlation.values.shape, k = -1).T                    # Obtain the upper triangular of the correlation matrix
print(heart_correlation)                                                                  # Print the upper triangular of the correlation matrix
print(heart_correlation.unstack().copy().sort_values(ascending = False).head(n = 91))     # Print the top 10 correlations associated with the relationship between two variables
print(heart_correlation.unstack().get(key = "a1p2").sort_values(ascending = False))       # Print the correlations associated with the predicted variable

heart_covariance = heart_data.cov().abs()                                                 # Obtain the absolute value of the covariance matrix for the data
print(heart_covariance)                                                                   # Print the entire (symmetric) covariance matrix for the data
heart_covariance *= np.tri(*heart_covariance.values.shape, k = -1).T                      # Obtain the upper triangular of the covariance matrix
print(heart_covariance)                                                                   # Print the upper triangular of the covariance matrix
print(heart_covariance.unstack().copy().sort_values(ascending = False).head(n = 91))      # Print the top 10 covariances associated with the relationship between two variables
print(heart_covariance.unstack().get(key = "a1p2").sort_values(ascending = False))        # Print the covariances associated with the predicted variable

sns.set(style = 'whitegrid', context = 'notebook')                                        # Set the features for the pair plot
sns.pairplot(heart_data, height = 1.5)                                                    # Initialize the pair plot with the data
plt.show()                                                                                # Show the pair plot