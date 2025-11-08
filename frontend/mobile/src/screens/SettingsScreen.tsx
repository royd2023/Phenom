import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { List, Switch, Button, Text, Divider, Card, Title } from 'react-native-paper';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SettingsScreen() {
  const [notifications, setNotifications] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [highQuality, setHighQuality] = useState(true);

  const handleNotificationsToggle = async () => {
    const newValue = !notifications;
    setNotifications(newValue);
    await AsyncStorage.setItem('notifications', JSON.stringify(newValue));
  };

  const handleAutoSaveToggle = async () => {
    const newValue = !autoSave;
    setAutoSave(newValue);
    await AsyncStorage.setItem('autoSave', JSON.stringify(newValue));
  };

  const handleHighQualityToggle = async () => {
    const newValue = !highQuality;
    setHighQuality(newValue);
    await AsyncStorage.setItem('highQuality', JSON.stringify(newValue));
  };

  const handleClearCache = () => {
    Alert.alert(
      'Clear Cache',
      'Are you sure you want to clear all cached data?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            try {
              await AsyncStorage.clear();
              Alert.alert('Success', 'Cache cleared successfully');
            } catch (error) {
              Alert.alert('Error', 'Failed to clear cache');
            }
          },
        },
      ]
    );
  };

  const handleExportData = () => {
    Alert.alert(
      'Export Data',
      'Export scan history as CSV file',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Export',
          onPress: () => {
            Alert.alert('Coming Soon', 'Export feature will be available soon');
          },
        },
      ]
    );
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Card style={styles.section}>
          <Card.Content>
            <Title>General Settings</Title>
            <List.Item
              title="Enable Notifications"
              description="Receive alerts for crop scan results"
              right={() => (
                <Switch
                  value={notifications}
                  onValueChange={handleNotificationsToggle}
                />
              )}
            />
            <Divider />
            <List.Item
              title="Auto-save Results"
              description="Automatically save crop scan results to history"
              right={() => (
                <Switch
                  value={autoSave}
                  onValueChange={handleAutoSaveToggle}
                />
              )}
            />
          </Card.Content>
        </Card>

        <Card style={styles.section}>
          <Card.Content>
            <Title>Camera Settings</Title>
            <List.Item
              title="High Quality Images"
              description="Use higher resolution for better crop analysis"
              right={() => (
                <Switch
                  value={highQuality}
                  onValueChange={handleHighQualityToggle}
                />
              )}
            />
          </Card.Content>
        </Card>

        <Card style={styles.section}>
          <Card.Content>
            <Title>Data Management</Title>
            <List.Item
              title="Export Scan History"
              description="Download all crop scan results as CSV"
              left={(props) => <List.Icon {...props} icon="download" />}
              onPress={handleExportData}
            />
            <Divider />
            <List.Item
              title="Clear Cache"
              description="Remove cached crop images and data"
              left={(props) => <List.Icon {...props} icon="delete" />}
              onPress={handleClearCache}
            />
          </Card.Content>
        </Card>

        <Card style={styles.section}>
          <Card.Content>
            <Title>About</Title>
            <List.Item
              title="Version"
              description="1.0.0"
              left={(props) => <List.Icon {...props} icon="information" />}
            />
            <Divider />
            <List.Item
              title="Privacy Policy"
              left={(props) => <List.Icon {...props} icon="shield-check" />}
              onPress={() => Alert.alert('Privacy Policy', 'Privacy policy content here')}
            />
            <Divider />
            <List.Item
              title="Terms of Service"
              left={(props) => <List.Icon {...props} icon="file-document" />}
              onPress={() => Alert.alert('Terms of Service', 'Terms of service content here')}
            />
          </Card.Content>
        </Card>

        <Card style={styles.disclaimerCard}>
          <Card.Content>
            <Title style={styles.disclaimerTitle}>Agricultural Disclaimer</Title>
            <Text style={styles.disclaimerText}>
              U-CHS (Universal Crop Health Scanner) is intended for crop stress screening
              purposes only and should not replace professional agricultural advice. For
              critical farming decisions, always consult with agronomists, crop
              specialists, or agricultural extension services.
            </Text>
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
  section: {
    marginBottom: 16,
    elevation: 2,
  },
  disclaimerCard: {
    backgroundColor: '#FFF3E0',
    marginBottom: 20,
  },
  disclaimerTitle: {
    fontSize: 16,
    color: '#E65100',
    marginBottom: 8,
  },
  disclaimerText: {
    fontSize: 12,
    color: '#333',
    lineHeight: 18,
  },
});
