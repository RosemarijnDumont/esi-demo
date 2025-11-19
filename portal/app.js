import React, { useState, useEffect, createContext, useContext } from 'react';
import ReactDOM from 'react-dom/client';

// 1. Authentication Context
const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null); // {username: '...', role: 'user'/'admin'}

    // Simulate login
    const login = (username, password) => {
        // In a real app, this would be an API call to authenticate
        if (username === 'admin' && password === 'admin') {
            setUser({ username: 'admin', role: 'admin' });
            return true;
        } else if (username === 'user' && password === 'user') {
            setUser({ username: 'user', role: 'user' });
            return true;
        }
        return false;
    };

    // Simulate logout
    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

const useAuth = () => useContext(AuthContext);

// Mock API functions
const mockApi = {
    fetchSoftware: async () => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    { id: 1, name: 'VS Code', version: '1.85', description: 'Code editor', approved: true },
                    { id: 2, name: 'Docker Desktop', version: '4.26', description: 'Containerization platform', approved: true },
                    { id: 3, name: 'Slack', version: '4.35', description: 'Communication tool', approved: true },
                    { id: 4, name: 'Zoom', version: '5.17', description: 'Video conferencing', approved: false },
                ]);
            }, 500);
        });
    },
    requestInstallation: async (softwareId, userId) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const software = mockSoftware.find(s => s.id === softwareId);
                if (software && software.approved) {
                    console.log(`User ${userId} requested installation of ${software.name}`);
                    // Simulate a successful installation request
                    resolve({ success: true, message: `Installation request for ${software.name} submitted successfully.` });
                } else if (software && !software.approved) {
                    reject({ success: false, message: `${software.name} is not approved for self-service installation.` });
                } else {
                    reject({ success: false, message: 'Software not found.' });
                }
            }, 1000);
        });
    },
    addSoftware: async (newSoftware) => {
        return new Promise(resolve => {
            setTimeout(() => {
                const id = Math.max(...mockSoftware.map(s => s.id)) + 1;
                const softwareWithId = { ...newSoftware, id, approved: false }; // New software is initially not approved
                mockSoftware.push(softwareWithId);
                resolve({ success: true, software: softwareWithId });
            }, 500);
        });
    },
    updateSoftware: async (updatedSoftware) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const index = mockSoftware.findIndex(s => s.id === updatedSoftware.id);
                if (index !== -1) {
                    mockSoftware[index] = { ...mockSoftware[index], ...updatedSoftware };
                    resolve({ success: true, software: mockSoftware[index] });
                } else {
                    reject({ success: false, message: 'Software not found.' });
                }
            }, 500);
        });
    },
    deleteSoftware: async (softwareId) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                const initialLength = mockSoftware.length;
                mockSoftware = mockSoftware.filter(s => s.id !== softwareId);
                if (mockSoftware.length < initialLength) {
                    resolve({ success: true, message: 'Software deleted successfully.' });
                } else {
                    reject({ success: false, message: 'Software not found.' });
                }
            }, 500);
        });
    }
};

let mockSoftware = [
    { id: 1, name: 'VS Code', version: '1.85', description: 'Code editor', approved: true },
    { id: 2, name: 'Docker Desktop', version: '4.26', description: 'Containerization platform', approved: true },
    { id: 3, name: 'Slack', version: '4.35', description: 'Communication tool', approved: true },
    { id: 4, name: 'Zoom', version: '5.17', description: 'Video conferencing', approved: false },
];

// 2. Components
const SoftwareCatalog = () => {
    const [softwareList, setSoftwareList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState(null);
    const { user } = useAuth();

    useEffect(() => {
        const fetchSoftware = async () => {
            const data = await mockApi.fetchSoftware();
            setSoftwareList(data);
            setLoading(false);
        };
        fetchSoftware();
    }, []);

    const handleInstallRequest = async (softwareId) => {
        if (!user) {
            setMessage({ type: 'error', text: 'Please log in to request installations.' });
            return;
        }
        try {
            const response = await mockApi.requestInstallation(softwareId, user.username);
            setMessage({ type: 'success', text: response.message });
        } catch (error) {
            setMessage({ type: 'error', text: error.message });
        }
    };

    if (loading) return <div>Loading software catalog...</div>;

    const approvedSoftware = softwareList.filter(s => s.approved);

    return (
        <div>
            <h2>Available Software</h2>
            {message && <div className={`status-message ${message.type}`}>{message.text}</div>}
            <div className="software-list">
                {approvedSoftware.length > 0 ? (
                    approvedSoftware.map(software => (
                        <div key={software.id} className="software-item">
                            <h3>{software.name}</h3>
                            <p>Version: {software.version}</p>
                            <p>{software.description}</p>
                            <button onClick={() => handleInstallRequest(software.id)}>Request Installation</button>
                        </div>
                    ))
                ) : (
                    <p>No approved software available.</p>
                )}
            </div>
        </div>
    );
};

const AdminSoftwareManagement = () => {
    const [softwareList, setSoftwareList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState(null);
    const [showAddModal, setShowAddModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [currentSoftware, setCurrentSoftware] = useState(null);

    const fetchSoftwareData = async () => {
        const data = await mockApi.fetchSoftware();
        setSoftwareList(data);
        setLoading(false);
    };

    useEffect(() => {
        fetchSoftwareData();
    }, []);

    const handleAddSoftware = async (newSoftware) => {
        try {
            const response = await mockApi.addSoftware(newSoftware);
            if (response.success) {
                setMessage({ type: 'success', text: `${response.software.name} added successfully.` });
                fetchSoftwareData(); // Refresh the list
                setShowAddModal(false);
            }
        } catch (error) {
            setMessage({ type: 'error', text: error.message });
        }
    };

    const handleUpdateSoftware = async (updatedSoftware) => {
        try {
            const response = await mockApi.updateSoftware(updatedSoftware);
            if (response.success) {
                setMessage({ type: 'success', text: `${response.software.name} updated successfully.` });
                fetchSoftwareData(); // Refresh the list
                setShowEditModal(false);
            }
        } catch (error) {
            setMessage({ type: 'error', text: error.message });
        }
    };

    const handleDeleteSoftware = async (softwareId) => {
        if (window.confirm('Are you sure you want to delete this software?')) {
            try {
                const response = await mockApi.deleteSoftware(softwareId);
                if (response.success) {
                    setMessage({ type: 'success', text: response.message });
                    fetchSoftwareData(); // Refresh the list
                }
            } catch (error) {
                setMessage({ type: 'error', text: error.message });
            }
        }
    };

    const openEditModal = (software) => {
        setCurrentSoftware(software);
        setShowEditModal(true);
    };

    if (loading) return <div>Loading software for administration...</div>;

    return (
        <div>
            <h2>Software Management (Admin)</h2>
            <button onClick={() => setShowAddModal(true)}>Add New Software</button>
            {message && <div className={`status-message ${message.type}`}>{message.text}</div>}
            <div className="admin-software-list">
                {softwareList.length > 0 ? (
                    softwareList.map(software => (
                        <div key={software.id} className="admin-software-item">
                            <h3>{software.name}</h3>
                            <p>Version: {software.version}</p>
                            <p>{software.description}</p>
                            <p>Approved: {software.approved ? 'Yes' : 'No'}</p>
                            <div className="admin-actions">
                                <button onClick={() => openEditModal(software)}>Edit</button>
                                <button onClick={() => handleDeleteSoftware(software.id)}>Delete</button>
                            </div>
                        </div>
                    ))
                ) : (
                    <p>No software configured.</p>
                )}
            </div>

            {showAddModal && (
                <Modal onClose={() => setShowAddModal(false)} title="Add New Software">
                    <SoftwareForm onSubmit={handleAddSoftware} />
                </Modal>
            )}

            {showEditModal && currentSoftware && (
                <Modal onClose={() => setShowEditModal(false)} title="Edit Software">
                    <SoftwareForm onSubmit={handleUpdateSoftware} initialData={currentSoftware} isEdit={true} />
                </Modal>
            )}
        </div>
    );
};

const SoftwareForm = ({ onSubmit, initialData = {}, isEdit = false }) => {
    const [name, setName] = useState(initialData.name || '');
    const [version, setVersion] = useState(initialData.version || '');
    const [description, setDescription] = useState(initialData.description || '');
    const [approved, setApproved] = useState(initialData.approved || false);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            id: initialData.id, // Only present for edits
            name,
            version,
            description,
            approved
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label>Name:</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div className="form-group">
                <label>Version:</label>
                <input type="text" value={version} onChange={(e) => setVersion(e.target.value)} required />
            </div>
            <div className="form-group">
                <label>Description:</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} required></textarea>
            </div>
            {isEdit && ( // Only allow changing approval status during edit
                <div className="form-group">
                    <label>
                        <input type="checkbox" checked={approved} onChange={(e) => setApproved(e.target.checked)} />
                        Approved
                    </label>
                </div>
            )}
            <button type="submit">{isEdit ? 'Update Software' : 'Add Software'}</button>
        </form>
    );
};

const Modal = ({ onClose, title, children }) => {
    return (
        <div className="modal">
            <div className="modal-content">
                <span className="close-button" onClick={onClose}>&times;</span>
                <h2>{title}</h2>
                {children}
            </div>
        </div>
    );
};

const Login = ({ onLoginSuccess }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');
        if (login(username, password)) {
            onLoginSuccess();
        } else {
            setError('Invalid username or password');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit">Login</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

const PortalApp = () => {
    const { user, logout } = useAuth();
    const [currentPage, setCurrentPage] = useState('catalog'); // 'catalog', 'admin'

    const handleLoginSuccess = () => {
        if (user && user.role === 'admin') {
            setCurrentPage('admin');
        } else {
            setCurrentPage('catalog');
        }
    };

    return (
        <div id="app">
            <nav className="navbar">
                <div>
                    <a href="#" onClick={() => setCurrentPage('catalog')}>Software Catalog</a>
                    {user && user.role === 'admin' && (
                        <a href="#" onClick={() => setCurrentPage('admin')}>Admin Dashboard</a>
                    )}
                </div>
                <div className="auth-buttons">
                    {user ? (
                        <>
                            <span>Welcome, {user.username} ({user.role})</span>
                            <button onClick={logout}>Logout</button>
                        </>
                    ) : (
                        <button onClick={() => setCurrentPage('login')}>Login</button>
                    )}
                </div>
            </nav>

            {currentPage === 'catalog' && <SoftwareCatalog />}
            {currentPage === 'admin' && user && user.role === 'admin' && <AdminSoftwareManagement />}
            {currentPage === 'login' && !user && <Login onLoginSuccess={handleLoginSuccess} />}
            {currentPage === 'admin' && (!user || user.role !== 'admin') && <div>Access Denied. Please log in as an administrator.</div>}
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(
    <React.StrictMode>
        <AuthProvider>
            <PortalApp />
        </AuthProvider>
    </React.StrictMode>
);
