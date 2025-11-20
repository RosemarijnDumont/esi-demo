
import request from 'supertest';
import app from '../../../backend/src/app'; // Assuming your Express app is exported from app.js
import * as ServiceDeskIntegration from '../../../backend/src/integrations/serviceDeskIntegration';

jest.mock('../../../backend/src/integrations/serviceDeskIntegration');

describe('Integration: Full Data Flow', () => {
  it('should fetch tickets from ServiceDesk and provide to frontend correctly', async () => {
    // Mock ServiceDesk response
    ServiceDeskIntegration.fetchTicketsByUserId.mockResolvedValue([
      { id: 'ticket1', status: 'Open', submittedAt: '2023-01-01', updatedAt: '2023-01-05', agent: { name: 'Agent A' } },
      { id: 'ticket2', status: 'Pending', submittedAt: '2023-01-02', updatedAt: '2023-01-06', agent: { name: 'Agent B' } },
    ]);

    // Simulate a request from the frontend to the backend API
    const res = await request(app).get('/api/tickets/userIntegrationTest');

    // Verify backend processed the data and returned it correctly
    expect(res.statusCode).toEqual(200);
    expect(res.body).toEqual([
      {
        id: 'ticket1',
        status: 'Open',
        submissionDate: '2023-01-01',
        lastUpdate: '2023-01-05',
        assignedAgent: 'Agent A',
      },
      {
        id: 'ticket2',
        status: 'Pending',
        submissionDate: '2023-01-02',
        lastUpdate: '2023-01-06',
        assignedAgent: 'Agent B',
      },
    ]);

    // Verify that the ServiceDesk integration was called
    expect(ServiceDeskIntegration.fetchTicketsByUserId).toHaveBeenCalledWith('userIntegrationTest');
  });
});
