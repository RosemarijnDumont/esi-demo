
import axios from 'axios';
import NetInfo from '@react-native-community/netinfo';
import AsyncStorage from '@react-native-async-storage/async-storage';

const BACKEND_URL = 'http://localhost:3000/api'; // Replace with your actual backend URL
const PENDING_SYNC_KEY = '@pending_sync_data';

/**
 * Persists data locally if offline, or sends to backend if online.
 * Implements retry logic and eventual consistency.
 * @param {object} data - The data payload to send.
 * @param {string} dataType - The type of data (e.g., 'entry', 'userProfile').
 * @returns {Promise<object>} - A promise that resolves with the sync status.
 */
export async function submitDataForSync(data, dataType) {
  const state = await NetInfo.fetch();

  if (state.isConnected) {
    try {
      const response = await axios.post(`${BACKEND_URL}/mobile/sync`, { data, dataType });
      console.log('Data successfully sent to backend:', response.data);
      // Upon successful acknowledgment from backend, consider confirming with backend
      // via a separate call if 'pending' status needs to be proactively cleared.
      return { status: 'synced', response: response.data };
    } catch (error) {
      console.error('Error sending data to backend, queuing for retry:', error.message);
      await savePendingDataLocally({ data, dataType, attempt: 1 });
      return { status: 'queued_for_retry', error: error.message };
    }
  } else {
    console.warn('Offline: Saving data locally for later synchronization.');
    await savePendingDataLocally({ data, dataType, attempt: 1 });
    return { status: 'saved_locally_offline' };
  }
}

/**
 * Saves data to local storage for synchronization when online.
 * Increments attempt count for retry logic.
 * @param {object} item - The data item to save, including data, dataType, and current attempt.
 */
async function savePendingDataLocally(item) {
  try {
    const pendingData = await AsyncStorage.getItem(PENDING_SYNC_KEY);
    let dataToSync = pendingData ? JSON.parse(pendingData) : [];

    // Check if an item with the same unique identifier (e.g., data.id) already exists
    // and update it, preventing duplicates, or add new item.
    const existingIndex = dataToSync.findIndex(d => d.data.id === item.data.id);
    if (existingIndex > -1) {
      dataToSync[existingIndex] = { ...item, attempt: (dataToSync[existingIndex].attempt || 0) + 1 };
      console.log(`Updated pending data item ${item.data.id}, attempt: ${dataToSync[existingIndex].attempt}`);
    } else {
      dataToSync.push(item);
      console.log(`Added new pending data item ${item.data.id}.`);
    }

    await AsyncStorage.setItem(PENDING_SYNC_KEY, JSON.stringify(dataToSync));
  } catch (error) {
    console.error('Error saving pending data locally:', error);
  }
}

/**
 * Periodically checks for network connectivity and attempts to sync locally stored data.
 * This function should be called when the app starts or when network status changes.
 */
export async function processPendingData() {
  const state = await NetInfo.fetch();

  if (state.isConnected) {
    try {
      const pendingData = await AsyncStorage.getItem(PENDING_SYNC_KEY);
      if (pendingData) {
        let dataToSync = JSON.parse(pendingData);
        if (dataToSync.length === 0) {
          console.log('No pending data to synchronize.');
          return { status: 'no_pending_data' };
        }

        console.log(`Attempting to synchronize ${dataToSync.length} pending items.`);
        const successfulSyncs = [];
        const failedSyncs = [];

        for (const item of dataToSync) {
          try {
            // Avoid infinite retries; limit attempts.
            if (item.attempt && item.attempt > 5) { // Example: Max 5 attempts
              console.warn(`Max retries reached for item ${item.data.id}. Moving to failed queue or manual review.`);
              failedSyncs.push({ ...item, reason: 'Max retries reached' });
              continue;
            }

            const response = await axios.post(`${BACKEND_URL}/mobile/sync`, { data: item.data, dataType: item.dataType });
            console.log(`Successfully synced pending item ${item.data.id}:`, response.data);
            successfulSyncs.push(item);
            // Optionally, call acknowledgeDataSync if needed after server confirms processing:
            // await axios.post(`${BACKEND_URL}/mobile/acknowledge-sync`, { entryId: item.data.id, mobileDeviceId: '...' });
          } catch (error) {
            console.error(`Failed to sync pending item ${item.data.id}:`, error.message);
            // Increment attempt and re-save for future retry
            await savePendingDataLocally({ ...item, attempt: (item.attempt || 0) + 1 });
            failedSyncs.push({ ...item, reason: error.message });
          }
        }

        // Remove successfully synced items from local storage
        const remainingData = dataToSync.filter(item => !successfulSyncs.includes(item));
        await AsyncStorage.setItem(PENDING_SYNC_KEY, JSON.stringify(remainingData));

        console.log(`Synchronization complete. Successful: ${successfulSyncs.length}, Failed: ${failedSyncs.length}`);
        return { status: 'processed', successful: successfulSyncs.length, failed: failedSyncs.length };
      }
    } catch (error) {
      console.error('Error processing pending data:', error);
      return { status: 'error', error: error.message };
    }
  }
  return { status: 'offline', message: 'Not connected to internet.' };
}

// --- Mobile App Notification Handling (Conceptual) ---
// This would typically involve a push notification service (e.g., Firebase Cloud Messaging)
// and an in-app listener.

/**
 * Registers the device for push notifications.
 * This function is conceptual and depends on the specific push notification service.
 */
export async function registerForPushNotifications() {
  // Example: using Firebase Messaging
  // const token = await firebase.messaging().getToken();
  // console.log('FCM Token:', token);
  // Send this token to your backend to associate with a user.
  // await axios.post(`${BACKEND_URL}/register-device-token`, { userId: '...', token });
  console.log('Device registered for push notifications (conceptual).');
}

/**
 * Handles incoming push notifications.
 * This function is conceptual and depends on the specific push notification service and app state.
 * @param {object} notification - The notification payload.
 */
export function handlePushNotification(notification) {
  console.log('Received push notification:', notification);
  // Display alert, update UI, navigate to a screen, etc.
  // Example: Alert.alert(notification.title, notification.body);
}

// Add a listener for network state changes to trigger processPendingData
NetInfo.addEventListener(state => {
  if (state.isConnected) {
    console.log('Network reconnected, attempting to process pending data...');
    processPendingData();
  }
});
