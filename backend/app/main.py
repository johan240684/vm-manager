from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.api import vms, templates, monitoring, hypervisors
from app.services.hypervisor import HypervisorService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize hypervisor service on startup
hypervisor_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global hypervisor_service
    logger.info("Starting VM Manager application...")
    hypervisor_service = HypervisorService()
    hypervisor_service.connect()
    logger.info("Connected to hypervisor")
    yield
    logger.info("Shutting down VM Manager application...")
    if hypervisor_service:
        hypervisor_service.disconnect()

# Create FastAPI app
app = FastAPI(
    title="VM Manager API",
    description="Web-based VM management system for Ubuntu servers",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts_list)

# Include routers
app.include_router(vms.router, prefix="/api/vms", tags=["VMs"])
app.include_router(templates.router, prefix="/api/templates", tags=["Templates"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring"])
app.include_router(hypervisors.router, prefix="/api/hypervisors", tags=["Hypervisors"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VM Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
