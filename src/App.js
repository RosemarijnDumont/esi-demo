import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard'; // Assuming you have a Dashboard component
import { getSessionToken, logout } from './services/authService';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check for an existing session token on app load
    const token = getSessionToken();
    if (token) {
      setIsAuthenticated(true);
      console.log('Existing session token found. User is authenticated.');
    } else {
      console.log('No existing session token found. User is not authenticated.');
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    console.log('App: Login success, setting isAuthenticated to true.');
  };

  const handleLogout = () => {
    logout();
    setIsAuthenticated(false);
    console.log('App: Logout initiated, setting isAuthenticated to false.');
  };

  return (
    <div className="App">
      <h1>My Application</h1>
      {isAuthenticated ? (
        <Dashboard onLogout={handleLogout} />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
};

export default App;
