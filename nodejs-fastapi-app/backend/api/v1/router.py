from fastapi import APIRouter
from .endpoints import colaboradores, apuestas, estadisticas, test

api_router = APIRouter()

api_router.include_router(
    colaboradores.router, 
    prefix="/colaboradores", 
    tags=["colaboradores"]
)

api_router.include_router(
    apuestas.router, 
    prefix="/apuestas", 
    tags=["apuestas"]
)

api_router.include_router(
    estadisticas.router, 
    prefix="/estadisticas", 
    tags=["estadisticas"]
)

api_router.include_router(
    test.router, 
    prefix="/test", 
    tags=["test"]
)