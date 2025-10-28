
import * as LocalDataService from './localDataService';
import * as RemoteDataService from './remoteDataService';
import { diff, applyChanges } from 'deep-diff';

const SYNC_INTERVAL = 30 * 1000; // 30 seconds

export const initializeSync = () => {
  setInterval(performSync, SYNC_INTERVAL);
  console.log('Sync service initialized.');
};

export const performSync = async () => {
  console.log('Performing data synchronization...');
  try {
    const localChanges = await LocalDataService.getPendingChanges();
    if (localChanges.length > 0) {
      console.log('Uploading local changes:', localChanges);
      await RemoteDataService.uploadChanges(localChanges);
      await LocalDataService.clearPendingChanges();
    }

    const remoteData = await RemoteDataService.fetchLatestData();
    const localData = await LocalDataService.getAllData();

    const changes = diff(localData, remoteData);

    if (changes && changes.length > 0) {
      console.log('Applying remote changes:', changes);
      const updatedLocalData = applyChanges(localData, changes);
      await LocalDataService.saveAllData(updatedLocalData);
    }
    console.log('Synchronization complete.');
  } catch (error) {
    console.error('Synchronization failed:', error);
    // Implement robust retry logic and error reporting here
  }
};

export const saveData = async (dataType, data) => {
  await LocalDataService.saveData(dataType, data);
  await LocalDataService.addPendingChange({ type: 'create', dataType, data });
  performSync(); // Trigger immediate sync after data modification
};

export const updateData = async (dataType, id, changes) => {
  await LocalDataService.updateData(dataType, id, changes);
  await LocalDataService.addPendingChange({ type: 'update', dataType, id, changes });
  performSync();
};

export const deleteData = async (dataType, id) => {
  await LocalDataService.deleteData(dataType, id);
  await LocalDataService.addPendingChange({ type: 'delete', dataType, id });
  performSync();
};
