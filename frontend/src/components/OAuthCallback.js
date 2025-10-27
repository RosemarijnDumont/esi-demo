
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { logClientError, logClientInfo } from '../utils/logClient';

const OAuthCallback = () => {
  const location = useLocation();
  const [message, setMessage] = useState('Processing OAuth callback...');
  const [error, setError] = useState(null);

  useEffect(() => {
    logClientInfo('OAuthCallback', 'Attempting to process OAuth callback', { search: location.search });

    const processCallback = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');
      const state = params.get('state');
      const errorParam = params.get('error');
      const errorDescription = params.get('error_description');

      if (errorParam) {
        const errorMessage = errorDescription || `OAuth error: ${errorParam}. Please try again.`;
        setError(errorMessage);
        setMessage('');
        logClientError('OAuthCallback', 'OAuth callback failed', { errorParam, errorDescription });
        // Additional monitoring for failed attempts
        reportOAuthError({ type: 'client_side_oauth_error', error: errorParam, description: errorDescription });
        return;
      }

      if (!code) {
        const noCodeError = 'Authorization code not found in callback. Please try again or contact support.';
        setError(noCodeError);
        setMessage('');
        logClientError('OAuthCallback', 'Authorization code missing', { search: location.search });
        reportOAuthError({ type: 'client_side_missing_code', description: noCodeError });
        return;
      }

      try {
        // Exchange code for token - this would typically be a backend call
        // For demonstration, we'll simulate a success or failure.
        const response = await axios.post('/api/oauth/token', {
          code,
          state,
          redirect_uri: window.location.origin + '/oauth/callback',
        });

        if (response.data.success) {
          setMessage('OAuth connection successful! Redirecting...');
          logClientInfo('OAuthCallback', 'OAuth connection successful');
          // Redirect to a success page or user's dashboard
          window.location.href = '/dashboard'; // Example redirect
        } else {
          const backendError = response.data.message || 'Failed to connect via OAuth. Please try again.';
          setError(backendError);
          setMessage('');
          logClientError('OAuthCallback', 'Backend reported OAuth failure', { responseData: response.data });
          reportOAuthError({ type: 'backend_oauth_error', description: backendError, details: response.data });
        }
      } catch (err) {
        const networkError = err.response?.data?.message || 'Network error or server issue. Please check your internet connection or try again later.';
        setError(networkError);
        setMessage('');
        logClientError('OAuthCallback', 'Error during OAuth token exchange', { error: err.message, response: err.response?.data });
        reportOAuthError({ type: 'network_error_oauth', description: networkError, details: err.message });
      }
    };

    processCallback();
  }, [location]);

  const reportOAuthError = async (errorDetails) => {
    try {
      await axios.post('/api/monitoring/oauth-error', {
        timestamp: new Date().toISOString(),
        ...errorDetails,
      });
    } catch (err) {
      console.error('Failed to report OAuth error:', err);
    }
  };

  return (
    <div style={styles.container}>
      {error ? (
        <div style={styles.errorCard}>
          <h2 style={styles.errorTitle}>OAuth Connection Failed</h2>
          <p style={styles.errorMessage}>{error}</p>
          <p style={styles.guidance}>Here are some steps you can take:</p>
          <ul style={styles.guidanceList}>
            <li>Double-check if you granted all necessary permissions.</li>
            <li>Try initiating the OAuth process again.</li>
            <li>Clear your browser cache and cookies, then try again.</li>
            <li>Ensure your browser is not blocking pop-ups from this site.</li>
            <li>If the issue persists, please <a href="/support" style={styles.link}>contact our support team</a> and provide the time of this error.</li>
          </ul>
        </div>
      ) : (
        <div style={styles.loadingCard}>
          <h2 style={styles.loadingMessage}>{message}</h2>
          <div style={styles.spinner}></div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#f7f9fc',
    fontFamily: 'Arial, sans-serif',
  },
  loadingCard: {
    backgroundColor: '#ffffff',
    padding: '40px',
    borderRadius: '10px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    textAlign: 'center',
    minWidth: '350px',
  },
  errorCard: {
    backgroundColor: '#fff3f3',
    border: '1px solid #ffcccc',
    padding: '40px',
    borderRadius: '10px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    textAlign: 'left',
    maxWidth: '500px',
  },
  errorTitle: {
    color: '#d32f2f',
    marginBottom: '15px',
    fontSize: '24px',
  },
  errorMessage: {
    color: '#555',
    marginBottom: '20px',
    lineHeight: '1.6',
  },
  guidance: {
    color: '#333',
    fontWeight: 'bold',
    marginBottom: '10px',
  },
  guidanceList: {
    listStyleType: 'disc',
    marginLeft: '20px',
    color: '#555',
    lineHeight: '1.8',
  },
  loadingMessage: {
    color: '#333',
    fontSize: '20px',
    marginBottom: '20px',
  },
  spinner: {
    border: '4px solid rgba(0, 0, 0, 0.1)',
    borderLeftColor: '#4a90e2',
    borderRadius: '50%',
    width: '30px',
    height: '30px',
    animation: 'spin 1s linear infinite',
    margin: '0 auto',
  },
  link: {
    color: '#4a90e2',
    textDecoration: 'none',
  },
};

// Add a global style for the spin animation (if not already in a global CSS file)
const styleSheet = document.styleSheets[0] || document.head.appendChild(document.createElement('style')).sheet;
styleSheet.insertRule(`
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
`, styleSheet.cssRules.length);

export default OAuthCallback;
