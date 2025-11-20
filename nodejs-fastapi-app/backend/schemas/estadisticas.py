from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID

class EstadisticasResponse(BaseModel):
    balance_total: Decimal
    total_apostado: Decimal
    apuestas_ganadas: int
    apuestas_perdidas: int
    total_apuestas: int
    porcentaje_exito: Decimal
    
    class Config:
        from_attributes = True