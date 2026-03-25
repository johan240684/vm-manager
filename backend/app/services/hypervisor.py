import logging
import libvirt
from typing import Optional, List, Dict, Any
from app.config import settings
from app.schemas import VM, VMState, ResourceMetrics
from datetime import datetime

logger = logging.getLogger(__name__)

class HypervisorService:
    """Service for managing hypervisors and VMs via libvirt"""
    
    def __init__(self):
        self.conn = None
        self.uri = settings.LIBVIRT_URI
    
    def connect(self) -> bool:
        """Connect to hypervisor"""
        try:
            self.conn = libvirt.open(self.uri)
            if self.conn is None:
                logger.error(f"Failed to open connection to {self.uri}")
                return False
            logger.info(f"Successfully connected to {self.uri}")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Libvirt error: {e}")
            return False
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from hypervisor"""
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                logger.info("Disconnected from hypervisor")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to hypervisor"""
        if self.conn is None:
            return False
        try:
            self.conn.getVersion()
            return True
        except:
            return False
    
    # ===== VM Operations =====
    
    def list_vms(self) -> List[Dict[str, Any]]:
        """List all VMs"""
        if not self.is_connected():
            return []
        
        vms = []
        try:
            # Get running domains
            for domain_id in self.conn.listDomainsID():
                domain = self.conn.lookupByID(domain_id)
                vms.append(self._domain_to_dict(domain))
            
            # Get inactive domains
            for domain_name in self.conn.listDefinedDomains():
                domain = self.conn.lookupByName(domain_name)
                vms.append(self._domain_to_dict(domain))
        except libvirt.libvirtError as e:
            logger.error(f"Error listing VMs: {e}")
        
        return vms
    
    def get_vm(self, vm_name: str) -> Optional[Dict[str, Any]]:
        """Get VM details"""
        if not self.is_connected():
            return None
        
        try:
            domain = self.conn.lookupByName(vm_name)
            return self._domain_to_dict(domain)
        except libvirt.libvirtError as e:
            logger.error(f"Error getting VM {vm_name}: {e}")
            return None
    
    def create_vm(self, vm_name: str, cpu: int, memory_mb: int, disk_gb: int, **kwargs) -> bool:
        """Create new VM from XML definition"""
        if not self.is_connected():
            return False
        
        try:
            xml_config = self._generate_vm_xml(vm_name, cpu, memory_mb, disk_gb, **kwargs)
            self.conn.defineXML(xml_config)
            logger.info(f"VM {vm_name} created successfully")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Error creating VM: {e}")
            return False
    
    def delete_vm(self, vm_name: str) -> bool:
        """Delete VM"""
        if not self.is_connected():
            return False
        
        try:
            domain = self.conn.lookupByName(vm_name)
            
            # Stop if running
            if domain.isActive():
                domain.destroy()
            
            # Delete domain
            domain.undefine()
            logger.info(f"VM {vm_name} deleted successfully")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Error deleting VM: {e}")
            return False
    
    def start_vm(self, vm_name: str) -> bool:
        """Start VM"""
        if not self.is_connected():
            return False
        
        try:
            domain = self.conn.lookupByName(vm_name)
            if not domain.isActive():
                domain.create()
                logger.info(f"VM {vm_name} started")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Error starting VM: {e}")
            return False
    
    def stop_vm(self, vm_name: str, force: bool = False) -> bool:
        """Stop VM"""
        if not self.is_connected():
            return False
        
        try:
            domain = self.conn.lookupByName(vm_name)
            if domain.isActive():
                if force:
                    domain.destroy()
                else:
                    domain.shutdown()
                logger.info(f"VM {vm_name} stopped")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Error stopping VM: {e}")
            return False
    
    def reboot_vm(self, vm_name: str) -> bool:
        """Reboot VM"""
        if not self.is_connected():
            return False
        
        try:
            domain = self.conn.lookupByName(vm_name)
            if domain.isActive():
                domain.reboot()
                logger.info(f"VM {vm_name} rebooted")
            return True
        except libvirt.libvirtError as e:
            logger.error(f"Error rebooting VM: {e}")
            return False
    
    def get_vm_metrics(self, vm_name: str) -> Optional[ResourceMetrics]:
        """Get VM resource metrics"""
        if not self.is_connected():
            return None
        
        try:
            domain = self.conn.lookupByName(vm_name)
            cpu_stats = domain.getCPUStats(total=True)[0]
            mem_stats = domain.memoryStats()
            
            cpu_percent = (cpu_stats.get('cpu_time', 0) / 1e9) % 100
            
            return ResourceMetrics(
                cpu_percent=max(0, min(100, cpu_percent)),
                memory_mb=mem_stats.get('actual', 0) // 1024,
                memory_percent=(mem_stats.get('actual', 0) / domain.maxMemory()) * 100,
                disk_read_bytes=0,  # Would need block stats
                disk_write_bytes=0,
                network_rx_bytes=0,  # Would need interface stats
                network_tx_bytes=0,
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error getting metrics for {vm_name}: {e}")
            return None
    
    def get_hypervisor_info(self) -> Dict[str, Any]:
        """Get hypervisor information"""
        if not self.is_connected():
            return {}
        
        try:
            info = self.conn.getInfo()
            node_info = self.conn.nodeInfo()
            
            return {
                "hostname": self.conn.getHostname(),
                "uri": self.conn.getURI(),
                "hypervisor": self.conn.getType(),
                "version": self.conn.getVersion(),
                "cpu_cores": node_info[2],
                "memory_gb": node_info[1] // (1024 ** 2),
                "vms_running": len(self.conn.listDomainsID()),
                "vms_total": len(self.conn.listDomainsID()) + len(self.conn.listDefinedDomains())
            }
        except Exception as e:
            logger.error(f"Error getting hypervisor info: {e}")
            return {}
    
    # ===== Helper Methods =====
    
    def _domain_to_dict(self, domain) -> Dict[str, Any]:
        """Convert libvirt domain to dictionary"""
        try:
            info = domain.info()
            state_map = {
                libvirt.VIR_DOMAIN_RUNNING: VMState.RUNNING,
                libvirt.VIR_DOMAIN_BLOCKED: VMState.RUNNING,
                libvirt.VIR_DOMAIN_PAUSED: VMState.PAUSED,
                libvirt.VIR_DOMAIN_SHUTDOWN: VMState.SHUTTING_DOWN,
                libvirt.VIR_DOMAIN_SHUTOFF: VMState.STOPPED,
                libvirt.VIR_DOMAIN_CRASHED: VMState.ERROR,
            }
            
            return {
                "id": domain.UUIDString(),
                "name": domain.name(),
                "state": state_map.get(info[0], VMState.ERROR),
                "cpu_count": info[3],
                "memory_mb": info[1] // 1024,
                "max_memory_mb": domain.maxMemory() // 1024,
            }
        except Exception as e:
            logger.error(f"Error converting domain: {e}")
            return {}
    
    def _generate_vm_xml(self, name: str, cpu: int, memory_mb: int, disk_gb: int, **kwargs) -> str:
        """Generate VM XML configuration"""
        network_bridge = kwargs.get("network_bridge", "br0")
        disk_path = kwargs.get("disk_path", f"/var/lib/libvirt/images/{name}.qcow2")
        
        xml = f"""
<domain type='kvm'>
    <name>{name}</name>
    <memory unit='MiB'>{memory_mb}</memory>
    <currentMemory unit='MiB'>{memory_mb}</currentMemory>
    <vcpu>{cpu}</vcpu>
    <os>
        <type arch='x86_64'>hvm</type>
        <boot dev='hd'/>
    </os>
    <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{disk_path}'/>
            <target dev='vda' bus='virtio'/>
        </disk>
        <interface type='bridge'>
            <mac address='52:54:00:12:34:56'/>
            <source bridge='{network_bridge}'/>
            <model type='virtio'/>
        </interface>
        <console type='pty'>
            <target type='virtio' port='0'/>
        </console>
    </devices>
</domain>
        """
        return xml.strip()
