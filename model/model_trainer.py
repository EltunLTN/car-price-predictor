import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import pickle
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, 'data', 'car_data.csv')
model_path = os.path.join(script_dir, 'car_price_model.pkl')

print("Məlumatlar yüklənir...")
df = pd.read_csv(csv_path)

print("Məlumatlar təmizlənir...")
df.dropna(inplace=True)

# Dəyərləri rəqəm tipinə çeviririk (YENİLƏNMİŞ: 'muherrik' əlavə edildi)
df['il'] = pd.to_numeric(df['il'], errors='coerce')
df['yurus'] = pd.to_numeric(df['yurus'], errors='coerce')
df['muherrik'] = pd.to_numeric(df['muherrik'], errors='coerce')
df['qiymet'] = pd.to_numeric(df['qiymet'], errors='coerce')

df.dropna(subset=['il', 'yurus', 'muherrik', 'qiymet'], inplace=True)
df = df.astype({'il': int, 'yurus': int, 'qiymet': int, 'muherrik': float})

df = df[(df['qiymet'] > 1000) & (df['qiymet'] < 200000)]
df = df[df['yurus'] < 1000000]

# DƏYİŞİKLİK: Təlim üçün istifadə ediləcək xüsusiyyətlərə 'muherrik' əlavə edildi
features = ['marka', 'model', 'il', 'yurus', 'muherrik']
target = 'qiymet'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# DƏYİŞİKLİK: Rəqəm tipli xüsusiyyətlərə 'muherrik' əlavə edildi
categorical_features = ['marka', 'model']
numeric_features = ['il', 'yurus', 'muherrik']

preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'
)

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])

print(f"{len(X_train)} məlumat üzərində model təlim edilir...")
pipeline.fit(X_train, y_train)

print("Modelin performansı yoxlanılır...")
predictions = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Test məlumatları üzrə orta mütləq xəta (MAE): {mae:.2f} AZN")

print("Hazır model yadda saxlanılır...")
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"✅ Model uğurla yaradıldı və '{model_path}' faylına yazıldı.")