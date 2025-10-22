import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_PROXY_URL || '/api';

const apiProxy = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const makeProxiedApiRequest = async (method, url, data = {}) => {
  try {
    const response = await apiProxy({ method, url, data });
    return response.data;
  } catch (error) {
    console.error(`Error during proxied API request to ${url}:`, error);
    // Implement robust error handling and retry mechanisms here
    throw error;
  }
};
