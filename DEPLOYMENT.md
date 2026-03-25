# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Ubuntu 20.04 or later
- At least 4GB RAM
- 2 CPU cores
- 20GB disk space

## Local Development

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vm-manager.git
cd vm-manager
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## Production Deployment

### Using Docker Compose

1. Update `.env` with production values:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with production config
```

2. Configure HTTPS with Nginx reverse proxy:
```bash
# Use Certbot for SSL certificates
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d yourdomain.com
```

3. Update nginx.conf with SSL configuration

4. Start services:
```bash
docker-compose up -d
```

### Using Kubernetes

A Kubernetes manifest file is included. Deploy with:
```bash
kubectl apply -f k8s/
```

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| Memory | 4GB | 8GB+ |
| Storage | 50GB | 100GB+ |
| Disk I/O | SATA | SSD |

## Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Security
SECRET_KEY=generate-a-strong-key
ALGORITHM=HS256

# Database
DATABASE_URL=postgresql://user:pass@db:5432/vmmanager

# Hypervisor
LIBVIRT_URI=qemu:///system

# Redis
REDIS_URL=redis://redis:6379
```

### Hypervisor Setup

#### KVM/QEMU

```bash
# Install
sudo apt-get install qemu-kvm libvirt-daemon virsh

# Start service
sudo systemctl start libvirtd

# Add current user to libvirt group
sudo usermod -aG libvirt $USER
```

#### Xen

```bash
# Install
sudo apt-get install xen-hypervisor-4.17-amd64

# Configure grub
# Edit /etc/default/grub: GRUB_DEFAULT="Ubuntu, with Xen 4.17-amd64"
sudo update-grub
sudo reboot
```

#### OpenVZ

```bash
# Install
sudo apt-get install openvz-kernel-host ploop vzctl vzquota

# Configure
sudo nano /etc/sysctl.conf
# Enable necessary settings
sudo sysctl -p
```

## SSL/TLS Setup

### Self-Signed Certificate

```bash
mkdir -p ./certs
openssl req -x509 -newkey rsa:4096 -nodes -out ./certs/cert.pem -keyout ./certs/key.pem -days 365
```

### Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./certs/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./certs/
```

## Backup and Recovery

### Database Backup

```bash
# Backup SQLite
docker-compose exec backend tar czf - vm_manager.db | gzip > backup.tar.gz

# Backup PostgreSQL
docker-compose exec postgres pg_dump -U vmmanager vmmanager > backup.sql
```

### VM Backup

```bash
# Backup all VMs
virsh list --name | while read vm; do
  virsh dumpxml $vm > /backup/$vm.xml
done
```

## Monitoring

### Health Checks

```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost/
```

### Logs

```bash
# View all logs
docker-compose logs

# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

## Updates

### Pull Latest Changes

```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Libvirt Connection Issues

```bash
# Check service status
sudo systemctl status libvirtd

# Restart service
sudo systemctl restart libvirtd

# Test connection
virsh -c qemu:///system list
```

### Port Already in Use

```bash
# Change ports in docker-compose.yml
# Or kill existing processes
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Database Issues

```bash
# Reset database
docker-compose exec backend rm vm_manager.db
docker-compose restart backend
```

## Security Best Practices

1. **Change default credentials**
2. **Use HTTPS in production**
3. **Generate strong SECRET_KEY**
4. **Configure firewall rules**
5. **Regular backups**
6. **Keep system updated**
7. **Use strong passwords for VMs**
8. **Enable audit logging**

## Performance Tuning

### Redis Tuning

```bash
# Update maxmemory policy in docker-compose.yml
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### PostgreSQL Tuning

```bash
# Optimize shared_buffers and work_mem in postgres.conf
```

### Nginx Tuning

```bash
# Update worker_connections in nginx.conf
worker_processes auto;
worker_connections 4096;
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/vm-manager/issues
- Documentation: /docs
- Email: support@example.com
