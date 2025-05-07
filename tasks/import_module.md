# Task Instruction: Import Module for DefectXray

## Objective
Develop the Import Module to ingest defect data from existing enterprise tools (e.g., Jira, Sentry) via APIs or file uploads (CSV, JSON). This module will normalize and store defect metadata in the PostgreSQL database for subsequent severity analysis and fix recommendations, positioning DefectXray as a complementary tool to existing defect tracking systems.

## Location
- `src/services/import`
- `src/backend` (for API endpoints)

## Dependencies
- Database setup (for storing defect metadata) as outlined in `tasks/database_setup.md`.

## Expected Output
- A functional Import Module capable of integrating with popular defect tracking tools like Jira and Sentry to ingest defect data.
- Support for manual file uploads (CSV, JSON) for enterprises without API access or with custom systems.
- API endpoints to trigger data imports from CI/CD pipelines or manual processes.
- Defect metadata stored in the PostgreSQL database with source tracking.

## Steps

### Step 1: Develop Integration Logic for Defect Tracking Tools
- **Description**: Create connectors to ingest defect data from popular defect tracking and monitoring tools.
- **Actions**:
  1. Write integration scripts for Jira to fetch defect data using its REST API (e.g., `/rest/api/3/issue`) and extract relevant fields like ID, summary, and stack trace (`src/services/import/jira_connector.js`).
  2. Develop integration for Sentry to retrieve error events via its API, capturing error details and environment data (`src/services/import/sentry_connector.js`).
  3. Standardize the output format across tools to include defect ID, title/summary, description, stack trace (if available), environment details, and creation date.
  4. Add a mechanism to track the source of the data (e.g., 'jira', 'sentry') in an `import_source` field.
- **Validation**: Test connectors with sample data from Jira and Sentry in a sandbox environment to ensure data is fetched and formatted correctly. Verify data is logged to a temporary file or console output for review.

### Step 2: Implement File Upload Support for Manual Imports
- **Description**: Enable ingestion of defect data via file uploads for flexibility with custom or legacy systems.
- **Actions**:
  1. Create a parser for CSV files to map columns (e.g., `id`, `summary`, `stackTrace`) to the internal defect format (`src/services/import/csv_parser.js`).
  2. Add support for JSON files with a predefined schema (e.g., array of defect objects) for structured data uploads (`src/services/import/json_parser.js`).
  3. Implement validation to check for required fields (e.g., `id`, `summary`) and flag incomplete records for manual review.
  4. Allow users to specify the source (e.g., 'manual_csv') for tracking purposes.
- **Validation**: Test with sample CSV and JSON files containing 100 defect records, including some with missing fields. Confirm that valid data is parsed correctly and incomplete records are flagged appropriately.

### Step 3: Store Defect Metadata in Database
- **Description**: Connect the Import Module to the PostgreSQL database to store ingested defect data.
- **Actions**:
  1. Use a database client library (e.g., `pg` for Node.js) to connect to the Azure PostgreSQL instance from the Import Module (`src/services/import/db_client.js`).
  2. Write insertion logic to store defect metadata in the `defects` table as defined in the database schema, including the new `import_source` field.
  3. Ensure data integrity by handling duplicate defects (e.g., based on `id` and `import_source`) and updating existing records if necessary.
- **Validation**: Simulate ingestion of 100 defects from multiple sources, then query the database to confirm that metadata (e.g., summary, stack trace, source) is stored correctly without duplicates.

### Step 4: Create API Endpoints for Data Import
- **Description**: Expose endpoints to allow manual or automated triggering of defect data imports.
- **Actions**:
  1. Develop a RESTful endpoint `/api/import` to accept defect data via file upload (CSV, JSON) or direct API calls with tool-specific parameters (e.g., Jira issue IDs) (`src/backend/routes/import.js`).
  2. Implement authentication (e.g., API keys or OAuth with Azure AD) to secure these endpoints.
  3. Add rate-limiting to prevent abuse (e.g., max 100 requests per minute per client).
  4. Return a response with import status, number of defects processed, and any validation errors.
- **Validation**: Use a tool like Postman to trigger imports with sample files and API calls. Verify that the API processes data correctly, returns accurate status messages, and enforces security measures.

### Step 5: Error Handling and Logging
- **Description**: Ensure the module handles errors gracefully and logs issues for debugging.
- **Actions**:
  1. Implement try-catch blocks around API integrations and file parsing to handle failures (e.g., API downtime, malformed files).
  2. Log errors and successful imports to a centralized logging system (e.g., Azure Monitor or a local file in development) with timestamps and context (`src/services/import/logger.js`).
  3. Notify administrators of critical failures (e.g., database connection loss) via an alert mechanism (to be integrated later with notification systems).
- **Validation**: Simulate integration failures (e.g., invalid API credentials, corrupted files) and confirm that errors are logged without crashing the module. Check logs for clarity and completeness.

### Step 6: Documentation
- **Description**: Document the setup, usage, and customization of the Import Module.
- **Actions**:
  1. Create a README file in `src/services/import` explaining how to configure integrations with defect tracking tools and upload file formats.
  2. Document the API endpoints in `src/backend/routes/README.md`, including request/response formats and authentication requirements.
  3. Provide examples of triggering imports from a CI/CD pipeline (e.g., a GitHub Actions workflow snippet) or manual upload process.
- **Validation**: Have a developer unfamiliar with the module follow the documentation to set up and trigger imports. Ensure they can do so without additional guidance.

## Conclusion
Completing these steps will establish the Import Module for DefectXray, enabling the ingestion and storage of defect data from existing enterprise tools and manual uploads. This module is a critical prerequisite for severity analysis and fix recommendations, forming the foundation of the defect analysis pipeline by leveraging external data sources.

**Version**: 0.1 | **Status**: Draft | **Last Updated**: 2025-05-03 