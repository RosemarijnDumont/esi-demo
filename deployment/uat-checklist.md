# User Acceptance Testing (UAT) Checklist - Food Ordering Form

This checklist outlines the steps for User Acceptance Testing to ensure all acceptance criteria are met for the new Food Ordering feature.

## Environment Details:
*   **UAT URL (Frontend):** `[Insert Frontend UAT URL here]`
*   **UAT URL (Backend API Base):** `[Insert Backend UAT API Base URL here]`
*   **Test User Credentials:** `[If applicable, e.g., username/password]`

## Acceptance Criteria:

*   **AC1:** A food ordering form is accessible to ML6 employees.
*   **AC2:** Users can select multiple food items and quantities.
*   **AC3:** Users can specify different delivery/pickup locations within the office.
*   **AC4:** Orders are submitted electronically to a designated vendor or system.
*   **AC5:** Confirmation of the order is provided to the user.

---

## Test Cases:

### 1. Form Accessibility and Initial Load (AC1)
*   **Test Case ID:** UAT-FE-001
*   **Description:** Verify the food ordering form loads correctly and is accessible.
*   **Steps:**
    1.  Navigate to the Frontend UAT URL.
    2.  Observe the page.
*   **Expected Result:** The food ordering form (with fields for item, quantity, location, submit button) is visible and interactive.
*   **Pass/Fail:**
*   **Comments:**

### 2. Adding and Selecting Food Items (AC2)
*   **Test Case ID:** UAT-FE-002
*   **Description:** Verify users can add multiple food items and select different options.
*   **Steps:**
    1.  On the food ordering form.
    2.  Select a food item (e.g., 