const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors'); // For development, if frontend and backend are on different ports

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// In-memory 'database' for demonstration. In a real app, use a proper DB.
let ideas = [];

// API endpoint to submit ideas
app.post('/api/ideas', (req, res) => {
  const { title, description, contact } = req.body;

  // Basic server-side validation
  if (!title || !description || !contact) {
    return res.status(400).json({ message: 'All fields are required.' });
  }

  const newIdea = {
    id: ideas.length > 0 ? Math.max(...ideas.map(idea => idea.id)) + 1 : 1,
    title,
    description,
    contact,
    submittedAt: new Date(),
  };

  ideas.push(newIdea);
  console.log('New idea submitted:', newIdea);
  res.status(201).json({ message: 'Idea submitted successfully!', idea: newIdea });
});

// Optional: API endpoint to get all ideas (for internal use/admin)
app.get('/api/ideas', (req, res) => {
  res.status(200).json(ideas);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
