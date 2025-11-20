from pydantic import BaseModel
from decimal import Decimal

class TestResponse(BaseModel):
    message: str

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from ....core.config import settings
from ....core.database import get_db

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

class TestRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_test_data(self) -> List[dict]:
        """Obtiene todas las apuestas de un usuario"""
        query = text(f"""
            SELECT 
                usuario_id
            FROM {settings.DATABASE_SCHEMA}.apuestas
        """)
        result = self.db.execute(query)

        return [dict(row._mapping) for row in result]


router = APIRouter()

@router.get("/", response_model=TestResponse)
async def get_test_data(
    db: Session = Depends(get_db)
):
    """Obtiene datos de test"""
    messages = []
    
    try:
        query = text(f"""
            SELECT 1
        """)
        
        result = db.execute(query)
        data = [dict(row._mapping) for row in result]
        messages.append(f"✅ Database connected {data}")
    except Exception as e:
        messages.append(f"❌ Database error: {str(e)}")
    
    try:
        repo = TestRepository(db)
        data = repo.get_test_data()
        messages.append(f"✅ Repository created {data}")
    except Exception as e:
        messages.append(f"❌ Repository error: {str(e)}")
    
    return {
        "message": " | ".join(messages)
    }