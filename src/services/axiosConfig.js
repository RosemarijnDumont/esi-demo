import axios from 'axios';
import { getSessionToken, removeSessionToken } from './authService';

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach the session token
instance.interceptors.request.use(
  (config) => {
    const token = getSessionToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('Attaching session token to request:', config.url);
    }
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration or invalid tokens
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.error('Unauthorized access detected. Status 401. Clearing session token.');
      removeSessionToken();
      // Optionally, redirect to login page
      // window.location.href = '/login';
    }
    console.error('Response interceptor error for request to:', error.config.url, 'with message:', error.response ? error.response.data : error.message);
    return Promise.reject(error);
  }
);

export default instance;
