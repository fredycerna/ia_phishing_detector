import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Ruta de entrada y salida
input_csv = "./data/phishing_dataset_urls.csv"
output_dir = "./data/raw/phishing_archived/"
os.makedirs(output_dir, exist_ok=True)

# Configuración de Chrome headless
options = Options()
options.headless = True
options.add_argument('--window-size=1280,1024')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# Función para obtener snapshot de Wayback Machine
def get_wayback_url(original_url):
    try:
        response = requests.get(f"https://archive.org/wayback/available?url={original_url}")
        if response.status_code == 200:
            data = response.json()
            if data.get("archived_snapshots"):
                return data["archived_snapshots"]["closest"]["url"]
    except Exception as e:
        print(f"Error consultando {original_url}: {e}")
    return None

# Leer CSV y procesar
df = pd.read_csv(input_csv)
for index, row in df.iterrows():
    url = row["url"]
    snapshot = get_wayback_url(url)
    if snapshot:
        try:
            driver.get(snapshot)
            time.sleep(4)
            path = os.path.join(output_dir, f"archived_{index+1:03}.png")
            driver.save_screenshot(path)
            print(f"Capturado: {path}")
        except Exception as e:
            print(f"Error en {snapshot}: {e}")
    else:
        print(f"Sin snapshot: {url}")

driver.quit()
