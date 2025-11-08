# U-CHS Quick Start Guide

Get the Universal Crop Health Scanner running in 5 minutes!

## Prerequisites

✅ Python 3.10+
✅ Node.js 18+
✅ Docker & Docker Compose

## Option 1: Docker (Recommended for Quick Start)

```bash
# Clone and navigate
cd Phenom

# Start all services
docker-compose up

# Access:
# - Backend API: http://localhost:8000/api/docs
# - Database: localhost:5432
# - PgAdmin: http://localhost:5050 (dev profile)
```

That's it! The backend is running.

## Option 2: Manual Setup (Development)

### Backend

```bash
cd backend

# Setup virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your values

# Run
uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000
**API Docs:** http://localhost:8000/api/docs

### Frontend Mobile

```bash
cd frontend/mobile

# Install dependencies
npm install

# Start Expo
npm start

# Scan QR code with Expo Go app
# Or press 'w' for web, 'a' for Android, 'i' for iOS
```

## First API Call

Test the health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2025-01-15T10:00:00",
  "ml_models_loaded": false
}
```

## Next Steps

1. **Read the docs:**
   - [Setup Guide](docs/setup.md) - Detailed setup instructions
   - [Architecture](docs/architecture.md) - System design
   - [Roadmap](docs/roadmap.md) - 90-day plan
   - [Contributing](CONTRIBUTING.md) - How to contribute

2. **Configure storage:**
   - Sign up for [Supabase](https://supabase.com) (free tier)
   - Create a storage bucket named `crop-images`
   - Add credentials to `backend/.env`

3. **Download ML models:**
   ```bash
   cd ml-pipeline/models
   # Download SAM model (choose based on your GPU)
   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
   ```

4. **Test the mobile app:**
   - Open Expo Go on your phone
   - Scan the QR code
   - Try the camera feature
   - Note: Analysis won't work until ML models are configured

5. **Start developing:**
   - Check GitHub Issues for tasks
   - Read the roadmap for current priorities
   - Join team discussions

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (should be 3.10+)
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

**Frontend errors:**
- Clear cache: `npx expo start --clear`
- Reinstall: `rm -rf node_modules && npm install`

**Docker issues:**
- Check ports aren't in use: `docker-compose down`
- Rebuild: `docker-compose build --no-cache`

**Database connection errors:**
- Make sure PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Test connection: `docker-compose exec postgres psql -U uchs_user -d uchs_db`

## Project Structure

```
Phenom/
├── backend/          # FastAPI backend
├── frontend/
│   ├── mobile/      # React Native app
│   └── web/         # React web app (future)
├── ml-pipeline/     # ML models and scripts
├── infrastructure/  # Docker, K8s, Terraform
├── docs/           # Documentation
└── docker-compose.yml
```

## Key Commands

```bash
# Backend
uvicorn app.main:app --reload          # Run backend
pytest tests/ -v                       # Run tests
black app/                             # Format code

# Frontend
npm start                              # Start Expo
npm test                               # Run tests
npm run lint                           # Lint code

# Docker
docker-compose up                      # Start all
docker-compose down                    # Stop all
docker-compose logs -f backend         # View logs
```

## Resources

- 📚 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/your-org/phenom/issues)
- 💬 [Discussions](https://github.com/your-org/phenom/discussions)
- 📖 [API Docs](http://localhost:8000/api/docs) (when running)

## Team Roles

As outlined in the roadmap:
- **Person A**: Frontend/Mobile + UI/UX
- **Person B**: Backend + ML Pipeline
- **Person C**: Data + User Research

Happy coding! 🌱🚀
