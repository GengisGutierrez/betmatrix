from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ....core.database import get_db
from ....repositories.colaborador_repository import ColaboradorRepository
from ....schemas.usuario import ColaboradorResponse, Colaboradores

router = APIRouter()

@router.get("/", response_model=List[Colaboradores])
async def get_colaboradores(db: Session = Depends(get_db)):
    """Obtiene todos los colaboradores"""
    repo = ColaboradorRepository(db)
    colaboradores = repo.get_all()
    return colaboradores

@router.get("/{colaborador_id}", response_model=ColaboradorResponse)
async def get_colaborador(
    colaborador_id: UUID,
    db: Session = Depends(get_db)
):
    """Obtiene un colaborador por ID"""
    repo = ColaboradorRepository(db)
    colaborador = repo.get_by_id(colaborador_id)
    
    if not colaborador:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    
    return colaborador
