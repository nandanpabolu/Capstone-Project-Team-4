"""
Patent Partners Assistant - Configuration Settings

Centralized configuration management for the application.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = Field(default="Patent Partners Assistant", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Database
    db_path: str = Field(default="./data/processed/patents.db", env="DB_PATH")
    db_backup_path: str = Field(default="./data/processed/backups/", env="DB_BACKUP_PATH")
    
    # Search Indexes
    index_path: str = Field(default="./indexes/", env="INDEX_PATH")
    bm25_index_path: str = Field(default="./indexes/bm25/", env="BM25_INDEX_PATH")
    faiss_index_path: str = Field(default="./indexes/faiss/", env="FAISS_INDEX_PATH")
    
    # Data Paths
    raw_data_path: str = Field(default="./data/raw/", env="RAW_DATA_PATH")
    processed_data_path: str = Field(default="./data/processed/", env="PROCESSED_DATA_PATH")
    
    # LLM Configuration
    llm_model: str = Field(default="llama2:7b", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=2048, env="LLM_MAX_TOKENS")
    ollama_base_url: str = Field(default="http://localhost:11434", env="OLLAMA_BASE_URL")
    
    # Search Configuration
    bm25_top_k: int = Field(default=200, env="BM25_TOP_K")
    faiss_top_k: int = Field(default=200, env="FAISS_TOP_K")
    fusion_alpha: float = Field(default=0.5, env="FUSION_ALPHA")
    final_top_k: int = Field(default=24, env="FINAL_TOP_K")
    window_size: int = Field(default=1, env="WINDOW_SIZE")
    
    # Chunking Configuration
    chunk_size: int = Field(default=512, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=128, env="CHUNK_OVERLAP")
    max_chunk_size: int = Field(default=800, env="MAX_CHUNK_SIZE")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=1, env="API_WORKERS")
    
    # UI Configuration
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    streamlit_host: str = Field(default="localhost", env="STREAMLIT_HOST")
    
    # Offline Mode
    offline: bool = Field(default=True, env="OFFLINE")
    
    # Logging
    log_retrieval_path: str = Field(default="./logs/retrieval.log", env="LOG_RETRIEVAL_PATH")
    log_generation_path: str = Field(default="./logs/generation.log", env="LOG_GENERATION_PATH")
    log_api_path: str = Field(default="./logs/api.log", env="LOG_API_PATH")
    
    # Export Configuration
    export_path: str = Field(default="./data/exports/", env="EXPORT_PATH")
    max_export_size: str = Field(default="50MB", env="MAX_EXPORT_SIZE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.index_path,
            self.bm25_index_path,
            self.faiss_index_path,
            self.raw_data_path,
            self.processed_data_path,
            self.db_backup_path,
            self.export_path,
            "./logs/",
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @property
    def db_url(self) -> str:
        """Get SQLite database URL."""
        return f"sqlite:///{self.db_path}"
    
    @property
    def is_offline(self) -> bool:
        """Check if offline mode is enabled."""
        return self.offline


# Global settings instance
settings = Settings()
