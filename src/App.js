import React from 'react';
import './App.css';
import OriginalApiConsumer from './components/OriginalApiConsumer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Frontend Application</h1>
        <p>API requests are now routed securely through the server.</p>
      </header>
      <main>
        <OriginalApiConsumer />
        {/* You would integrate other components that consume APIs here */}
      </main>
    </div>
  );
}

export default App;
