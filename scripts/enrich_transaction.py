import pandas as pd
import requests
import argparse
import os
import json

def clean_nan_values(df):
    # Convertir todos los NaN a None
    return df.where(pd.notnull(df), None)

def main(file_path, sheet_name):
    # Leer base_url de una variable de entorno o usar un valor por defecto
    base_url = os.getenv('BASE_URL', 'http://127.0.0.1:8000/')
    url = base_url.rstrip('/') + '/transactions/'

    # Cargar datos
    transactions_df = pd.read_excel(file_path, sheet_name=sheet_name, keep_default_na=False)

    # Limpiar los datos para convertir NaN a None
    cleaned_df = clean_nan_values(transactions_df)

    # Preparar la lista de transacciones
    transactions = cleaned_df.to_dict(orient='records')

    # Enviar la solicitud POST
    response = requests.post(url, json=transactions)

    if response.status_code in [200, 201]:
        print("Transacciones importadas con éxito. Respuesta:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error al importar transacciones: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importar datos de transacciones desde un archivo Excel a la API.")
    parser.add_argument('--file', type=str, default='transactions.xlsx', help='Ruta al archivo Excel que contiene las transacciones.')
    parser.add_argument('--sheet', type=str, default='Transacciones', help='Nombre de la hoja del Excel para importar. Por defecto es "Transacciones".')

    args = parser.parse_args()
    main(args.file, args.sheet)
