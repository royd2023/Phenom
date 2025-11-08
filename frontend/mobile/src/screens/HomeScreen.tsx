import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Text, Card } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';
import CardActions from 'react-native-paper/lib/typescript/components/Card/CardActions';

type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

const HomeScreen = ({ navigation }: Props) => {
  return (
    <View style={styles.container}>
      <Text variant="headlineLarge" style={styles.title}>Welcome to U-CHS</Text>
      <Text variant="bodyMedium" style={styles.subtitle}>Universal Crop Health Scanner</Text>

      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleMedium">Ready to scan your crops?</Text>
          <Text variant="bodySmall">Use your phone's camera to get instant AI-powered analysis.</Text>
        </Card.Content>
        <Card.Actions>
          <Button mode="contained" onPress={() => navigation.navigate('Camera')}>
            Start New Scan
          </Button>
        </Card.Actions>
      </Card>

      <Button onPress={() => navigation.navigate('History')}>View Scan History</Button>
      <Button onPress={() => navigation.navigate('Settings')}>Go to Settings</Button>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 16, gap: 16},
  title: { fontWeight: 'bold' },
  subtitle: { marginBottom: 20 },
  card: { flex: 1, width: '100%', alignItems: 'center', justifyContent: 'center' },
});

export default HomeScreen;