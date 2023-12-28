# Enriquecimiento de Transacciones

API REST desarrollada en Django para enriquecer transacciones bancarias. Incorpora funcionalidades CRUD para manejar categorías, comercios y keywords, optimizando la comprensión y gestión de datos transaccionales.

## Configuración Inicial

1. Clonar el repositorio:

```bash
git clone https://github.com/jfollert/transaction_enrichment
```

2. Acceder al directorio del proyecto:
```bash
cd transaction_enrichment
```

3. Crear y activar un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar el Proyecto

Para ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Ejecutar Tests

Para ejecutar los tests:
```bash
python manage.py test
```

## Consideraciones
### Formato de las Transacciones

Cada transacción procesada por la API debe seguir el siguiente formato JSON:

```json
{
  "id": "uuid",
  "description": "Descripción de la transacción",
  "amount": monto_decimal,
  "date": "fecha_iso8601"
}
```

Es importante que las transacciones cumplan con este formato para garantizar un correcto procesamiento y enriquecimiento por parte de la API.

### Seguridad de la API
Actualmente, queda pendiente implementar un mecanismo de seguridad, como el uso de un API_KEY, para asegurar que solo clientes autorizados puedan acceder a los servicios de gestión de recursos y al proceso de enriquecimiento de transacciones.

## Scripts de Importación
### Importar Datos desde Excel

Utilice los scripts para importar datos de categorías, comercios y keywords desde archivos Excel:

- Importar categorías:
  ```bash
  python import_categories.py --file ruta/al/archivo.xlsx --sheet NombreDeLaHoja
  ```

- Importar comercios:
  ```bash
  python import_merchants.py --file ruta/al/archivo.xlsx --sheet NombreDeLaHoja
  ```

- Importar keywords:
  ```bash
  python import_keywords.py --file ruta/al/archivo.xlsx --sheet NombreDeLaHoja
  ```

### Procesar Transacciones desde Excel
Para procesar transacciones desde un archivo Excel y enriquecerlas usando la API:

```bash
python enrich_transaction.py --file ruta/al/archivo.xlsx --sheet NombreDeLaHoja
```

## Servicios CRUD

Los servicios CRUD para `Categorías`, `Comercios` y `Keywords` están disponibles en los siguientes endpoints, con los verbos HTTP correspondientes:

### Categorías (`/categories/`)
- `GET /categories/`: Listar todas las categorías.
- `POST /categories/`: Crear una nueva categoría (el ID es generado automáticamente).
- `PUT /categories/{id}`: Actualizar una categoría existente por su ID o crear una nueva con el ID especificado.
- `GET /categories/{id}`: Obtener una categoría por su ID.
- `DELETE /categories/{id}`: Eliminar una categoría por su ID.

### Comercios (`/merchants/`)
- `GET /merchants/`: Listar todos los comercios.
- `POST /merchants/`: Crear un nuevo comercio (el ID es generado automáticamente).
- `PUT /merchants/{id}`: Actualizar un comercio existente por su ID o crear uno nuevo con el ID especificado.
- `GET /merchants/{id}`: Obtener un comercio por su ID.
- `DELETE /merchants/{id}`: Eliminar un comercio por su ID.

### Keywords (`/keywords/`)
- `GET /keywords/`: Listar todas las keywords.
- `POST /keywords/`: Crear una nueva keyword (el ID es generado automáticamente).
- `PUT /keywords/{id}`: Actualizar una keyword existente por su ID o crear una nueva con el ID especificado.
- `GET /keywords/{id}`: Obtener una keyword por su ID.
- `DELETE /keywords/{id}`: Eliminar una keyword por su ID.

## Enriquecimiento de Transacciones

El proceso de enriquecimiento de transacciones se realiza a través de la siguiente lógica:

1. **Lectura de Datos**: El script `enrich_transaction.py` lee transacciones desde un archivo Excel y las envía al servicio de enriquecimiento utilizando la API.

2. **Extracción de Información**: Para cada transacción, se extrae información relevante como descripción, monto y fecha.

3. **Identificación de Keywords**: Se buscan coincidencias entre las descripciones de las transacciones y las keywords almacenadas en la base de datos.

4. **Enriquecimiento de Datos**: 
   - Si se encuentra una coincidencia de keyword, se enriquece la transacción con información del comercio y categoría asociados a esa keyword.
   - Se agregan campos adicionales a la transacción, como el nombre y logo del comercio, y el nombre y tipo de la categoría.

5. **Respuesta del Servicio**: 
   - Cada transacción enriquecida es devuelta con los detalles añadidos.
   - Se incluye información sobre el total de transacciones procesadas, la tasa de categorización y la tasa de identificación de comercios.

Este proceso permite a los usuarios obtener una visión más detallada y estructurada de sus transacciones, facilitando la gestión y análisis de datos financieros.

### Formato de Respuesta del Servicio de Enriquecimiento
El servicio de procesamiento de transacciones devuelve una respuesta con el siguiente formato:

```json
{
  "transactions": [
    {
      "id": "id_transaccion",
      "amount": monto,
      "description": "descripcion",
      "date": "fecha",
      "merchant": {
        "name": "nombre_comercio",
        "logo": "url_logo"
      },
      "category": {
        "name": "nombre_categoria",
        "type": "tipo_categoria"
      }
    },
    // Más transacciones...
  ],
  "amount_of_transactions": numero_total_transacciones,
  "categorization_rate": tasa_categorizacion,
  "merchant_identification_rate": tasa_identificacion_comercio
}
```

Cada transacción enriquecida incluye detalles como ID, monto, descripción, fecha, información del comercio y categoría.

# Propuesta para Futuros Trabajos

1. **Mejora de la Identificación de Keywords**: Implementar algoritmos más sofisticados para un análisis de texto más preciso y eficiente.

2. **Integración de Aprendizaje Automático**: Desarrollar un modelo de aprendizaje automático que mejore la clasificación y categorización de transacciones.

3. **Optimización del Rendimiento y Escalabilidad**: Aumentar la capacidad de procesamiento y escala para manejar grandes volúmenes de datos.

4. **Uso de Elasticsearch para la Gestión de Keywords**: Implementar Elasticsearch como servidor de búsqueda para gestionar y buscar keywords de manera más eficiente. Esto podría mejorar significativamente la velocidad y precisión de las búsquedas, especialmente con un gran conjunto de datos.