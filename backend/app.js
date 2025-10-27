
const express = require('express');
const app = express();
const monitoringRoutes = require('./routes/monitoring');

// Middleware to parse JSON bodies
app.use(express.json());

// Integrate monitoring routes
app.use('/', monitoringRoutes);

// Existing routes (example)
app.post('/api/oauth/token', (req, res) => {
  // Simulate backend token exchange
  console.log('Backend received OAuth code:', req.body.code);
  if (req.body.code === 'valid_code') {
    res.json({ success: true, message: 'Token exchanged successfully' });
  } else if (req.body.code === 'error_code_backend') {
    res.status(500).json({ success: false, message: 'Invalid or expired code provided by OAuth provider.' });
  } else if (req.body.code === 'network_failure_simulate') {
    // Simulate a network failure on the backend side after a delay
    setTimeout(() => {
      res.status(500).json({ success: false, message: 'Simulated backend service outage.' });
    }, 200);
  }
  else {
    res.status(400).json({ success: false, message: 'Invalid authorization code.' });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
