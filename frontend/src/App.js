
import React, { useState } from 'react';
import './App.css'; // Assuming some basic styling
import MFAEnrollment from './components/MFAEnrollment';
import MFAChallenge from './components/MFAChallenge';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [enrollingMFA, setEnrollingMFA] = useState(false);

  const handleLogin = (username, password) => {
    // Simulate initial login. In a real app, this would be an API call.
    // If successful and MFA is enabled for the user, set mfaRequired to true.
    // For this demonstration, we'll assume MFA is always required after a successful "login".
    if (username === 'testuser' && password === 'password') {
      setMfaRequired(true);
      console.log('Login successful, MFA required.');
    } else {
      alert('Invalid credentials');
    }
  };

  const handleMfaSuccess = () => {
    setMfaRequired(false);
    setLoggedIn(true);
    alert('MFA Verified! You are now logged in.');
  };

  const handleMfaFailure = () => {
    console.log('MFA verification failed.');
    // Optionally, handle lockout or re-challenge
  };

  const handleEnrollmentStart = () => {
    setEnrollingMFA(true);
  };

  const handleEnrollmentComplete = () => {
    setEnrollingMFA(false);
    // After enrollment, potentially redirect to login or dashboard
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to the MFA Demo App</h1>
      </header>
      <main>
        {!loggedIn && !mfaRequired && !enrollingMFA && (
          <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={(e) => {
              e.preventDefault();
              handleLogin(e.target.username.value, e.target.password.value);
            }}>
              <div className="form-group">
                <label htmlFor="username">Username:</label>
                <input type="text" id="username" name="username" defaultValue="testuser" required />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password:</label>
                <input type="password" id="password" name="password" defaultValue="password" required />
              </div>
              <button type="submit">Login</button>
            </form>
            <p>New user or need to set up MFA? <button onClick={handleEnrollmentStart}>Enroll in MFA</button></p>
          </div>
        )}

        {mfaRequired && !loggedIn && (
          <MFAChallenge onMfaSuccess={handleMfaSuccess} onMfaFailure={handleMfaFailure} />
        )}

        {enrollingMFA && (
          <MFAEnrollment onEnrollmentComplete={handleEnrollmentComplete} />
        )}

        {loggedIn && (
          <div className="dashboard">
            <h2>Dashboard</h2>
            <p>You are successfully logged in!</p>
            <button onClick={() => setLoggedIn(false)}>Logout</button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
