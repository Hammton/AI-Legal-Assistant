from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Legal Document Verification Agent"
    VERSION: str = "0.1.0"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # LLM Settings
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "openai"  # "openai" or "anthropic"
    DEFAULT_MODEL: str = "gpt-4"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/legal_docs"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Document Processing
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".doc"]
    UPLOAD_DIR: str = "./uploads"
    
    # Agent Settings
    AGENT_TIMEOUT_SECONDS: int = 300
    ENABLE_HITL: bool = True
    RISK_THRESHOLD_CRITICAL: int = 76
    RISK_THRESHOLD_HIGH: int = 51
    RISK_THRESHOLD_MEDIUM: int = 26
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
