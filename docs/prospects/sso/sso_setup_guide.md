# SSO Setup Guide for Trial Accounts

This guide provides step-by-step instructions for trial account administrators to set up SAML Single Sign-On (SSO) for your trial organization. Enabling SSO will allow your users to authenticate using your Identity Provider (IdP) credentials, streamlining access to our platform.

## Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [General SAML SSO Configuration Steps](#general-saml-sso-configuration-steps)
3.  [IdP-Specific Guides](#idp-specific-guides)
    *   [Okta](#okta)
    *   [Azure AD](#azure-ad)
4.  [Testing Your SSO Configuration](#testing-your-sso-configuration)
5.  [Troubleshooting](#troubleshooting)

## 1. Prerequisites

Before you begin, ensure you have:

*   An active trial account with administrator privileges.
*   Access to your organization's Identity Provider (IdP) administration console (e.g., Okta, Azure AD).
*   Understanding of SAML concepts (e.g., IdP metadata, Assertion Consumer Service URL, Entity ID).

## 2. General SAML SSO Configuration Steps

Follow these general steps, then refer to your specific IdP guide for detailed instructions.

1.  **Access SSO Settings in Your Trial Account:**
    *   Log in to your trial account as an administrator.
    *   Navigate to `Settings > Security > Single Sign-On (SSO)`.
    *   Enable the 