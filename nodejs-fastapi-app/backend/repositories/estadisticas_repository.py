from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from uuid import UUID
from ..core.config import settings

class EstadisticasRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_usuario(self, usuario_id: UUID) -> Optional[dict]:
        """Obtiene estadísticas de un usuario usando la función de BD"""
        query = text(f"""
            SELECT * FROM {settings.DATABASE_SCHEMA_FUNCTIONS}.obtener_estadisticas_usuario(:usuario_id)
        """)
        
        result = self.db.execute(query, {"usuario_id": usuario_id})
        row = result.first()
        
        if row:
            return {
                "balance_total": row[0],
                "total_apostado": row[1],
                "apuestas_ganadas": row[2],
                "apuestas_perdidas": row[3],
                "total_apuestas": row[4],
                "porcentaje_exito": row[5]
            }
        
        # Retornar valores por defecto si no hay datos
        return {
            "balance_total": 0,
            "total_apostado": 0,
            "apuestas_ganadas": 0,
            "apuestas_perdidas": 0,
            "total_apuestas": 0,
            "porcentaje_exito": 0
        }