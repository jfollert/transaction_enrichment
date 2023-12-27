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