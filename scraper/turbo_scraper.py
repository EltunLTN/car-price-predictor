import requests
from bs4 import BeautifulSoup
import csv
import time
import os

HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, 'data')
os.makedirs(data_dir, exist_ok=True)
csv_path = os.path.join(data_dir, 'car_data.csv')

BASE_URL = "https://turbo.az/autos"

csv_file = open(csv_path, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['marka', 'model', 'il', 'yurus', 'muherrik', 'qiymet'])

print("Təkmilləşdirilmiş skript işə salındı. Məlumatlar toplanır...")
data_found_count = 0

for page in range(1, 1971):
    print(f"{page}-ci səhifə analiz edilir...")
    url = f"{BASE_URL}?page={page}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', class_='products-i')

        if not products:
            print(f"Səhifə {page}-də elan tapılmadı.")
            continue
        
        for product in products:
            marka, model, il, yurus, muherrik, qiymet = None, None, None, None, None, None
            
            name_div = product.find('div', class_='products-i__name')
            if name_div:
                full_name = name_div.text.strip()
                name_parts = full_name.split()
                marka = name_parts[0] if len(name_parts) > 0 else None
                model = ' '.join(name_parts[1:]) if len(name_parts) > 1 else None

            price_div = product.find('div', class_='products-i__price')
            if price_div:
                qiymet_text = price_div.text.strip()
                qiymet = ''.join(filter(str.isdigit, qiymet_text))

            attributes_div = product.find('div', class_='products-i__attributes')
            if attributes_div:
                attributes_text = attributes_div.text.strip()
                attributes_parts = attributes_text.split(',')
                
                if len(attributes_parts) > 0:
                    il = ''.join(filter(str.isdigit, attributes_parts[0]))
               
                if len(attributes_parts) > 1:
                    engine_text = attributes_parts[1].strip()
                    muherrik = ''.join(c for c in engine_text if c.isdigit() or c == '.')
                
                if len(attributes_parts) > 2:
                    yurus_raw = attributes_parts[2].strip()
                    yurus = ''.join(filter(str.isdigit, yurus_raw))

            if all([marka, model, il, yurus, muherrik, qiymet]):
                csv_writer.writerow([marka, model, il, yurus, muherrik, qiymet])
                data_found_count += 1

    except requests.exceptions.RequestException as e:
        print(f"Səhifəyə daxil olarkən xəta baş verdi: {e}")
    
    time.sleep(1.5)

csv_file.close()

print(f"\n✅ Skrapinq uğurla tamamlandı. Cəmi {data_found_count} avtomobil məlumatı toplandı.")
