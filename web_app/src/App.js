import React, { useEffect, useState } from 'react';
import { configureWebSocket } from './services/dataSync'; // Assuming a similar dataSync service on web for consistency

function App() {
  const [data, setData] = useState([]);
  const userId = 'user123'; // Replace with actual user ID from session/auth

  useEffect(() => {
    const ws = configureWebSocket(userId, (message) => {
      if (message.type === 'DATA_UPDATE') {
        console.log('Real-time data update received:', message.payload);
        // Update UI with new data
        setData(prevData => [...prevData, message.payload]);
      }
    });

    // Clean up WebSocket connection on component unmount
    return () => {
      ws.close();
    };
  }, [userId]);

  return (
    <div className="App">
      <h1>Welcome to the Dashboard</h1>
      <p>Real-time data will appear here:</p>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{JSON.stringify(item)}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
