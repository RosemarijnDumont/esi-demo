import axios from 'axios';

const API_BASE_URL = '/api/proxy'; // New server-side proxy endpoint

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Generic request function to handle API calls through the proxy
export const makeRequest = async (method, url, data = {}, headers = {}) => {
  try {
    const response = await api({
      method,
      url,
      data,
      headers,
    });
    return response.data;
  } catch (error) {
    console.error(`API request error (${method} ${url}):`, error);
    throw error;
  }
};

// Example usage for a GET request
export const getSomeData = async (endpoint, params = {}) => {
  return makeRequest('GET', endpoint, { params });
};

// Example usage for a POST request
export const postSomeData = async (endpoint, payload = {}) => {
  return makeRequest('POST', endpoint, payload);
};

export default api;