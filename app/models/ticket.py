from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from enum import Enum

class TicketEstado(str, Enum):
    REVISION = "revision"
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PAGADO = "pagado"
    RECIBIDO = "recibido"

class TicketProducto(BaseModel):
    producto_id: str
    cantidad: int
    precio_unitario: float

class TicketBase(BaseModel):
    productos: List[TicketProducto]
    total: float
    direccion: str
    telefono: str
    observaciones: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: str
    usuario_id: str
    estado: TicketEstado = TicketEstado.REVISION
    comprobante_pago_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
