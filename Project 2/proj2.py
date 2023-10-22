# Perform PCA analysis on sonar data for mines versus the surrounding rocks

import numpy as np                                                                                                                                      # For extracting methods for arrays
import matplotlib.pyplot as plt                                                                                                                         # For extracting plotting functions
import pandas as pd                                                                                                                                     # For extracting CSV files
from sklearn.model_selection import train_test_split                                                                                                    # For splitting the CSV into training and testing data
from sklearn.preprocessing import StandardScaler                                                                                                        # For standardizing the dataset for each feature to align with the normal distribution so that each feature has equal spread
from sklearn.neural_network import MLPClassifier                                                                                                        # For extracting the MLP (multi-layer Perceptron) machine learning model
from sklearn.decomposition import PCA                                                                                                                   # For extracting the PCA (Principal Component Analysis) machine learning model
from sklearn.metrics import accuracy_score, confusion_matrix                                                                                            # For finding the accuracy of the prediction in each machine learning model against the test data

sonar_all_data = pd.read_csv('sonar_all_data_2.csv', header = None)                                                                                     # Extract the CSV file

X = sonar_all_data[np.arange(0, 60)]                                                                                                                    # Assign the input variables
y = sonar_all_data[[60]]                                                                                                                                # Assign the output variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)                                                            # Instantiate the input and output training and test data

sc = StandardScaler()                                                                                                                                   # Initialize the standard scaler
sc.fit(X_train)                                                                                                                                         # Compute the transformation required from the training data
X_train_std = sc.transform(X_train)                                                                                                                     # Apply the transformation to the training data
X_test_std = sc.transform(X_test)                                                                                                                       # Apply the same transformation to the test data

y_pred_mlp_accuracy_values = []                                                                                                                         # Initialize an array storing all accuracy values for PCA component analysis with a varying number of components used
y_pred_mlp_max_accuracy = 0.0                                                                                                                           # Initialize a value that stores the maximum accuracy obtained in the PCA component analysis
y_pred_mlp_max_array = []                                                                                                                               # Initialize an array storing the predicted values array that obtains the maximum accuracy compared against the test data
n_components_max = 0                                                                                                                                    # Initialize a value that store the number of components required in the PCA component analysis to obtain the maximum accuracy
for n in range(1, 60 + 1):                                                                                                                              # For each component number ranging up to the maximum number of time samples in the data
    pca = PCA(n_components = n)                                                                                                                         # Initialize the PCA (Principal Component Analysis) with n components
    X_train_pca = pca.fit_transform(X_train_std)                                                                                                        # Apply the PCA to the training data
    X_test_pca = pca.transform(X_test_std)                                                                                                              # Apply the same PCA to the test data
    sonar_mlp = MLPClassifier(hidden_layer_sizes = (100), activation = 'logistic', max_iter = 2000, alpha = 0.00001, solver = 'adam', tol = 0.0001)     # Initialize the multi-layer Perceptron machine learning model with optimal parameters
    sonar_mlp.fit(X_train_pca, y_train.values.ravel())                                                                                                  # Train the multi-layer Perceptron model with the training data
    y_pred_mlp_array = sonar_mlp.predict(X_test_pca)                                                                                                    # Predict the output variable with the test data
    y_pred_mlp_accuracy_values.append(accuracy_score(y_test, y_pred_mlp_array))                                                                         # Add the accuracy value obtained from running PCA/MLP with n components to the array that stores all accuracy values
    if accuracy_score(y_test, y_pred_mlp_array) > y_pred_mlp_max_accuracy:                                                                              # If the maximum accuracy is found
        y_pred_mlp_max_accuracy = accuracy_score(y_test, y_pred_mlp_array)                                                                              # Set the new maximum accuracy to this variable
        y_pred_mlp_max_array = y_pred_mlp_array                                                                                                         # Set the predicted values array that obtains the highest accuracy to the test data to this variable
        n_components_max = n                                                                                                                            # Set the number of components required to achieve the highest accuracy to this variable
    print('Accuracy for PCA with MLP, Test Data: %.2f' % accuracy_score(y_test, y_pred_mlp_array))                                                      # Print the accuracy achieved in the PCA component analysis for n components
    print('Number of PCA Components:', n)                                                                                                               # Print the number of components used in the PCA component analysis
print('Maximum Accuracy for PCA with MLP, Test Data: %.2f' % y_pred_mlp_max_accuracy)                                                                   # Print the maximum accuracy achieved in the PCA component analysis
print('Number of PCA Components to Achieve Maximum Accuracy:', n_components_max)                                                                        # Print the number of components required for the PCA component analysis to obtain the desired accuracy

confuse_matrix = confusion_matrix(y_test, y_pred_mlp_max_array)                                                                                         # Generate the confusion matrix from the PCA/MLP machine learning model
print(confuse_matrix)                                                                                                                                   # Print this confusion matrix

n_components_values = np.arange(1, 60 + 1)                                                                                                              # Generate the total list of the number of components analyzed in the PCA component analysis
plt.plot(n_components_values, y_pred_mlp_accuracy_values)                                                                                               # Plot each accuracy value attained at each component increment in the PCA component analysis
plt.xlabel("Number of PCA Components")
plt.ylabel("Accuracy Value for PCA with MLP")
plt.title("Accuracy Value for PCA with MLP on Number of PCA Components")
plt.show()