import pandas as pd
import os
import io 

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
from helper import get_features

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


def GetRFValues(target):
    # Set the file path
    folder = 'data_files'
    files = os.listdir(folder)
    file_path = os.path.join(folder, files[0])
    data = pd.read_excel(file_path)
    # Remove rows with missing values
    data.dropna(inplace=True)

    column_names = data.columns.tolist()

    # Select the feature columns
    features = get_features(column_names, target)

    # Split the data into training and testing sets
    train_data, test_data, train_target, test_target = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

    # Impute missing values in the training data
    imputer = SimpleImputer(strategy='mean')
    train_data_imputed = pd.DataFrame(imputer.fit_transform(train_data), columns=train_data.columns)

    # Impute missing values in the testing data
    test_data_imputed = pd.DataFrame(imputer.transform(test_data), columns=test_data.columns)

    # Create the Random Forest Regressor model
    rf_regressor = RandomForestRegressor()

    # Fit the regressor to the imputed training data
    rf_regressor.fit(train_data_imputed, train_target)

    # Perform predictions on the imputed test data
    predictions = rf_regressor.predict(test_data_imputed)

    # Calculate the mean squared error, mean absolute error, and R-squared
    mse = mean_squared_error(test_target, predictions)
    mae = mean_absolute_error(test_target, predictions)
    r2 = r2_score(test_target, predictions)

    buf = io.BytesIO()

    # Plotting a straight line
    plt.figure(figsize=(10, 6))
    plt.plot(test_target, test_target, label='Straight Line', color='blue')
    plt.scatter(test_target, predictions, color='red', label='Data Points')
    plt.title('Prediction of Seawater Density using Random Forest Regression Model', fontweight='bold')
    plt.xlabel('Actual Density (kg/m³)', fontweight='bold')  # Use '\u00b3' for superscript 3
    plt.ylabel('Predicted Density (kg/m³)', fontweight='bold')
    plt.legend()
    plt.savefig(buf, format='png')

    buf.seek(0)
    plt.close()

    return mse, mae, r2, buf