# Enabling SAML SSO for Trial Accounts

## Overview

This document outlines the process for configuring and managing SAML Single Sign-On (SSO) for trial accounts. Previously, SSO was restricted to paid plans. This feature allows enterprise trial prospects to evaluate the product with SSO enabled, thereby reducing friction in the sales cycle and accelerating conversions.

## Prerequisites

*   Access to the SSO Core Service API (e.g., via a sales/support internal tool or direct API calls).
*   Understanding of SAML 2.0 concepts (Identity Provider, Service Provider, Entity ID, SSO URL, X.509 Certificate).
*   The trial account must exist in the system.

## Configuration Steps

To enable SAML SSO for a trial account, follow these steps:

### 1. Gather Identity Provider (IdP) Details from the Prospect

Obtain the following information from the trial prospect's Identity Provider:

*   **IdP Entity ID (Issuer URL):** A unique identifier for the Identity Provider.
*   **IdP SSO URL (SAML 2.0 Endpoint):** The URL where authentication requests are sent.
*   **IdP X.509 Certificate:** The public key certificate used by the IdP to sign SAML assertions.
    *   **Important:** Ensure the certificate is provided in PEM format.

### 2. Provide Service Provider (SP) Metadata to the Prospect

Before configuring SSO on our side, the prospect will likely need our Service Provider (SP) metadata to configure their IdP. Our system can generate this dynamically:

*   **SP Entity ID:** `http://your-service.com/saml/metadata/<account_id>`
*   **SP Assertion Consumer Service (ACS) URL:** `http://your-service.com/saml/acs/<account_id>`

These URLs can be retrieved for a given `account_id` via the `/api/v1/sso/saml/metadata?account_id=<account_id>` endpoint (GET request), which returns the full XML metadata.

### 3. Create/Update SAML Configuration via API

Using the IdP details gathered in Step 1, create or update the SAML configuration for the trial account.

**Endpoint:** `POST /api/v1/sso/saml/config` (To create)
**Endpoint:** `PUT /api/v1/sso/saml/config` (To update existing)

**Headers:**
*   `Content-Type: application/json`
*   `X-Account-Id: <trial_account_id>` (This header is used for authorization and to identify the account)

**Request Body (JSON):**

```json
{
    "idp_entity_id": "<IdP Entity ID from prospect>",
    "idp_sso_url": "<IdP SSO URL from prospect>",
    "idp_x509_cert": "<IdP X.509 Certificate content - PEM format>"
}
```

*   **Note:** The `sp_entity_id` and `sp_acs_url` can optionally be provided if custom values are needed, but the system will generate defaults if not provided.

**Example API Call (using `curl` for creation):**

```bash
curl -X POST \
  http://localhost:5001/api/v1/sso/saml/config \
  -H 'Content-Type: application/json' \
  -H 'X-Account-Id: trial_acc_123' \
  -d '{{
    "idp_entity_id": "http://mock-idp.com/entityid",
    "idp_sso_url": "http://mock-idp.com/sso",
    "idp_x509_cert": "-----BEGIN CERTIFICATE-----\nMIIDDDCCAfSgAwIBAgIUdGhpcyBpcyBhIG1vY2sgY2VydGlmaWNhdGU=\n-----END CERTIFICATE-----"
  }}'
```

**Expected Response (201 Created/200 OK):**

```json
{
    "account_id": "trial_acc_123",
    "idp_entity_id": "http://mock-idp.com/entityid",
    "idp_sso_url": "http://mock-idp.com/sso",
    "idp_x509_cert": "-----BEGIN CERTIFICATE-----\nMIIDDDCCAfSgAwIBAgIUdGhpcyBpcyBhIG1vY2sgY2VydGlmaWNhdGU=\n-----END CERTIFICATE-----",
    "sp_acs_url": "http://your-service.com/saml/acs/trial_acc_123",
    "sp_entity_id": "http://your-service.com/saml/metadata/trial_acc_123",
    "id": null
}
```

### 4. Verify SSO Authentication

Once the configuration is saved, trial users associated with the `trial_acc_123` account should be able to log in via their Identity Provider, which will redirect them to `http://your-service.com/saml/acs/trial_acc_123` with a SAML response.

**Internal Testing:**

Simulate an IdP-initiated login flow by sending a SAML response to the ACS URL. (This typically requires a SAML developer tool or a simple script).

### Deleting SAML Configuration

To remove a SAML configuration for a trial account:

**Endpoint:** `DELETE /api/v1/sso/saml/config`

**Headers:**
*   `X-Account-Id: <trial_account_id>`

**Example API Call:**

```bash
curl -X DELETE \
  http://localhost:5001/api/v1/sso/saml/config \
  -H 'X-Account-Id: trial_acc_123'
```

**Expected Response (204 No Content):** (No body content expected for a successful delete)

## Logging and Error Handling

*   Successful SSO configuration events and updates are logged at `INFO` level.
*   Errors during configuration (e.g., invalid data, account not found) result in `400 Bad Request`.
*   Authorization failures result in `401 Unauthorized` or `403 Forbidden`.
*   Unexpected server errors are logged at `ERROR` level and return `500 Internal Server Error`.
*   Specific error messages are provided for troubleshooting.

## Security Considerations

*   The IdP X.509 Certificate should be stored securely, ideally encrypted at rest in a production database.
*   All API endpoints are protected by authentication and role-based authorization.
*   Ensure that the SAML integration library handles message signing, encryption, and replay attacks properly.
*   This implementation does not degrade performance or security for existing paid SSO customers as the core logic is shared, with an added authorization check for `AccountType.TRIAL`.

## Cost Implications

This backend implementation itself has minimal direct cost implications. The primary costs associated with enabling SSO for trial accounts would be:

*   **Support/Sales Overhead:** Time spent by internal teams assisting with configuration.
*   **SAML Library Licensing (if applicable):** If a commercial SAML library is used, trial accounts may count towards usage metrics.
*   **Increased Network Traffic:** Minor increase due to more SAML authentication flows. (Negligible for typical trial volumes).
*   **Database Storage:** Minimal increase for storing trial account SAML configurations.

These costs are expected to be offset by the increased conversion rates of enterprise prospects.

## Future Enhancements

*   Dedicated UI for sales/support to manage SSO configurations.
*   Automated provisioning/de-provisioning of users via SAML.
*   Support for additional SSO protocols (e.g., OIDC).
*   More granular attribute mapping configuration.
