# Task Instruction: Severity Analysis Engine for DefectXray

## Objective
Develop the Severity Analysis Engine to classify defects based on their impact across the software stack (UI, backend, database) into low, medium, or high severity. This module will analyze defect metadata captured by the Defect Detection Module and provide customizable classification rules for enterprise needs.

## Location
- `src/services/analysis`
- `src/backend` (for API endpoints)

## Dependencies
- Database setup (for accessing defect metadata) as outlined in `tasks/database_setup.md`.
- Defect Detection Module (for defect data input) as outlined in `tasks/defect_detection.md`.

## Expected Output
- A functional Severity Analysis Engine capable of classifying defects as low (UI only), medium (UI + backend/data models), or high (UI + backend + database) based on predefined and customizable rules.
- API endpoints to trigger severity analysis for individual defects or batches.
- Classified severity data stored in the PostgreSQL database and accessible for reporting and recommendations.

## Steps

### Step 1: Develop Core Severity Classification Logic
- **Description**: Implement the logic to analyze defect metadata and determine severity based on impact scope.
- **Actions**:
  1. Create a rule-based engine to evaluate defect metadata attributes (e.g., affected components, error type, stack trace) against severity criteria (`src/services/analysis/classifier.js`).
     - **Low Severity**: Affects only UI (e.g., CSS misalignment in a React component). Rule: Error source limited to frontend files or UI test failures.
     - **Medium Severity**: Impacts UI and backend/data models (e.g., UI form fails due to incorrect API response). Rule: Error involves frontend and API/backend test failures.
     - **High Severity**: Affects UI, backend, and database (e.g., form submission fails due to database constraint violation). Rule: Error traces to database errors or constraints alongside UI/backend issues.
  2. Implement a scoring mechanism to weigh factors like user impact (e.g., critical feature vs. minor UI element) and error frequency to adjust severity if needed.
  3. Ensure the engine handles edge cases (e.g., incomplete metadata) by assigning a default severity (e.g., medium) with a flag for manual review.
- **Validation**: Use sample defect data with known impacts (e.g., a UI-only bug, a full-stack failure) to test classification accuracy. Verify that the engine outputs the expected severity level for each case.

### Step 2: Implement Customization Features for Severity Rules
- **Description**: Allow enterprises to tailor severity classification to their specific workflows and priorities.
- **Actions**:
  1. Develop a configuration interface to define custom rules (e.g., via JSON or a UI form in later phases) stored in the database or a config file (`src/services/analysis/custom_rules.js`).
     - Example: Allow a rule to classify any defect in a specific module (e.g., payment processing) as high severity regardless of stack impact.
  2. Create logic to override default rules with custom ones based on project or user settings.
  3. Provide a fallback to default rules if custom configurations are invalid or not provided.
- **Validation**: Test with a custom rule set (e.g., elevate all UI defects to medium for a specific project) and confirm that the engine applies custom rules correctly while maintaining default behavior for other projects.

### Step 3: Integrate with Database
- **Description**: Connect the engine to the PostgreSQL database for defect data retrieval and storage, with performance optimization.
- **Actions**:
  1. Use `pg` library in Node.js to establish a connection pool to the PostgreSQL database.
  2. Write queries to fetch defect data (e.g., `SELECT * FROM defects WHERE status = 'pending_analysis' LIMIT 100`).
  3. Implement a caching layer with Redis on Azure Cache to store precomputed severity rules or frequently accessed defect metadata, reducing database load.
  4. Set cache expiration to 10 minutes for rule data to balance freshness and performance.
  5. Store analysis results back to the database with fields for severity level, confidence score, and analysis timestamp.
  6. Document database integration and caching setup in `src/severity_engine/db_integration.md`.
- **Validation**: Test connection with a sample query to retrieve 100 defects. Verify analysis results are saved correctly by querying the database post-analysis. Confirm cache reduces query time by checking Redis hit/miss logs.

### Step 4: Create API Endpoints for Severity Analysis
- **Description**: Expose endpoints to allow manual or automated triggering of severity analysis.
- **Actions**:
  1. Develop a RESTful endpoint `/api/analysis/classify` to analyze a single defect or a batch by ID (`src/backend/routes/analysis.js`).
  2. Create an endpoint `/api/analysis/rules` to retrieve or update custom severity rules (secured for admin access only).
  3. Implement authentication (e.g., API keys or OAuth with Azure AD) to secure these endpoints.
  4. Return a response with classification results or confirmation of rule updates.
- **Validation**: Use a tool like Postman to trigger analysis for sample defects. Verify that the API returns correct severity classifications and that rule updates are reflected in subsequent analyses.

### Step 5: Error Handling and Logging
- **Description**: Ensure the engine handles errors gracefully and logs issues for debugging.
- **Actions**:
  1. Implement error handling for database access failures, invalid defect data, or rule processing errors using try-catch blocks.
  2. Log analysis activities, errors, and results to a centralized logging system (e.g., Azure Monitor or local file in development) with detailed context (`src/services/analysis/logger.js`).
  3. Flag defects with analysis failures for manual review by updating a status field in the database.
- **Validation**: Simulate failures (e.g., invalid defect metadata, database outage) and confirm that errors are logged, defects are flagged for review, and the engine continues processing other defects.

### Step 6: Ensure Data Consistency
- **Description**: Implement transaction logic to prevent race conditions during concurrent defect updates.
- **Actions**:
  1. Use database transactions (`BEGIN`, `COMMIT`, `ROLLBACK`) for atomic updates when writing severity analysis results to the `defects` table.
  2. Implement a locking mechanism (e.g., `SELECT ... FOR UPDATE`) to handle concurrent analysis of the same defect.
  3. Test concurrent updates by simulating 50 simultaneous analysis tasks on the same defect batch.
  4. Document consistency mechanisms in `src/severity_engine/consistency.md`.
- **Validation**: Run concurrent analysis simulations and query the database to confirm no duplicate or inconsistent severity records. Review test results for integrity.

### Step 7: Implement Rule Versioning
- **Description**: Add versioning for custom severity rules to support rollback and auditability.
- **Actions**:
  1. Create a `severity_rules_version` table to store rule versions with fields for `version_id`, `rule_set_json`, `created_at`, and `created_by`.
  2. Implement an API endpoint `/api/rules/version` to save new rule versions and retrieve historical ones.
  3. Add rollback functionality to revert to a previous rule version if needed.
  4. Document versioning process in `src/severity_engine/rule_versioning.md`.
- **Validation**: Test rule versioning by saving multiple versions and reverting to a prior one. Confirm analysis uses the correct rule version via API logs and database queries.

### Step 8: Documentation
- **Description**: Document the setup, usage, and customization of the Severity Analysis Engine.
- **Actions**:
  1. Create a README file in `src/services/analysis` explaining the classification logic, default rules, and how to configure custom rules.
  2. Document the API endpoints in `src/backend/routes/README.md`, including request/response formats for triggering analysis and managing rules.
  3. Provide examples of integrating severity analysis into a CI/CD pipeline or manual workflow.
- **Validation**: Have a developer unfamiliar with the engine follow the documentation to classify defects and customize rules. Ensure they can do so without additional guidance.

## Conclusion
Completing these steps will establish the Severity Analysis Engine for DefectXray, enabling accurate classification of defects based on their impact across the software stack. This module is essential for prioritizing defect resolution in enterprise workflows and serves as a prerequisite for generating fix recommendations.

**Version**: 0.1 | **Status**: Draft | **Last Updated**: 2025-05-03 