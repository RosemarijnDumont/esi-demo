import React from 'react';
import DataFetcher from './components/DataFetcher';

function App() {
  return (
    <div className="App">
      <h1>Frontend Application</h1>
      <p>This application now routes API requests through a server-side proxy to enhance security.</p>
      {/* Example of a component using the new proxied API call */}
      <DataFetcher endpoint="/external-service/some-resource" />
      {/* Add other components that were making direct API calls here, updated to use src/services/api.js */}
    </div>
  );
}

export default App;