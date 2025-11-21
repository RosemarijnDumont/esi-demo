# App-Based MFA Frontend Implementation

This project implements the frontend components for app-based Multi-Factor Authentication (MFA), including enrollment and challenge flows.

## Project Structure

- `frontend/src/components/MFAEnrollment.js`: Handles the display of QR codes for MFA enrollment and manual key entry.
- `frontend/src/components/MFAChallenge.js`: Manages the MFA challenge during login, where users input a token from their authenticator app.
- `frontend/src/App.js`: The main application component that orchestrates the different MFA flows (login, enrollment, challenge).
- `frontend/src/App.css`: Provides basic styling for the application.
- `frontend/src/index.js`: The entry point for the React application.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Running the Application

To start the development server:

```bash
npm start
# or
yarn start
```

The application will typically open in your browser at `http://localhost:3000`.

## Features Implemented

- **MFA Enrollment:** Users can initiate MFA enrollment, receive a QR code to scan with their authenticator app, or manually enter a secret key.
- **MFA Challenge:** During a simulated login, users are prompted to enter a 6-digit code from their authenticator app to complete the authentication process.
- **User Flow Management:** The `App.js` component manages the state transitions between login, MFA enrollment, and MFA challenge.

## Simulated API Interactions

This frontend application simulates interactions with a backend API for:

- **Generating MFA Secret/QR Code:** In `MFAEnrollment.js`, `generateSecret` simulates an API call to get a new secret key and QR code data.
- **Confirming MFA Enrollment:** In `MFAEnrollment.js`, `handleEnrollmentConfirmation` simulates an API call to confirm that the user has successfully set up their authenticator app.
- **Verifying MFA Token:** In `MFAChallenge.js`, the `handleSubmit` function simulates an API call to verify the entered MFA token against the backend.
- **User Login:** In `App.js`, `handleLogin` simulates an initial username/password authentication.

**Note:** For a production environment, these simulated calls should be replaced with actual API integrations to your backend authentication service.

## Future Enhancements

- Integration with a real backend API for MFA secret generation and token verification.
- Implement push notification handling for app-based MFA if the chosen solution supports it.
- Enhance error handling and feedback for users during enrollment and challenge flows.
- Add robust styling and responsiveness for various devices.
- Implement a proper routing solution (e.g., React Router) for managing different application views.
- Add a dedicated page for users to manage their MFA settings (e.g., re-enroll, disable).

