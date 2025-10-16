const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

const sendEmailNotification = async (to, subject, htmlContent) => {
  try {
    await transporter.sendMail({
      from: process.env.EMAIL_USER,
      to,
      subject,
      html: htmlContent,
    });
    console.log(`Email sent to ${to} with subject: ${subject}`);
  } catch (error) {
    console.error(`Failed to send email to ${to}:`, error);
    throw error;
  }
};

const triggerInAppNotification = (userId, message) => {
  // This would typically interface with a real-time system (e.g., WebSocket, long-polling)
  // For now, we'll log it as a placeholder for the actual implementation.
  console.log(`In-app notification triggered for user ${userId}: ${message}`);
  // Example: Emit an event that the web/mobile app's WebSocket client listens for
  // io.to(userId).emit('newNotification', { message, timestamp: new Date() });
};

module.exports = { sendEmailNotification, triggerInAppNotification };
