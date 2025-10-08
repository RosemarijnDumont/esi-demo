const request = require('supertest');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

// We need to create a new app instance for testing to isolate it
const createApp = () => {
  const app = express();
  app.use(cors());
  app.use(bodyParser.json());

  let ideas = []; // Reset ideas for each test app instance

  app.post('/api/ideas', (req, res) => {
    const { title, description, contact } = req.body;
    if (!title || !description || !contact) {
      return res.status(400).json({ message: 'All fields are required.' });
    }
    const newIdea = {
      id: ideas.length > 0 ? Math.max(...ideas.map(idea => idea.id)) + 1 : 1,
      title,
      description,
      contact,
      submittedAt: new Date(),
    };
    ideas.push(newIdea);
    res.status(201).json({ message: 'Idea submitted successfully!', idea: newIdea });
  });

  app.get('/api/ideas', (req, res) => {
    res.status(200).json(ideas);
  });

  return app;
};

describe('Backend API /api/ideas', () => {
  let app;

  beforeEach(() => {
    app = createApp(); // Create a fresh app for each test
  });

  test('should return 400 if title is missing', async () => {
    const res = await request(app)
      .post('/api/ideas')
      .send({ description: 'Test Description', contact: 'test@example.com' });
    expect(res.statusCode).toEqual(400);
    expect(res.body.message).toEqual('All fields are required.');
  });

  test('should return 400 if description is missing', async () => {
    const res = await request(app)
      .post('/api/ideas')
      .send({ title: 'Test Title', contact: 'test@example.com' });
    expect(res.statusCode).toEqual(400);
    expect(res.body.message).toEqual('All fields are required.');
  });

  test('should return 400 if contact is missing', async () => {
    const res = await request(app)
      .post('/api/ideas')
      .send({ title: 'Test Title', description: 'Test Description' });
    expect(res.statusCode).toEqual(400);
    expect(res.body.message).toEqual('All fields are required.');
  });

  test('should successfully submit a new idea', async () => {
    const newIdea = {
      title: 'New Idea',
      description: 'This is a brilliant new idea.',
      contact: 'submitter@example.com',
    };
    const res = await request(app)
      .post('/api/ideas')
      .send(newIdea);
    expect(res.statusCode).toEqual(201);
    expect(res.body.message).toEqual('Idea submitted successfully!');
    expect(res.body.idea).toMatchObject(newIdea);
    expect(res.body.idea).toHaveProperty('id');
    expect(res.body.idea).toHaveProperty('submittedAt');

    // Verify it's stored by fetching all ideas
    const getRes = await request(app).get('/api/ideas');
    expect(getRes.statusCode).toEqual(200);
    expect(getRes.body.length).toBe(1);
    expect(getRes.body[0]).toMatchObject(newIdea);
  });

  test('should get all submitted ideas', async () => {
    await request(app)
      .post('/api/ideas')
      .send({ title: 'Idea 1', description: 'Desc 1', contact: 'c1@example.com' });
    await request(app)
      .post('/api/ideas')
      .send({ title: 'Idea 2', description: 'Desc 2', contact: 'c2@example.com' });

    const res = await request(app).get('/api/ideas');
    expect(res.statusCode).toEqual(200);
    expect(res.body.length).toEqual(2);
    expect(res.body[0].title).toEqual('Idea 1');
    expect(res.body[1].title).toEqual('Idea 2');
  });

  test('should handle multiple submissions correctly with auto-incrementing IDs', async () => {
    const idea1 = { title: 'First Idea', description: 'D1', contact: 'a@b.com' };
    const idea2 = { title: 'Second Idea', description: 'D2', contact: 'c@d.com' };

    const res1 = await request(app).post('/api/ideas').send(idea1);
    expect(res1.statusCode).toEqual(201);
    expect(res1.body.idea.id).toEqual(1);

    const res2 = await request(app).post('/api/ideas').send(idea2);
    expect(res2.statusCode).toEqual(201);
    expect(res2.body.idea.id).toEqual(2);

    const getRes = await request(app).get('/api/ideas');
    expect(getRes.body.length).toEqual(2);
  });
});