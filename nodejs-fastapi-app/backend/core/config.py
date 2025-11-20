from pydantic_settings import BaseSettings
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int = 5432
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str = "databricks_postgres"
    DATABASE_SCHEMA: str = "sch_guch_ctrl_tb"
    DATABASE_SCHEMA_VIEWS: str = "sch_guch_ctrl_vw"
    DATABASE_SCHEMA_FUNCTIONS: str = "sch_guch_ctrl_fn"
      
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # App
    PROJECT_NAME: str = "Betmatrix"
    VERSION: str = "1.0.0"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?sslmode=require"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()