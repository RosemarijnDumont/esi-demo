// backend/queue/notificationQueue.js
const Queue = require('bull');
const config = require('../../config/config');
const logger = require('../utils/logger');

const notificationQueue = new Queue('notifications', config.redis.url);

notificationQueue.on('completed', (job) => {
    logger.info(`Job ${job.id} of type ${job.name} completed.`);
});

notificationQueue.on('failed', (job, err) => {
    logger.error(`Job ${job.id} of type ${job.name} failed: ${err.message}`);
});

notificationQueue.on('error', (err) => {
    logger.error('Notification queue error:', err);
});

module.exports = notificationQueue;
