import React from 'react';
import ApplicationForm from './components/ApplicationForm';
import './App.css'; // Assuming you have some basic CSS

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Client Onboarding Portal</h1>
      </header>
      <main>
        <ApplicationForm />
      </main>
    </div>
  );
}

export default App;
