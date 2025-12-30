from fastapi import APIRouter, HTTPException
from typing import List
from app.models.producto import Producto

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", response_model=List[Producto])
async def get_productos():
    # TODO: Implement Google Sheets sync
    return [
        {
            "id": "prod-001",
            "nombre": "Producto Demo",
            "descripcion": "Descripción demo",
            "precio": 100.0,
            "cantidad_disponible": 10,
            "categoria": "General",
            "imagenes": []
        }
    ]
