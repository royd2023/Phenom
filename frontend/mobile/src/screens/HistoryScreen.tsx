import React, { useState } from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity } from 'react-native';
import { Card, Title, Paragraph, Chip, Text, ActivityIndicator, Button } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useGetTestHistoryQuery } from '../services/api';

type HistoryScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'MainTabs'>;

interface ScanHistoryItem {
  id: string;
  timestamp: string;
  cropType: string;
  severity: 'none' | 'low' | 'medium' | 'high';
  stressDetected: boolean;
  imageUri: string;
}

export default function HistoryScreen() {
  const navigation = useNavigation<HistoryScreenNavigationProp>();
  const [page, setPage] = useState(1);
  const { data, isLoading, error, refetch } = useGetTestHistoryQuery({
    page,
    limit: 20
  });

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'none':
        return '#4CAF50';
      case 'low':
        return '#8BC34A';
      case 'medium':
        return '#FF9800';
      case 'high':
        return '#F44336';
      default:
        return '#757575';
    }
  };

  const handleScanPress = (item: ScanHistoryItem) => {
    navigation.navigate('Result', {
      testId: item.id,
      imageUri: item.imageUri,
    });
  };

  const renderItem = ({ item }: { item: ScanHistoryItem }) => (
    <TouchableOpacity onPress={() => handleScanPress(item)}>
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <View style={styles.infoContainer}>
              <Text style={styles.cropType}>
                {item.cropType.charAt(0).toUpperCase() + item.cropType.slice(1)}
              </Text>
              <View style={styles.dateContainer}>
                <Text style={styles.date}>
                  {new Date(item.timestamp).toLocaleDateString()}
                </Text>
                <Text style={styles.time}>
                  {new Date(item.timestamp).toLocaleTimeString()}
                </Text>
              </View>
            </View>
            <Chip
              style={[
                styles.statusChip,
                { backgroundColor: getSeverityColor(item.severity) }
              ]}
              textStyle={styles.statusChipText}
            >
              {item.severity}
            </Chip>
          </View>
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );

  const renderEmpty = () => (
    <View style={styles.emptyContainer}>
      <Text style={styles.emptyText}>No scan history available</Text>
      <Paragraph style={styles.emptySubtext}>
        Scan your first crop to see results here
      </Paragraph>
    </View>
  );

  if (isLoading && page === 1) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Failed to load scan history</Text>
        <Button mode="contained" onPress={() => refetch()}>
          Retry
        </Button>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={data?.scans || []}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={renderEmpty}
        onRefresh={refetch}
        refreshing={isLoading}
        onEndReached={() => {
          if (data?.hasMore) {
            setPage(p => p + 1);
          }
        }}
        onEndReachedThreshold={0.5}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  listContent: {
    padding: 16,
  },
  card: {
    marginBottom: 12,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  infoContainer: {
    flex: 1,
  },
  cropType: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 4,
  },
  dateContainer: {
    marginTop: 2,
  },
  date: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  time: {
    fontSize: 12,
    color: '#666',
    marginTop: 2,
  },
  statusChip: {
    height: 28,
  },
  statusChipText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 12,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 100,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
  },
});
