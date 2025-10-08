import React, { useState } from 'react';

const IdeaSubmissionForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [contact, setContact] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!title || !description || !contact) {
      setMessage('Please fill in all fields.');
      return;
    }

    try {
      const response = await fetch('/api/ideas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, description, contact }),
      });

      if (response.ok) {
        setMessage('Idea submitted successfully!');
        setTitle('');
        setDescription('');
        setContact('');
      } else {
        const errorData = await response.json();
        setMessage(errorData.message || 'Error submitting idea.');
      }
    } catch (error) {
      setMessage('Network error. Please try again.');
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="idea-submission-form">
      <h2>Submit a New Idea</h2>
      {message && <p className={message.includes('successfully') ? 'success-message' : 'error-message'}>{message}</p>}
      <div>
        <label htmlFor="title">Idea Title:</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        ></textarea>
      </div>
      <div>
        <label htmlFor="contact">Your Contact Info:</label>
        <input
          type="text"
          id="contact"
          value={contact}
          onChange={(e) => setContact(e.target.value)}
          required
        />
      </div>
      <button type="submit">Submit Idea</button>
    </form>
  );
};

export default IdeaSubmissionForm;