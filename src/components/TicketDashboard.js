import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TicketDashboard.css';

const TicketDashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [filteredTickets, setFilteredTickets] = useState([]);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [sortCriterion, setSortCriterion] = useState('submissionDate');

  useEffect(() => {
    fetchTickets();
    const interval = setInterval(fetchTickets, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [tickets, filterStatus, sortCriterion]);

  const fetchTickets = async () => {
    try {
      // Replace with your actual API endpoint for fetching user tickets
      const response = await axios.get('/api/user/tickets');
      setTickets(response.data);
    } catch (error) {
      console.error('Error fetching tickets:', error);
    }
  };

  const applyFiltersAndSort = () => {
    let tempTickets = [...tickets];

    // Filter
    if (filterStatus !== 'all') {
      tempTickets = tempTickets.filter(ticket => ticket.status === filterStatus);
    }

    // Sort
    tempTickets.sort((a, b) => {
      if (sortCriterion === 'submissionDate') {
        return new Date(b.submissionDate) - new Date(a.submissionDate);
      } else if (sortCriterion === 'lastUpdate') {
        return new Date(b.lastUpdate) - new Date(a.lastUpdate);
      }
      // Add more sorting criteria as needed
      return 0;
    });

    setFilteredTickets(tempTickets);
  };

  const handleTicketSelect = (ticket) => {
    setSelectedTicket(ticket);
  };

  return (
    <div className="ticket-dashboard">
      <h2>My IT Tickets</h2>

      <div className="controls">
        <div className="filter-sort-group">
          <label htmlFor="status-filter">Filter by Status:</label>
          <select
            id="status-filter"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="all">All</option>
            <option value="open">Open</option>
            <option value="pending">Pending</option>
            <option value="closed">Closed</option>
            {/* Add more status options as per your system */}
          </select>
        </div>

        <div className="filter-sort-group">
          <label htmlFor="sort-by">Sort by:</label>
          <select
            id="sort-by"
            value={sortCriterion}
            onChange={(e) => setSortCriterion(e.target.value)}
          >
            <option value="submissionDate">Submission Date</option>
            <option value="lastUpdate">Last Update</option>
            {/* Add more sorting options as per your system */}
          </select>
        </div>
      </div>

      <div className="ticket-list-detail-container">
        <div className="ticket-list">
          {filteredTickets.length > 0 ? (
            filteredTickets.map((ticket) => (
              <div
                key={ticket.id}
                className={`ticket-item ${selectedTicket && selectedTicket.id === ticket.id ? 'selected' : ''}`}
                onClick={() => handleTicketSelect(ticket)}
              >
                <h3>{ticket.subject}</h3>
                <p>Status: <span className={`status-${ticket.status.toLowerCase()}`}>{ticket.status}</span></p>
                <p>Submitted: {new Date(ticket.submissionDate).toLocaleDateString()}</p>
              </div>
            ))
          ) : (
            <p>No tickets found.</p>
          )}
        </div>

        <div className="ticket-detail">
          {selectedTicket ? (
            <div>
              <h3>Ticket Details: {selectedTicket.subject}</h3>
              <p><strong>ID:</strong> {selectedTicket.id}</p>
              <p><strong>Status:</strong> <span className={`status-${selectedTicket.status.toLowerCase()}`}>{selectedTicket.status}</span></p>
              <p><strong>Description:</strong> {selectedTicket.description}</p>
              <p><strong>Submission Date:</strong> {new Date(selectedTicket.submissionDate).toLocaleString()}</p>
              <p><strong>Last Update:</strong> {new Date(selectedTicket.lastUpdate).toLocaleString()}</p>
              <p><strong>Assigned Agent:</strong> {selectedTicket.assignedAgent || 'N/A'}</p>
              {selectedTicket.priority && <p><strong>Priority:</strong> {selectedTicket.priority}</p>}
              {/* Add more details as needed */}
            </div>
          ) : (
            <p>Select a ticket to view details.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TicketDashboard;