import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const Reports = () => {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const start = performance.now();
      const response = await axios.get('/api/reports');
      const end = performance.now();
      console.log(`Reports data fetched in ${(end - start).toFixed(2)} ms`);
      setReportData(response.data);
    } catch (err) {
      console.error("Error fetching report data:", err);
      setError("Failed to load report data. Please try again later.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <div className="text-center py-8">Loading reports...</div>;
  if (error) return <div className="text-center py-8 text-red-500">Error: {error}</div>;
  if (!reportData) return <div className="text-center py-8">No report data available.</div>;

  const chartData = {
    labels: reportData.projectStatus.map(d => d.status),
    datasets: [
      {
        label: 'Projects by Status',
        data: reportData.projectStatus.map(d => d.count),
        backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
      },
    ],
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Reports</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="text-lg font-semibold">Project Status Overview</h2>
          <Bar data={chartData} />
        </div>
        <div className="bg-white shadow p-4 rounded-lg">
          <h2 className="text-lg font-semibold">Recent Activities</h2>
          <ul className="list-disc pl-5">
            {reportData.recentActivities.map((activity, index) => (
              <li key={index} className="mb-2">
                <span className="font-medium">{activity.user}</span> {activity.action} on <span className="font-medium">{activity.project}</span> at {new Date(activity.timestamp).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Reports;
