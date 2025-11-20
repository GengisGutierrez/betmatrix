from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ....core.database import get_db
from ....repositories.estadisticas_repository import EstadisticasRepository
from ....schemas.estadisticas import EstadisticasResponse

router = APIRouter()

@router.get("/{usuario_id}", response_model=EstadisticasResponse)
async def get_estadisticas_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtiene las estadísticas de un usuario"""
    repo = EstadisticasRepository(db)
    estadisticas = repo.get_by_usuario(usuario_id)
    
    if not estadisticas:
        raise HTTPException(status_code=404, detail="Estadísticas no encontradas")
    
    return estadisticas