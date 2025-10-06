import { render, screen, fireEvent } from '@testing-library/react';
import FoodOrderForm from '../../components/FoodOrderForm';

describe('FoodOrderForm Unit Tests', () => {
  test('renders form with all fields', () => {
    render(<FoodOrderForm />);
    expect(screen.getByLabelText(/select food items/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/quantity/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pickup location/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit order/i })).toBeInTheDocument();
  });

  test('allows adding multiple food items', () => {
    render(<FoodOrderForm />);
    const addButton = screen.getByRole('button', { name: /add item/i });
    fireEvent.click(addButton);
    // Assuming a new row or input field appears for another item
    expect(screen.getAllByLabelText(/select food items/i).length).toBeGreaterThan(1);
  });

  test('validates required fields on submission', async () => {
    render(<FoodOrderForm />);
    const submitButton = screen.getByRole('button', { name: /submit order/i });
    fireEvent.click(submitButton);
    // Expect validation messages to appear (these will depend on actual implementation)
    expect(await screen.findByText(/food item is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/quantity is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/pickup location is required/i)).toBeInTheDocument();
  });

  test('updates quantity correctly', () => {
    render(<FoodOrderForm />);
    const quantityInput = screen.getByLabelText(/quantity/i);
    fireEvent.change(quantityInput, { target: { value: '2' } });
    expect(quantityInput.value).toBe('2');
  });

  test('updates pickup location correctly', () => {
    render(<FoodOrderForm />);
    const locationSelect = screen.getByLabelText(/pickup location/i);
    fireEvent.change(locationSelect, { target: { value: 'floor-2' } });
    expect(locationSelect.value).toBe('floor-2');
  });
});
