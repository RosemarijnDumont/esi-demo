
import { getTicketsByUserId, getTicketDetails } from '../../../backend/src/services/ticketService';
import * as ServiceDeskIntegration from '../../../backend/src/integrations/serviceDeskIntegration';

jest.mock('../../../backend/src/integrations/serviceDeskIntegration');

describe('getTicketsByUserId', () => {
  it('should return formatted tickets from ServiceDesk', async () => {
    ServiceDeskIntegration.fetchTicketsByUserId.mockResolvedValue([
      { id: '1', status: 'OPEN', submittedAt: '2023-01-01', updatedAt: '2023-01-05', agent: { name: 'Agent Smith' } },
    ]);

    const tickets = await getTicketsByUserId('user123');
    expect(tickets).toEqual([
      {
        id: '1',
        status: 'Open',
        submissionDate: '2023-01-01',
        lastUpdate: '2023-01-05',
        assignedAgent: 'Agent Smith',
      },
    ]);
  });

  it('should handle no tickets gracefully', async () => {
    ServiceDeskIntegration.fetchTicketsByUserId.mockResolvedValue([]);
    const tickets = await getTicketsByUserId('user123');
    expect(tickets).toEqual([]);
  });
});

describe('getTicketDetails', () => {
  it('should return formatted ticket details from ServiceDesk', async () => {
    ServiceDeskIntegration.fetchTicketDetailsById.mockResolvedValue({
      id: '1', status: 'OPEN', subject: 'My Issue', description: 'Details here',
      submittedAt: '2023-01-01', updatedAt: '2023-01-05', agent: { name: 'Agent Smith' }
    });

    const ticket = await getTicketDetails('1');
    expect(ticket).toEqual({
      id: '1',
      status: 'Open',
      subject: 'My Issue',
      description: 'Details here',
      submissionDate: '2023-01-01',
      lastUpdate: '2023-01-05',
      assignedAgent: 'Agent Smith',
    });
  });

  it('should return null if ticket not found', async () => {
    ServiceDeskIntegration.fetchTicketDetailsById.mockResolvedValue(null);
    const ticket = await getTicketDetails('999');
    expect(ticket).toBeNull();
  });
});
