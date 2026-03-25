# VM Manager

A powerful, web-based GUI for managing virtual machines on Ubuntu servers. One-click VM deployment, templates, monitoring, and automation.

## Features

✅ **One-Click VM Deployment** - Deploy VMs instantly from pre-configured templates  
✅ **Multi-Hypervisor Support** - KVM, Xen, OpenVZ, and more  
✅ **VM Templates** - Ubuntu, Windows, CentOS, Debian, and custom templates  
✅ **Real-time Monitoring** - CPU, Memory, Disk, and Network monitoring  
✅ **Automation** - Scheduled backups, auto-scaling, batch operations  
✅ **Intuitive Dashboard** - Modern React interface  
✅ **API-First Architecture** - RESTful API for programmatic access  
✅ **Docker Support** - Easy deployment and containerization  

## Quick Start

### Prerequisites

- Ubuntu 20.04 or later
- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (optional)
- KVM/Libvirt installed and configured

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/vm-manager.git
cd vm-manager
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

#### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run build
```

#### 4. Run with Docker Compose
```bash
cd ..
docker-compose up -d
```

The web interface will be available at `http://localhost:3000`

## Architecture

```
vm-manager/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── api/
│   │   │   ├── vms.py
│   │   │   ├── templates.py
│   │   │   ├── monitoring.py
│   │   │   └── hypervisors.py
│   │   ├── services/
│   │   │   ├── vm_manager.py
│   │   │   ├── hypervisor.py
│   │   │   ├── monitoring.py
│   │   │   └── template_manager.py
│   │   └── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .gitignore
└── README.md
```

## API Endpoints

### VMs
- `GET /api/vms` - List all VMs
- `POST /api/vms` - Create new VM
- `GET /api/vms/{id}` - Get VM details
- `PUT /api/vms/{id}` - Update VM
- `DELETE /api/vms/{id}` - Delete VM
- `POST /api/vms/{id}/start` - Start VM
- `POST /api/vms/{id}/stop` - Stop VM
- `POST /api/vms/{id}/reboot` - Reboot VM

### Templates
- `GET /api/templates` - List available templates
- `POST /api/templates` - Create custom template

### Monitoring
- `GET /api/monitoring/stats` - Get system statistics
- `GET /api/vms/{id}/metrics` - Get VM metrics

### Hypervisors
- `GET /api/hypervisors` - List connected hypervisors
- `GET /api/hypervisors/{id}/status` - Get hypervisor status

## Configuration

Copy `.env.example` to `.env` and configure:

```env
# Backend
FASTAPI_ENV=production
DATABASE_URL=postgresql://user:password@db:5432/vmmanager
SECRET_KEY=your-secret-key

# Hypervisor
LIBVIRT_URI=qemu:///system
HYPERVISOR_TYPE=kvm

# Redis (for caching & job queue)
REDIS_URL=redis://redis:6379

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## Development

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm start
```

## Features in Detail

### One-Click Deployment
1. Select template (Ubuntu 22.04, Windows 2022, etc.)
2. Configure resources (CPU, RAM, Storage)
3. Click Deploy
4. VM is ready in seconds

### Templates
Pre-configured VMs for quick deployment:
- **Ubuntu** - 20.04, 22.04 LTS
- **Windows** - Windows 2019, 2022
- **CentOS** - 7, 8, Stream
- **Debian** - 10, 11, 12
- Custom templates for your organization

### Monitoring & Automation
- Real-time resource monitoring
- Scheduled backups
- Auto-scaling policies
- Performance alerts
- Log aggregation

## Security

- JWT authentication
- Role-based access control (RBAC)
- API key management
- HTTPS/TLS support
- Encrypted credentials storage

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/yourusername/vm-manager/issues) on GitHub.

## Roadmap

- [ ] Web console (VNC/SPICE)
- [ ] Terraform provider
- [ ] Kubernetes integration
- [ ] Advanced networking
- [ ] Cloud import/export
- [ ] Mobile app
- [ ] Multi-cloud support

---

**Made with ❤️ for VM administrators**
