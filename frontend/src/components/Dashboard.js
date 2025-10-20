import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const start = performance.now();
      const response = await axios.get('/api/dashboard');
      const end = performance.now();
      console.log(`Dashboard data fetched in ${(end - start).toFixed(2)} ms`);
      setDashboardData(response.data);
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
      setError("Failed to load dashboard data. Please try again later.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <div className="text-center py-8">Loading dashboard...</div>;
  if (error) return <div className="text-center py-8 text-red-500">Error: {error}</div>;
  if (!dashboardData) return <div className="text-center py-8">No dashboard data available.</div>;

  const chartData = {
    labels: dashboardData.salesData.map(d => d.date),
    datasets: [
      {
        label: 'Sales',
        data: dashboardData.salesData.map(d => d.amount),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="text-lg font-semibold">Total Sales</h2>
          <p className="text-3xl">${dashboardData.totalSales.toLocaleString()}</p>
        </div>
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="text-lg font-semibold">New Users</h2>
          <p className="text-3xl">{dashboardData.newUsers.toLocaleString()}</p>
        </div>
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="text-lg font-semibold">Active Projects</h2>
          <p className="text-3xl">{dashboardData.activeProjects.toLocaleString()}</p>
        </div>
      </div>
      <div className="bg-white shadow p-4 rounded-lg">
        <h2 className="text-lg font-semibold mb-4">Sales Over Time</h2>
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
