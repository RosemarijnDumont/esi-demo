const express = require('express');
const router = express.Router();
const axios = require('axios');

const API_KEY = process.env.EXTERNAL_API_KEY; // Stored securely in environment variables

router.post('/secure-data', async (req, res) => {
  try {
    const externalApiResponse = await axios.post('https://external-api.com/data', req.body, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 