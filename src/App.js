import React from 'react';
import './App.css';
import TicketDashboard from './components/TicketDashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>ServiceDesk Portal</h1>
        {/* You would typically have navigation and user authentication here */}
        <nav>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Knowledge Base</a></li>
            <li><a href="#">Submit New Ticket</a></li>
            <li><a href="#tickets">My Tickets</a></li> {/* Link to the dashboard */}
            <li><a href="#">Profile</a></li>
          </ul>
        </nav>
      </header>
      <main>
        <section id="tickets">
          <TicketDashboard />
        </section>
        {/* Other portal content would go here */}
      </main>
    </div>
  );
}

export default App;