# Self-Service Ticket Status Dashboard API

This API provides secure endpoints for authenticated users to retrieve real-time IT ticket data.

## Endpoints

- `GET /tickets`: Retrieve all open tickets for the authenticated user.
- `GET /tickets/{ticket_id}`: Retrieve details for a specific ticket.

## Authentication

All endpoints require authentication. Use a valid JWT token in the `Authorization` header (`Bearer <token>`).

## Data Model

### Ticket

```json
{
  "ticket_id": "string",
  "subject": "string",
  "status": "string",
  "submission_date": "datetime",
  "last_update": "datetime",
  "assigned_agent": "string"
}
```
