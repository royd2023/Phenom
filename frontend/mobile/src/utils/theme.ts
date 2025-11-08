import {
  MD3LightTheme as DefaultTheme,
} from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#4CAF50', // Green for agriculture
    secondary: '#FFC107', // Amber for warnings
  },
};