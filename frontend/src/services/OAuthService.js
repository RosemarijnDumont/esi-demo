
// frontend/src/services/OAuthService.js

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

const OAuthService = {
  initiateOAuth: async (provider, redirectUri, state) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/oauth/initiate`, {
        provider,
        redirectUri,
        state, // Pass the state parameter to the backend
      });
      return response.data;
    } catch (error) {
      console.error('Error initiating OAuth:', error);
      throw error;
    }
  },

  handleOAuthCallback: async (provider, code, state) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/oauth/callback`, {
        provider,
        code,
        state, // Pass the state parameter to the backend
      });
      return response.data;
    } catch (error) {
      console.error('Error handling OAuth callback:', error);
      throw error;
    }
  },
};

export default OAuthService;
