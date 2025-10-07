import axios from './axiosConfig';

const SESSION_TOKEN_KEY = 'session_token';

export const setSessionToken = (token) => {
  console.log('Setting session token:', token);
  localStorage.setItem(SESSION_TOKEN_KEY, token);
};

export const getSessionToken = () => {
  const token = localStorage.getItem(SESSION_TOKEN_KEY);
  console.log('Retrieving session token:', token);
  return token;
};

export const removeSessionToken = () => {
  console.log('Removing session token');
  localStorage.removeItem(SESSION_TOKEN_KEY);
};

export const login = async (credentials) => {
  try {
    console.log('Attempting login with credentials:', credentials);
    const response = await axios.post('/auth/login', credentials);
    const { token } = response.data;
    if (token) {
      setSessionToken(token);
      console.log('Login successful. Token received and stored.');
    }
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response ? error.response.data : error.message);
    removeSessionToken(); // Clear potential stale token on login failure
    throw error;
  }
};

export const logout = () => {
  console.log('Initiating logout.');
  removeSessionToken();
};
