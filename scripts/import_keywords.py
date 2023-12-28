import pandas as pd
import requests
import argparse
import os

def main(file_path, sheet_name):
    # Leer base_url de una variable de entorno o usar un valor por defecto
    base_url = os.getenv('BASE_URL', 'http://127.0.0.1:8000/')
    url = base_url.rstrip('/') + '/keywords/' 

    # Cargar datos
    keywords_df = pd.read_excel(file_path, sheet_name=sheet_name)

    for _, row in keywords_df.iterrows():
        keyword_id = row['id']
        api_url = f"{url}{keyword_id}/" 

        data = {
            'keyword': row['keyword'],
            'merchant_id': row['merchant_id']
        }

        response = requests.put(api_url, json=data)

        if response.status_code == 201:
            print(f"Keyword {row['keyword']} importada con éxito.")
        elif response.status_code == 204:
            print(f"Keyword {row['keyword']} actualizada con éxito.")
        else:
            print(f"Error al importar la Keyword {row['keyword']}: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importar datos de keywords desde un archivo Excel a la API.")
    parser.add_argument('--file', type=str, default='transactions.xlsx', help='Ruta al archivo Excel que contiene las keywords.')
    parser.add_argument('--sheet', type=str, default='Keywords', help='Nombre de la hoja del Excel para importar. Por defecto es "Keywords".')

    args = parser.parse_args()
    main(args.file, args.sheet)
