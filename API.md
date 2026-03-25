# API Documentation

VM Manager provides a comprehensive RESTful API for all VM management operations.

## Authentication

All API endpoints (except `/health` and `/`) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### VMs

#### List VMs
```
GET /vms
```

Query Parameters:
- `state` (optional): Filter by VM state (running, stopped, paused, error)
- `hypervisor` (optional): Filter by hypervisor

Response:
```json
[
  {
    "id": "vm-uuid",
    "name": "my-vm",
    "state": "running",
    "cpu_count": 2,
    "memory_mb": 2048,
    "ip_address": "192.168.1.100",
    "mac_address": "52:54:00:12:34:56",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get VM Details
```
GET /vms/{vm_name}
```

Response:
```json
{
  "id": "vm-uuid",
  "name": "my-vm",
  "state": "running",
  "cpu_count": 2,
  "memory_mb": 2048,
  "max_memory_mb": 4096,
  "ip_address": "192.168.1.100",
  "mac_address": "52:54:00:12:34:56",
  "created_at": "2024-01-01T00:00:00Z",
  "modified_at": "2024-01-02T00:00:00Z"
}
```

#### Create VM
```
POST /vms
Content-Type: application/json

{
  "name": "my-vm",
  "hostname": "my-vm.example.com",
  "cpu_count": 2,
  "memory_mb": 2048,
  "disk_gb": 50,
  "hypervisor_type": "kvm",
  "template_id": "ubuntu-22-04",
  "network_bridge": "br0",
  "auto_start": false,
  "description": "My test VM"
}
```

Response:
```json
{
  "success": true,
  "message": "VM 'my-vm' created successfully",
  "vm_id": "my-vm"
}
```

#### Update VM
```
PUT /vms/{vm_name}
Content-Type: application/json

{
  "cpu_count": 4,
  "memory_mb": 4096,
  "auto_start": true
}
```

#### Delete VM
```
DELETE /vms/{vm_name}
```

Response:
```json
{
  "success": true,
  "message": "VM 'my-vm' deleted successfully",
  "vm_id": "my-vm"
}
```

#### Start VM
```
POST /vms/{vm_name}/start
```

#### Stop VM
```
POST /vms/{vm_name}/stop
```

Query Parameters:
- `force` (optional, boolean): Force stop the VM

#### Reboot VM
```
POST /vms/{vm_name}/reboot
```

### Templates

#### List Templates
```
GET /templates
```

Response:
```json
[
  {
    "id": "ubuntu-22-04",
    "name": "Ubuntu 22.04 LTS",
    "os_type": "ubuntu",
    "os_version": "22.04",
    "description": "Ubuntu 22.04 LTS with minimal configuration",
    "default_cpu": 2,
    "default_memory_mb": 2048,
    "default_disk_gb": 50,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Template
```
GET /templates/{template_id}
```

#### Create Custom Template
```
POST /templates
Content-Type: application/json

{
  "name": "Custom Ubuntu",
  "os_type": "ubuntu",
  "os_version": "22.04",
  "description": "Custom Ubuntu template",
  "image_url": "https://example.com/ubuntu-22.04.qcow2",
  "default_cpu": 4,
  "default_memory_mb": 4096,
  "default_disk_gb": 100
}
```

### Monitoring

#### Get System Statistics
```
GET /monitoring/stats
```

Response:
```json
{
  "total_vms": 10,
  "running_vms": 8,
  "stopped_vms": 2,
  "total_cpu_cores": 16,
  "total_memory_gb": 32,
  "used_memory_gb": 18.5,
  "total_disk_gb": 1000,
  "used_disk_gb": 450.3,
  "hypervisors": 1,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

#### Get VM Metrics
```
GET /monitoring/vms/{vm_name}/metrics
```

Response:
```json
{
  "vm_id": "vm-uuid",
  "vm_name": "my-vm",
  "metrics": {
    "cpu_percent": 25.5,
    "memory_mb": 1024,
    "memory_percent": 50.0,
    "disk_read_bytes": 1024000,
    "disk_write_bytes": 512000,
    "network_rx_bytes": 2048000,
    "network_tx_bytes": 1024000,
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

#### Get VM Metrics History
```
GET /monitoring/vms/history/{vm_name}
```

Query Parameters:
- `hours` (optional, default: 24): Number of hours of history to retrieve

#### Get Alerts
```
GET /monitoring/alerts
```

### Hypervisors

#### List Hypervisors
```
GET /hypervisors
```

Response:
```json
[
  {
    "id": "main-hypervisor",
    "name": "Main KVM Host",
    "uri": "qemu:///system",
    "hypervisor_type": "kvm",
    "status": "connected",
    "hostname": "kvm-host-1",
    "cpu_cores": 16,
    "memory_gb": 32,
    "vms_running": 8,
    "vms_total": 10
  }
]
```

#### Get Hypervisor Details
```
GET /hypervisors/{hypervisor_id}
```

#### Get Hypervisor Status
```
GET /hypervisors/{hypervisor_id}/status
```

Response:
```json
{
  "hypervisor_id": "main-hypervisor",
  "status": "connected",
  "uptime": "120 days",
  "cpu_usage_percent": 35.5,
  "memory_usage_percent": 58.3,
  "disk_usage_percent": 45.0,
  "vms_running": 8,
  "vms_total": 10
}
```

## Response Format

All successful responses return HTTP 2xx status codes:

```json
{
  "data": {...},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

Error responses return appropriate HTTP status codes with error details:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE"
}
```

## Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful request with no content
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting

The API implements rate limiting:
- 100 requests per minute for authenticated users
- 10 requests per minute for unauthenticated requests

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067200
```

## Webhook Support (Future)

Webhooks can be configured to receive notifications for VM events:

```bash
POST /webhooks
{
  "url": "https://example.com/webhook",
  "events": ["vm.created", "vm.deleted", "vm.state_changed"]
}
```

## Pagination

List endpoints support pagination:

Query Parameters:
- `skip` (optional, default: 0): Number of records to skip
- `limit` (optional, default: 100): Maximum records to return

Response headers:
```
X-Total-Count: 250
X-Skip: 0
X-Limit: 100
```

## Versioning

Current API version: `v1`

Future versions will be available at `/api/v2`, `/api/v3`, etc.

## Examples

### Create and Start a VM

```bash
# Create VM
curl -X POST http://localhost:8000/api/vms \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "web-server",
    "hostname": "web-server.example.com",
    "cpu_count": 4,
    "memory_mb": 4096,
    "disk_gb": 80,
    "template_id": "ubuntu-22-04"
  }'

# Start VM
curl -X POST http://localhost:8000/api/vms/web-server/start \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get VM Metrics

```bash
curl -X GET http://localhost:8000/api/monitoring/vms/my-vm/metrics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## SDKs

Official SDKs are available for:
- Python: `vm-manager-sdk`
- JavaScript/TypeScript: `vm-manager-js-sdk`
- Go: `vm-manager-go-sdk`

## Support

For API questions and support:
- Documentation: https://docs.example.com
- GitHub Issues: https://github.com/yourusername/vm-manager/issues
- Email: api-support@example.com
