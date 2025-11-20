
import request from 'supertest';
import app from '../../../backend/src/app'; // Assuming your Express app is exported from app.js
import { getTicketsByUserId } from '../../../backend/src/services/ticketService';

jest.mock('../../../backend/src/services/ticketService');

describe('API Performance Tests', () => {
  const TEST_USER_ID = 'perfTestUser';
  const NUM_MOCK_TICKETS = 1000;

  beforeEach(() => {
    // Mock a large number of tickets for performance testing
    const mockTickets = Array.from({ length: NUM_MOCK_TICKETS }, (_, i) => ({
      id: `ticket${i}`,
      status: i % 2 === 0 ? 'Open' : 'Closed',
      submissionDate: `2023-01-${(i % 28) + 1}`,
      lastUpdate: `2023-01-${(i % 28) + 2}`,
      assignedAgent: `Agent ${i % 10}`,
    }));
    getTicketsByUserId.mockResolvedValue(mockTickets);
  });

  it('should respond within an acceptable time under load (getTicketsByUserId)', async () => {
    const startTime = Date.now();
    const res = await request(app).get(`/api/tickets/${TEST_USER_ID}`);
    const endTime = Date.now();

    expect(res.statusCode).toEqual(200);
    // Define an acceptable response time threshold (e.g., 500ms)
    const RESPONSE_TIME_THRESHOLD = 500;
    const responseTime = endTime - startTime;

    console.log(`GET /api/tickets/${TEST_USER_ID} took ${responseTime}ms for ${NUM_MOCK_TICKETS} tickets.`);
    expect(responseTime).toBeLessThan(RESPONSE_TIME_THRESHOLD);
  });

  // You could add more performance tests for different endpoints or scenarios
  // e.g., filtering, sorting, or specific ticket details lookup.

});
