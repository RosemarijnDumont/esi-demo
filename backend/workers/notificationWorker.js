// backend/workers/notificationWorker.js
const notificationQueue = require('../queue/notificationQueue');
const notificationService = require('../services/notificationService');
const logger = require('../utils/logger');

// Process jobs concurrently
notificationQueue.process(5, notificationService.processNotificationQueue);

logger.info('Notification worker started, processing jobs...');
