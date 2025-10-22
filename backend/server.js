
require('dotenv').config(); // Load environment variables
const express = require('express');
const http = require('http');
const kue = require('kue');
const { syncMobileData } = require('./src/services/dataSyncService');
const { sendNotification } = require('./src/services/notificationService');

const app = express();
const server = http.createServer(app); // Create HTTP server
// The Socket.IO instance is initialized in notificationService.js, requiring `server`
// This ensures Socket.IO uses the same HTTP server instance.

const PORT = process.env.PORT || 3000;

// Centralized Error Handling
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  // Implement graceful shutdown, error logging to external service
  process.exit(1); // Exit with a failure code
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Implement graceful shutdown, error logging
  process.exit(1); // Exit with a failure code
});

// Middleware
app.use(express.json()); // For parsing application/json

// --- Routes for Data Sync and Notifications ---

// Example Mobile App endpoint for data submission
app.post('/api/mobile/sync', async (req, res) => {
  const { data, dataType } = req.body;
  if (!data || !dataType) {
    return res.status(400).json({ message: 'Missing data or dataType.' });
  }
  try {
    const result = await syncMobileData(data, dataType);
    res.status(202).json({ message: 'Data queued for synchronization.', ...result });
  } catch (error) {
    console.error('Error in mobile data sync endpoint:', error);
    res.status(500).json({ message: 'Failed to queue data for synchronization.', error: error.message });
  }
});

// Example endpoint to trigger a notification (e.g., from an admin dashboard)
app.post('/api/notify', async (req, res) => {
  const { type, options } = req.body;
  if (!type || !options) {
    return res.status(400).json({ message: 'Missing notification type or options.' });
  }
  try {
    const result = await sendNotification(type, options);
    res.status(202).json({ message: 'Notification queued.', ...result });
  } catch (error) {
    console.error('Error in notification trigger endpoint:', error);
    res.status(500).json({ message: 'Failed to queue notification.', error: error.message });
  }
});

// Kue UI (optional, for monitoring the job queue)
app.use('/kue-ui', kue.app);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK', message: 'Service is healthy' });
});

// Generic 404 handler
app.use((req, res, next) => {
  res.status(404).json({ message: 'Not Found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({ message: err.message || 'Something broke!', error: process.env.NODE_ENV === 'production' ? {} : err });
});

// Start the server
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Kue UI available at http://localhost:${PORT}/kue-ui`);
});

// Export the server for use in other modules (e.g., Socket.IO initialization)
module.exports = { app, server };
