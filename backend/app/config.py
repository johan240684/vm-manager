from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # FastAPI
    FASTAPI_ENV: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1,0.0.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./vm_manager.db"
    
    # Hypervisor
    LIBVIRT_URI: str = "qemu:///system"
    HYPERVISOR_TYPES: List[str] = ["kvm", "xen", "openvz", "vmware"]
    
    # Redis (for caching and job queue)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Features
    ENABLE_MONITORING: bool = True
    ENABLE_AUTOMATION: bool = True
    MONITORING_INTERVAL: int = 30  # seconds
    
    # File paths
    TEMPLATES_PATH: str = "./templates"
    BACKUPS_PATH: str = "./backups"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def cors_origins_list(self) -> List[str]:
        return [item.strip() for item in self.CORS_ORIGINS.split(",") if item.strip()]

    @property
    def allowed_hosts_list(self) -> List[str]:
        return [item.strip() for item in self.ALLOWED_HOSTS.split(",") if item.strip()]

settings = Settings()
