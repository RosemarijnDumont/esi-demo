
import React, { useEffect } from 'react';
import { SafeAreaView, StyleSheet, Text, View } from 'react-native';
import DataEntryForm from './src/components/DataEntryForm';
import { processPendingData, registerForPushNotifications, handlePushNotification } from './src/services/dataSyncClient';
import NetInfo from '@react-native-community/netinfo';

export default function App() {
  useEffect(() => {
    // Register for push notifications on app start
    registerForPushNotifications();

    // Process any pending data on app start, in case there was data saved offline
    processPendingData();

    // Set up a periodic check for pending data in case network status changes are missed
    const intervalId = setInterval(() => {
      console.log('Running periodic check for pending data...');
      processPendingData();
    }, 60 * 1000); // Check every 60 seconds

    // Listen for incoming push notifications (conceptual)
    // Example: firebase.messaging().onMessage(handlePushNotification);
    // Example: firebase.messaging().onNotificationOpenedApp(handlePushNotification);

    return () => {
      clearInterval(intervalId);
      // Cleanup any other listeners if necessary
    };
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.header}>Data Sync & Notifications Demo</Text>
      <DataEntryForm />
      {/* Further UI components for displaying synced data or notifications would go here */}
      <View style={{ flex: 1, justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 20 }}>
        <Text style={{ fontSize: 12, color: '#888' }}>Status: Connected to Backend & Syncing...</Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginVertical: 20,
    color: '#333',
  },
});
