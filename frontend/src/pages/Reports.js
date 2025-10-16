import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import 'chart.js/auto';
import './Reports.css';

const Reports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('monthly'); // Example filter for reports

  const fetchData = useCallback(async (currentFilter) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found.');
      }
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        params: { filter: currentFilter } // Pass filter to API
      };
      // Optimized API endpoint for reports, potentially paginated or aggregated
      const response = await axios.get('/api/reports', config);
      setReportData(response.data);
    } catch (err) {
      console.error('Failed to fetch report data:', err);
      setError('Failed to load report data. Please try again later.');
      if (err.response && (err.response.status === 401 || err.response.status === 403)) {
        localStorage.removeItem('token');
        // window.location.href = '/login';
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(filter);
    // Implement caching logic, e.g., Service Worker or browser cache headers for API
  }, [filter, fetchData]);

  const handleFilterChange = (event) => {
    setFilter(event.target.value);
  };

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
          backgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#1ABC9C',
            '#9B59B6',
            '#F1C40F'
          ],
          hoverBackgroundColor: [
            '#FF6384',
            '#36A2EB',
            '#FFCE56',
            '#1ABC9C',
            '#9B59B6',
            '#F1C40F'
          ]
        }
      ]
    };
  };

  if (loading) {
    return <div className="reports-container">Loading reports...</div>;
  }

  if (error) {
    return <div className="reports-container error-message">Error: {error}</div>;
  }

  if (!reportData) {
    return <div className="reports-container">No report data available.</div>;
  }

  return (
    <div className="reports-container">
      <h1>Reports</h1>
      <div className="filter-controls">
        <label htmlFor="report-filter">Select Report Period:</label>
        <select id="report-filter" value={filter} onChange={handleFilterChange}>
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="quarterly">Quarterly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      <section className="reports-section">
        <h2>Sales by Category</h2>
        <div className="chart-container">
          <Pie data={processChartData(reportData.salesByCategory, 'category', 'sales', 'Sales by Category')} />
        </div>
      </section>

      <section className="reports-section">
        <h2>Regional Performance</h2>
        <div className="chart-container">
          <Bar data={processChartData(reportData.regionalPerformance, 'region', 'revenue', 'Revenue by Region')} />
        </div>
      </section>
    </div>
  );
};

export default Reports;
