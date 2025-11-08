import React, { useEffect } from 'react';
import { View, StyleSheet, ScrollView, Image } from 'react-native';
import { Card, Title, Paragraph, Button, Chip, ActivityIndicator, Text } from 'react-native-paper';
import { useRoute, useNavigation, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useGetTestResultQuery } from '../services/api';

type ResultScreenRouteProp = RouteProp<RootStackParamList, 'Result'>;
type ResultScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Result'>;

interface Parameter {
  name: string;
  value: string;
  unit: string;
  status: 'normal' | 'abnormal' | 'warning';
  referenceRange: string;
}

export default function ResultScreen() {
  const route = useRoute<ResultScreenRouteProp>();
  const navigation = useNavigation<ResultScreenNavigationProp>();
  const { testId, imageUri } = route.params;

  const { data: result, isLoading, error } = useGetTestResultQuery(testId, {
    pollingInterval: 3000, // Poll every 3 seconds while processing
    skipPollingIfUnfocused: true,
  });

  useEffect(() => {
    if (result?.status === 'completed') {
      // Stop polling once completed
    }
  }, [result?.status]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal':
        return '#4CAF50';
      case 'abnormal':
        return '#F44336';
      case 'warning':
        return '#FF9800';
      default:
        return '#757575';
    }
  };

  const handleDone = () => {
    navigation.navigate('MainTabs');
  };

  if (isLoading || !result) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" />
        <Text style={styles.loadingText}>Analyzing crop health...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Failed to load results</Text>
        <Button mode="contained" onPress={handleDone}>
          Back to Home
        </Button>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.imageCard}>
          <Card.Content>
            <Image
              source={{ uri: imageUri }}
              style={styles.image}
              resizeMode="contain"
            />
          </Card.Content>
        </Card>

        <Card style={styles.summaryCard}>
          <Card.Content>
            <Title>Overall Status</Title>
            <Chip
              style={[
                styles.statusChip,
                { backgroundColor: getStatusColor(result.overallStatus) }
              ]}
              textStyle={styles.statusChipText}
            >
              {result.overallStatus.toUpperCase()}
            </Chip>
            <Paragraph style={styles.timestamp}>
              Test Date: {new Date(result.timestamp).toLocaleString()}
            </Paragraph>
          </Card.Content>
        </Card>

        <Card style={styles.resultsCard}>
          <Card.Content>
            <Title>Test Parameters</Title>
            {result.parameters.map((param: Parameter, index: number) => (
              <View key={index} style={styles.parameterRow}>
                <View style={styles.parameterHeader}>
                  <Text style={styles.parameterName}>{param.name}</Text>
                  <Chip
                    compact
                    style={[
                      styles.parameterStatus,
                      { backgroundColor: getStatusColor(param.status) }
                    ]}
                    textStyle={styles.parameterStatusText}
                  >
                    {param.status}
                  </Chip>
                </View>
                <Text style={styles.parameterValue}>
                  {param.value} {param.unit}
                </Text>
                <Text style={styles.referenceRange}>
                  Reference: {param.referenceRange}
                </Text>
              </View>
            ))}
          </Card.Content>
        </Card>

        {result.notes && (
          <Card style={styles.notesCard}>
            <Card.Content>
              <Title>Clinical Notes</Title>
              <Paragraph>{result.notes}</Paragraph>
            </Card.Content>
          </Card>
        )}

        <Card style={styles.disclaimerCard}>
          <Card.Content>
            <Title style={styles.disclaimerTitle}>Disclaimer</Title>
            <Paragraph>
              These results are for screening purposes only. Please consult with a
              agronomists or crop specialists.
            </Paragraph>
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={handleDone}
          style={styles.doneButton}
          contentStyle={styles.doneButtonContent}
        >
          Done
        </Button>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  errorText: {
    fontSize: 16,
    color: '#F44336',
    marginBottom: 16,
  },
  imageCard: {
    marginBottom: 16,
    elevation: 4,
  },
  image: {
    width: '100%',
    height: 200,
  },
  summaryCard: {
    marginBottom: 16,
    elevation: 4,
  },
  statusChip: {
    alignSelf: 'flex-start',
    marginTop: 8,
    marginBottom: 8,
  },
  statusChipText: {
    color: 'white',
    fontWeight: 'bold',
  },
  timestamp: {
    fontSize: 12,
    color: '#666',
  },
  resultsCard: {
    marginBottom: 16,
    elevation: 4,
  },
  parameterRow: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  parameterHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  parameterName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  parameterStatus: {
    height: 24,
  },
  parameterStatusText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  parameterValue: {
    fontSize: 18,
    color: '#6200EE',
    marginBottom: 2,
  },
  referenceRange: {
    fontSize: 12,
    color: '#666',
  },
  notesCard: {
    marginBottom: 16,
    elevation: 4,
    backgroundColor: '#E3F2FD',
  },
  disclaimerCard: {
    marginBottom: 16,
    backgroundColor: '#FFF3E0',
  },
  disclaimerTitle: {
    fontSize: 16,
    color: '#E65100',
  },
  doneButton: {
    marginBottom: 20,
    borderRadius: 8,
  },
  doneButtonContent: {
    paddingVertical: 8,
  },
});
