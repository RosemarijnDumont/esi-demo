# SSO for Trial Accounts

## Overview
This document outlines the functionality and configuration for enabling Single Sign-On (SSO) for trial accounts. Previously, SSO was only available for paid plans. This feature extends SSO capabilities to trial users, allowing them to evaluate the product more effectively with their existing identity providers.

## Features
- **SAML 2.0 Support**: Trial accounts can now configure SAML 2.0 based SSO.
- **Admin Configuration**: Trial account administrators can configure SSO settings via the provided API endpoints.
- **Seamless Authentication**: Trial users can authenticate via their organization's Identity Provider (IdP) after SSO is configured.

## Configuration Guide

### Prerequisites
- A trial account must exist in the system.
- Access to the Identity Service API.

### API Endpoints

#### 1. Configure SAML SSO for a Trial Account
Enables and configures SAML SSO for a specified trial account.

- **Endpoint**: `POST /api/trial-accounts/{accountId}/sso`
- **Request Body Example**:
  ```json
  {
    "idpMetadataUrl": "https://idp.example.com/saml/metadata",
    "entityId": "https://sp.example.com/saml/metadata",
    "acsUrl": "https://sp.example.com/saml/acs"
  }
  ```
- **Success Response**: `200 OK`
- **Error Responses**:
    - `404 Not Found`: If the `accountId` does not exist.
    - `500 Internal Server Error`: If there's an error in SAML configuration (e.g., invalid metadata).

#### 2. Get SAML SSO Configuration for a Trial Account
Retrieves the current SAML SSO configuration for a specified trial account.

- **Endpoint**: `GET /api/trial-accounts/{accountId}/sso`
- **Success Response**: `200 OK` with SAMLConfig object in body.
  ```json
  {
    "idpMetadataUrl": "https://idp.example.com/saml/metadata",
    "entityId": "https://sp.example.com/saml/metadata",
    "acsUrl": "https://sp.example.com/saml/acs"
  }
  ```
- **Error Response**: `404 Not Found`: If the `accountId` does not exist or SSO is not configured.

#### 3. Check SSO Enabled Status for a Trial Account
Checks if SSO is enabled for a specified trial account.

- **Endpoint**: `GET /api/trial-accounts/{accountId}/sso/enabled`
- **Success Response**: `200 OK` with a boolean value in the body (`true` if enabled, `false` otherwise).

## Security Considerations
- All API endpoints are secured and require appropriate authentication and authorization.
- SAML configurations are stored securely.
- Input validation is performed on all incoming SSO configuration data.
- Proper error handling and logging are implemented for all SSO-related operations to detect and respond to potential security incidents.

## Future Enhancements
- Support for additional SSO protocols (e.g., OpenID Connect).
- UI for configuring SSO settings for trial accounts.
- Automated testing for SAML integrations.
