# U-CHS Project Structure

Complete file structure for the Universal Crop Health Scanner project.

## Root Directory

```
Phenom/
├── .github/                      # GitHub Actions CI/CD
│   └── workflows/
│       ├── backend-ci.yml       # Backend testing and build
│       └── frontend-ci.yml      # Frontend testing and build
│
├── backend/                      # FastAPI Backend Service
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   │
│   │   ├── api/                 # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── health.py        # Health check endpoints
│   │   │   ├── analysis.py      # Image analysis endpoints
│   │   │   ├── images.py        # Image management endpoints
│   │   │   └── users.py         # User authentication endpoints
│   │   │
│   │   ├── core/                # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # Application settings
│   │   │   └── logging_config.py # Logging configuration
│   │   │
│   │   ├── models/              # Data models and schemas
│   │   │   ├── __init__.py
│   │   │   └── schemas.py       # Pydantic models
│   │   │
│   │   ├── services/            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── ml_service.py    # ML inference (SAM + DINO)
│   │   │   └── storage_service.py # Image storage (Supabase/S3)
│   │   │
│   │   └── utils/               # Utility functions
│   │       └── __init__.py
│   │
│   ├── tests/                   # Backend tests
│   │   ├── unit/                # Unit tests
│   │   └── integration/         # Integration tests
│   │
│   ├── .env.example             # Environment variables template
│   ├── Dockerfile               # Docker configuration
│   └── requirements.txt         # Python dependencies
│
├── frontend/                     # Frontend Applications
│   ├── mobile/                  # React Native Mobile App
│   │   ├── src/
│   │   │   ├── components/      # Reusable UI components
│   │   │   │
│   │   │   ├── screens/         # Screen components
│   │   │   │   ├── HomeScreen.tsx
│   │   │   │   ├── CameraScreen.tsx
│   │   │   │   ├── ResultScreen.tsx
│   │   │   │   ├── HistoryScreen.tsx
│   │   │   │   └── SettingsScreen.tsx
│   │   │   │
│   │   │   ├── navigation/      # Navigation configuration
│   │   │   │   └── AppNavigator.tsx
│   │   │   │
│   │   │   ├── services/        # API and external services
│   │   │   │   └── api.ts       # RTK Query API client
│   │   │   │
│   │   │   ├── store/           # Redux store
│   │   │   │   └── index.ts
│   │   │   │
│   │   │   ├── utils/           # Utility functions
│   │   │   │   └── theme.ts
│   │   │   │
│   │   │   └── assets/          # Images, fonts, etc.
│   │   │
│   │   ├── tests/               # Mobile app tests
│   │   ├── App.tsx              # Root component
│   │   ├── app.json             # Expo configuration
│   │   ├── package.json         # NPM dependencies
│   │   └── tsconfig.json        # TypeScript configuration
│   │
│   └── web/                     # React Web App (Future)
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── services/
│       │   └── utils/
│       └── tests/
│
├── ml-pipeline/                  # ML Models and Data
│   ├── models/                  # Model weights and configs
│   │   ├── README.md            # Model download instructions
│   │   ├── sam_vit_h_4b8939.pth # SAM model (to download)
│   │   └── grounding_dino/      # Grounding DINO (auto-downloaded)
│   │
│   ├── scripts/                 # Training and inference scripts
│   │   ├── download_models.py
│   │   ├── evaluate.py
│   │   └── fine_tune.py
│   │
│   ├── notebooks/               # Jupyter notebooks for experiments
│   │   ├── model_exploration.ipynb
│   │   └── prompt_engineering.ipynb
│   │
│   └── data/                    # Dataset management
│       ├── raw/                 # Original images
│       ├── processed/           # Preprocessed images
│       └── annotations/         # Labels and metadata
│
├── infrastructure/               # DevOps and Infrastructure
│   ├── docker/                  # Additional Docker files
│   │   ├── nginx.conf
│   │   └── docker-compose.prod.yml
│   │
│   ├── k8s/                     # Kubernetes manifests
│   │   ├── deployment.yml
│   │   ├── service.yml
│   │   └── ingress.yml
│   │
│   └── terraform/               # Infrastructure as Code
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── docs/                         # Documentation
│   ├── setup.md                 # Development setup guide
│   ├── architecture.md          # System architecture
│   └── roadmap.md               # 90-day development plan
│
├── .gitignore                    # Git ignore rules
├── .dockerignore                 # Docker ignore rules
├── docker-compose.yml            # Docker Compose configuration
├── README.md                     # Project overview
├── QUICKSTART.md                 # Quick start guide
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
└── PROJECT_STRUCTURE.md          # This file
```

## Key Files Explained

### Backend

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app initialization, middleware, routes |
| `app/api/*.py` | API endpoint definitions |
| `app/services/ml_service.py` | SAM and Grounding DINO inference |
| `app/services/storage_service.py` | Image upload/download to Supabase/S3 |
| `app/models/schemas.py` | Pydantic models for request/response validation |
| `app/core/config.py` | Environment configuration using pydantic-settings |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Template for environment variables |

### Frontend Mobile

| File | Purpose |
|------|---------|
| `App.tsx` | Root component with providers (Redux, Navigation, Theme) |
| `src/navigation/AppNavigator.tsx` | Navigation structure (Stack + Tabs) |
| `src/screens/*.tsx` | Screen components for each view |
| `src/services/api.ts` | RTK Query API client with all endpoints |
| `src/store/index.ts` | Redux store configuration |
| `package.json` | NPM dependencies (React Native, Expo, etc.) |
| `app.json` | Expo configuration (permissions, splash, icons) |

### ML Pipeline

| Directory | Purpose |
|-----------|---------|
| `models/` | Store downloaded model weights (SAM, DINO) |
| `scripts/` | Python scripts for model operations |
| `notebooks/` | Jupyter notebooks for experimentation |
| `data/` | Image datasets and annotations |

### Infrastructure

| File/Directory | Purpose |
|----------------|---------|
| `docker-compose.yml` | Local development orchestration |
| `k8s/` | Production Kubernetes deployment |
| `terraform/` | Cloud infrastructure provisioning |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview and quick links |
| `QUICKSTART.md` | 5-minute setup guide |
| `docs/setup.md` | Detailed development setup |
| `docs/architecture.md` | System design and data flow |
| `docs/roadmap.md` | 90-day development timeline |
| `CONTRIBUTING.md` | How to contribute code |

## File Statistics

- **Total Backend Files**: ~20 Python files
- **Total Frontend Files**: ~15 TypeScript/TSX files
- **Total Config Files**: ~10 (Docker, CI/CD, etc.)
- **Total Documentation**: ~7 Markdown files

## Tech Stack Summary

### Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **ML**: PyTorch, SAM, Grounding DINO
- **Database**: PostgreSQL (via SQLAlchemy)
- **Storage**: Supabase / AWS S3

### Frontend
- **Language**: TypeScript
- **Framework**: React Native (Expo)
- **State**: Redux Toolkit + RTK Query
- **UI**: React Native Paper
- **Navigation**: React Navigation

### DevOps
- **Containers**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Orchestration**: Kubernetes (future)
- **IaC**: Terraform (future)

## Next Steps

1. ✅ Project structure created
2. ⬜ Download ML model weights
3. ⬜ Set up Supabase account
4. ⬜ Configure environment variables
5. ⬜ Run first API call
6. ⬜ Test mobile app
7. ⬜ Start Week 1 tasks from roadmap

For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md).
