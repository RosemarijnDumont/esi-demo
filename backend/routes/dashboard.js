const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const db = require('../config/db'); // Assuming a db connection module
const NodeCache = require('node-cache'); // For server-side caching
const appCache = new NodeCache({ stdTTL: 300, checkperiod: 120 }); // Cache for 5 minutes

// Helper to execute SQL queries
const executeQuery = (sql, params = []) => {
  return new Promise((resolve, reject) => {
    db.query(sql, params, (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });
};

// Optimize database queries and API response for Dashboard
router.get('/', auth, async (req, res) => {
  const cacheKey = `dashboard_${req.user.id}`; // Cache per user
  const cachedData = appCache.get(cacheKey);

  if (cachedData) {
    console.log('Serving dashboard data from cache');
    return res.json(cachedData);
  }

  try {
    // Example: Optimized query to fetch daily sales avoiding N+1 problems
    const dailySalesQuery = `
      SELECT DATE(orderDate) as date, SUM(totalAmount) as sales
      FROM Orders
      WHERE userId = ? AND orderDate >= CURDATE() - INTERVAL 30 DAY
      GROUP BY DATE(orderDate)
      ORDER BY date ASC;
    `;

    const productPerformanceQuery = `
      SELECT p.productName, SUM(oi.quantity * oi.price) as revenue
      FROM OrderItems oi
      JOIN Products p ON oi.productId = p.id
      JOIN Orders o ON oi.orderId = o.id
      WHERE o.userId = ? AND o.orderDate >= CURDATE() - INTERVAL 90 DAY
      GROUP BY p.productName
      ORDER BY revenue DESC
      LIMIT 10;
    `;

    const totalRevenueQuery = `
      SELECT SUM(totalAmount) as totalRevenue
      FROM Orders
      WHERE userId = ? AND orderDate >= CURDATE() - INTERVAL 365 DAY;
    `;

    const newCustomersQuery = `
      SELECT COUNT(id) as newCustomers
      FROM Users
      WHERE registrationDate >= CURDATE() - INTERVAL 30 DAY;
    `;
    
    const conversionRateQuery = `
        SELECT 
            (SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as conversionRate
        FROM Orders
        WHERE userId = ? AND orderDate >= CURDATE() - INTERVAL 30 DAY;
    `;

    const userId = req.user.id; // User ID from authenticated token

    const [dailySales, productPerformance, totalRevenueResult, newCustomersResult, conversionRateResult] = await Promise.all([
      executeQuery(dailySalesQuery, [userId]),
      executeQuery(productPerformanceQuery, [userId]),
      executeQuery(totalRevenueQuery, [userId]),
      executeQuery(newCustomersQuery),
      executeQuery(conversionRateQuery, [userId])
    ]);

    const dashboardData = {
      dailySales,
      productPerformance,
      totalRevenue: totalRevenueResult[0]?.totalRevenue || 0,
      newCustomers: newCustomersResult[0]?.newCustomers || 0,
      conversionRate: conversionRateResult[0]?.conversionRate || 0
    };

    appCache.set(cacheKey, dashboardData); // Cache the fetched data
    res.json(dashboardData);

  } catch (err) {
    console.error('Database query error for dashboard:', err);
    res.status(500).json({ msg: 'Server error', error: err.message });
  }
});

module.exports = router;
