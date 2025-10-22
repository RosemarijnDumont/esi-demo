
import React from 'react';
import './styles/base.css';
import './styles/components.css';
import './styles/layout.css';
import DarkModeToggle from './components/DarkModeToggle';

function App() {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <nav>
          <ul>
            <li><a href="#dashboard">Dashboard</a></li>
            <li><a href="#reports">Reports</a></li>
            <li><a href="#settings">Settings</a></li>
          </ul>
        </nav>
      </aside>
      <div className="content-area">
        <header className="header">
          <h1>Welcome!</h1>
          <DarkModeToggle />
        </header>
        <main className="main-content container">
          <section className="card">
            <h2>Dashboard Overview</h2>
            <p>This is a an overview of your recent activities. This content should display correctly on all screen sizes and in both light and dark modes.</p>
            <button className="button">View Details</button>
          </section>

          <section className="card">
            <h3>Recent Reports</h3>
            <p>Here are your latest reports. The text here is designed to have sufficient contrast in dark mode.</p>
            <div className="input-field-wrapper">
              <input type="text" className="input-field" placeholder="Search reports..." />
            </div>
          </section>

          <section className="card">
            <h3>Data Display Example</h3>
            <table>
              <thead>
                <tr>
                  <th>Column 1</th>
                  <th>Column 2</th>
                  <th>Column 3</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Data A1</td>
                  <td>Data A2</td>
                  <td>Data A3</td>
                </tr>
                <tr>
                  <td>Data B1</td>
                  <td>Data B2</td>
                  <td>Data B3</td>
                </tr>
              </tbody>
            </table>
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;
