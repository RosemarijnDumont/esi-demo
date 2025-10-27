export const handleApiError = (error, componentName = 'Unknown Component') => {
  let errorMessage = 'An unexpected error occurred.';
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    errorMessage = `Error from server (${error.response.status}): ${error.response.data.message || error.response.data}`;
    console.error(`[${componentName}] Server Error:`, error.response.data);
  } else if (error.request) {
    // The request was made but no response was received
    errorMessage = 'No response received from the server. Please check your network connection.';
    console.error(`[${componentName}] Network Error:`, error.request);
  } else {
    // Something happened in setting up the request that triggered an Error
    errorMessage = `Request setup error: ${error.message}`;
    console.error(`[${componentName}] Request Error:`, error.message);
  }
  // Optionally, you could display a user-friendly notification here
  // For example: alert(errorMessage);
  return errorMessage;
};

export const withApiRetry = async (apiCallFn, retries = 3, delay = 1000) => {
  for (let i = 0; i < retries; i++) {
    try {
      return await apiCallFn();
    } catch (error) {
      if (i < retries - 1) {
        console.warn(`API call failed, retrying in ${delay / 1000}s... (Attempt ${i + 1}/${retries})`, error);
        await new Promise(res => setTimeout(res, delay));
      } else {
        throw error; // Re-throw error after final retry attempt
      }
    }
  }
};
