from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from uuid import UUID

class ApuestaBase(BaseModel):
    monto_apostado: Decimal = Field(gt=0, description="Monto debe ser mayor a 0")
    cuota: Decimal = Field(gt=0, description="Cuota debe ser mayor a 0")
    descripcion: str
    deporte_slug: str
    resultado: Optional[str] = "Pendiente"

class ApuestaCreate(ApuestaBase):
    usuario_id: UUID
    deporte_slug: str

class ApuestaUpdate(BaseModel):
    resultado: Optional[str] = None
    monto_resultado: Optional[Decimal] = None

class ApuestaResponse(BaseModel):
    id: int
    usuario_id: UUID
    monto_apostado: Decimal
    resultado: str
    deporte: str
    cuota: Decimal
    descripcion: str
    monto_resultado: Optional[Decimal]
    created_at: datetime
    
    class Config:
        from_attributes = True