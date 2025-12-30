from fastapi import APIRouter, HTTPException, status
from app.models.usuario import UsuarioCreate, Usuario
from datetime import datetime
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Usuario)
async def register(usuario: UsuarioCreate):
    # TODO: Implement actual registration logic
    return {
        "id": str(uuid.uuid4()),
        "email": usuario.email,
        "nombre": usuario.nombre,
        "telefono": usuario.telefono,
        "rol": "user",
        "created_at": datetime.now()
    }

@router.post("/login")
async def login():
    # TODO: Implement JWT generation
    return {"access_token": "mock-jwt-token", "token_type": "bearer"}
