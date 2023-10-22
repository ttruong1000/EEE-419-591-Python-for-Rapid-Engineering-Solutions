# Ensemble learning with Project 1 machine learning results on heart1.csv data

import pandas as pd                                                                                                                  # For extracting CSV files
from sklearn.model_selection import train_test_split                                                                                 # For splitting the CSV into training and testing data
from sklearn.preprocessing import StandardScaler                                                                                     # For standardizing the dataset for each feature to align with the normal distribution so that each feature has equal spread
from sklearn.linear_model import Perceptron, LogisticRegression                                                                      # For extracting the Perceptron and Logistic Regression machine learning models
from sklearn.svm import SVC                                                                                                          # For extracting the Support Vector Machine machine learning model
from sklearn.tree import DecisionTreeClassifier                                                                                      # For extracting the Decision Tree machine learning model
from sklearn.ensemble import RandomForestClassifier                                                                                  # For extracting the Random Forest machine learning model
from sklearn.neighbors import KNeighborsClassifier                                                                                   # For extracting the K-Nearest Neighbor machine learning model
from sklearn.ensemble import VotingClassifier                                                                                        # For extracting ensemble machine learning methods (Voting Classifier)
from sklearn.metrics import accuracy_score                                                                                           # For finding the accuracy of the prediction in each machine learning model against the test data

heart_data = pd.read_csv('heart1.csv')                                                                                               # Extract the CSV file

X = heart_data[['age', 'sex', 'cpt', 'rbp', 'sc', 'fbs', 'rer', 'mhr', 'eia', 'opst', 'dests', 'nmvcf', 'thal']]                     # Assign the input variables
y = heart_data[['a1p2']]                                                                                                             # Assign the output variable
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)                                         # Instantiate the input and output training and test data

sc = StandardScaler()                                                                                                                # Initialize the standard scaler
sc.fit(X_train)                                                                                                                      # Compute the transformation required from the training data
X_train_std = sc.transform(X_train)                                                                                                  # Apply the transformation to the training data
X_test_std = sc.transform(X_test)                                                                                                    # Apply the same transformation to the test data

# Perceptron
heart_perceptron = Perceptron(max_iter = 25, tol = 1e-3, eta0 = 0.00001, fit_intercept = True, random_state = 0, verbose = True)     # Initialize the Perceptron machine learning model with optimal parameters
heart_perceptron.fit(X_train_std, y_train.values.ravel())                                                                            # Train the Perceptron model with the training data
y_pred_perceptron = heart_perceptron.predict(X_test_std)                                                                             # Predict the output variable with the test data
print('Accuracy for Perceptron, Test Data: %.2f' % accuracy_score(y_test, y_pred_perceptron))                                        # Print the accuracy of this model against the test data

# Logistic Regression
heart_logistic_regression = LogisticRegression(C = 0.25, solver = 'liblinear', multi_class = 'ovr', random_state = 0)                # Initialize the Logistic Regression machine learning model with optimal parameters
heart_logistic_regression.fit(X_train_std, y_train.values.ravel())                                                                   # Train the Logistic Regression model with the training data
y_pred_logistic_regression = heart_logistic_regression.predict(X_test_std)                                                           # Predict the output variable with the test data
print('Accuracy for Logistic Regression, Test Data: %.2f' % accuracy_score(y_test, y_pred_logistic_regression))                      # Print the accuracy of this model against the test data

# Support Vector Machine (pick one version) [Linear. C = 0.2 for similar accuracy results]
heart_svm_rbf = SVC(kernel = 'rbf', C = 0.175, random_state = 0)                                                                     # Initialize the SVC machine learning model with optimal parameters
heart_svm_rbf.fit(X_train_std, y_train.values.ravel())                                                                               # Train the SVC model with the training data
y_pred_svm_rbf = heart_svm_rbf.predict(X_test_std)                                                                                   # Predict the output variable with the test data
print('Accuracy for SVM, RBF, Test Data: %.2f' % accuracy_score(y_test, y_pred_svm_rbf))                                             # Print the accuracy of this model against the test data

# Decision Tree Learning
heart_decision_tree = DecisionTreeClassifier(criterion = 'entropy', max_depth = 3, random_state = 0)                                 # Initialize the Decision Tree machine learning model with optimal parameters
heart_decision_tree.fit(X_train, y_train.values.ravel())                                                                             # Train the Decision Tree model with the training data
y_pred_decision_tree = heart_decision_tree.predict(X_test)                                                                           # Predict the output variable with the test data
print('Accuracy for Decision Tree, Test Data: %.2f' % accuracy_score(y_test, y_pred_decision_tree))                                  # Print the accuracy of this model against the test data

# Random Forest
heart_random_forest = RandomForestClassifier(criterion = 'entropy', n_estimators = 200, random_state = 1, n_jobs = 5)                # Initialize the Random Forest machine learning model with optimal parameters
heart_random_forest.fit(X_train, y_train.values.ravel())                                                                             # Train the Random Forest model with the training data
y_pred_random_forest = heart_random_forest.predict(X_test)                                                                           # Predict the output variable with the test data
print('Accuracy for Random Forest, Test Data: %.2f' % accuracy_score(y_test, y_pred_random_forest))                                  # Print the accuracy of this model against the test data

# K-Nearest Neighbor (find the best value of K)
heart_knn = KNeighborsClassifier(n_neighbors = 25, p = 2, metric = 'minkowski')                                                      # Initialize the K-Nearest Neighbors machine learning model with optimal parameters
heart_knn.fit(X_train_std, y_train.values.ravel())                                                                                   # Train the K-Nearest Neighbors model with the training data
y_pred_knn = heart_knn.predict(X_test_std)                                                                                           # Predict the output variable with the test data
print('Accuracy for K-Nearest Neighbor, Test Data: %.2f' % accuracy_score(y_test, y_pred_knn))                                       # Print the accuracy of this model against the test data

# Ensemble Learning - Voting Classifier
final_model_1 = VotingClassifier(estimators = [('Logistic Regression', heart_logistic_regression), 
                                               ('SVC', heart_svm_rbf), 
                                               ('Perceptron', heart_perceptron)], voting = 'hard')                                   # Making the final ensemble machine model using the voting classifier with the top three classifiers
final_model_2 = VotingClassifier(estimators = [('Logistic Regression', heart_logistic_regression), 
                                               ('SVC', heart_svm_rbf), 
                                               ('Perceptron', heart_perceptron), 
                                               ('K-Nearest Neighbors', heart_knn)], voting = 'hard')                                 # Making the final ensemble machine model using the voting classifier with the top four classifiers
final_model_3 = VotingClassifier(estimators = [('Logistic Regression', heart_logistic_regression), 
                                               ('SVC', heart_svm_rbf), 
                                               ('Perceptron', heart_perceptron), 
                                               ('K-Nearest Neighbors', heart_knn), 
                                               ('Random Forest', heart_random_forest)], voting = 'hard')                             # Making the final ensemble machine model using the voting classifier with the top five classifiers

final_model_1.fit(X_train_std, y_train.values.ravel())                                                                               # Training the ensemble model on the training data set for the voting classifier with the top three classifiers
final_model_2.fit(X_train_std, y_train.values.ravel())                                                                               # Training the ensemble model on the training data set for the voting classifier with the top four classifiers
final_model_3.fit(X_train_std, y_train.values.ravel())                                                                               # Training the ensemble model on the training data set for the voting classifier with the top five classifiers

y_pred_final_1 = final_model_1.predict(X_test_std)                                                                                   # Predict the output variable with the test data for the voting classifier with the top three classifiers
y_pred_final_2 = final_model_2.predict(X_test_std)                                                                                   # Predict the output variable with the test data for the voting classifier with the top four classifiers
y_pred_final_3 = final_model_3.predict(X_test_std)                                                                                   # Predict the output variable with the test data for the voting classifier with the top five classifiers

# Accuracy improves for ensemble learning using the top three machine learning methods; increased by 1%
print('Accuracy for Ensemble Learning, Top Three Methods: %.2f' % accuracy_score(y_test, y_pred_final_1))                            # Print the accuracy of the ensemble model for the voting classifier with the top three classifiers
prediction_sum_1 = y_pred_logistic_regression + y_pred_svm_rbf + y_pred_perceptron                                                   # Take the sum of the predicted output variable arrays from the top three classifiers
heart_disease_count_1 = 0                                                                                                            # Initialize how many entries classify heart disease
no_heart_disease_count_1 = 0                                                                                                         # Initialize how many entries does not classify heart disease
for i in prediction_sum_1:                                                                                                           # For each entry in the summed array
    if prediction_sum_1[i] >= 4.5:                                                                                                   # If the entry at index i is at least 6 (1.5 times the number of methods used for the voting classifier)
        heart_disease_count_1 += 1                                                                                                   # Classify this as heart disease
    else:                                                                                                                            # Else, if the entry at index i is less than 6
        no_heart_disease_count_1 += 1                                                                                                # Classify this as not heart disease
if(heart_disease_count_1 == int(1 / 2 * len(prediction_sum_1))):                                                                     # If the number of entries of heart disease matches half the size of the the summed array (tie case)
    print('Were ties counted in the voting in the ensemble learning for three methods?: Yes')                                        # Print that ties were counted in the voting classifier
else:                                                                                                                                # Else, if the number of entries of heart disease does not match half the size of the the summed array (no tie case)
    print('Were ties counted in the voting in the ensemble learning for three methods?: No')                                         # Print that no ties were counted in the voting classifier

# Accuracy does not improve for ensemble learning using the top four machine learning methods; decreases by 1%
print('Accuracy for Ensemble Learning, Top Four Methods: %.2f' % accuracy_score(y_test, y_pred_final_2))                             # Print the accuracy of the ensemble model for the voting classifier with the top four classifiers
prediction_sum_2 = y_pred_logistic_regression + y_pred_svm_rbf + y_pred_perceptron + y_pred_knn                                      # Take the sum of the predicted output variable arrays from the top four classifiers
heart_disease_count_2 = 0                                                                                                            # Initialize how many entries classify heart disease
no_heart_disease_count_2 = 0                                                                                                         # Initialize how many entries does not classify heart disease
for i in prediction_sum_2:                                                                                                           # For each entry in the summed array
    if prediction_sum_2[i] >= 6:                                                                                                     # If the entry at index i is at least 6 (1.5 times the number of methods used for the voting classifier)
        heart_disease_count_2 += 1                                                                                                   # Classify this as heart disease
    else:                                                                                                                            # Else, if the entry at index i is less than 6
        no_heart_disease_count_2 += 1                                                                                                # Classify this as not heart disease
if(heart_disease_count_2 == int(1 / 2 * len(prediction_sum_2))):                                                                     # If the number of entries of heart disease matches half the size of the the summed array (tie case)
    print('Were ties counted in the voting in the ensemble learning for four methods?: Yes')                                         # Print that ties were counted in the voting classifier
else:                                                                                                                                # Else, if the number of entries of heart disease does not match half the size of the the summed array (no tie case)
    print('Were ties counted in the voting in the ensemble learning for four methods?: No')                                          # Print that no ties were counted in the voting classifier

# Accuracy is the same for ensemble learning using the top five machine learning methods as that for the best performing machine learning method used
print('Accuracy for Ensemble Learning, Top Five Methods: %.2f' % accuracy_score(y_test, y_pred_final_3))                             # Print the accuracy of the ensemble model for the voting classifier with the top five classifiers
prediction_sum_3 = y_pred_logistic_regression + y_pred_svm_rbf + y_pred_perceptron + y_pred_knn + y_pred_random_forest               # Take the sum of the predicted output variable arrays from the top five classifiers
heart_disease_count_3 = 0                                                                                                            # Initialize how many entries classify heart disease
no_heart_disease_count_3 = 0                                                                                                         # Initialize how many entries does not classify heart disease
for i in prediction_sum_3:                                                                                                           # For each entry in the summed array
    if prediction_sum_3[i] >= 7.5:                                                                                                   # If the entry at index i is at least 6 (1.5 times the number of methods used for the voting classifier)
        heart_disease_count_3 += 1                                                                                                   # Classify this as heart disease
    else:                                                                                                                            # Else, if the entry at index i is less than 6
        no_heart_disease_count_3 += 1                                                                                                # Classify this as not heart disease
if(heart_disease_count_3 == int(1 / 2 * len(prediction_sum_3))):                                                                     # If the number of entries of heart disease matches half the size of the the summed array (tie case)
    print('Were ties counted in the voting in the ensemble learning for five methods?: Yes')                                         # Print that ties were counted in the voting classifier
else:                                                                                                                                # Else, if the number of entries of heart disease does not match half the size of the the summed array (no tie case)
    print('Were ties counted in the voting in the ensemble learning for five methods?: No')                                          # Print that no ties were counted in the voting classifier