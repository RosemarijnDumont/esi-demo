import React, { useEffect, useState } from 'react';
import { getSomeData } from '../services/api';

const DataFetcher = ({ endpoint }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getSomeData(endpoint);
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint]);

  if (loading) return <div>Loading data...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>No data available.</div>;

  return (
    <div>
      <h2>Data from {endpoint}</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
};

export default DataFetcher;