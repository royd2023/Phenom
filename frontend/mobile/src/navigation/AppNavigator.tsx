import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeScreen';
import CameraScreen from '../screens/CameraScreen';
import ResultScreen from '../screens/ResultScreen';
import HistoryScreen from '../screens/HistoryScreen';
import SettingsScreen from '../screens/SettingsScreen';

export type RootStackParamList = {
  Home: undefined;
  Camera: undefined;
  Result: { analysisId: string };
  History: undefined;
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const AppNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Home">
      <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'U-CHS Home' }} />
      <Stack.Screen name="Camera" component={CameraScreen} options={{ title: 'Scan Crop' }} />
      <Stack.Screen name="Result" component={ResultScreen} options={{ title: 'Analysis Result' }} />
      <Stack.Screen name="History" component={HistoryScreen} options={{ title: 'Scan History' }} />
      <Stack.Screen name="Settings" component={SettingsScreen} options={{ title: 'Settings' }} />
    </Stack.Navigator>
  );
};

export default AppNavigator;