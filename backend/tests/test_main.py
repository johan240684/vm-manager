import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_list_vms():
    """Test listing VMs"""
    response = client.get("/api/vms")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_list_templates():
    """Test listing templates"""
    response = client.get("/api/templates")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_system_stats():
    """Test getting system stats"""
    response = client.get("/api/monitoring/stats")
    # This may fail if hypervisor is not connected
    if response.status_code != 503:
        assert response.status_code == 200
        data = response.json()
        assert "total_vms" in data
        assert "running_vms" in data

def test_list_hypervisors():
    """Test listing hypervisors"""
    response = client.get("/api/hypervisors")
    # This may fail if hypervisor is not connected
    if response.status_code != 503:
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.xfail(reason="Requires hypervisor connection")
def test_create_vm():
    """Test creating a VM"""
    vm_data = {
        "name": "test-vm",
        "hostname": "test-vm.example.com",
        "cpu_count": 2,
        "memory_mb": 2048,
        "disk_gb": 50,
        "hypervisor_type": "kvm",
        "template_id": "ubuntu-22-04"
    }
    response = client.post("/api/vms", json=vm_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
