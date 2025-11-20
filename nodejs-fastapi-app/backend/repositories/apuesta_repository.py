from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from ..core.config import settings

class ApuestaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_usuario(self, usuario_id: UUID) -> List[dict]:
        """Obtiene todas las apuestas de un usuario"""
        query = text(f"""
            SELECT 
                a.id,
                a.usuario_id,
                a.monto_apostado,
                a.resultado,
                td.nombre as deporte,
                a.cuota,
                a.descripcion,
                a.monto_resultado,
                a.created_at
            FROM {settings.DATABASE_SCHEMA}.apuestas a
            INNER JOIN {settings.DATABASE_SCHEMA}.tipos_deporte td ON a.deporte_id = td.id
            WHERE a.usuario_id = :usuario_id 
              AND a.deleted_at IS NULL
            ORDER BY a.created_at DESC
        """)
        
        result = self.db.execute(query, {"usuario_id": usuario_id})
        return [dict(row._mapping) for row in result]
    
    def create(
        self, 
        usuario_id: UUID, 
        deporte_slug: str,
        monto_apostado: Decimal,
        cuota: Decimal,
        descripcion: str,
        resultado: str = "Pendiente"
    ) -> dict:
        """Crea una nueva apuesta"""
        query = text(f"""
            INSERT INTO {settings.DATABASE_SCHEMA}.apuestas (
                usuario_id,
                deporte_id,
                monto_apostado,
                cuota,
                resultado,
                descripcion
            )
            SELECT 
                :usuario_id,
                td.id,
                :monto_apostado,
                :cuota,
                :resultado,
                :descripcion
            FROM {settings.DATABASE_SCHEMA}.tipos_deporte td
            WHERE td.slug = :deporte_slug
            RETURNING id, usuario_id, monto_apostado, cuota, resultado, descripcion, created_at
        """)
        
        result = self.db.execute(query, {
            "usuario_id": usuario_id,
            "deporte_slug": deporte_slug,
            "monto_apostado": monto_apostado,
            "cuota": cuota,
            "resultado": resultado,
            "descripcion": descripcion
        })
        self.db.commit()
        
        row = result.first()
        return dict(row._mapping) if row else None
    
    def update_resultado(
        self, 
        apuesta_id: int, 
        resultado: str, 
        monto_resultado: Decimal
    ) -> bool:
        """Actualiza el resultado de una apuesta"""
        query = text(f"""
            UPDATE {settings.DATABASE_SCHEMA}.apuestas
            SET resultado = :resultado,
                monto_resultado = :monto_resultado,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :apuesta_id
              AND deleted_at IS NULL
        """)
        
        result = self.db.execute(query, {
            "apuesta_id": apuesta_id,
            "resultado": resultado,
            "monto_resultado": monto_resultado
        })
        self.db.commit()
        
        return result.rowcount > 0