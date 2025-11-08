import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Button, Card, Text, Title, Paragraph } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';

type HomeScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

export default function HomeScreen() {
  const navigation = useNavigation<HomeScreenNavigationProp>();

  const handleStartTest = () => {
    navigation.navigate('Camera');
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.title}>Welcome to U-CHS</Title>
            <Paragraph style={styles.subtitle}>
              Urine Culture Health Screening
            </Paragraph>
            <Paragraph style={styles.description}>
              Quick and accurate urinalysis using AI-powered image recognition
            </Paragraph>
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={handleStartTest}
          style={styles.startButton}
          contentStyle={styles.startButtonContent}
          icon="camera"
        >
          Start New Test
        </Button>

        <Card style={styles.infoCard}>
          <Card.Content>
            <Title style={styles.infoTitle}>How it works</Title>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>1</Text>
              <Text style={styles.stepText}>Collect urine sample using test strip</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>2</Text>
              <Text style={styles.stepText}>Wait for color changes (60 seconds)</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>3</Text>
              <Text style={styles.stepText}>Capture clear photo of the test strip</Text>
            </View>
            <View style={styles.stepContainer}>
              <Text style={styles.stepNumber}>4</Text>
              <Text style={styles.stepText}>Get instant AI-powered results</Text>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.warningCard}>
          <Card.Content>
            <Title style={styles.warningTitle}>Important</Title>
            <Paragraph>
              This app is for screening purposes only. Always consult with a healthcare
              professional for medical diagnosis and treatment decisions.
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
    color: '#6200EE',
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
    backgroundColor: '#6200EE',
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
