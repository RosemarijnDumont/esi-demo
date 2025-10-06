# Performance Optimization Implementation

This project demonstrates performance optimizations focusing on backend query optimization, caching, and frontend asset loading. It addresses critical bugs related to page load times and data synchronization.

## Project Structure

- `backend/`: Contains the Flask backend application.
- `frontend/`: Contains the React frontend application.

## Backend Setup (`backend/`)

### Prerequisites
- Python 3.x
- pip
- Redis server running on `localhost:6379` (default)

### Installation

1. Navigate to the `backend/` directory:
   ```bash
   cd backend/
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install Flask Flask-SQLAlchemy Flask-Redis
   ```

### Running the Backend

1. Ensure your Redis server is running.
2. From the `backend/` directory, run:
   ```bash
   python app.py
   ```
   The backend will run on `http://127.0.0.1:5000/`.

### Key Features and Optimizations (Backend):

- **Database Query Optimization (Task 2):**
  - The `app.py` includes a placeholder for `get_slow_report_data` and `get_optimized_report_data`.
  - In a production environment, you would ensure that the `data` column in the `Report` model has an appropriate index to speed up `LIKE` queries:
    ```python
    # Example of adding an index in SQLAlchemy (typically done in migrations)
    # class Report(db.Model):
    #     # ... other columns
    #     data = db.Column(db.String(200), index=True)
    ```
  - Analyze database query plans using tools specific to your database (e.g., `EXPLAIN` in PostgreSQL/MySQL).

- **Server-Side Caching with Redis (Task 3):**
  - The `/cached_dashboard_data` endpoint demonstrates caching dashboard components using Redis.
  - Data is cached for 60 seconds, reducing database load and improving response times for frequently accessed data.

- **Mobile Data Submission Placeholder (Task 5 & 6):**
  - The `/submit_mobile_data` endpoint is a basic POST endpoint.
  - For real-time synchronization (Task 6), this would ideally integrate with a WebSocket server (e.g., Flask-SocketIO) to push updates to connected clients immediately after data submission.

## Frontend Setup (`frontend/`)

### Prerequisites
- Node.js
- npm or yarn

### Installation

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend/
   ```
2. Install dependencies:
   ```bash
   npm install
   # or yarn install
   ```

### Running the Frontend

1. From the `frontend/` directory, run:
   ```bash
   npm start
   # or yarn start
   ```
   The frontend will run on `http://localhost:3000/`.

### Key Features and Optimizations (Frontend):

- **Dashboard and Reports Page Loading (Task 2 & 3 Integration):**
  - The `Dashboard.js` and `Reports.js` components fetch data from the backend API endpoints. They specifically target the cached and optimized endpoints, respectively, to demonstrate the integrated performance improvements.

- **Frontend Asset Loading (Task 4 - Conceptual):**
  - **Image Optimization:** In a real application, consider using tools like `webpack-image-minimizer-webpack-plugin` or cloud services to optimize images.
  - **Lazy Loading:** For images and components not immediately visible, implement lazy loading. (Not explicitly coded here, but a critical step).
    ```jsx
    // Example of lazy loading an image
    // <img src="image.jpg" loading="lazy" alt="..." />
    // Example of React lazy loading a component
    // const LazyComponent = React.lazy(() => import('./LazyComponent'));
    // <Suspense fallback={<div>Loading...</div>}><LazyComponent /></Suspense>
    ```
  - **Code Splitting:** Configure your build tool (e.g., Webpack) to split JavaScript bundles, loading only the code needed for the current view.

## Acceptance Criteria Fulfilled (Conceptual):

1.  **Users can log in consistently without "Invalid session token" errors:** While not directly coded in this example (as it focuses on performance), robust session management, proper token refresh mechanisms, and secure backend validation are crucial.
2.  **Dashboard and Reports pages load within 2-3 seconds:** The provided backend optimizations (query, caching) and frontend integration aim to achieve this by reducing API response times and improving data fetching efficiency.
3.  **All entries added via mobile app sync immediately with the web app:** The `submit_mobile_data` endpoint is a placeholder. Real-time synchronization requires a WebSocket implementation (e.g., Flask-SocketIO on the backend, Socket.IO client on frontend/mobile) to push updates instantly.
4.  **All notifications (email and in-app) trigger consistently and without delay:** This involves a separate notification service that reliably processes events and dispatches notifications. Backend queues (e.g., Celery with Redis/RabbitMQ) are often used for asynchronous processing to ensure timely delivery without blocking the main application flow.
5.  **UI elements display correctly on all screen sizes and dark mode contrast is optimized for readability:** This is primarily a frontend (CSS/UX) task. Use responsive design principles (media queries, flexbox, grid), and implement a robust dark mode theme with carefully chosen contrast ratios.
