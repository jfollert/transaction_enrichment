import pandas as pd
import requests
import argparse
import os

def main(file_path, sheet_name):
    # Leer base_url de una variable de entorno o usar un valor por defecto
    base_url = os.getenv('BASE_URL', 'http://127.0.0.1:8000/')
    url = base_url.rstrip('/') + '/categories/' 

    # Cargar datos
    categorias_df = pd.read_excel(file_path, sheet_name=sheet_name)

    for _, row in categorias_df.iterrows():
        category_id = row['id']
        api_url = f"{url}{category_id}/" 

        data = {
            'name': row['name'],
            'type': row['type'],
        }

        response = requests.put(api_url, json=data)

        if response.status_code == 201:
            print(f"Categoría {row['name']} importada con éxito.")
        elif response.status_code == 204:
            print(f"Categoría {row['name']} actualizada con éxito.")
        else:
            print(f"Error al importar la categoría {row['name']}: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importar datos de categorías desde un archivo Excel a la API.")
    parser.add_argument('--file', type=str, default='transactions.xlsx', help='Ruta al archivo Excel que contiene las categorías.')
    parser.add_argument('--sheet', type=str, default='Categorías', help='Nombre de la hoja del Excel para importar. Por defecto es "Categorías".')

    args = parser.parse_args()
    main(args.file_path, args.sheet)
