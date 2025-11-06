import React, { useState } from 'react';
import { submitApplicationForm } from '../services/api';

const ApplicationForm = () => {
  const [formData, setFormData] = useState({
    // Initialize with your form fields
    fullName: '',
    email: '',
    // ... other form fields
  });
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmissionStatus('submitting');
    setErrorMessage(null);
    try {
      const response = await submitApplicationForm(formData);
      setSubmissionStatus('success');
      console.log('Backend response:', response);
      // Optionally, redirect user or show a success message
    } catch (error) {
      setSubmissionStatus('error');
      setErrorMessage('Failed to submit application. Please try again.');
      console.error('Submission error details:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="application-form">
      <h2>Client Application Form</h2>
      <div>
        <label htmlFor="fullName">Full Name:</label>
        <input
          type="text"
          id="fullName"
          name="fullName"
          value={formData.fullName}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      {/* Add other form fields here */}
      <button type="submit" disabled={submissionStatus === 'submitting'}>
        {submissionStatus === 'submitting' ? 'Submitting...' : 'Submit Application'}
      </button>

      {submissionStatus === 'success' && (
        <p className="success-message">Application submitted successfully!</p>
      )}
      {submissionStatus === 'error' && (
        <p className="error-message">{errorMessage}</p>
      )}
    </form>
  );
};

export default ApplicationForm;
