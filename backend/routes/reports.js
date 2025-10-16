const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const db = require('../config/db');
const NodeCache = require('node-cache');
const appCache = new NodeCache({ stdTTL: 300, checkperiod: 120 }); // Cache for 5 minutes

const executeQuery = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.query(sql, params, (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });
};

// Optimized API response for Reports with filtering and server-side caching
router.get('/', auth, async (req, res) => {
  const { filter } = req.query; // e.g., 'daily', 'weekly', 'monthly', 'quarterly', 'yearly'
  const userId = req.user.id;
  const cacheKey = `reports_${userId}_${filter}`; // Cache per user and filter
  const cachedData = appCache.get(cacheKey);

  if (cachedData) {
    console.log(`Serving reports for filter '${filter}' from cache`);
    return res.json(cachedData);
  }

  let dateInterval;
  switch (filter) {
    case 'daily':
      dateInterval = '1 DAY';
      break;
    case 'weekly':
      dateInterval = '7 DAY';
      break;
    case 'monthly':
      dateInterval = '1 MONTH';
      break;
    case 'quarterly':
      dateInterval = '3 MONTH';
      break;
    case 'yearly':
      dateInterval = '1 YEAR';
      break;
    default:
      dateInterval = '1 MONTH'; // Default to monthly if no valid filter
  }

  try {
    // Example: Optimized query for sales by category
    const salesByCategoryQuery = `
      SELECT c.categoryName as category, SUM(oi.quantity * oi.price) as sales
      FROM OrderItems oi
      JOIN Products p ON oi.productId = p.id
      JOIN Categories c ON p.categoryId = c.id
      JOIN Orders o ON oi.orderId = o.id
      WHERE o.userId = ? AND o.orderDate >= CURDATE() - INTERVAL ${dateInterval}
      GROUP BY c.categoryName
      ORDER BY sales DESC;
    `;

    // Example: Optimized query for regional performance
    const regionalPerformanceQuery = `
      SELECT u.region, SUM(o.totalAmount) as revenue
      FROM Orders o
      JOIN Users u ON o.userId = u.id
      WHERE o.orderDate >= CURDATE() - INTERVAL ${dateInterval}
      GROUP BY u.region
      ORDER BY revenue DESC;
    `;

    const [salesByCategory, regionalPerformance] = await Promise.all([
      executeQuery(salesByCategoryQuery, [userId]),
      executeQuery(regionalPerformanceQuery)
    ]);

    const reportData = {
      salesByCategory,
      regionalPerformance,
    };

    appCache.set(cacheKey, reportData); // Cache the fetched data
    res.json(reportData);

  } catch (err) {
    console.error('Database query error for reports:', err);
    res.status(500).json({ msg: 'Server error', error: err.message });
  }
});

module.exports = router;
