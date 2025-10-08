import React from 'react';
import './App.css'; // Assuming you have a global App.css or similar
import IdeaSubmissionForm from './components/IdeaSubmissionForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Intranet Portal</h1>
        <nav>
          <ul>
            <li><a href="#">Home</a></li>
            {/* Link to the idea submission form */}
            <li><a href="/submit-idea">Submit Idea</a></li>
            <li><a href="#">Announcements</a></li>
            <li><a href="#">Documents</a></li>
          </ul>
        </nav>
      </header>
      <main>
        {/* Example of how to integrate the form within your routing system */}
        {/* For a simple example, we can render it directly or use a basic conditional render */}
        {window.location.pathname === '/submit-idea' ? (
          <IdeaSubmissionForm />
        ) : (
          <div>
            <h2>Welcome to the Intranet!</h2>
            <p>This is your central hub for company information and resources.</p>
            {/* Other intranet content */}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;