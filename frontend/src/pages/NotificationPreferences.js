import React, { useState, useEffect } from 'react';
import './NotificationPreferences.css';

const NotificationPreferences = () => {
  const [preferences, setPreferences] = useState({
    email: {
      newFeatures: true,
      promotions: false,
      systemAlerts: true,
    },
    inApp: {
      newFeatures: true,
      systemAlerts: true,
      mentions: true,
    },
  });

  useEffect(() => {
    // In a real application, fetch user preferences from an API
    const fetchPreferences = async () => {
      try {
        const response = await fetch('/api/user/preferences'); // Replace with your API endpoint
        if (response.ok) {
          const data = await response.json();
          setPreferences(data);
        } else {
          console.error('Failed to fetch preferences');
        }
      } catch (error) {
        console.error('Error fetching preferences:', error);
      }
    };
    fetchPreferences();
  }, []);

  const handleToggle = (type, category) => {
    setPreferences((prevPreferences) => ({
      ...prevPreferences,
      [type]: {
        ...prevPreferences[type],
        [category]: !prevPreferences[type][category],
      },
    }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch('/api/user/preferences', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(preferences),
      });

      if (response.ok) {
        alert('Preferences saved successfully!');
      } else {
        alert('Failed to save preferences.');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
      alert('Error saving preferences.');
    }
  };

  return (
    <div className="notification-preferences-page">
      <h2>Notification Preferences</h2>

      <section className="preference-section">
        <h3>Email Notifications</h3>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.email.newFeatures}
              onChange={() => handleToggle('email', 'newFeatures')}
            />
            New Features & Updates
          </label>
        </div>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.email.promotions}
              onChange={() => handleToggle('email', 'promotions')}
            />
            Promotions & Offers
          </label>
        </div>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.email.systemAlerts}
              onChange={() => handleToggle('email', 'systemAlerts')}
            />
            System Alerts (Recommended)
          </label>
        </div>
      </section>

      <section className="preference-section">
        <h3>In-App Notifications</h3>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.inApp.newFeatures}
              onChange={() => handleToggle('inApp', 'newFeatures')}
            />
            New Features & Updates
          </label>
        </div>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.inApp.systemAlerts}
              onChange={() => handleToggle('inApp', 'systemAlerts')}
            />
            System Alerts (Recommended)
          </label>
        </div>
        <div className="preference-item">
          <label>
            <input
              type="checkbox"
              checked={preferences.inApp.mentions}
              onChange={() => handleToggle('inApp', 'mentions')}
            />
            Mentions & Replies
          </label>
        </div>
      </section>

      <button onClick={handleSave} className="save-button">
        Save Preferences
      </button>
    </div>
  );
};

export default NotificationPreferences;
