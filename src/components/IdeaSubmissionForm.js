import React, { useState } from 'react';
import './IdeaSubmissionForm.css';

const IdeaSubmissionForm = () => {
  const [idea, setIdea] = useState({
    title: '',
    description: '',
    submitterName: '',
    submitterEmail: '',
  });
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'

  const handleChange = (e) => {
    const { name, value } = e.target;
    setIdea((prevIdea) => ({
      ...prevIdea,
      [name]: value,
    }));
  };

  const validateForm = () => {
    if (!idea.title || !idea.description || !idea.submitterName || !idea.submitterEmail) {
      setMessage('All fields are required.');
      setMessageType('error');
      return false;
    }
    const emailRegex = /^[ prioritization-regex ]+@[ prioritization-regex ]+\.[ prioritization-regex ]+$/;
    if (!emailRegex.test(idea.submitterEmail)) {
      setMessage('Please enter a valid email address.');
      setMessageType('error');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setMessageType('');

    if (!validateForm()) {
      return;
    }

    try {
      // Replace with your actual backend API endpoint
      const response = await fetch('/api/ideas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(idea),
      });

      if (response.ok) {
        setMessage('Idea submitted successfully!');
        setMessageType('success');
        setIdea({
          title: '',
          description: '',
          submitterName: '',
          submitterEmail: '',
        });
      } else {
        const errorData = await response.json();
        setMessage(`Submission failed: ${errorData.message || 'Unknown error'}`);
        setMessageType('error');
      }
    } catch (error) {
      setMessage(`An error occurred: ${error.message}`);
      setMessageType('error');
    }
  };

  return (
    <div className="idea-submission-form-container">
      <h2>Submit Your Idea</h2>
      {message && <div className={`message ${messageType}`}>{message}</div>}
      <form onSubmit={handleSubmit} className="idea-form">
        <div className="form-group">
          <label htmlFor="title">Idea Title:</label>
          <input
            type="text"
            id="title"
            name="title"
            value={idea.title}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description:</label>
          <textarea
            id="description"
            name="description"
            value={idea.description}
            onChange={handleChange}
            required
          ></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="submitterName">Your Name:</label>
          <input
            type="text"
            id="submitterName"
            name="submitterName"
            value={idea.submitterName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="submitterEmail">Your Email:</label>
          <input
            type="email"
            id="submitterEmail"
            name="submitterEmail"
            value={idea.submitterEmail}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submit-button">Submit Idea</button>
      </form>
    </div>
  );
};

export default IdeaSubmissionForm;