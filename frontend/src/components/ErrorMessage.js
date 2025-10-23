
// frontend/src/components/ErrorMessage.js

import React from 'react';
import PropTypes from 'prop-types';
import './ErrorMessage.css'; // Assuming you have a CSS file for styling

const ErrorMessage = ({ title, message, suggestion, errorCode }) => {
  return (
    <div className="error-message-container">
      {title && <h2 className="error-message-title">{title}</h2>}
      <p className="error-message-text">{message}</p>
      {suggestion && <p className="error-message-suggestion"><strong>Suggestion:</strong> {suggestion}</p>}
      {errorCode && <p className="error-message-code">Error Code: {errorCode}</p>}
      <div className="error-message-actions">
        {/* You can add action buttons here, e.g., 'Try Again', 'Contact Support' */}
        {/* <button className="btn btn-primary" onClick={() => window.location.reload()}>Try Again</button> */}
        {/* <button className="btn btn-secondary" onClick={() => navigate('/support')}>Contact Support</button> */}
      </div>
    </div>
  );
};

ErrorMessage.propTypes = {
  title: PropTypes.string,
  message: PropTypes.string.isRequired,
  suggestion: PropTypes.string,
  errorCode: PropTypes.string,
};

ErrorMessage.defaultProps = {
  title: 'Error',
  suggestion: null,
  errorCode: null,
};

export default ErrorMessage;
