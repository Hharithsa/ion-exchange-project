from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

import pandas as pd
import base64
import os

from methods import rf, lr, gb
from helper import clear_uploads_directory

app = Flask(__name__)
api = Api(app)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'data_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html') 

class Values(Resource):
    def get(self): 

        algo = request.args.get('algo')
        target_column = request.args.get('target')

        match algo:
            case "rf":
                mse, mae, r2, buf = rf.GetRFValues(target_column)
            case "lr":
                mse, mae, r2, buf = lr.GetLRValues(target_column) 
            case "gb":
                mse, mae, r2, buf = gb.GetGBValues(target_column)

        return jsonify( 
            mse=mse, 
            mae=mae, 
            r2=r2,  
            plot=base64.b64encode(buf.getvalue()).decode('utf-8'))

class DataFiles(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"})

        if file:    
            # Clear the uploads directory
            clear_uploads_directory()
            
            # Save the file with a secure filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read the Excel file to get column names
            try:
                df = pd.read_excel(filepath, engine='openpyxl')
                column_names = df.columns.tolist()  # Extract column names
                return jsonify(columns= column_names)
            except Exception as e:
                return jsonify(error= str(e))

api.add_resource(Values, "/values")
api.add_resource(DataFiles, "/data-files")

if __name__ == '__main__':
    app.run(debug=True)
