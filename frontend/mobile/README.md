# U-CHS Mobile App

A React Native mobile application for Urine Culture Health Screening using AI-powered image recognition.

## Features

- Camera integration for capturing test strip images
- AI-powered urinalysis results
- Test history tracking
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
    │   ├── ResultScreen.tsx         # Test results display
    │   ├── HistoryScreen.tsx        # Test history list
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
- Image analysis (`POST /api/analyze`)
- Retrieving test results (`GET /api/results/:id`)
- Test history (`GET /api/history`)
- Deleting results (`DELETE /api/results/:id`)

Update the `EXPO_PUBLIC_API_URL` environment variable to point to your backend server.

## Key Features by Screen

### HomeScreen
- Welcome message and app introduction
- "Start New Test" button
- How-to instructions
- Medical disclaimer

### CameraScreen
- Live camera preview
- Alignment guide overlay
- Image capture with processing
- Automatic navigation to results

### ResultScreen
- Test strip image display
- Overall status indicator
- Detailed parameter results
- Reference ranges
- Clinical notes
- Medical disclaimer

### HistoryScreen
- Chronological list of past tests
- Status indicators
- Pull-to-refresh
- Infinite scroll pagination
- Navigate to past results

### SettingsScreen
- Notification preferences
- Auto-save toggle
- Image quality settings
- Data export
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
