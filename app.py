from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np 
import os

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'model', 'car_price_model.pkl')
data_path = os.path.join(script_dir, 'data', 'car_data.csv')
with open(model_path, 'rb') as f:
    model = pickle.load(f)
car_data = pd.read_csv(data_path)
makes = sorted(car_data['marka'].unique())
models_by_make = {make: sorted(car_data[car_data['marka'] == make]['model'].unique()) for make in makes}

@app.route('/')
def home():
    return render_template('index.html', makes=makes)
@app.route('/get_models/<make>')
def get_models(make):
    models = models_by_make.get(make, [])
    return jsonify(models)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    input_data = pd.DataFrame([data], columns=['marka', 'model', 'il', 'yurus', 'muherrik'])
    input_data['il'] = pd.to_numeric(input_data['il'])
    input_data['yurus'] = pd.to_numeric(input_data['yurus'])
    input_data['muherrik'] = pd.to_numeric(input_data['muherrik'])
    log_prediction = model.predict(input_data)
    prediction = np.expm1(log_prediction)
    
    output = round(prediction[0])
    return jsonify({'prediction': output})


if __name__ == '__main__':
    app.run(debug=True)
