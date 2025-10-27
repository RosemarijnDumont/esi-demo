import axios from 'axios';

const API_GATEWAY_BASE_URL = '/api/v1'; // This will be your new server-side endpoint

const apiGateway = axios.create({
  baseURL: API_GATEWAY_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generic function to handle POST requests to the API Gateway
export const postToApiGateway = async (endpoint, data) => {
  try {
    const response = await apiGateway.post(endpoint, data);
    return response.data;
  } catch (error) {
    console.error(`Error posting to API Gateway endpoint ${endpoint}:`, error);
    throw error; // Re-throw to be handled by the calling component
  }
};

// Example service method for a hypothetical external API call
// You would replace this with your actual external API integrations
export const makeSecureExternalApiCall = async (payload) => {
  // The 'external-api-endpoint' here refers to a server-side route that in turn calls the actual external API
  return postToApiGateway('/external-api-proxy', payload);
};

// Add more service methods here for each external API you need to proxy
// For example:
/*
export const getSecureWeatherData = async (location) => {
  return postToApiGateway('/weather-proxy', { location });
};

export const postSecurePayment = async (paymentDetails) => {
  return postToApiGateway('/payment-proxy', paymentDetails);
};
*/
