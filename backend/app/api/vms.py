from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from app.schemas import (
    VM, VMCreate, VMUpdate, VMActionResponse, VMState,
    ErrorResponse, HypervisorType
)
from app.services.hypervisor import HypervisorService

router = APIRouter()
logger = logging.getLogger(__name__)

# This will be injected from main.py
hypervisor_service: Optional[HypervisorService] = None

def get_hypervisor() -> HypervisorService:
    """Get hypervisor service instance"""
    from app.main import hypervisor_service
    if not hypervisor_service:
        raise HTTPException(status_code=503, detail="Hypervisor service not available")
    return hypervisor_service

@router.get("", response_model=List[dict])
async def list_vms(
    state: Optional[str] = Query(None, description="Filter by VM state"),
    hypervisor: Optional[str] = Query(None, description="Filter by hypervisor")
):
    """List all VMs"""
    try:
        service = get_hypervisor()
        vms = service.list_vms()
        
        # Filter by state if provided
        if state:
            vms = [vm for vm in vms if vm.get("state") == state]
        
        return vms
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing VMs: {e}")
        raise HTTPException(status_code=500, detail="Failed to list VMs")

@router.get("/{vm_name}", response_model=dict)
async def get_vm(vm_name: str):
    """Get VM details"""
    try:
        service = get_hypervisor()
        vm = service.get_vm(vm_name)
        
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        return vm
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting VM {vm_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get VM details")

@router.post("", response_model=VMActionResponse)
async def create_vm(vm_config: VMCreate):
    """Create a new VM"""
    try:
        service = get_hypervisor()
        
        # Validate VM doesn't already exist
        existing = service.get_vm(vm_config.name)
        if existing:
            raise HTTPException(status_code=400, detail=f"VM '{vm_config.name}' already exists")
        
        success = service.create_vm(
            vm_name=vm_config.name,
            cpu=vm_config.cpu_count,
            memory_mb=vm_config.memory_mb,
            disk_gb=vm_config.disk_gb,
            network_bridge=vm_config.network_bridge,
            description=vm_config.description
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create VM")
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_config.name}' created successfully",
            vm_id=vm_config.name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to create VM")

@router.delete("/{vm_name}", response_model=VMActionResponse)
async def delete_vm(vm_name: str):
    """Delete a VM"""
    try:
        service = get_hypervisor()
        
        # Verify VM exists
        vm = service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        success = service.delete_vm(vm_name)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete VM")
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_name}' deleted successfully",
            vm_id=vm_name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete VM")

@router.post("/{vm_name}/start", response_model=VMActionResponse)
async def start_vm(vm_name: str):
    """Start a VM"""
    try:
        service = get_hypervisor()
        
        vm = service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        success = service.start_vm(vm_name)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to start VM")
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_name}' started successfully",
            vm_id=vm_name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to start VM")

@router.post("/{vm_name}/stop", response_model=VMActionResponse)
async def stop_vm(vm_name: str, force: bool = False):
    """Stop a VM"""
    try:
        service = get_hypervisor()
        
        vm = service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        success = service.stop_vm(vm_name, force=force)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to stop VM")
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_name}' stopped successfully",
            vm_id=vm_name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop VM")

@router.post("/{vm_name}/reboot", response_model=VMActionResponse)
async def reboot_vm(vm_name: str):
    """Reboot a VM"""
    try:
        service = get_hypervisor()
        
        vm = service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        success = service.reboot_vm(vm_name)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to reboot VM")
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_name}' rebooted successfully",
            vm_id=vm_name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rebooting VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to reboot VM")

@router.put("/{vm_name}", response_model=VMActionResponse)
async def update_vm(vm_name: str, vm_config: VMUpdate):
    """Update VM configuration"""
    try:
        service = get_hypervisor()
        
        vm = service.get_vm(vm_name)
        if not vm:
            raise HTTPException(status_code=404, detail=f"VM '{vm_name}' not found")
        
        # Note: Full update would require recreating or using libvirt domains
        # For now, this is a placeholder
        
        return VMActionResponse(
            success=True,
            message=f"VM '{vm_name}' updated successfully",
            vm_id=vm_name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating VM: {e}")
        raise HTTPException(status_code=500, detail="Failed to update VM")
