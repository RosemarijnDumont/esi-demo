
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import io from 'socket.io-client';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:3000';

const Dashboard = () => {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notifications, setNotifications] = useState([]);

  // Function to fetch initial data
  const fetchEntries = async () => {
    try {
      setLoading(true);
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 500));
      const response = await axios.get(`${BACKEND_URL}/api/entries`); // Assuming an endpoint for entries
      setEntries(response.data);
    } catch (err) {
      console.error('Error fetching entries:', err);
      setError('Failed to load entries.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEntries();

    // Setup WebSocket connection for real-time updates
    const socket = io(BACKEND_URL);

    socket.on('connect', () => {
      console.log('Connected to WebSocket server.');
    });

    // Listen for 'new_notification' events from the backend (notificationService.js)
    socket.on('new_notification', (notification) => {
      console.log('Received in-app notification:', notification);
      setNotifications((prevNotifications) => [...prevNotifications, notification]);
      // If the notification indicates new data, refresh the entries
      if (notification.eventType === 'web_client_update') {
        console.log('New data notification received, refreshing entries...');
        fetchEntries(); // Re-fetch entries to reflect mobile updates
      }
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server.');
    });

    socket.on('error', (err) => {
        console.error('WebSocket Error:', err);
    });

    // Cleanup on component unmount
    return () => {
      socket.disconnect();
    };
  }, []); // Empty dependency array means this runs once on mount

  if (loading) return <div style={{ textAlign: 'center', padding: '20px' }}>Loading dashboard data...</div>;
  if (error) return <div style={{ textAlign: 'center', padding: '20px', color: 'red' }}>Error: {error}</div>;

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Dashboard</h1>
      
      <div style={styles.notificationsSection}>
        <h2>Notifications</h2>
        {notifications.length === 0 ? (
          <p>No new notifications.</p>
        ) : (
          <ul>
            {notifications.map((notif, index) => (
              <li key={index} style={styles.notificationItem}>
                <strong>{notif.message}</strong>: {JSON.stringify(notif.data)}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div style={styles.entriesSection}>
        <h2>Recent Entries (Synced from Mobile)</h2>
        {entries.length === 0 ? (
          <p>No entries to display.</p>
        ) : (
          <ul style={styles.entriesList}>
            {entries.map((entry) => (
              <li key={entry.id} style={styles.entryItem}>
                <strong>{entry.title}</strong>: {entry.description} - ${entry.amount} (Added: {new Date(entry.timestamp).toLocaleString()})
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
    maxWidth: '900px',
    margin: '30px auto',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  header: {
    fontSize: '2em',
    color: '#333',
    marginBottom: '25px',
    textAlign: 'center',
  },
  notificationsSection: {
    marginBottom: '30px',
    padding: '15px',
    backgroundColor: '#e6f7ff',
    borderLeft: '5px solid #1890ff',
    borderRadius: '4px',
  },
  notificationItem: {
    marginBottom: '8px',
    fontSize: '0.9em',
    color: '#555',
  },
  entriesSection: {
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '4px',
    border: '1px solid #eee',
  },
  entriesList: {
    listStyleType: 'none',
    padding: 0,
  },
  entryItem: {
    backgroundColor: '#fafafa',
    padding: '10px 15px',
    marginBottom: '10px',
    borderRadius: '5px',
    border: '1px solid #e0e0e0',
    fontSize: '0.95em',
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
};

export default Dashboard;
