import React from 'react';
import IdeaSubmissionForm from './components/IdeaSubmissionForm';
import './App.css'; // Assuming you have some basic styling

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Intranet Idea Hub</h1>
      </header>
      <main>
        <IdeaSubmissionForm />
      </main>
    </div>
  );
}

export default App;