const express = require('express');
const -
const path = require('path');
const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json());
// Add a simple caching header for static assets
app.use(express.static(path.join(__dirname, '../frontend/build'), { maxAge: '1h' }));

// --- Mock Database (replace with actual database integration) ---
const mockDatabase = {
  dashboardData: {
    totalSales: 1234567,
    newUsers: 789,
    activeProjects: 45,
    salesData: Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      amount: Math.floor(Math.random() * 10000) + 1000
    })),
  },
  reportData: {
    projectStatus: [
      { status: 'Completed', count: 50 },
      { status: 'In Progress', count: 30 },
      { status: 'On Hold', count: 10 },
      { status: 'Pending', count: 5 },
    ],
    recentActivities: Array.from({ length: 10 }, (_, i) => ({
      user: `User ${i + 1}`,
      action: `performed action ${i + 1}`,
      project: `Project ${i + 1}`,
      timestamp: new Date(Date.now() - i * 60 * 60 * 1000).toISOString(),
    })),
  },
};

// --- API Endpoints ---

// Dashboard Data Endpoint
app.get('/api/dashboard', (req, res) => {
  // Simulate network delay and database query (remove in production with actual DB)
  setTimeout(() => {
    // In a real application, you would fetch this from a database.
    // Implement caching here for frequently accessed dashboard data.
    res.json(mockDatabase.dashboardData);
  }, 300); // Simulate 300ms delay
});

// Reports Data Endpoint
app.get('/api/reports', (req, res) => {
  // Simulate network delay and database query (remove in production with actual DB)
  setTimeout(() => {
    // In a real application, you would fetch this from a database.
    // Implement caching here for frequently accessed report data.
    res.json(mockDatabase.reportData);
  }, 400); // Simulate 400ms delay
});

// Serve static files from the React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
