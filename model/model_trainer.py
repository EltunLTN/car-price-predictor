import pandas as pd
import numpy as np # Logarifma üçün numpy əlavə edirik
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import pickle
import os

# ... (fayl yollarını təyin edən hissə eyni qalır) ...
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
csv_path = os.path.join(project_root, 'data', 'car_data.csv')
model_path = os.path.join(script_dir, 'car_price_model.pkl')

print("Məlumatlar yüklənir...")
df = pd.read_csv(csv_path)
# ... (məlumatların təmizlənməsi eyni qalır) ...
print("Məlumatlar təmizlənir...")
df.dropna(inplace=True)
df['il'] = pd.to_numeric(df['il'], errors='coerce')
df['yurus'] = pd.to_numeric(df['yurus'], errors='coerce')
df['muherrik'] = pd.to_numeric(df['muherrik'], errors='coerce')
df['qiymet'] = pd.to_numeric(df['qiymet'], errors='coerce')
df.dropna(subset=['il', 'yurus', 'muherrik', 'qiymet'], inplace=True)
df = df.astype({'il': int, 'yurus': int, 'qiymet': int, 'muherrik': float})
df = df[(df['qiymet'] > 1000) & (df['qiymet'] < 2000000)] # Lüks maşınları saxlamaq üçün yuxarı limiti artırırıq
df = df[df['yurus'] < 1000000]

features = ['marka', 'model', 'il', 'yurus', 'muherrik']
target = 'qiymet'

X = df[features]
y = df[target]

# ƏSAS DƏYİŞİKLİK: Qiymətin (y) logarifmasını götürürük
# np.log1p(y) = np.log(y + 1) deməkdir, 0 qiymətindən qorunmaq üçün istifadə olunur
y_log = np.log1p(y)

# Modeli orijinal y ilə deyil, logarifmlənmiş y_log ilə təlim edirik
X_train, X_test, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)

# ... (pipeline yaradılması eyni qalır) ...
categorical_features = ['marka', 'model']
numeric_features = ['il', 'yurus', 'muherrik']
preprocessor = ColumnTransformer(transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)], remainder='passthrough')
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])


print(f"{len(X_train)} məlumat üzərində model təlim edilir...")
# DƏYİŞİKLİK: Modeli logarifmlənmiş dəyərlərlə təlim edirik
pipeline.fit(X_train, y_train_log)

# ... (modeli yadda saxlamaq eyni qalır) ...
print("Hazır model yadda saxlanılır...")
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"✅ Model uğurla yaradıldı və '{model_path}' faylına yazıldı.")