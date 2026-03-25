# Project Structure

Complete directory layout of VM Manager:

```
vm-manager/
│
├── backend/                        # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app entry point
│   │   ├── config.py              # Configuration management
│   │   ├── schemas.py             # Pydantic data models
│   │   ├── models.py              # Database models (SQLalchemy)
│   │   │
│   │   ├── api/                   # API Routers
│   │   │   ├── __init__.py
│   │   │   ├── vms.py            # VM endpoints
│   │   │   ├── templates.py      # Template endpoints
│   │   │   ├── monitoring.py     # Monitoring endpoints
│   │   │   └── hypervisors.py    # Hypervisor endpoints
│   │   │
│   │   ├── services/              # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── hypervisor.py      # Hypervisor management (libvirt)
│   │   │   ├── vm_manager.py      # VM management logic
│   │   │   ├── template_manager.py # Template management
│   │   │   └── monitoring.py      # Monitoring service
│   │   │
│   │   ├── database/              # Database utilities
│   │   │   ├── __init__.py
│   │   │   └── db.py             # Database connection & setup
│   │   │
│   │   └── utils/                 # Utility functions
│   │       ├── __init__.py
│   │       ├── auth.py           # Authentication utilities
│   │       └── helpers.py        # Helper functions
│   │
│   ├── tests/                     # Backend tests
│   │   ├── __init__.py
│   │   ├── test_main.py          # Main API tests
│   │   ├── test_vms.py           # VM endpoint tests
│   │   ├── test_templates.py     # Template endpoint tests
│   │   └── conftest.py           # Pytest configuration
│   │
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   ├── Dockerfile                # Docker image definition
│   ├── pytest.ini                # Pytest configuration
│   └── run.py                    # Development server runner
│
├── frontend/                      # React Frontend
│   ├── src/
│   │   ├── main.jsx              # React entry point
│   │   ├── App.jsx               # Main App component
│   │   ├── App.css               # App styles
│   │   ├── index.css             # Global styles
│   │   │
│   │   ├── components/           # Reusable components
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Table.jsx
│   │   │   └── NotificationToast.jsx
│   │   │
│   │   ├── pages/                # Page components
│   │   │   ├── Dashboard.jsx     # Dashboard page
│   │   │   ├── VMs.jsx           # VMs management page
│   │   │   ├── Templates.jsx     # Templates page
│   │   │   ├── Monitoring.jsx    # Monitoring page
│   │   │   └── Settings.jsx      # Settings page (future)
│   │   │
│   │   ├── services/             # API & services
│   │   │   ├── api.js            # API client
│   │   │   ├── auth.js           # Auth service
│   │   │   └── storage.js        # Local storage service
│   │   │
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useApi.js
│   │   │   ├── useAuth.js
│   │   │   └── useNotification.js
│   │   │
│   │   ├── utils/                # Utility functions
│   │   │   ├── format.js         # Formatting utilities
│   │   │   └── validate.js       # Validation utilities
│   │   │
│   │   └── context/              # React Context
│   │       ├── AuthContext.jsx
│   │       └── NotificationContext.jsx
│   │
│   ├── public/                   # Static files
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── tests/                    # Frontend tests
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   │
│   ├── package.json              # NPM dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── Dockerfile                # Docker image definition
│   ├── nginx.conf                # Nginx configuration
│   └── .eslintrc.json            # ESLint configuration
│
├── .github/                      # GitHub configuration
│   ├── workflows/
│   │   └── ci.yml               # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.yml
│   └── pull_request_template.md
│
├── docs/                         # Documentation (future)
│   ├── api/
│   ├── architecture/
│   └── tutorials/
│
├── docker-compose.yml            # Docker Compose definition
├── Makefile                      # Make commands
├── .gitignore                    # Git ignore rules
├── .editorconfig                 # Editor configuration
├── LICENSE                       # MIT License
│
├── README.md                     # Project overview
├── QUICKSTART.md                 # Quick start guide
├── DEPLOYMENT.md                 # Deployment guide
├── CONTRIBUTING.md               # Contributing guide
├── API.md                        # API documentation
├── ROADMAP.md                    # Development roadmap
└── CHANGELOG.md                  # Version history

```

## Directory Descriptions

### `/backend`
Backend API server built with FastAPI. Manages all VM operations via libvirt.

**Key files:**
- `app/main.py` - FastAPI application instance
- `app/services/hypervisor.py` - Libvirt integration
- `app/api/vms.py` - VM CRUD operations

**Key dependencies:**
- FastAPI - Web framework
- libvirt-python - VM management
- Pydantic - Data validation
- SQLAlchemy - ORM

### `/frontend`
React-based web interface for VM management dashboard.

**Key files:**
- `src/App.jsx` - Main application component
- `src/pages/` - Page components
- `src/services/api.js` - API client

**Key dependencies:**
- React 18 - UI framework
- React Router - Navigation
- Axios - HTTP client
- TailwindCSS - Styling
- Recharts - Charting

### `/docker-compose.yml`
Container orchestration for local development and production deployment.

**Services:**
- `backend` - API server (port 8000)
- `frontend` - Web UI (port 80)
- `redis` - Caching (port 6379)
- `postgres` - Database (optional, port 5432)

### `/.github/`
GitHub-specific configurations for CI/CD, issue templates, and PR templates.

### Documentation Files
- `README.md` - Project overview and features
- `QUICKSTART.md` - Get started in 5 minutes
- `DEPLOYMENT.md` - Production deployment guide
- `API.md` - API reference documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `ROADMAP.md` - Future features and timeline

## Key Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template |
| `docker-compose.yml` | Container orchestration |
| `vite.config.js` | Frontend build configuration |
| `pytest.ini` | Test runner configuration |
| `.editorconfig` | Code style consistency |
| `.gitignore` | Git exclusions |
| `Makefile` | Development commands |

## Development Workflow

1. **Backend Development**
   - Edit files in `backend/app/`
   - Tests go in `backend/tests/`
   - API files in `backend/app/api/`

2. **Frontend Development**
   - Components in `frontend/src/components/`
   - Pages in `frontend/src/pages/`
   - Services in `frontend/src/services/`

3. **Adding a New Feature**
   - Backend: Add route in `api/`, service in `services/`, schema in `schemas.py`
   - Frontend: Add page/component, API call in `services/api.js`
   - Tests: Add test files in `tests/`
   - Docs: Update `README.md` or relevant docs

## Import Paths

### Backend
```python
# API routes
from app.api import vms, templates
# Services
from app.services.hypervisor import HypervisorService
# Schemas
from app.schemas import VM, VMCreate
# Configuration
from app.config import settings
```

### Frontend
```javascript
// Components
import Header from './components/Header';
// Pages
import Dashboard from './pages/Dashboard';
// Services
import { vmAPI } from './services/api';
// Styles
import './App.css';
```

---

See individual README files in each directory for more details.
