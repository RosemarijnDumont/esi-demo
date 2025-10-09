import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import OrderForm from '../components/OrderForm';

describe('OrderForm', () => {
  const foodItems = [
    { id: 1, name: 'Pizza', price: 10 },
    { id: 2, name: 'Burger', price: 8 },
  ];
  const locations = ['Office A', 'Office B', 'Office C'];

  it('renders correctly', () => {
    render(<OrderForm foodItems={foodItems} locations={locations} onSubmit={() => {}} />);
    expect(screen.getByText(/food order form/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/select pickup location:/i)).toBeInTheDocument();
    expect(screen.getByText(/pizza/i)).toBeInTheDocument();
    expect(screen.getByText(/burger/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit order/i })).toBeInTheDocument();
  });

  it('allows users to select food items and quantities', () => {
    render(<OrderForm foodItems={foodItems} locations={locations} onSubmit={() => {}} />);
    const pizzaQuantityInput = screen.getByLabelText(/pizza quantity/i);
    fireEvent.change(pizzaQuantityInput, { target: { value: '2' } });
    expect(pizzaQuantityInput.value).toBe('2');

    const burgerQuantityInput = screen.getByLabelText(/burger quantity/i);
    fireEvent.change(burgerQuantityInput, { target: { value: '1' } });
    expect(burgerQuantityInput.value).toBe('1');
  });

  it('allows users to select a pickup location', () => {
    render(<OrderForm foodItems={foodItems} locations={locations} onSubmit={() => {}} />);
    const locationSelect = screen.getByLabelText(/select pickup location:/i);
    fireEvent.change(locationSelect, { target: { value: 'Office B' } });
    expect(locationSelect.value).toBe('Office B');
  });

  it('submits the order with correct data', () => {
    const mockOnSubmit = jest.fn();
    render(<OrderForm foodItems={foodItems} locations={locations} onSubmit={mockOnSubmit} />);

    const pizzaQuantityInput = screen.getByLabelText(/pizza quantity/i);
    fireEvent.change(pizzaQuantityInput, { target: { value: '2' } });

    const locationSelect = screen.getByLabelText(/select pickup location:/i);
    fireEvent.change(locationSelect, { target: { value: 'Office C' } });

    fireEvent.click(screen.getByRole('button', { name: /submit order/i }))

    expect(mockOnSubmit).toHaveBeenCalledWith({
      items: [{ id: 1, quantity: 2 }],
      location: 'Office C',
    });
  });
});