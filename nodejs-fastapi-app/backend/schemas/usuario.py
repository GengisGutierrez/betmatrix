from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: str

class Colaboradores(BaseModel):
    id: UUID
    nombre: str
    operador_nombre: str

class ColaboradorResponse(BaseModel):
    id: UUID
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    estado: str
    numero_cuenta: str
    operador_nombre: str
    
    class Config:
        from_attributes = True