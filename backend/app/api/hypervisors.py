from fastapi import APIRouter, HTTPException
from typing import List
import logging
from app.schemas import Hypervisor

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("", response_model=List[dict])
async def list_hypervisors():
    """List all connected hypervisors"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service:
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        info = hypervisor_service.get_hypervisor_info()
        
        if not info:
            raise HTTPException(status_code=503, detail="No hypervisors connected")
        
        return [{
            "id": "main-hypervisor",
            "name": "Main KVM Host",
            "uri": info.get("uri", ""),
            "hypervisor_type": info.get("hypervisor", "kvm").lower(),
            "status": "connected" if hypervisor_service.is_connected() else "disconnected",
            "hostname": info.get("hostname", "unknown"),
            "cpu_cores": info.get("cpu_cores", 0),
            "memory_gb": info.get("memory_gb", 0),
            "vms_running": info.get("vms_running", 0),
            "vms_total": info.get("vms_total", 0)
        }]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing hypervisors: {e}")
        raise HTTPException(status_code=500, detail="Failed to list hypervisors")

@router.get("/{hypervisor_id}", response_model=dict)
async def get_hypervisor(hypervisor_id: str):
    """Get hypervisor details"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service:
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        if hypervisor_id != "main-hypervisor":
            raise HTTPException(status_code=404, detail="Hypervisor not found")
        
        info = hypervisor_service.get_hypervisor_info()
        
        return {
            "id": "main-hypervisor",
            "name": "Main KVM Host",
            "uri": info.get("uri", ""),
            "hypervisor_type": info.get("hypervisor", "kvm").lower(),
            "status": "connected" if hypervisor_service.is_connected() else "disconnected",
            "hostname": info.get("hostname", "unknown"),
            "cpu_cores": info.get("cpu_cores", 0),
            "memory_gb": info.get("memory_gb", 0),
            "vms_running": info.get("vms_running", 0),
            "vms_total": info.get("vms_total", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting hypervisor details: {e}")
        raise HTTPException(status_code=500, detail="Failed to get hypervisor details")

@router.get("/{hypervisor_id}/status", response_model=dict)
async def get_hypervisor_status(hypervisor_id: str):
    """Get hypervisor status"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service:
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        is_connected = hypervisor_service.is_connected()
        info = hypervisor_service.get_hypervisor_info() if is_connected else {}
        
        return {
            "hypervisor_id": hypervisor_id,
            "status": "connected" if is_connected else "disconnected",
            "uptime": "N/A",
            "cpu_usage_percent": 0,
            "memory_usage_percent": 0,
            "disk_usage_percent": 0,
            "vms_running": info.get("vms_running", 0),
            "vms_total": info.get("vms_total", 0)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting hypervisor status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get hypervisor status")
