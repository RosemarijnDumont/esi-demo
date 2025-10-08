import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import NotificationCenter from './components/NotificationCenter';
import NotificationPreferences from './pages/NotificationPreferences';
import './App.css'; // Assuming you have some global styles here

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav>
            <ul>
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/preferences">Notification Preferences</Link>
              </li>
              <li>
                <NotificationCenter />
              </li>
            </ul>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<h1>Welcome to the Notification Demo!</h1>} />
            <Route path="/preferences" element={<NotificationPreferences />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
