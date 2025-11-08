import React from 'react';
import { FlatList, StyleSheet } from 'react-native';
import { List, Text } from 'react-native-paper';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';

// import { useGetHistoryQuery } from '../services/api';

type Props = NativeStackScreenProps<RootStackParamList, 'History'>;

const HistoryScreen = ({ navigation }: Props) => {
  // const { data: history, error, isLoading } = useGetHistoryQuery();

  // Mock data
  const history = [
    { id: '1', cropType: 'Lettuce', date: '2025-11-01', severity: 'Low' },
    { id: '2', cropType: 'Tomato', date: '2025-11-02', severity: 'Medium' },
    { id: '3', cropType: 'Basil', date: '2025-11-03', severity: 'None' },
  ];

  return (
    <FlatList
      data={history}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <List.Item
          title={`${item.cropType} Scan`}
          description={`Severity: ${item.severity} - ${item.date}`}
          left={props => <List.Icon {...props} icon="leaf" />}
          onPress={() => navigation.navigate('Result', { analysisId: item.id })}
        />
      )}
    />
  );
};

export default HistoryScreen;