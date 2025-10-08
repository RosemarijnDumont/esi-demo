import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import IdeaSubmissionForm from './IdeaSubmissionForm';

// Mock the fetch API
global.fetch = jest.fn();

describe('IdeaSubmissionForm', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders the form with all fields', () => {
    render(<IdeaSubmissionForm />);
    expect(screen.getByLabelText(/Idea Title:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description:/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Your Contact Info:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit Idea/i })).toBeInTheDocument();
  });

  test('shows validation error if fields are empty on submit', async () => {
    render(<IdeaSubmissionForm />);
    fireEvent.click(screen.getByRole('button', { name: /Submit Idea/i }));
    expect(await screen.findByText(/Please fill in all fields./i)).toBeInTheDocument();
    expect(fetch).not.toHaveBeenCalled();
  });

  test('submits the form successfully', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ message: 'Idea submitted successfully!' }),
    });

    render(<IdeaSubmissionForm />);

    fireEvent.change(screen.getByLabelText(/Idea Title:/i), { target: { value: 'New Feature Idea' } });
    fireEvent.change(screen.getByLabelText(/Description:/i), { target: { value: 'Implement dark mode.' } });
    fireEvent.change(screen.getByLabelText(/Your Contact Info:/i), { target: { value: 'test@example.com' } });

    fireEvent.click(screen.getByRole('button', { name: /Submit Idea/i }));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith('/api/ideas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'New Feature Idea',
          description: 'Implement dark mode.',
          contact: 'test@example.com',
        }),
      });
    });

    expect(await screen.findByText(/Idea submitted successfully!/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Idea Title:/i)).toHaveValue('');
    expect(screen.getByLabelText(/Description:/i)).toHaveValue('');
    expect(screen.getByLabelText(/Your Contact Info:/i)).toHaveValue('');
  });

  test('shows error message on submission failure', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: () => Promise.resolve({ message: 'Submission failed unexpectedly.' }),
    });

    render(<IdeaSubmissionForm />);

    fireEvent.change(screen.getByLabelText(/Idea Title:/i), { target: { value: 'Failing Idea' } });
    fireEvent.change(screen.getByLabelText(/Description:/i), { target: { value: 'This should fail.' } });
    fireEvent.change(screen.getByLabelText(/Your Contact Info:/i), { target: { value: 'fail@example.com' } });

    fireEvent.click(screen.getByRole('button', { name: /Submit Idea/i }));

    expect(await screen.findByText(/Submission failed unexpectedly./i)).toBeInTheDocument();
  });

  test('shows network error message on fetch exception', async () => {
    fetch.mockImplementationOnce(() => Promise.reject(new Error('Network Down')));

    render(<IdeaSubmissionForm />);

    fireEvent.change(screen.getByLabelText(/Idea Title:/i), { target: { value: 'Network Problem' } });
    fireEvent.change(screen.getByLabelText(/Description:/i), { target: { value: 'Simulate network error.' } });
    fireEvent.change(screen.getByLabelText(/Your Contact Info:/i), { target: { value: 'net@example.com' } });

    fireEvent.click(screen.getByRole('button', { name: /Submit Idea/i }));

    expect(await screen.findByText(/Network error. Please try again./i)).toBeInTheDocument();
  });
});