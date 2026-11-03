Writing an end-to-end (e2e) test cases for an e-commerce app
advanced

Writing an end-to-end (e2e) test cases for an e-commerce app
============================================================

In this project, you will write end-to-end (e2e) test cases for an e-commerce application for an online book store.

Start building, submit solution and get feedback from the community.

Start Working
In this project, you will write **end-to-end** (e2e) test cases for an e-commerce application for an online book store. The goal is to guarantee the app does not have regressions after new updates and ensures a seamless user journey from search to checkout.

**Project Base URL**
--------------------

You should run your tests against the following application:

* **URL:** <https://bookcart.azurewebsites.net/>

**Requirements**
----------------

The tests should cover the critical paths of the application. You must implement automation for the following requirements:

1. User authentication (Login and user registration).
2. Product search and navigation (Finding books by title or category).
3. Shopping cart management (Adding, removing, and updating quantities of items).
4. Checkout process (Completing a purchase).

**Constraints**
---------------

* **Tooling:** Use a modern framework (e.g., Playwright, Cypress, Robot Framework, or Selenium).
* **Assertions:** Ensure every test has meaningful assertions (checking URLs, visibility of elements, and API responses where applicable).
* **Selector strategy:** Avoid using fragile selectors like long XPaths or CSS classes that might change. Give preference to User-facing attributes (Text, Labels, Placeholders) or Data attributes (data-test-id="login-button").
* **Smart use of hooks:** Avoid code duplication by using life-cycle hooks correctly (before, before each, after, after each).
* **Flakiness Prevention:** No fixed waits, never use sleep(5000) or wait(5000). Instead, use Dynamic waiting (waiting for an element to be visible, attached, or for an API response to complete).
* **Clean up:** Ensure tests are independent. One test should not depend on the state left by a previous one.
* **Reporting:** Implement a reporting tool (like Allure Report or the framework's native reporter) to visualize test results.

**Advanced Challenges (Optional)**
----------------------------------

If you want to take this project to the next level:

1. **CI/CD Integration:** Set up a GitHub Action to run your tests automatically on every push.
2. **API Testing:** Add a layer of API tests to validate the back-end endpoints directly.
3. **Cross-browser Testing:** Configure the project to run tests in Chromium, Firefox, and WebKit.
4. **Visual Testing:** Implement visual regression tests to check if the UI layout changed unexpectedly.

