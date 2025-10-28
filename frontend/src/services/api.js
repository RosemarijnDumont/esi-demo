import axios from 'axios';

const API_BASE_URL = '/api/proxy'; // All requests will now go through our backend proxy

export const fetchDataSecurely = async (payload) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/secure-data`, payload);
    return response.data;
  } catch (error) {
    console.error('Error fetching data securely:', error);
    throw error;
  }
};