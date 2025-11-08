# U-CHS Architecture Documentation

## System Overview

U-CHS (Universal Crop Health Scanner) is a full-stack application that uses zero-shot machine learning models to analyze crop health from smartphone photos.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │  Mobile App      │          │   Web App        │         │
│  │  (React Native)  │          │   (React)        │         │
│  └────────┬─────────┘          └────────┬─────────┘         │
│           │                              │                    │
│           └──────────────┬───────────────┘                    │
└───────────────────────────┼──────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   API Gateway   │
                    └───────┬────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                      Backend (FastAPI)                        │
│                           │                                   │
│  ┌────────────────────────┼───────────────────────────────┐  │
│  │         API Layer      │                               │  │
│  │  ┌─────────┬──────────┬───────────┬─────────┐         │  │
│  │  │ Health  │ Analysis │  Images   │  Users  │         │  │
│  │  │ Routes  │  Routes  │  Routes   │ Routes  │         │  │
│  │  └────┬────┴────┬─────┴─────┬─────┴────┬────┘         │  │
│  └───────┼─────────┼───────────┼──────────┼──────────────┘  │
│          │         │           │          │                  │
│  ┌───────▼─────────▼───────────▼──────────▼──────────────┐  │
│  │              Service Layer                             │  │
│  │  ┌──────────────┐  ┌─────────────────┐  ┌──────────┐  │  │
│  │  │  ML Service  │  │ Storage Service │  │   Auth   │  │  │
│  │  │  (SAM +      │  │ (Supabase/S3)   │  │ Service  │  │  │
│  │  │   Grounding  │  │                 │  │          │  │  │
│  │  │   DINO)      │  │                 │  │          │  │  │
│  │  └──────┬───────┘  └────────┬────────┘  └─────┬────┘  │  │
│  └─────────┼─────────────────────┼──────────────────┼─────┘  │
│            │                     │                  │         │
└────────────┼─────────────────────┼──────────────────┼────────┘
             │                     │                  │
    ┌────────▼──────┐    ┌────────▼────────┐  ┌──────▼──────┐
    │  ML Models    │    │ Object Storage  │  │  PostgreSQL │
    │  (SAM, DINO)  │    │ (Images/Masks)  │  │  Database   │
    └───────────────┘    └─────────────────┘  └─────────────┘
```

## Component Details

### Frontend Layer

#### Mobile App (React Native + Expo)
- **Purpose**: Primary user interface for farmers
- **Key Features**:
  - Camera integration (photo capture)
  - Image gallery selection
  - Real-time analysis results
  - Analysis history
  - Settings management

#### Web App (React)
- **Purpose**: Desktop/browser access for larger operations
- **Key Features**:
  - Batch image upload
  - Advanced analytics dashboard
  - Export capabilities
  - Admin features

### API Gateway
- Request routing
- Rate limiting
- CORS handling
- Authentication middleware

### Backend Layer

#### API Endpoints

**Health Routes** (`/api/v1/health`)
- `GET /health` - System health check
- `GET /ready` - Kubernetes readiness probe
- `GET /live` - Kubernetes liveness probe

**Analysis Routes** (`/api/v1/analysis`)
- `POST /upload` - Upload image and trigger analysis
- `GET /{analysis_id}` - Retrieve analysis results

**Images Routes** (`/api/v1/images`)
- `GET /` - List user's images
- `DELETE /{image_id}` - Delete image

**Users Routes** (`/api/v1/users`)
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /me` - Get current user info

#### Service Layer

**ML Service**
- Loads and manages ML models
- Preprocesses images
- Runs zero-shot segmentation
- Post-processes results
- Calculates metrics (IoU, area %, confidence)

**Storage Service**
- Manages image uploads
- Handles file storage (Supabase/S3)
- Generates public URLs
- Manages file deletion

**Auth Service** (TODO)
- User authentication
- JWT token generation/validation
- Password hashing
- Session management

### Data Layer

#### PostgreSQL Database
Schema:
```sql
-- Users table
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  hashed_password VARCHAR,
  full_name VARCHAR,
  is_active BOOLEAN,
  created_at TIMESTAMP
)

-- Analyses table
analyses (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  image_url VARCHAR,
  crop_type VARCHAR,
  prompt TEXT,
  stress_detected BOOLEAN,
  stress_severity VARCHAR,
  processing_time_ms FLOAT,
  created_at TIMESTAMP
)

-- Segmentation results table
segmentation_results (
  id UUID PRIMARY KEY,
  analysis_id UUID REFERENCES analyses(id),
  mask_url VARCHAR,
  confidence FLOAT,
  bounding_box JSON,
  area_percentage FLOAT
)
```

#### Object Storage (Supabase/S3)
- Original images: `/uploads/{analysis_id}_{filename}`
- Segmentation masks: `/masks/{analysis_id}_{result_id}.png`
- Annotated images: `/annotated/{analysis_id}.jpg`

### ML Pipeline

#### Zero-Shot Inference Flow

```
1. Image Upload
   ↓
2. Preprocessing
   - Resize (max 1024px)
   - Color correction
   - Format normalization
   ↓
3. Grounding DINO Detection
   - Input: Image + text prompt
   - Output: Bounding boxes + confidence scores
   ↓
4. SAM Segmentation
   - Input: Image + bounding boxes
   - Output: Precise segmentation masks
   ↓
5. Post-processing
   - Filter low confidence (<0.5)
   - Calculate area percentages
   - Merge overlapping segments
   ↓
6. Result Generation
   - Severity calculation
   - Recommendation engine
   - Metadata compilation
```

#### Model Details

**Segment Anything Model (SAM)**
- Model: `vit_h` (2.4GB) / `vit_l` (1.2GB) / `vit_b` (375MB)
- Input: Image (1024x1024) + prompts (boxes/points/text)
- Output: Binary segmentation masks
- Inference time: ~500ms (GPU) / ~3s (CPU)

**Grounding DINO**
- Model: `IDEA-Research/grounding-dino-base`
- Input: Image + text description
- Output: Bounding boxes + labels + confidence
- Inference time: ~300ms (GPU) / ~2s (CPU)

## Data Flow

### Image Analysis Request

```
1. User captures photo → Mobile App
2. App uploads to → Backend API (/api/v1/analysis/upload)
3. Backend stores → Object Storage
4. Backend invokes → ML Service
5. ML Service:
   a. Loads image
   b. Runs Grounding DINO (text → boxes)
   c. Runs SAM (boxes → masks)
   d. Calculates metrics
6. Backend saves → Database
7. Backend returns → Analysis Response
8. App displays → Results Screen
```

### Authentication Flow (Future)

```
1. User registers → POST /api/v1/users/register
2. Backend hashes password → Save to DB
3. User logs in → POST /api/v1/users/login
4. Backend validates → Returns JWT token
5. App stores token → AsyncStorage
6. Subsequent requests → Include token in header
7. Backend validates token → Allow access
```

## Deployment Architecture

### Development
```
localhost:8000  → Backend (uvicorn)
localhost:19006 → Mobile (Expo)
localhost:5432  → PostgreSQL
```

### Production (Future)
```
AWS/Azure/GCP:
  - EKS/AKS/GKE → Kubernetes cluster
    - Deployment: backend-api (3 replicas)
    - Deployment: ml-inference (2 replicas with GPU)
    - Service: LoadBalancer
  - RDS/CloudSQL → Managed PostgreSQL
  - S3/Blob Storage → Object storage
  - CloudFront/CDN → Static assets

Mobile:
  - iOS App Store
  - Google Play Store
```

## Performance Considerations

### Bottlenecks
1. **ML Inference** (slowest): 0.8-5s depending on hardware
2. **Image Upload**: 0.5-2s depending on network
3. **Database Queries**: <100ms (optimized)

### Optimizations
- **Model caching**: Load models once at startup
- **Async processing**: Use FastAPI background tasks
- **Image compression**: Resize before upload
- **GPU acceleration**: Use CUDA when available
- **CDN**: Serve images via CDN
- **Batch processing**: Allow multiple images at once

## Security

### Current
- CORS configuration
- Input validation (file types, sizes)
- SQL injection prevention (SQLAlchemy ORM)

### Future (TODO)
- JWT authentication
- Rate limiting
- API key management
- Image content validation
- Encryption at rest
- HTTPS only
- Input sanitization
- Role-based access control (RBAC)

## Monitoring & Logging

### Logs
- Application logs → `logs/app.log`
- Request/response logs → Uvicorn
- Error tracking → Sentry (future)

### Metrics (Future)
- Prometheus metrics
- Grafana dashboards
- Key metrics:
  - Request latency (p50, p95, p99)
  - ML inference time
  - Success/failure rates
  - Active users
  - Storage usage

## Scalability

### Horizontal Scaling
- **Backend**: Stateless, can add replicas
- **ML Service**: Separate deployment, GPU-enabled nodes
- **Database**: Connection pooling, read replicas

### Vertical Scaling
- GPU nodes for ML inference
- Larger database instances
- Increased storage capacity

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Backend Framework | FastAPI | Fast, async, auto-docs, type hints |
| Mobile Framework | React Native | Cross-platform, large ecosystem |
| State Management | Redux Toolkit | Predictable state, good dev tools |
| Database | PostgreSQL | Reliable, supports JSON, widely used |
| Storage | Supabase/S3 | Managed, scalable, cost-effective |
| ML Framework | PyTorch | Industry standard, model availability |
| Vision Models | SAM + DINO | State-of-art zero-shot capabilities |
| Containerization | Docker | Consistent environments, easy deploy |
| CI/CD | GitHub Actions | Integrated, free for public repos |

## Future Enhancements

1. **Real-time processing**: WebSocket for live analysis
2. **Offline mode**: Mobile app works without internet
3. **Batch processing**: Analyze multiple images at once
4. **Model fine-tuning**: Custom models per crop type
5. **Analytics dashboard**: Trends over time
6. **Integration APIs**: Connect with farm management systems
7. **Multi-language support**: i18n
8. **Mobile notifications**: Alert on analysis completion
