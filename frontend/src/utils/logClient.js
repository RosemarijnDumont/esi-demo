
import axios from 'axios';

const LOG_ENDPOINT = '/api/client-log';

const sendLog = (level, component, message, details = {}) => {
  try {
    axios.post(LOG_ENDPOINT, {
      timestamp: new Date().toISOString(),
      level,
      component,
      message,
      details: JSON.stringify(details), // Stringify details to ensure it's a valid JSON string
      userAgent: navigator.userAgent,
      url: window.location.href,
    });
  } catch (error) {
    console.error('Failed to send client log:', error);
  }
};

export const logClientInfo = (component, message, details) => {
  sendLog('INFO', component, message, details);
};

export const logClientWarning = (component, message, details) => {
  sendLog('WARNING', component, message, details);
};

export const logClientError = (component, message, details) => {
  sendLog('ERROR', component, message, details);
};
