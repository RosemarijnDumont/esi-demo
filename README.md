# Trial SSO Configuration Frontend

This project implements the frontend for configuring Single Sign-On (SSO) for trial accounts. It provides a user interface for trial administrators to:

- Upload Identity Provider (IdP) metadata XML.
- Configure optional attribute mappings.
- Enable or disable SSO for their trial account.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Client-Side Validation](#client-side-validation)
- [Error Handling](#error-handling)
- [Documentation](#documentation)

## Features

- **IdP Metadata XML Upload**: Form field for pasting IdP metadata XML.
- **Attribute Mapping**: Optional input for custom attribute mappings.
- **SSO Toggle**: Button to enable/disable SSO for the trial account.
- **Status Messages**: Clear success and error alerts for user feedback.

## Technologies

- **React**: Frontend JavaScript library.
- **Chakra UI**: Component library for styling.
- **Axios**: Promise-based HTTP client for API requests.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   # or yarn install
   ```

### Running the Application

1. Start the development server:
   ```bash
   npm start
   # or yarn start
   ```
   The application will typically run on `http://localhost:3000`.

2. Ensure your backend API is running and accessible. The `API_BASE_URL` in `SSOConfiguration.js` should point to your backend.
   It is recommended to set `REACT_APP_API_BASE_URL` in a `.env` file:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8080/api # Or your production API URL
   ```

## Project Structure

- `src/
  - `components/SSOConfiguration.js`: Contains the main React component for SSO configuration.
  - `App.js`: Main application component, sets up Chakra UI and includes `SSOConfiguration`.
  - `index.js`: Entry point of the React application.

## API Endpoints

The frontend interacts with the following backend API endpoints:

- `GET /api/trial-sso/config`: Retrieves the current SSO configuration for the trial account.
- `POST /api/trial-sso/config`: Submits or updates the SSO configuration (IdP metadata XML, attribute mappings).
- `PATCH /api/trial-sso/toggle`: Toggles the SSO enabled/disabled status for the trial account.

## Client-Side Validation

- The `IdP Metadata XML` field is checked to ensure it's not empty before submission.

## Error Handling

- API errors are caught and displayed to the user via `Alert` components.
- Specific error messages from the backend are prioritized, otherwise generic fallback messages are used.

## Documentation

- The UI includes a link to external `SSO for Trial Accounts Documentation` (e.g., `/docs/sso-trial`). This documentation should be created and maintained separately to guide users through the SAML setup process.
