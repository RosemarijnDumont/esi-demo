
import React, { useState } from 'react';

const MFAChallenge = ({ onMfaSuccess, onMfaFailure }) => {
  const [mfaToken, setMfaToken] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // In a real application, this would be an API call to your backend
    // to verify the MFA token.
    if (mfaToken === '123456') { // Simulate a valid token for demonstration
      onMfaSuccess();
    } else {
      setError('Invalid MFA token. Please try again.');
      onMfaFailure();
    }
  };

  return (
    <div className="mfa-challenge-container">
      <h2>Multi-Factor Authentication</h2>
      <p>Please enter the 6-digit code from your authenticator app.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="mfaToken">MFA Code:</label>
          <input
            type="text"
            id="mfaToken"
            value={mfaToken}
            onChange={(e) => setMfaToken(e.target.value)}
            maxLength="6"
            pattern="[0-9]{6}"
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        <button type="submit" className="verify-button">Verify Code</button>
      </form>
    </div>
  );
};

export default MFAChallenge;
