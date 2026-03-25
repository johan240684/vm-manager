from fastapi import APIRouter, HTTPException
from typing import List
import logging
from app.schemas import Template, TemplateCreate

router = APIRouter()
logger = logging.getLogger(__name__)

# Mock database of templates
TEMPLATES_DB = [
    {
        "id": "ubuntu-22-04",
        "name": "Ubuntu 22.04 LTS",
        "os_type": "ubuntu",
        "os_version": "22.04",
        "description": "Ubuntu 22.04 LTS with minimal configuration",
        "icon_url": "https://assets.ubuntu.com/v1_b9e9e82e-ubuntu-logo14.png",
        "default_cpu": 2,
        "default_memory_mb": 2048,
        "default_disk_gb": 50,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "ubuntu-20-04",
        "name": "Ubuntu 20.04 LTS",
        "os_type": "ubuntu",
        "os_version": "20.04",
        "description": "Ubuntu 20.04 LTS with minimal configuration",
        "icon_url": "https://assets.ubuntu.com/v1_b9e9e82e-ubuntu-logo14.png",
        "default_cpu": 2,
        "default_memory_mb": 2048,
        "default_disk_gb": 50,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "debian-12",
        "name": "Debian 12 Bookworm",
        "os_type": "debian",
        "os_version": "12",
        "description": "Debian 12 Bookworm minimal",
        "icon_url": "https://www.debian.org/logos/openlogo.svg",
        "default_cpu": 2,
        "default_memory_mb": 1024,
        "default_disk_gb": 30,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "centos-stream-9",
        "name": "CentOS Stream 9",
        "os_type": "centos",
        "os_version": "9",
        "description": "CentOS Stream 9 minimal",
        "icon_url": "https://www.centos.org/assets/img/logo.png",
        "default_cpu": 2,
        "default_memory_mb": 2048,
        "default_disk_gb": 40,
        "created_at": "2024-01-01T00:00:00Z"
    },
    {
        "id": "fedora-39",
        "name": "Fedora 39",
        "os_type": "fedora",
        "os_version": "39",
        "description": "Fedora 39 minimal",
        "icon_url": "https://fedoraproject.org/static/images/fedora_logo.png",
        "default_cpu": 2,
        "default_memory_mb": 2048,
        "default_disk_gb": 40,
        "created_at": "2024-01-01T00:00:00Z"
    }
]

@router.get("", response_model=List[dict])
async def list_templates():
    """List all available templates"""
    try:
        return TEMPLATES_DB
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        raise HTTPException(status_code=500, detail="Failed to list templates")

@router.get("/{template_id}", response_model=dict)
async def get_template(template_id: str):
    """Get template details"""
    try:
        template = next((t for t in TEMPLATES_DB if t["id"] == template_id), None)
        
        if not template:
            raise HTTPException(status_code=404, detail=f"Template '{template_id}' not found")
        
        return template
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting template: {e}")
        raise HTTPException(status_code=500, detail="Failed to get template")

@router.post("", response_model=dict)
async def create_template(template: TemplateCreate):
    """Create custom template"""
    try:
        # Generate ID from name
        template_id = template.name.lower().replace(" ", "-")
        
        new_template = {
            "id": template_id,
            "name": template.name,
            "os_type": template.os_type,
            "os_version": template.os_version,
            "description": template.description,
            "icon_url": template.icon_url,
            "default_cpu": template.default_cpu,
            "default_memory_mb": template.default_memory_mb,
            "default_disk_gb": template.default_disk_gb,
            "image_url": template.image_url,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        TEMPLATES_DB.append(new_template)
        return new_template
    except Exception as e:
        logger.error(f"Error creating template: {e}")
        raise HTTPException(status_code=500, detail="Failed to create template")
