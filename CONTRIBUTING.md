# Contributing to U-CHS

Thank you for your interest in contributing to the Universal Crop Health Scanner project!

## Getting Started

1. Read [docs/setup.md](docs/setup.md) for development environment setup
2. Read [docs/architecture.md](docs/architecture.md) to understand the system
3. Check [docs/roadmap.md](docs/roadmap.md) for current priorities

## Development Workflow

### 1. Branching Strategy

We use Git Flow:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features (branch from `develop`)
- `bugfix/*` - Bug fixes (branch from `develop`)
- `hotfix/*` - Urgent production fixes (branch from `main`)

### 2. Making Changes

```bash
# Create a feature branch
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Commit with meaningful messages
git add .
git commit -m "Add feature: description of what you did"

# Push your branch
git push origin feature/your-feature-name
```

### 3. Commit Message Guidelines

Follow conventional commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build process or tooling changes

**Examples:**
```
feat(backend): add zero-shot segmentation endpoint
fix(mobile): resolve camera permission issue on Android
docs(api): update API endpoint documentation
test(ml-service): add unit tests for preprocessing
```

### 4. Pull Request Process

1. **Before submitting:**
   - Run tests: `pytest` (backend) or `npm test` (frontend)
   - Run linters: `black`, `flake8`, `mypy` (backend) or `npm run lint` (frontend)
   - Update documentation if needed
   - Add tests for new features

2. **Create PR:**
   - Use a clear, descriptive title
   - Fill out the PR template
   - Link related issues
   - Request review from team members

3. **PR Template:**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] All tests passing

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings generated
   ```

4. **Review process:**
   - At least 1 approval required
   - All CI checks must pass
   - Resolve all conversations
   - Squash merge into `develop`

## Code Style Guidelines

### Python (Backend)

```python
# Use Black formatter (line length 100)
black app/ --line-length 100

# Follow PEP 8
# Use type hints
def analyze_image(image_data: bytes, prompt: str) -> List[SegmentationResult]:
    """Docstrings for all functions"""
    pass

# Imports order: stdlib, third-party, local
import os
from typing import List

import numpy as np
from fastapi import APIRouter

from app.models.schemas import SegmentationResult
```

### TypeScript (Frontend)

```typescript
// Use 2 spaces for indentation
// Use semicolons
// Prefer const over let

// Interfaces for props
interface HomeScreenProps {
  navigation: NavigationProp;
}

// Arrow functions for components
export const HomeScreen = ({ navigation }: HomeScreenProps) => {
  // ...
};

// Descriptive variable names
const isLoading = false;
const analysisResults = [];
```

## Testing Guidelines

### Backend Tests

```python
# tests/unit/test_ml_service.py
import pytest
from app.services.ml_service import MLService

def test_preprocess_image():
    """Test image preprocessing"""
    service = MLService()
    # ... test code

@pytest.mark.asyncio
async def test_analyze_image():
    """Test image analysis"""
    # ... async test code
```

Run tests:
```bash
cd backend
pytest tests/ -v
pytest tests/unit/test_ml_service.py::test_preprocess_image -v
```

### Frontend Tests

```typescript
// src/components/__tests__/HomeScreen.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { HomeScreen } from '../HomeScreen';

describe('HomeScreen', () => {
  it('renders scan button', () => {
    const { getByText } = render(<HomeScreen />);
    expect(getByText('Scan Crop')).toBeTruthy();
  });
});
```

Run tests:
```bash
cd frontend/mobile
npm test
npm test -- HomeScreen.test.tsx
```

## Documentation

- Update README.md for major features
- Add inline comments for complex logic
- Update API documentation in docstrings
- Update architecture.md for structural changes

## Performance Considerations

- **Backend**: Profile slow endpoints, optimize database queries
- **Frontend**: Avoid unnecessary re-renders, use React.memo
- **ML**: Monitor inference time, consider model optimization

## Common Tasks

### Adding a New API Endpoint

1. Define schema in `backend/app/models/schemas.py`
2. Create route in `backend/app/api/your_router.py`
3. Implement service logic in `backend/app/services/`
4. Add tests in `backend/tests/`
5. Update API client in `frontend/mobile/src/services/api.ts`

### Adding a New Screen

1. Create component in `frontend/mobile/src/screens/`
2. Add route to `frontend/mobile/src/navigation/AppNavigator.tsx`
3. Add to type definitions
4. Create tests in `src/screens/__tests__/`

### Adding a New ML Feature

1. Implement in `backend/app/services/ml_service.py`
2. Add configuration to `backend/app/core/config.py`
3. Add tests with mock data
4. Document in `docs/architecture.md`

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an issue with reproduction steps
- **Features**: Propose in GitHub Discussions first
- **Security**: Email [security@uchs.com] (do not open public issue)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Help others learn and grow

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project website (future)

Thank you for contributing! 🌱
