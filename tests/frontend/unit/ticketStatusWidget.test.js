
import React from 'react';
import { render, screen } from '@testing-library/react';
import TicketStatusWidget from '../../../frontend/src/components/TicketStatusWidget';

describe('TicketStatusWidget', () => {
  it('should display the correct ticket status', () => {
    render(<TicketStatusWidget status="Open" />);
    expect(screen.getByText(/Status: Open/i)).toBeInTheDocument();
  });

  it('should display the assigned agent', () => {
    render(<TicketStatusWidget assignedAgent="John Doe" />);
    expect(screen.getByText(/Assigned Agent: John Doe/i)).toBeInTheDocument();
  });

  it('should display the submission date', () => {
    render(<TicketStatusWidget submissionDate="2023-01-01" />);
    expect(screen.getByText(/Submission Date: 2023-01-01/i)).toBeInTheDocument();
  });

  it('should display the last update date', () => {
    render(<TicketStatusWidget lastUpdate="2023-01-05" />);
    expect(screen.getByText(/Last Update: 2023-01-05/i)).toBeInTheDocument();
  });
});
