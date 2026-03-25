from fastapi import APIRouter, HTTPException
import logging
from datetime import datetime
from app.schemas import VMMetrics, SystemStats, ResourceMetrics

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """Get overall system statistics"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service or not hypervisor_service.is_connected():
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        vms = hypervisor_service.list_vms()
        running_vms = [vm for vm in vms if vm.get("state") == "running"]
        
        hv_info = hypervisor_service.get_hypervisor_info()
        
        return SystemStats(
            total_vms=len(vms),
            running_vms=len(running_vms),
            stopped_vms=len(vms) - len(running_vms),
            total_cpu_cores=hv_info.get("cpu_cores", 0),
            total_memory_gb=hv_info.get("memory_gb", 0),
            used_memory_gb=0.0,  # Would need to aggregate VM memory
            total_disk_gb=1000,  # Placeholder
            used_disk_gb=0.0,    # Would need to aggregate VM disk
            hypervisors=1,
            timestamp=datetime.now()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system statistics")

@router.get("/vms/{vm_name}/metrics", response_model=VMMetrics)
async def get_vm_metrics(vm_name: str):
    """Get VM resource metrics"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service or not hypervisor_service.is_connected():
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        vm = hypervisor_service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        metrics = hypervisor_service.get_vm_metrics(vm_name)
        if not metrics:
            raise HTTPException(status_code=500, detail="Failed to retrieve metrics")
        
        return VMMetrics(
            vm_id=vm.get("id"),
            vm_name=vm.get("name"),
            metrics=metrics
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting VM metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get VM metrics")

@router.get("/vms/history/{vm_name}")
async def get_vm_metrics_history(vm_name: str, hours: int = 24):
    """Get VM metrics history"""
    try:
        from app.main import hypervisor_service
        
        if not hypervisor_service or not hypervisor_service.is_connected():
            raise HTTPException(status_code=503, detail="Hypervisor service not available")
        
        vm = hypervisor_service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        # This would fetch from a time-series database like InfluxDB or Prometheus
        # For now, return mock data
        return {
            "vm_id": vm.get("id"),
            "vm_name": vm.get("name"),
            "hours": hours,
            "data": []
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting VM metrics history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get VM metrics history")

@router.get("/alerts")
async def get_alerts():
    """Get system alerts and warnings"""
    try:
        return {
            "alerts": [],
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")
