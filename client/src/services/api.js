import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api'; // Use environment variable or default to /api

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const apiService = {
  /**
   * Generic proxy request function.
   * @param {string} serviceName - The name of the third-party service (e.g., 'service_a', 'service_b').
   * @param {string} endpoint - The specific endpoint of the third-party service (e.g., '/data', '/users').
   * @param {string} method - The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
   * @param {object} [data=null] - The request body for POST/PUT requests.
   * @param {object} [params=null] - Query parameters for GET requests.
   * @returns {Promise<object>} The response data from the third-party service.
   */
  proxyRequest: async (serviceName, endpoint, method, data = null, params = null) => {
    try {
      const response = await apiClient.request({
        url: `/proxy/${serviceName}${endpoint}`,
        method: method,
        data: data,
        params: params,
      });
      return response.data;
    } catch (error) {
      console.error(`Error during proxy request for ${serviceName}${endpoint}:`, error);
      throw error;
    }
  },

  // Example usage for a GET request to 'service_a'
  getServiceAData: async (id) => {
    return apiService.proxyRequest('service_a', `/data/${id}`, 'GET');
  },

  // Example usage for a POST request to 'service_b'
  