
const kue = require('kue');
const redis = require('redis');
const db = require('../config/database'); // Assuming a database connection
const { sendNotification } = require('./notificationService');

const queue = kue.createQueue();
const redisClient = redis.createClient();

// --- Data Synchronization --- //

/**
 * Persists data from mobile app to the database and dispatches for web app synchronization.
 * Implements retry mechanisms for robust data handling.
 * @param {object} data - The data payload from the mobile application.
 * @param {string} dataType - The type of data being synced (e.g., 'entry', 'userProfile').
 */
async function syncMobileData(data, dataType) {
  return new Promise((resolve, reject) => {
    const job = queue.create('processDataSync', { data, dataType })
      .attempts(5) // Retry up to 5 times
      .backoff({ delay: 5000, type: 'fixed' }) // 5-second fixed delay between retries
      .save(err => {
        if (err) {
          console.error(`Failed to create data sync job: ${err}`);
          return reject(new Error('Failed to queue data for synchronization.'));
        }
        console.log(`Data sync job created: ${job.id} for type: ${dataType}`);
        resolve({ jobId: job.id, status: 'queued' });
      });
  });
}

// Process data synchronization jobs
// This worker will attempt to save data to the database and notify connected web clients.
queue.process('processDataSync', async (job, done) => {
  const { data, dataType } = job.data;
  console.log(`Processing data sync job ${job.id} for type: ${dataType}`);
  try {
    // Simulate database save operation
    await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate async DB operation
    // In a real application, you'd insert/update records in your database here.
    // Example: await db.query(`INSERT INTO ${dataType}s SET ?`, data);
    console.log(`Successfully synced data for job ${job.id}.`);

    // After successful database write, notify web clients (e.g., via WebSockets)
    sendNotification(`New ${dataType} available`, data, 'web_client_update');

    done();
  } catch (error) {
    console.error(`Error processing data sync job ${job.id}: ${error.message}`);
    // If it's a transient error, the job will be retried automatically by Kue.
    done(new Error(`Data sync failed: ${error.message}`));
  }
});

queue.on('job complete', function(id) {
  kue.Job.get(id, function(err, job) {
    if (err) return;
    job.remove(function(err) {
      if (err) throw err;
      console.log('Removed completed job %s', job.id);
    });
  });
});

queue.on('job failed', function(id, err) {
  console.error(`Job ${id} failed: ${err}`);
  // Here you could add alerts, log to a different system, or trigger manual review.
});

// --- Acknowledgement and Retry Mechanisms for Data Sync (Client-side conceptual) ---
// On the mobile app, when data is submitted:
// 1. Send data to the backend.
// 2. Expect an immediate acknowledgment (job ID, status: 'queued').
// 3. If acknowledgment is not received within a timeout, retry sending the data.
// 4. Implement a local persistent queue on the mobile app for offline submissions.
//    These submissions should be retried automatically when connectivity is restored.
// On the web app, when data is received via notification (e.g., WebSocket):
// 1. Display the new data.
// 2. Send an implicit or explicit acknowledgment back to the server if needed (e.g., if the server needs to know a specific client has updated).


/**
 * Acknowledges successful data synchronization for a given mobile entry.
 * This could be called by the mobile client upon receiving confirmation from the server
 * that its data was successfully processed and reflected on the web.
 * @param {string} entryId - The ID of the entry that was synced.
 * @param {string} mobileDeviceId - The ID of the mobile device that submitted the entry.
 */
async function acknowledgeDataSync(entryId, mobileDeviceId) {
  try {
    // Update a status in the database, e.g., mark the entry as 'synced' for the mobile device.
    // This helps in preventing duplicate syncs or knowing which entries are truly 'pending' from the mobile perspective.
    // Example: await db.query('UPDATE mobile_entries SET status = ? WHERE id = ? AND device_id = ?', ['synced', entryId, mobileDeviceId]);
    console.log(`Acknowledged data sync for entry ${entryId} from device ${mobileDeviceId}`);
    return { success: true, message: 'Data sync acknowledged.' };
  } catch (error) {
    console.error(`Error acknowledging data sync for entry ${entryId}: ${error.message}`);
    throw new Error('Failed to acknowledge data sync.');
  }
}

module.exports = { 
  syncMobileData, 
  acknowledgeDataSync, 
  queue, // Export queue for potential external management/monitoring
};
