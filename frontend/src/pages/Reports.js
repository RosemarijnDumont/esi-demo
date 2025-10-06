
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Reports() {
  const [reportsData, setReportsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReportsData = async () => {
      try {
        // --- Task 2: Utilize optimized report data API ---
        // In a real application, you would ensure the backend for this is indeed optimized.
        const response = await axios.get('/optimized_report_data');
        setReportsData(response.data);
      } catch (err) {
        setError('Failed to load reports data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReportsData();
  }, []);

  if (loading) {
    return <div>Loading reports...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <h1>Reports</h1>
      {reportsData && reportsData.length > 0 ? (
        <ul>
          {reportsData.map((report, index) => (
            <li key={index}>{report}</li>
          ))}
        </ul>
      ) : (
        <p>No reports data available.</p>
      )}
    </div>
  );
}

export default Reports;
