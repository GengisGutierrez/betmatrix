from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from uuid import UUID
from ..core.config import settings

class ColaboradorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[dict]:
        """Obtiene todos los colaboradores desde la vista"""
        query = text(f"""
            SELECT 
                c.id,
                c.nombre || ' ' || c.apellido as nombre,
                o.nombre || ' ' || o.apellido as operador_nombre
            FROM {settings.DATABASE_SCHEMA}.colaboradores c
            INNER JOIN {settings.DATABASE_SCHEMA}.operadores o ON c.operador_id = o.id
            WHERE c.deleted_at IS NULL
            ORDER BY c.created_at DESC
        """)
        result = self.db.execute(query)

        return [dict(row._mapping) for row in result]
       
    def get_all_hierarchy(self) -> List[dict]:
        """Obtiene todos los colaboradores desde la vista"""
        query = text(f"""
            SELECT 
                c.id,
                c.nombre,
                c.apellido,
                c.email,
                c.telefono,
                c.estado,
                ct.numero_cuenta,
                o.nombre || ' ' || o.apellido as operador_nombre
            FROM {settings.DATABASE_SCHEMA}.colaboradores c
            INNER JOIN {settings.DATABASE_SCHEMA}.cuentas ct ON c.id = ct.usuario_id
            INNER JOIN {settings.DATABASE_SCHEMA}.operadores o ON c.operador_id = o.id
            WHERE c.deleted_at IS NULL
            ORDER BY c.created_at DESC
        """)
        
        result = self.db.execute(query)
        return [dict(row._mapping) for row in result]
    
    def get_by_id(self, colaborador_id: UUID) -> Optional[dict]:
        """Obtiene un colaborador por ID"""
        query = text(f"""
            SELECT 
                c.id,
                c.nombre,
                c.apellido,
                c.email,
                c.telefono,
                c.estado,
                ct.numero_cuenta,
                o.nombre || ' ' || o.apellido as operador_nombre
            FROM {settings.DATABASE_SCHEMA}.colaboradores c
            INNER JOIN {settings.DATABASE_SCHEMA}.cuentas ct ON c.cuenta_id = ct.id
            INNER JOIN {settings.DATABASE_SCHEMA}.operadores o ON c.operador_id = o.id
            WHERE c.id = :colaborador_id 
              AND c.deleted_at IS NULL
        """)
        
        result = self.db.execute(query, {"colaborador_id": colaborador_id})
        row = result.first()
        return dict(row._mapping) if row else None