# U-CHS 90-Day Development Roadmap

## Goal
Build and validate a prototype mobile/web app that uses foundation vision models (SAM, Grounding DINO) to perform zero-shot crop stress detection using smartphone or drone images.

## Week 0: Setup (Days 1-7)

### Team Organization
- [ ] Assign roles:
  - Person A: Front-end/mobile app (React Native/Flutter) + UI/UX
  - Person B: Back-end & inference pipeline (Python/FastAPI + ML models)
  - Person C: Data pipeline, prompt engineering, model evaluation + user interviews

### Infrastructure
- [ ] Set up GitHub repo with branching strategy
- [ ] Configure CI/CD pipeline (GitHub Actions)
- [ ] Set up development environments
- [ ] Choose compute infrastructure (Google Colab, Azure, or local GPU)

### Initial Data
- [ ] Collect 2-3 pilot image datasets (public/small greenhouse)
- [ ] Set up basic data storage structure

## Week 1-2: MVP Foundation (Days 8-21)

### Backend
- [ ] Integrate SAM + Grounding DINO pretrained models
- [ ] Run simple inference on sample images (controlled lighting)
- [ ] Test with lettuce/leafy greens initially

### Prompt Engineering
- [ ] Define 5-10 text prompts:
  - "nitrogen-stress leaves"
  - "early blight lesion"
  - "yellowing leaves"
  - etc.
- [ ] Test segmentation output qualitatively

### Frontend
- [ ] Build minimal UI to upload image
- [ ] Send image to backend
- [ ] Display segmentation mask + overlay

### Data
- [ ] Label pilot dataset (even if small) for baseline comparison

## Week 3-4: Core Features (Days 22-35)

### Backend
- [ ] Create metrics pipeline (IoU, detection accuracy, area %)
- [ ] Explore few-shot adaptation for agricultural domain
- [ ] Handle variable image sizes

### Frontend
- [ ] Add results page showing:
  - Stress detected: yes/no
  - Area percentage affected
  - Suggested actions
- [ ] Implement image history

### User Research
- [ ] Conduct 3-5 interviews with greenhouse/vertical farm operators
- [ ] Document painpoints and requirements
- [ ] Validate camera workflow and smartphone access

## Week 5-6: Robustness (Days 36-49)

### Backend Improvements
- [ ] Handle variable lighting/backgrounds
- [ ] Add preprocessing: white balance, color correction, cropping
- [ ] Optimize inference speed

### Prompt Library
- [ ] Build 10+ prompt templates
- [ ] Test across 2-3 crop types
- [ ] Document success rates per crop type

### Data Collection
- [ ] Collect ~50 additional images (different varieties & stress types)
- [ ] Leverage OSU network or partners

### Frontend
- [ ] Add manual annotation/correction feature
- [ ] Implement image comparison view

## Week 7-8: Validation (Days 50-63)

### Prototype Testing
- [ ] Select one crop type for mini-pilot (leafy greens)
- [ ] Run 20+ test cases
- [ ] Record performance metrics and failure modes

### UX Iteration
- [ ] Refine UI based on user feedback
- [ ] Add camera instructions and lighting guidelines
- [ ] Test mobile vs web usage patterns

### Actionable Results
- [ ] Implement recommendation engine
  - "Check nutrient levels"
  - "Inspect for fungus in highlighted region"
- [ ] Add severity scoring (low/medium/high)

### Demo Prep
- [ ] Create pitch deck for OSU accelerator
- [ ] Prepare internal demo

## Week 9-12: Scale & Polish (Days 64-90)

### Advanced Features
- [ ] Integrate drone/overhead image support (if feasible)
- [ ] Add batch processing capability
- [ ] Implement user accounts and history tracking

### Performance Optimization
- [ ] Optimize model inference time
- [ ] Consider lighter model variants (Lite-SAM)
- [ ] Target < 5 second processing time

### Pilot User Testing
- [ ] Run test with 1-2 real users/farms
- [ ] Collect real-world feedback
- [ ] Track usage metrics

### Metrics & Reporting
- [ ] Log all usage data
- [ ] Calculate:
  - Segmentation success rate
  - User satisfaction scores
  - Potential ROI (time saved, yield protected)

### Go/No-Go Decision
- [ ] Present working prototype
- [ ] Review user feedback
- [ ] Evaluate technical performance
- [ ] Decision: Continue to MVP launch or pivot?

## Success Metrics (90 Days)

- ✅ Prototype works with minimum 3 crop types (2-3 varieties each)
- ✅ Successful segmentation with IoU > 0.5 in pilot dataset
- ✅ At least 5 user interviews with actionable feedback
- ✅ Upload → segmentation latency < 5 seconds
- ✅ Clear value story: "X minutes saved / Y dollars saved"

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- PyTorch
- SAM (Segment Anything Model)
- Grounding DINO
- PostgreSQL + Supabase

### Frontend
- React Native (Mobile)
- React (Web)
- Redux Toolkit
- React Native Paper

### Infrastructure
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- AWS/Azure/GCP for hosting
- Supabase for database and storage

## Risk Mitigation

### Technical Risks
- **Model accuracy < 70%**: Pivot to few-shot learning or narrower crop focus
- **Inference too slow**: Use lighter models or cloud GPU
- **Poor real-world lighting**: Add preprocessing pipeline

### Business Risks
- **No user adoption**: Validate value prop early (Week 3-4)
- **Competition from big players**: Focus on speed-to-market and flexibility
- **Data scarcity**: Partner with extension services early

## Next Steps After 90 Days

If successful:
1. Launch beta to 10-20 users
2. Collect 1,000+ real-world images
3. Fine-tune models for top 5 crop types
4. Develop subscription model ($50-200/month)
5. Pursue funding (accelerators, grants, investors)

If pivoting:
1. Narrow to single crop type or use case
2. Partner with equipment provider for hardware integration
3. Explore B2B2C model through consultants/extension services
