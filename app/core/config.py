from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Criminal Case Platform"
    API_V1_STR: str = "/api/v1"
    
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192" # Free tier best model
    
    ACTIVE_LLM_PROVIDER: str = "groq" # Can be 'gemini' or 'groq'

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
