from fastapi import APIRouter
from typing import List
from app.models.ticket import Ticket, TicketCreate
from datetime import datetime
import uuid

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/crear", response_model=Ticket)
async def crear_ticket(ticket: TicketCreate):
    # TODO: Implement database saving
    return {
        "id": str(uuid.uuid4()),
        "usuario_id": "user-mock-id",
        "productos": ticket.productos,
        "total": ticket.total,
        "direccion": ticket.direccion,
        "telefono": ticket.telefono,
        "observaciones": ticket.observaciones,
        "estado": "revision",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
