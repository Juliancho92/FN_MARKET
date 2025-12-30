from pydantic import BaseModel
from typing import List, Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad_disponible: int
    categoria: str
    imagenes: List[str] = []

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: str

    class Config:
        from_attributes = True
