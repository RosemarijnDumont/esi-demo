import axios from 'axios';

const API_BASE_URL = 'https://api.clientonboarding.com'; // Replace with your actual API base URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const submitApplicationForm = async (formData) => {
  try {
    console.log('Attempting to submit form with data:', formData); // Client-side logging
    const response = await api.post('/application/submit', formData);
    console.log('Form submission successful:', response.data); // Client-side logging
    return response.data;
  } catch (error) {
    console.error('Form submission failed:', error.response ? error.response.data : error.message); // Client-side logging
    throw error;
  }
};
