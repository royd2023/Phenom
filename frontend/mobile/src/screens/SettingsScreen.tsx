import React from 'react';
import { View, StyleSheet } from 'react-native';
import { List, Switch, Text } from 'react-native-paper';

const SettingsScreen = () => {
  const [isNotificationsOn, setIsNotificationsOn] = React.useState(false);
  const onToggleSwitch = () => setIsNotificationsOn(!isNotificationsOn);

  return (
    <View style={styles.container}>
      <List.Section>
        <List.Subheader>Preferences</List.Subheader>
        <List.Item
          title="Enable Notifications"
          right={() => <Switch value={isNotificationsOn} onValueChange={onToggleSwitch} />}
        />
        <List.Item title="Export Scan Data" left={() => <List.Icon icon="export" />} onPress={() => console.log('Exporting data...')} />
        <List.Item title="Clear Cache" left={() => <List.Icon icon="delete" />} onPress={() => console.log('Clearing cache...')} />
      </List.Section>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
});

export default SettingsScreen;