
import request from 'supertest';
import app from '../../../backend/src/app'; // Assuming your Express app is exported from app.js
import { getTicketsByUserId, getTicketDetails } from '../../../backend/src/services/ticketService';

// Mock the ticketService
jest.mock('../../../backend/src/services/ticketService', () => ({
  getTicketsByUserId: jest.fn(),
  getTicketDetails: jest.fn(),
}));

describe('GET /api/tickets/:userId', () => {
  it('should return 200 and tickets for a valid user', async () => {
    const mockTickets = [{ id: '1', status: 'Open' }];
    getTicketsByUserId.mockResolvedValue(mockTickets);

    const res = await request(app).get('/api/tickets/user123');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual(mockTickets);
  });

  it('should return 404 if no tickets found for user', async () => {
    getTicketsByUserId.mockResolvedValue([]); // No tickets found

    const res = await request(app).get('/api/tickets/user456');
    expect(res.statusCode).toEqual(404);
    expect(res.body).toEqual({ message: 'No tickets found for user' });
  });
});

describe('GET /api/ticket/:ticketId', () => {
  it('should return 200 and ticket details for a valid ticket ID', async () => {
    const mockTicketDetails = { id: '1', subject: 'Issue X' };
    getTicketDetails.mockResolvedValue(mockTicketDetails);

    const res = await request(app).get('/api/ticket/1');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual(mockTicketDetails);
  });

  it('should return 404 if ticket is not found', async () => {
    getTicketDetails.mockResolvedValue(null); // Ticket not found

    const res = await request(app).get('/api/ticket/999');
    expect(res.statusCode).toEqual(404);
    expect(res.body).toEqual({ message: 'Ticket not found' });
  });
});
