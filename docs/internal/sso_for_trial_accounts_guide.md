# SSO for Trial Accounts: Internal Configuration Guide

## Overview
This document outlines the process for sales and support teams to configure Single Sign-On (SSO) for trial accounts. Enabling SSO for trial accounts allows enterprise prospects to evaluate our product with their existing identity providers, streamlining their evaluation process and improving conversion rates.

## Prerequisites
- **Admin Panel Access**: Sales or support team member must have appropriate access to the internal administration panel.
- **Trial Account ID**: The unique identifier for the trial account.
- **SAML Identity Provider Metadata URL or XML**: The customer's Identity Provider (IdP) metadata, typically provided as a URL or an XML file. This metadata contains the necessary information for our system to communicate with the IdP (e.g., IdP entity ID, SSO URL, X.509 certificate).

## Configuration Steps
Follow these steps to enable SSO for a trial account:

1.  **Log in to the Admin Panel**
    *   Navigate to the Admin Panel URL (e.g., `https://your-admin-panel-domain.com`).
    *   Enter your administrator credentials and log in.

2.  **Locate the Trial Account**
    *   Once logged in, use the search functionality or navigate to the "Accounts" section.
    *   Search for the specific trial account using its Account ID or name.
    *   Click on the trial account to view its details.

3.  **Navigate to SSO Configuration**
    *   On the trial account's detail page, find the "SSO Configuration" or "Security Settings" tab/section.
    *   Click on it to open the SSO configuration interface.

4.  **Enter Identity Provider Metadata**
    *   You will see an input field for "IdP Metadata URL" or an option to upload an "IdP Metadata XML" file.
    *   **If the customer provides a Metadata URL**: Enter the complete URL into the designated field.
    *   **If the customer provides a Metadata XML file**: Use the "Upload XML" button to select and upload the file.
    *   **Important**: Ensure the metadata is valid and accessible by our system.

5.  **Enable SSO**
    *   Locate the "Enable SSO" toggle or checkbox.
    *   Toggle it to the "On" position or check the box to activate SSO for the trial account.

6.  **Save Configuration**
    *   Click the "Save" or "Apply Changes" button to store the SSO configuration.
    *   The system will perform a validation check on the IdP metadata. If there are any errors, an error message will be displayed, and you will need to correct the metadata before saving.
    *   A success message should appear upon successful saving.

7.  **Inform the Customer**
    *   Once SSO is successfully configured, inform the trial account contact person.
    *   Provide them with the Service Provider (SP) metadata (our application's metadata) if they require it for their IdP configuration.
    *   Provide them with the direct SSO login URL for their trial account (e.g., `https://your-application-domain.com/login?account_id=<TrialAccountID>`).

## Troubleshooting
-   **Invalid Metadata Error**: Double-check the IdP Metadata URL or XML for typos or formatting issues. Request the customer to provide a valid metadata file.
-   **Authentication Failure**: Ensure the customer's IdP is correctly configured with our Service Provider (SP) metadata. Verify that attributes (e.g., email) are being sent correctly by the IdP.
-   **Performance Issues**: If a customer reports slow logins via SSO, escalate to the engineering team with relevant details (account ID, time of incident).

## Support Contacts
For any issues or further assistance, please contact the Engineering Support team via [Link to Internal Support Channel/Jira/Slack].
