
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TicketFilterSort from '../../../frontend/src/components/TicketFilterSort';

describe('TicketFilterSort', () => {
  it('should call onFilterChange when filter is applied', () => {
    const mockOnFilterChange = jest.fn();
    render(<TicketFilterSort onFilterChange={mockOnFilterChange} onSortChange={() => {}} />);
    const filterSelect = screen.getByLabelText(/Filter by:/i);
    fireEvent.change(filterSelect, { target: { value: 'Open' } });
    expect(mockOnFilterChange).toHaveBeenCalledWith('status', 'Open');
  });

  it('should call onSortChange when sort is applied', () => {
    const mockOnSortChange = jest.fn();
    render(<TicketFilterSort onFilterChange={() => {}} onSortChange={mockOnSortChange} />);
    const sortSelect = screen.getByLabelText(/Sort by:/i);
    fireEvent.change(sortSelect, { target: { value: 'submissionDate' } });
    expect(mockOnSortChange).toHaveBeenCalledWith('submissionDate');
  });
});
