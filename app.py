from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import os

app = Flask(__name__)

# --- Model və Data Yollarını Təyin Etmək ---
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'model', 'car_price_model.pkl')
data_path = os.path.join(script_dir, 'data', 'car_data.csv')

# --- Modeli Yükləmək ---
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# --- Datanı Yükləmək və Hazırlamaq ---
car_data = pd.read_csv(data_path)
# Markaları və modelləri hazırlayırıq
makes = sorted(car_data['marka'].unique())
# Hər markaya uyğun modelləri bir lüğətdə saxlayırıq
models_by_make = {make: sorted(car_data[car_data['marka'] == make]['model'].unique()) for make in makes}

# --- Əsas Səhifə ---
@app.route('/')
def home():
    # Marka siyahısını HTML şablona göndəririk
    return render_template('index.html', makes=makes)

# --- Modelləri Dinamik Gətirmək üçün API ---
@app.route('/get_models/<make>')
def get_models(make):
    # Seçilmiş markaya uyğun modelləri qaytarırıq
    models = models_by_make.get(make, [])
    return jsonify(models)

# --- Qiymət Təxmini üçün API ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # DİQQƏT: 'muherrik' də əlavə edildi
    input_data = pd.DataFrame([data], columns=['marka', 'model', 'il', 'yurus', 'muherrik'])

    input_data['il'] = pd.to_numeric(input_data['il'])
    input_data['yurus'] = pd.to_numeric(input_data['yurus'])
    input_data['muherrik'] = pd.to_numeric(input_data['muherrik'])

    prediction = model.predict(input_data)
    output = round(prediction[0])
    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(debug=True)