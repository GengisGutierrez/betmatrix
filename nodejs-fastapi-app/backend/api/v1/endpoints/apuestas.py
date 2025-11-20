from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ....core.database import get_db
from ....repositories.apuesta_repository import ApuestaRepository
from ....schemas.apuesta import ApuestaCreate, ApuestaResponse, ApuestaUpdate

router = APIRouter()

@router.get("/usuario/{usuario_id}", response_model=List[ApuestaResponse])
async def get_apuestas_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtiene todas las apuestas de un usuario"""
    repo = ApuestaRepository(db)
    apuestas = repo.get_by_usuario(usuario_id)
    return apuestas

@router.post("/", response_model=ApuestaResponse, status_code=status.HTTP_201_CREATED)
async def create_apuesta(
    apuesta: ApuestaCreate,
    db: Session = Depends(get_db)
):
    """Crea una nueva apuesta"""
    repo = ApuestaRepository(db)
    
    try:
        nueva_apuesta = repo.create(
            usuario_id=apuesta.usuario_id,
            deporte_slug=apuesta.deporte_slug,
            monto_apostado=apuesta.monto_apostado,
            cuota=apuesta.cuota,
            descripcion=apuesta.descripcion,
            resultado=apuesta.resultado or "Pendiente"
        )
        
        if not nueva_apuesta:
            raise HTTPException(
                status_code=400, 
                detail="No se pudo crear la apuesta. Verifica que el deporte exista."
            )
        
        return nueva_apuesta
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear apuesta: {str(e)}")

@router.patch("/{apuesta_id}", response_model=dict)
async def update_apuesta(
    apuesta_id: int,
    apuesta_update: ApuestaUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza el resultado de una apuesta"""
    repo = ApuestaRepository(db)
    
    if not apuesta_update.resultado or apuesta_update.monto_resultado is None:
        raise HTTPException(
            status_code=400,
            detail="Debe proporcionar resultado y monto_resultado"
        )
    
    success = repo.update_resultado(
        apuesta_id=apuesta_id,
        resultado=apuesta_update.resultado,
        monto_resultado=apuesta_update.monto_resultado
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Apuesta no encontrada")
    
    return {"message": "Apuesta actualizada correctamente"}