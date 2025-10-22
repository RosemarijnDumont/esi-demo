
const nodemailer = require('nodemailer');
const kue = require('kue');
const redis = require('redis');
const { server } = require('../../server'); // Assuming your main server file exports a server instance for Socket.IO
const io = require('socket.io')(server); // Initialize Socket.IO with your server

const queue = kue.createQueue();
const redisClient = redis.createClient();

// --- Notification Service Configuration ---

// Email transporter setup (using Mailtrap for development/testing)
const transporter = nodemailer.createTransport({
  host: process.env.EMAIL_HOST || 'smtp.mailtrap.io',
  port: process.env.EMAIL_PORT || 2525,
  auth: {
    user: process.env.EMAIL_USER || 'your_mailtrap_user',
    pass: process.env.EMAIL_PASS || 'your_mailtrap_password'
  }
});

// --- Notification Delivery ---

/**
 * Sends various types of notifications (email, in-app).
 * Queues notifications for asynchronous processing and includes retry logic.
 * @param {string} type - The type of notification (e.g., 'email', 'in-app').
 * @param {object} options - Options specific to the notification type (e.g., to, subject, message, userId).
 */
async function sendNotification(type, options) {
  return new Promise((resolve, reject) => {
    const job = queue.create('sendNotification', { type, options })
      .attempts(3) // Retry up to 3 times
      .backoff({ delay: 2000, type: 'fixed' }) // 2-second fixed delay between retries
      .save(err => {
        if (err) {
          console.error(`Failed to create notification job: ${err}`);
          return reject(new Error('Failed to queue notification.'));
        }
        console.log(`Notification job created: ${job.id} for type: ${type}`);
        resolve({ jobId: job.id, status: 'queued' });
      });
  });
}

// Process notification jobs
queue.process('sendNotification', async (job, done) => {
  const { type, options } = job.data;
  console.log(`Processing notification job ${job.id} for type: ${type}`);

  try {
    switch (type) {
      case 'email':
        await sendEmail(options);
        break;
      case 'in-app':
        await sendInAppNotification(options);
        break;
      // Add more notification types as needed
      default:
        throw new Error(`Unknown notification type: ${type}`);
    }
    console.log(`Successfully sent ${type} notification for job ${job.id}.`);
    done();
  } catch (error) {
    console.error(`Error sending ${type} notification for job ${job.id}: ${error.message}`);
    done(new Error(`Notification delivery failed: ${error.message}`));
  }
});

/**
 * Sends an email using the configured transporter.
 * @param {object} emailOptions - Options for sending email (to, subject, html/text).
 */
async function sendEmail(emailOptions) {
  const mailOptions = {
    from: process.env.EMAIL_FROM || 'no-reply@yourdomain.com',
    to: emailOptions.to,
    subject: emailOptions.subject,
    html: emailOptions.html || emailOptions.text, // Prefer HTML, fallback to text
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent: %s', info.messageId);
    // Consider logging email success to a monitoring system
    return info;
  } catch (error) {
    console.error('Error sending email:', error);
    // Check for specific error types (e.g., rate limits, invalid recipient)
    // Implement exponential backoff for retries if due to rate limits
    throw error; // Re-throw to allow Kue to handle retries
  }
}

/**
 * Sends an in-app notification via WebSockets.
 * Assumes a 'userId' in options to target specific users, or 'broadcast' for all connected users.
 * @param {object} inAppOptions - Options for in-app notification (userId, message, data, eventType).
 */
async function sendInAppNotification(inAppOptions) {
  const { userId, message, data, eventType = 'new_notification' } = inAppOptions;

  if (!io) {
    console.warn('Socket.IO not initialized. In-app notifications will not be sent.');
    return; // Or throw an error depending on desired strictness
  }

  if (userId) {
    // Emit to a specific user (assuming user-specific rooms or client-side filtering)
    io.to(userId).emit(eventType, { message, data });
    console.log(`In-app notification sent to user ${userId}: ${message}`);
  } else {
    // Broadcast to all connected clients
    io.emit(eventType, { message, data, broadcast: true });
    console.log(`In-app notification broadcast: ${message}`);
  }
}

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
  console.error(`Notification Job ${id} failed: ${err}`);
  // Here you could integrate with a third-party alert service (e.g., PagerDuty, Slack).
  // For email failures, consider a dead-letter queue or manual review.
});

module.exports = { 
  sendNotification, 
  sendEmail, // Export for direct use if needed (e.g., password reset flow)
  sendInAppNotification, // Export for direct use if needed
  queue, // Export queue for potential external management/monitoring
  io, // Export Socket.IO instance for other modules to use
};
