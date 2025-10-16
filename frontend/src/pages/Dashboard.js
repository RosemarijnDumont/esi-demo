import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import 'chart.js/auto';
import './Dashboard.css';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found.');
      }
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };
      const response = await axios.get('/api/dashboard', config); // Optimized API endpoint
      setDashboardData(response.data);
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again later.');
      // Potentially redirect to login if token is invalid or expired
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        // Handle invalid/expired token - e.g., clear local storage and redirect to login
        localStorage.removeItem('token');
        // window.location.href = '/login'; // Example redirection
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();

    // Client-side caching strategy: Re-fetch data every 5 minutes
    const intervalId = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(intervalId);
  }, [fetchData]);

  const processChartData = (data, labelKey, valueKey, label) => {
    if (!data || data.length === 0) {
      return {
        labels: [],
        datasets: []
      };
    }
    return {
      labels: data.map(item => item[labelKey]),
      datasets: [
        {
          label: label,
          data: data.map(item => item[valueKey]),
          fill: true,
          backgroundColor: 'rgba(75,192,192,0.2)',
          borderColor: 'rgba(75,192,192,1)',
          tension: 0.1
        }
      ]
    };
  };

  if (loading) {
    return <div className="dashboard-container">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="dashboard-container error-message">Error: {error}</div>;
  }

  if (!dashboardData) {
    return <div className="dashboard-container">No dashboard data available.</div>;
  }

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>
      <section className="dashboard-section">
        <h2>Daily Sales Overview</h2>
        <div classNameName="chart-container">
          <Line data={processChartData(dashboardData.dailySales, 'date', 'sales', 'Daily Sales')} />
        </div>
      </section>

      <section className="dashboard-section">
        <h2>Product Performance</h2>
        <div classNameName="chart-container">
          <Bar data={processChartData(dashboardData.productPerformance, 'productName', 'revenue', 'Product Revenue')} />
        </div>
      </section>

      <section className="dashboard-section">
        <h2>Key Metrics</h2>
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Total Revenue</h3>
            <p>${dashboardData.totalRevenue?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="metric-card">
            <h3>New Customers</h3>
            <p>{dashboardData.newCustomers || 'N/A'}</p>
          </div>
          <div className="metric-card">
            <h3>Conversion Rate</h3>
            <p>{dashboardData.conversionRate?.toFixed(2) || 'N/A'}%</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
