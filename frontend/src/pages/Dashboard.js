
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // --- Task 3: Utilize cached dashboard data ---
        const response = await axios.get('/cached_dashboard_data');
        setDashboardData(response.data);
      } catch (err) {
        setError('Failed to load dashboard data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      {dashboardData ? (
        <div>
          <p>Metric 1: {dashboardData.metric1}</p>
          <p>Metric 2: {dashboardData.metric2}</p>
          <h2>Dashboard Items:</h2>
          <ul>
            {dashboardData.items && dashboardData.items.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No dashboard data available.</p>
      )}
    </div>
  );
}

export default Dashboard;
