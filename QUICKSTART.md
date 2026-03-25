# Quick Start Guide

Get VM Manager up and running in minutes!

## Prerequisites

- Docker & Docker Compose installed
- Ubuntu 20.04 or later (for KVM support)
- Minimum 4GB RAM
- 2GB free disk space

## 5-Minute Setup with Docker

### Step 1: Clone Repository
```bash
git clone https://github.com/johan240684/vm-manager.git
cd vm-manager
```

### Step 2: Configure Environment
```bash
cp backend/.env.example backend/.env
# Edit backend/.env if needed
```

### Step 3: Start Services
```bash
docker-compose up -d
```

### Step 4: Access Application
- **Dashboard**: http://localhost
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## Local Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

## First Steps

### 1. Check Dashboard
Browse to http://localhost to see your VM infrastructure overview.

### 2. Navigate to VMs
Click "Virtual Machines" in the sidebar to see available VMs.

### 3. Create Your First VM
- Click **Create VM** button
- Fill in VM details:
  - **Name**: `my-first-vm`
  - **Hostname**: `my-first-vm.local`
  - **CPU**: 2 cores
  - **Memory**: 2048 MB
  - **Disk**: 50 GB
  - **Template**: Ubuntu 22.04 LTS
- Click **Create**

### 4. Start the VM
- Find your VM in the list
- Click the ▶️ (play) icon to start
- Wait for state to change to "running"

### 5. Monitor Performance
- Go to **Monitoring** tab
- View real-time system statistics
- Check individual VM metrics

## Common Tasks

### Stop a VM
1. Go to Virtual Machines
2. Click ⏹️ (stop) icon
3. VM state will change to "stopped"

### Reboot a VM
1. Go to Virtual Machines
2. Click ↻ (reboot) icon
3. VM will restart

### Delete a VM
⚠️ **Warning**: This is irreversible!

1. Go to Virtual Machines
2. Click 🗑️ (delete) icon
3. Confirm deletion

### Browse Templates
1. Go to **Templates**
2. View available pre-configured systems
3. Click **Use Template** to deploy based on template

### Check System Status
1. Go to **Dashboard**
2. View:
   - Total VMs and running VMs
   - Hypervisor status
   - CPU and memory usage
   - Quick action buttons

## API Usage

### List VMs via API
```bash
curl http://localhost:8000/api/vms
```

### Get VM Details
```bash
curl http://localhost:8000/api/vms/my-first-vm
```

### Get System Stats
```bash
curl http://localhost:8000/api/monitoring/stats
```

### Interactive API Docs
Visit http://localhost:8000/docs to test API endpoints directly!

## Docker Compose Commands

### View Logs
```bash
docker-compose logs -f
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Remove Everything (Clean Slate)
```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml
# Or kill the process using the port
lsof -i :8000  # Find process using port 8000
kill -9 <PID>
```

### Libvirt Connection Error
```bash
# Check if libvirt is installed
sudo apt-get install qemu-kvm libvirt-daemon

# Start libvirt service
sudo systemctl start libvirtd
sudo systemctl enable libvirtd
```

### Docker Permission Error
```bash
# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Containers Not Starting
```bash
# Check logs
docker-compose logs

# Rebuild images
docker-compose build --no-cache
docker-compose up -d
```

## Environment Variables

Common environment variables in `.env`:

```env
# Debug mode
DEBUG=false

# API settings
FASTAPI_ENV=production

# Hypervisor
LIBVIRT_URI=qemu:///system

# Database
DATABASE_URL=sqlite:///./vm_manager.db

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## Next Steps

1. **Read Full Documentation**: See [README.md](README.md)
2. **API Reference**: See [API.md](API.md)
3. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support & Help

- **Documentation**: Full docs in [README.md](README.md)
- **Issues**: GitHub Issues page
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

## Video Tutorial (Optional)

Coming soon...

---

Need help? Check the [FAQ](FAQ.md) or open an issue!
