import React, { useState, useEffect } from 'react';
import './NotificationCenter.css';

const NotificationCenter = () => {
  const [notifications, setNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Simulate real-time updates with WebSockets or long-polling
    // In a real application, you would establish a WebSocket connection here
    const ws = new WebSocket('ws://localhost:8080/ws/notifications'); // Replace with your WebSocket endpoint

    ws.onmessage = (event) => {
      const newNotification = JSON.parse(event.data);
      setNotifications((prevNotifications) => [newNotification, ...prevNotifications]);
    };

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    // Clean up WebSocket connection on unmount
    return () => {
      ws.close();
    };
  }, []);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  const markAsRead = (id) => {
    setNotifications((prevNotifications) =>
      prevNotifications.map((notification) =>
        notification.id === id ? { ...notification, read: true } : notification
      )
    );
  };

  return (
    <div className="notification-center">
      <button className="notification-icon" onClick={toggleOpen}>
        S
        {notifications.filter((n) => !n.read).length > 0 && (
          <span className="notification-badge">
            {notifications.filter((n) => !n.read).length}
          </span>
        )}
      </button>
      {isOpen && (
        <div className="notification-dropdown">
          <h3>Notifications</h3>
          {notifications.length === 0 ? (
            <p>No new notifications.</p>
          ) : (
            <ul>
              {notifications.map((notification) => (
                <li
                  key={notification.id}
                  className={notification.read ? 'read' : ''}
                  onClick={() => !notification.read && markAsRead(notification.id)}
                >
                  <p className="notification-message">{notification.message}</p>
                  <span className="notification-timestamp">
                    {new Date(notification.timestamp).toLocaleString()}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationCenter;
