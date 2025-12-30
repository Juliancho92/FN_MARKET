# FN MARKET

Aplicación web e-commerce para venta de productos internos empresariales.

## Tech Stack

- **Backend**: FastAPI
- **Base de datos**: SQLite (Desarrollo) / PostgreSQL (Producción)
- **Inventario**: Google Sheets API
- **Almacenamiento**: Cloudinary
- **Frontend**: React/Vue (Planeado)
- **Deploy**: Netlify (Frontend) + Serverless (Backend)

## Estructura del Proyecto

```
fn-market/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── ...
├── requirements.txt
└── ...
```

## Instalación

1. Crear entorno virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Una vez ejecutando, visitar: `http://localhost:8000/docs`
