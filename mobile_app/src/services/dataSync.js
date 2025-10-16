import Sockette from 'sockette';

const configureWebSocket = (userId, onMessageCallback) => {
  const ws = new Sockette(`ws://localhost:8080/ws?userId=${userId}`, {
    timeout: 5000,
    maxAttempts: 10,
    onopen: e => console.log('Connected!', e),
    onmessage: e => onMessageCallback(JSON.parse(e.data)),
    onclose: e => console.log('Closed!', e),
    onerror: e => console.log('Error:', e),
  });

  return ws;
};

const sendMobileData = async (endpoint, data) => {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
};

export { configureWebSocket, sendMobileData };
