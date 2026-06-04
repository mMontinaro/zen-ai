from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_URL: str = "http://ollama:11434"
    MODEL: str = "llama3.1"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()