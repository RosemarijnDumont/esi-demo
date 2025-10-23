
// frontend/src/components/OAuthCallback.js

import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import OAuthService from '../services/OAuthService';
import { useAuth } from '../contexts/AuthContext';
import ErrorMessage from './ErrorMessage';

const OAuthCallback = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { login } = useAuth();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handleCallback = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code');
      const state = params.get('state');
      const provider = params.get('provider'); // Assuming provider is also passed in the callback for context

      if (!code || !state || !provider) {
        setError({
          code: 'MISSING_PARAMS',
          message: 'OAuth callback parameters are missing.',
          suggestion: 'Please try connecting your account again. If the issue persists, contact support.',
        });
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const data = await OAuthService.handleOAuthCallback(provider, code, state);
        login(data.token, data.user); // Assuming the callback returns a token and user info
        // Redirect to a dashboard or previous page, preserving user context
        const redirectTo = localStorage.getItem('oauth_redirect_to') || '/dashboard';
        localStorage.removeItem('oauth_redirect_to');
        navigate(redirectTo);
      } catch (err) {
        console.error('OAuth callback failed:', err);
        const errorCode = err.response?.data?.errorCode || 'UNKNOWN_ERROR';
        let errorMessage = 'An unexpected error occurred during OAuth. Please try again.';
        let suggestion = 'If the issue persists, try clearing your browser cache and cookies, or ensure pop-ups are allowed.';

        switch (errorCode) {
          case 'INVALID_STATE':
            errorMessage = 'Security error: The OAuth state parameter mismatch.';
            suggestion = 'This might be due to an expired session or a manipulated URL. Please try initiating the connection again.';
            break;
          case 'AUTHORIZATION_DENIED':
            errorMessage = 'You denied the authorization request.';
            suggestion = 'To connect your account, you must grant the necessary permissions.';
            break;
          case 'ALREADY_CONNECTED':
            errorMessage = 'This account is already connected.';
            suggestion = 'You may already have connected this account with a different user.';
            break;
          case 'PROVIDER_ERROR':
            errorMessage = `The OAuth provider reported an error: ${err.response?.data?.message || ''}`.trim();
            suggestion = 'Please check your account settings on the provider\\'s side or try again later.';
            break;
          default:
            // Generic error message already set
            break;
        }

        setError({ code: errorCode, message: errorMessage, suggestion });
      } finally {
        setLoading(false);
      }
    };

    handleCallback();
  }, [location, navigate, login]);

  if (loading) {
    return <div className="oauth-loading">Connecting your account...</div>;
  }

  return (
    <div className="oauth-callback-container">
      {error && (
        <ErrorMessage
          title="OAuth Connection Failed"
          message={error.message}
          suggestion={error.suggestion}
          errorCode={error.code}
        />
      )}
    </div>
  );
};

export default OAuthCallback;
