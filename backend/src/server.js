require('dotenv').config();
const express = require('express');
const app = express();
const proxyRoutes = require('./api/routes/proxyRoutes');
const errorHandler = require('./utils/errorHandler');

app.use(express.json()); // Middleware to parse JSON request bodies

app.use('/api/proxy', proxyRoutes); // Mount the proxy routes

app.use(errorHandler); // Centralized error handling

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));