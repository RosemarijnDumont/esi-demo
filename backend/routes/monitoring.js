
const express = require('express');
const router = express.Router();
const { recordOAuthError, recordClientLog } = require('../services/monitoringService');

// Route for client-side logs
r.post('/api/client-log', (req, res) => {
    const { timestamp, level, component, message, details, userAgent, url } = req.body;
    recordClientLog({ timestamp, level, component, message: JSON.parse(message), details: JSON.parse(details), userAgent, url });
    res.status(200).send('Log received');
});

// Route for OAuth error reporting
r.post('/api/monitoring/oauth-error', (req, res) => {
    const { timestamp, type, error, description, details } = req.body;
    recordOAuthError({ timestamp, type, error, description, details });
    res.status(200).send('OAuth error reported');
});

module.exports = router;
