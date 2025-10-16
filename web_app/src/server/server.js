const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

const clients = new Map(); // Store userId -> WebSocket

app.use(express.json());

app.post('/api/data', (req, res) => {
  const { userId, data } = req.body;
  // Process data and save to database
  console.log(`Received data for userId ${userId}:`, data);

  // Push update to connected web client
  const ws = clients.get(userId);
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'DATA_UPDATE', payload: data }));
  }
  res.status(200).send({ message: 'Data received and synchronized' });
});

wss.on('connection', (ws, req) => {
  const userId = new URLSearchParams(req.url.split('?')[1]).get('userId');
  if (userId) {
    clients.set(userId, ws);
    console.log(`WebSocket client connected for userId: ${userId}`);
  }

  ws.on('message', message => {
    console.log(`Received message: ${message}`);
    // Handle messages from client if needed
  });

  ws.on('close', () => {
    if (userId) {
      clients.delete(userId);
      console.log(`WebSocket client disconnected for userId: ${userId}`);
    }
  });

  ws.on('error', error => {
    console.error(`WebSocket error for userId ${userId}:`, error);
  });
});

const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
