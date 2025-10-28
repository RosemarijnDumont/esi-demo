// frontend/src/App.js
import React, { useEffect } from 'react';
import { initializeTheme, toggleTheme } from './utils/themeManager';
import './styles/global.css'; // Your global styles
import './styles/responsive.css'; // Import the responsive and dark mode styles

function App() {
    useEffect(() => {
        initializeTheme();
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>My Application</h1>
                <button onClick={toggleTheme}>Toggle Theme</button>
            </header>
            {/* Your routing and other components go here */}
            <main>
                <p>Welcome to the application!</p>
                <div className="card">
                    <h2>Dashboard Overview</h2>
                    <p>Some important information...</p>
                </div>
                <button className="btn btn-primary">Action Button</button>
            </main>
        </div>
    );
}

export default App;
