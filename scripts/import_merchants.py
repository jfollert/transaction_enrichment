import pandas as pd
import requests
import argparse
import os

def main(file_path, sheet_name):
    # Leer base_url de una variable de entorno o usar un valor por defecto
    base_url = os.getenv('BASE_URL', 'http://127.0.0.1:8000/')
    url = base_url.rstrip('/') + '/merchants/' 

    # Cargar datos
    comercios_df = pd.read_excel(file_path, sheet_name=sheet_name)

    for _, row in comercios_df.iterrows():
        merchant_id = row['id']
        api_url = f"{url}{merchant_id}/" 

        data = {
            'merchant_name': row['merchant_name'],
            'merchant_logo': row['merchant_logo'] if not pd.isna(row['merchant_logo']) else ''
        }

        # Agregar category_id solo si existe
        if not pd.isna(row['category_id']):
            data['category_id'] = row['category_id']

        response = requests.put(api_url, json=data)

        if response.status_code == 201:
            print(f"Comercio {row['merchant_name']} creado con éxito.")
        elif response.status_code == 204:
            print(f"Comercio {row['merchant_name']} actualizado con éxito.")
        else:
            print(f"Error al procesar el Comercio {row['merchant_name']}: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importar datos de comercios desde un archivo Excel a la API.")
    parser.add_argument('--file', type=str, default='./transactions.xlsx', help='Ruta al archivo Excel que contiene los comercios.')
    parser.add_argument('--sheet', type=str, default='Comercios', help='Nombre de la hoja del Excel para importar. Por defecto es "Comercios".')

    args = parser.parse_args()
    main(args.file, args.sheet)
