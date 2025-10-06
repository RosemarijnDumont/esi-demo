
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Reports from './pages/Reports';
// Import other components/pages as needed for a complete application

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
            <li>
              <Link to="/reports">Reports</Link>
            </li>
            {/* Add more navigation links here */}
          </ul>
        </nav>

        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/reports" element={<Reports />} />
          {/* Define other routes here */}
          <Route path="/" element={<h2>Welcome to the Performance Optimized App!</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
