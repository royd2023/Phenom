import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Button, Card, Text, Title, Paragraph } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';

type HomeScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

export default function HomeScreen() {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  const handleStartScan = () => {
    navigation.navigate('Camera');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.title}>Universal Crop Health Scanner</Title>
            <Paragraph style={styles.subtitle}>
              AI-Powered Plant Stress Detection
            </Paragraph>
            <Paragraph style={styles.description}>
              Zero-shot plant phenotyping using SAM + Grounding DINO
            </Paragraph>
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={handleStartScan}
          style={styles.startButton}
          contentStyle={styles.startButtonContent}
          icon="camera"
        >
          Scan Crop
        </Button>

        <Card style={styles.infoCard}>
          <Card.Content>
            <Title style={styles.infoTitle}>How it works</Title>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>1</Text>
              <Text style={styles.stepText}>Take a photo of your crop or plant leaves</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>2</Text>
              <Text style={styles.stepText}>Select your crop type (lettuce, basil, tomato, etc.)</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>3</Text>
              <Text style={styles.stepText}>Enter what to detect (e.g., "nitrogen stress", "disease")</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>4</Text>
              <Text style={styles.stepText}>Get instant AI-powered crop health analysis</Text>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.warningCard}>
          <Card.Content>
            <Title style={styles.warningTitle}>Important</Title>
            <Paragraph>
              This app provides crop stress screening and recommendations. For critical
              agricultural decisions, consult with agronomists or crop specialists.
            </Paragraph>
          </Card.Content>
        </Card>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    padding: 16,
  },
  card: {
    marginBottom: 20,
    elevation: 4,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#4CAF50',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    marginTop: 4,
  },
  description: {
    fontSize: 14,
    textAlign: 'center',
    color: '#888',
    marginTop: 8,
  },
  startButton: {
    marginBottom: 20,
    borderRadius: 8,
    backgroundColor: '#4CAF50',
  },
  startButtonContent: {
    paddingVertical: 8,
  },
  infoCard: {
    marginBottom: 20,
    elevation: 2,
  },
  infoTitle: {
    fontSize: 20,
    marginBottom: 16,
    color: '#333',
  },
  stepContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#4CAF50',
    color: 'white',
    textAlign: 'center',
    lineHeight: 32,
    marginRight: 12,
    fontWeight: 'bold',
  },
  stepText: {
    flex: 1,
    fontSize: 14,
    color: '#333',
  },
  warningCard: {
    backgroundColor: '#FFF3E0',
    marginBottom: 20,
  },
  warningTitle: {
    fontSize: 18,
    color: '#E65100',
    marginBottom: 8,
  },
});
