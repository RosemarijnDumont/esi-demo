// backend/services/notificationService.js
const notificationQueue = require('../queue/notificationQueue');
const emailService = require('./emailService');
const inAppNotificationService = require('./inAppNotificationService');
const logger = require('../utils/logger');

exports.sendNotification = async (type, userId, data) => {
    try {
        await notificationQueue.add(type, { userId, data });
        logger.info(`Notification of type ${type} added to queue for user ${userId}`);
    } catch (error) {
        logger.error(`Error adding notification to queue for user ${userId}:`, error);
        throw new Error('Failed to add notification to queue.');
    }
};

exports.processNotificationQueue = async (job) => {
    const { type, userId, data } = job.data;
    logger.info(`Processing ${type} notification for user ${userId}...`);

    try {
        switch (type) {
            case 'email':
                await emailService.sendEmail(userId, data.subject, data.body);
                break;
            case 'inApp':
                await inAppNotificationService.sendInAppNotification(userId, data.message);
                break;
            case 'passwordReset':
                // Example: Assume data contains `resetToken` and `ttl`
                await emailService.sendPasswordResetEmail(userId, data.resetToken);
                break;
            default:
                logger.warn(`Unknown notification type: ${type}`);
        }
        logger.info(`${type} notification successfully processed for user ${userId}.`);
    } catch (error) {
        logger.error(`Error processing ${type} notification for user ${userId}:`, error);
        // In a real application, you might want to re-queue, dead-letter, or alert.
        throw error; // Re-throw to indicate job failure
    }
};
