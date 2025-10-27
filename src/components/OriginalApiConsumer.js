import React, { useEffect, useState } from 'react';
import { makeSecureExternalApiCall } from '../services/apiGateway';
import { handleApiError, withApiRetry } from '../utils/apiErrorHandling';

// This is an example component that previously made a direct API call
// It now uses the new secure API Gateway service.

function OriginalApiConsumer() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        // Replace the direct API call with the secure service method
        // The payload here would be whatever data your original API call needed
        const result = await withApiRetry(() => makeSecureExternalApiCall({ query: 'example', param: 'value' }));
        setData(result);
      } catch (err) {
        const errorMessage = handleApiError(err, 'OriginalApiConsumer');
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading data securely...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;
  if (!data) return <div>No data received.</div>

  return (
    <div>
      <h2>Data from Secure API Call</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default OriginalApiConsumer;
