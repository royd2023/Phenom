# Development Setup Guide

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **Docker**: Latest version
- **Git**: Latest version
- **GPU** (recommended): CUDA-compatible GPU for ML inference

## Initial Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd phenom
```

### 2. Backend Setup

#### Using Virtual Environment (Development)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your configuration
# Set DATABASE_URL, SECRET_KEY, SUPABASE_URL, etc.

# Run the backend
uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/api/docs`

#### Using Docker

```bash
# From project root
docker-compose up backend postgres

# Or run everything
docker-compose up
```

### 3. Frontend Mobile Setup

```bash
cd frontend/mobile

# Install dependencies
npm install

# Start Expo development server
npm start

# Run on specific platform
npm run android  # For Android
npm run ios      # For iOS (Mac only)
npm run web      # For web browser
```

### 4. Database Setup

#### Using Docker (Recommended)

```bash
docker-compose up postgres
```

#### Manual PostgreSQL Setup

```bash
# Install PostgreSQL 15

# Create database
createdb uchs_db

# Update DATABASE_URL in backend/.env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/uchs_db
```

## ML Models Setup

### Download Model Weights

```bash
cd ml-pipeline/models

# SAM Model (choose one based on your needs)
# vit_h (largest, most accurate, ~2.4GB)
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

# vit_l (medium)
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

# vit_b (smallest, fastest)
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

### Grounding DINO

Grounding DINO will be automatically downloaded from Hugging Face on first use.

## Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
# Application
PROJECT_NAME=U-CHS API
VERSION=0.1.0
DEBUG=True

# Database
DATABASE_URL=postgresql://uchs_user:uchs_password@localhost:5432/uchs_db

# Authentication
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage (Supabase)
STORAGE_PROVIDER=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_BUCKET=crop-images

# ML Models
MODEL_CACHE_DIR=./ml-pipeline/models
SAM_MODEL_TYPE=vit_h
USE_GPU=True
MAX_IMAGE_SIZE=1024

# Logging
LOG_LEVEL=INFO
```

### Generate Secret Key

```bash
openssl rand -hex 32
```

### Frontend Configuration

Update API endpoint in `frontend/mobile/src/services/api.ts`:

```typescript
const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'  // Development
  : 'https://your-production-api.com/api/v1';  // Production
```

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend/mobile
npm test
npm test -- --coverage  # With coverage
```

## Code Quality

### Backend

```bash
cd backend

# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Frontend

```bash
cd frontend/mobile

# Lint
npm run lint

# Type checking
npm run type-check
```

## Troubleshooting

### Backend Issues

**ImportError: No module named 'app'**
- Make sure you're in the `backend/` directory
- Activate virtual environment

**Database connection error**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Test connection: `psql <DATABASE_URL>`

**CUDA/GPU errors**
- Set `USE_GPU=False` in .env to use CPU
- Verify CUDA installation: `nvidia-smi`

### Frontend Issues

**Expo metro bundler errors**
- Clear cache: `npx expo start --clear`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**API connection errors**
- Check backend is running
- Verify API_BASE_URL in api.ts
- On Android emulator, use `http://10.0.2.2:8000` instead of `localhost:8000`
- On iOS simulator, `http://localhost:8000` works

### Docker Issues

**Port already in use**
- Change ports in docker-compose.yml
- Or stop conflicting services

**Image build fails**
- Clear Docker cache: `docker-compose build --no-cache`

## Next Steps

1. **Verify setup**: Visit `http://localhost:8000/api/docs` to see API documentation
2. **Test health endpoint**: `curl http://localhost:8000/api/v1/health`
3. **Run mobile app**: Start Expo and scan QR code with Expo Go app
4. **Read roadmap**: See `docs/roadmap.md` for development plan
5. **Start coding**: Check GitHub issues for tasks to work on

## Useful Commands

```bash
# Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
npx expo start
npx expo start --android
npx expo start --ios
npx expo start --web

# Docker
docker-compose up
docker-compose down
docker-compose logs -f backend
docker-compose exec backend bash

# Database
docker-compose exec postgres psql -U uchs_user -d uchs_db
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
- [SAM GitHub](https://github.com/facebookresearch/segment-anything)
- [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO)
