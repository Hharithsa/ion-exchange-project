#Seawater ultrasonic Velocity Regression model
import pandas as pd
import os
import io 

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

def GetLRValues(target):
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
    train_data, test_data, train_target, test_target = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

    # Create the Linear Regression model
    lr_model = LinearRegression()

    # Fit the model to the training data
    lr_model.fit(train_data, train_target)

    # Make predictions on the test data
    predictions = lr_model.predict(test_data)

    # Calculate evaluation metrics
    mse = mean_squared_error(test_target, predictions)
    mae = mean_absolute_error(test_target, predictions)
    r2 = r2_score(test_target, predictions)


    buf = io.BytesIO()

    # Plotting a straight line
    plt.figure(figsize=(10, 6))
    plt.plot(test_target, test_target, label='Straight Line', color='blue')
    plt.scatter(test_target, predictions, color='red', label='Data Points')
    plt.title('Prediction of Seawater Ultrasonic Velocity using Linear Regression Model', fontweight='bold')
    plt.xlabel('Actual Ultrsonic Velocity (m/s)', fontweight='bold')
    plt.ylabel('Predicted DensityUltrasonic Velocity (m/s)', fontweight='bold')
    plt.legend()
    plt.savefig(buf, format='png')

    buf.seek(0)
    plt.close()

    return mse, mae, r2, buf