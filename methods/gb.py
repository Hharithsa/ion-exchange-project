import pandas as pd
import numpy as np
import os
import io 

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

def GetGBValues(target):

    # Set the file path
    folder = 'data_files'
    files = os.listdir(folder)
    file_path = os.path.join(folder, files[0])
    data = pd.read_excel(file_path)
    # Remove rows with missing values
    data.dropna(inplace=True)

    # Select the feature columns
    features = []

    column_names = data.columns.tolist()
    for column in column_names:
        if column != target:
            features.append(column)

    print(features)
    print(target)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

    # Create a pipeline with an imputer and the GradientBoostingRegressor
    pipeline = make_pipeline(SimpleImputer(strategy='mean', missing_values=np.nan), GradientBoostingRegressor())

    # Fit the pipeline on the training data
    pipeline.fit(X_train, y_train)

    # Make predictions on the testing data
    predictions = pipeline.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    buf = io.BytesIO()

    # Plotting a straight line
    plt.figure(figsize=(10, 6))
    plt.plot(y_test, y_test, label='Straight Line', color='blue')
    plt.scatter(y_test, predictions, color='red', label='Data Points')
    plt.title('Prediction of Seawater Specific Heat using GB Regressor Model',fontweight='bold')
    plt.xlabel('Actual Specific Heat (kJ/kg.K)', fontweight='bold')  # Use '\u00b3' for superscript 3
    plt.ylabel('Predicted Specific Heat (kJ/kg.K)', fontweight='bold')
    plt.legend()

    plt.savefig(buf, format='png')

    buf.seek(0)
    plt.close()

    return mse, mae, r2, buf