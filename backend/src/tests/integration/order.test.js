const request = require('supertest');
const app = require('../../app'); // Assuming your express app is exported from app.js
const Order = require('../../models/Order'); // Assuming an Order model
const mongoose = require('mongoose');

describe('Order API Integration Tests', () => {
  beforeAll(async () => {
    // Connect to a test database
    await mongoose.connect(process.env.MONGO_URI_TEST, { useNewUrlParser: true, useUnifiedTopology: true });
  });

  afterEach(async () => {
    // Clean up the database after each test
    await Order.deleteMany();
  });

  afterAll(async () => {
    // Disconnect from the test database
    await mongoose.connection.close();
  });

  test('POST /api/orders should create a new order', async () => {
    const newOrder = {
      items: [{ foodItem: 'Pizza', quantity: 1 }],
      pickupLocation: 'floor-3',
      userId: 'testUser123'
    };
    const response = await request(app)
      .post('/api/orders')
      .send(newOrder)
      .expect(201);

    expect(response.body).toHaveProperty('_id');
    expect(response.body.items[0].foodItem).toBe('Pizza');
    expect(response.body.pickupLocation).toBe('floor-3');

    const orderInDb = await Order.findById(response.body._id);
    expect(orderInDb).not.toBeNull();
    expect(orderInDb.items[0].foodItem).toBe('Pizza');
  });

  test('POST /api/orders should return 400 for invalid data', async () => {
    const invalidOrder = {
      items: [], // Empty items array
      pickupLocation: '',
      userId: 'testUser123'
    };
    await request(app)
      .post('/api/orders')
      .send(invalidOrder)
      .expect(400);
  });

  test('GET /api/orders should retrieve all orders', async () => {
    await Order.create({ items: [{ foodItem: 'Burger', quantity: 1 }], pickupLocation: 'floor-1', userId: 'user1' });
    await Order.create({ items: [{ foodItem: 'Salad', quantity: 2 }], pickupLocation: 'floor-2', userId: 'user2' });

    const response = await request(app)
      .get('/api/orders')
      .expect(200);

    expect(response.body.length).toBe(2);
    expect(response.body[0].items[0].foodItem).toBe('Burger');
  });

  test('GET /api/orders/:id should retrieve a single order', async () => {
    const order = await Order.create({ items: [{ foodItem: 'Pasta', quantity: 1 }], pickupLocation: 'floor-manager', userId: 'user3' });

    const response = await request(app)
      .get(`/api/orders/${order._id}`)
      .expect(200);

    expect(response.body.items[0].foodItem).toBe('Pasta');
  });
});
