from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class HypervisorType(str, Enum):
    KVM = "kvm"
    XEN = "xen"
    OPENVZ = "openvz"
    VMWARE = "vmware"
    HYPERV = "hyperv"

class VMState(str, Enum):
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    SHUTTING_DOWN = "shutting_down"
    ERROR = "error"

# VM Schemas
class VMBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    hostname: str = Field(..., min_length=1, max_length=255)
    cpu_count: int = Field(default=2, ge=1, le=128)
    memory_mb: int = Field(default=2048, ge=512, le=1048576)
    disk_gb: int = Field(default=50, ge=10, le=10000)
    hypervisor_type: HypervisorType = HypervisorType.KVM
    template_id: Optional[str] = None
    network_bridge: str = "br0"
    auto_start: bool = False

class VMCreate(VMBase):
    pass

class VMUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cpu_count: Optional[int] = None
    memory_mb: Optional[int] = None
    auto_start: Optional[bool] = None

class VM(VMBase):
    id: str
    state: VMState
    ip_address: Optional[str] = None
    mac_address: str
    created_at: datetime
    modified_at: datetime
    
    class Config:
        from_attributes = True

# Template Schemas
class TemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    os_type: str  # e.g., "ubuntu", "windows", "centos"
    os_version: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    default_cpu: int = 2
    default_memory_mb: int = 2048
    default_disk_gb: int = 50

class TemplateCreate(TemplateBase):
    image_url: str

class Template(TemplateBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Monitoring Schemas
class ResourceMetrics(BaseModel):
    cpu_percent: float = Field(ge=0, le=100)
    memory_mb: int
    memory_percent: float = Field(ge=0, le=100)
    disk_read_bytes: int
    disk_write_bytes: int
    network_rx_bytes: int
    network_tx_bytes: int
    timestamp: datetime

class VMMetrics(BaseModel):
    vm_id: str
    vm_name: str
    metrics: ResourceMetrics
    
    class Config:
        from_attributes = True

class SystemStats(BaseModel):
    total_vms: int
    running_vms: int
    stopped_vms: int
    total_cpu_cores: int
    total_memory_gb: int
    used_memory_gb: float
    total_disk_gb: int
    used_disk_gb: float
    hypervisors: int
    timestamp: datetime

# Hypervisor Schemas
class HypervisorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    uri: str
    hypervisor_type: HypervisorType

class Hypervisor(HypervisorBase):
    id: str
    status: str  # "connected", "disconnected"
    hostname: str
    cpu_cores: int
    memory_gb: int
    vms_running: int
    vms_total: int
    
    class Config:
        from_attributes = True

# Action Schemas
class VMActionResponse(BaseModel):
    success: bool
    message: str
    vm_id: str

class VMActionCreate(BaseModel):
    action: str  # "start", "stop", "reboot", "force_stop"

# Response Schemas
class HealthCheck(BaseModel):
    status: str
    version: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
