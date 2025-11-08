import React from 'react';
import { View, StyleSheet, ActivityIndicator } from 'react-native';
import { Text, Card, Title, Paragraph } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';
// import { useGetResultByIdQuery } from '../services/api';

type Props = NativeStackScreenProps<RootStackParamList, 'Result'>;

const ResultScreen = ({ route }: Props) => {
  const { analysisId } = route.params;
  // const { data, error, isLoading } = useGetResultByIdQuery(analysisId);

  // Mock data until API is connected
  const isLoading = false;
  const error = null;
  const data = {
    stressDetected: 'Yes',
    severity: 'Medium',
    areaPercentage: '15%',
    recommendation: 'Check nutrient levels for nitrogen deficiency.'
  };

  if (isLoading) return <ActivityIndicator animating={true} size="large" style={styles.centered} />;
  if (error) return <Text>Error loading results.</Text>;

  return (
    <View style={styles.container}>
      <Title>Analysis for ID: {analysisId}</Title>
      <Card>
        <Card.Cover source={{ uri: `https://picsum.photos/seed/${analysisId}/700` }} />
        <Card.Content style={styles.content}>
          <Paragraph>Stress Detected: {data?.stressDetected}</Paragraph>
          <Paragraph>Severity: {data?.severity}</Paragraph>
          <Paragraph>Affected Area: {data?.areaPercentage}</Paragraph>
          <Title>Recommendation</Title>
          <Paragraph>{data?.recommendation}</Paragraph>
        </Card.Content>
      </Card>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  content: { paddingTop: 16, gap: 8 },
});

export default ResultScreen;