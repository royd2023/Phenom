# U-CHS Quick Start Guide

Get the Universal Crop Health Scanner running in 5 minutes!

## Prerequisites

✅ Python 3.10+  
✅ Node.js 18+  
✅ Docker & Docker Compose  
✅ **Supabase account** (free) - [Sign up here](https://supabase.com)

## Team Setup (Do This First!)

**One person on your team** should set up Supabase, then share credentials with everyone.

👉 **Follow**: [docs/team-setup.md](docs/team-setup.md) for complete Supabase setup

**Quick version:**
1. Create Supabase project at [supabase.com](https://supabase.com)
2. Create storage bucket named `crop-images`
3. Share DATABASE_URL, SUPABASE_URL, and SUPABASE_KEY with team

## Individual Developer Setup

### 1. Get Team Credentials

Ask your team lead (Person B) for:
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY`

### 2. Configure Environment

```bash
cd Phenom

# Copy environment template
cp .env.example .env

# Edit .env and paste your team's Supabase credentials
nano .env  # or code .env, or vim .env
```

### 3. Start Backend

**Option A: Docker (Recommended)**

```bash
docker-compose up
```

**Option B: Manual**

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000  
**API Docs:** http://localhost:8000/api/docs

### 4. Start Frontend Mobile

```bash
cd frontend/mobile
npm install
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

1. **Download ML models** (optional for initial testing):
   ```bash
   cd ml-pipeline/models
   # Download SAM model (choose based on your GPU)
   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
   ```

2. **Read the docs:**
   - [Team Setup](docs/team-setup.md) - Supabase configuration
   - [Setup Guide](docs/setup.md) - Detailed setup
   - [Architecture](docs/architecture.md) - System design
   - [Roadmap](docs/roadmap.md) - 90-day plan

3. **Start developing:**
   - Check GitHub Issues for tasks
   - Read the roadmap for priorities
   - Join team discussions

## Troubleshooting

**Backend won't start:**
- Check DATABASE_URL in .env is correct
- Verify Supabase project is active
- Check Python version: `python --version` (should be 3.10+)

**"Connection refused" to database:**
- Verify Supabase credentials in .env
- Check Supabase dashboard - project might be paused

**Frontend errors:**
- Clear cache: `npx expo start --clear`
- Reinstall: `rm -rf node_modules && npm install`

**Images not uploading:**
- Verify SUPABASE_BUCKET=crop-images in .env
- Check bucket exists in Supabase Storage
- Ensure bucket policies allow uploads

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
docker-compose up                      # Start backend
docker-compose down                    # Stop all
docker-compose logs -f backend         # View logs

# Local DB (offline development)
docker-compose --profile local-db up   # Use local PostgreSQL instead of Supabase
```

## Resources

- 📚 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/your-org/phenom/issues)
- 💬 [Discussions](https://github.com/your-org/phenom/discussions)
- 📖 [API Docs](http://localhost:8000/api/docs) (when running)
- 🗄️ [Supabase Dashboard](https://supabase.com/dashboard)

## Team Roles

As outlined in the roadmap:
- **Person A**: Frontend/Mobile + UI/UX
- **Person B**: Backend + ML Pipeline + **Supabase Admin**
- **Person C**: Data + User Research

Happy coding! 🌱🚀
