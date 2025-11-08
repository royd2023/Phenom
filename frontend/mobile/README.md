# U-CHS Mobile App

A React Native mobile application for Universal Crop Health Scanner using AI-powered zero-shot plant phenotyping.

## Features

- Camera integration for capturing crop and plant images
- AI-powered crop stress detection using SAM + Grounding DINO
- Crop type selection (lettuce, basil, tomato, pepper, microgreens)
- Custom detection prompts (nitrogen stress, disease, etc.)
- Scan history tracking
- Agronomic recommendations for farmers
- Settings and configuration
- Clean, Material Design UI

## Technology Stack

- **React Native** with Expo
- **TypeScript** for type safety
- **Redux Toolkit** with RTK Query for state management and API calls
- **React Navigation** for navigation
- **React Native Paper** for Material Design components
- **Expo Camera** for image capture

## Prerequisites

- Node.js 16+ and npm/yarn
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator

## Installation

1. Install dependencies:
```bash
cd /c/Users/rdinh/Documents/CODE/Phenom/frontend/mobile
npm install
```

2. Set up environment variables:
Create a `.env` file with:
```
EXPO_PUBLIC_API_URL=http://your-backend-url:8000/api
```

## Running the App

### Development Mode

```bash
# Start Expo development server
npm start

# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android

# Run on web
npm run web
```

### Production Build

```bash
# Build for iOS
expo build:ios

# Build for Android
expo build:android
```

## Project Structure

```
frontend/mobile/
├── App.tsx                          # Root component
├── app.json                         # Expo configuration
├── package.json                     # Dependencies
├── tsconfig.json                    # TypeScript config
└── src/
    ├── navigation/
    │   └── AppNavigator.tsx         # Navigation setup
    ├── screens/
    │   ├── HomeScreen.tsx           # Home/landing screen
    │   ├── CameraScreen.tsx         # Camera capture screen
    │   ├── ResultScreen.tsx         # Crop analysis results display
    │   ├── HistoryScreen.tsx        # Scan history list
    │   └── SettingsScreen.tsx       # App settings
    ├── services/
    │   └── api.ts                   # RTK Query API client
    ├── store/
    │   └── index.ts                 # Redux store configuration
    └── utils/
        └── theme.ts                 # App theme and styles
```

## API Integration

The app connects to the backend API for:
- Crop image analysis (`POST /api/analyze`)
- Retrieving crop scan results (`GET /api/results/:id`)
- Scan history (`GET /api/history`)
- Deleting results (`DELETE /api/results/:id`)

Update the `EXPO_PUBLIC_API_URL` environment variable to point to your backend server.

## Key Features by Screen

### HomeScreen
- Welcome message and app introduction
- "Scan Crop" button
- How-to instructions for farmers
- Agricultural disclaimer

### CameraScreen
- Live camera preview with crop alignment guide
- Crop type selector (lettuce, basil, tomato, pepper, microgreens)
- Detection prompt input (e.g., "nitrogen stress", "disease")
- Good lighting guidance
- Image capture with AI processing
- Automatic navigation to results

### ResultScreen
- Crop image display
- Stress detection status (Yes/No)
- Severity level (None/Low/Medium/High)
- Affected area percentage
- Detection confidence score
- Agronomic recommendations for farmers
- Agricultural disclaimer

### HistoryScreen
- Chronological list of past crop scans
- Crop type and severity indicators
- Pull-to-refresh
- Infinite scroll pagination
- Navigate to past scan results

### SettingsScreen
- Notification preferences
- Auto-save toggle
- Image quality settings for crop analysis
- Scan data export
- Cache management
- App information

## Testing

```bash
npm test
```

## Linting

```bash
npm run lint
```

## Notes

- Camera permissions are required for image capture
- The app includes proper error handling and loading states
- All screens follow Material Design guidelines
- TypeScript ensures type safety throughout the app
- Redux Toolkit Query handles API caching and state management

## License

Proprietary - All rights reserved
