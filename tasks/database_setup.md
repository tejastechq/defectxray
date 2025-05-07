# Task Instruction: Database Setup for DefectXray

## Objective
Design and implement the PostgreSQL database schema for DefectXray to store defect metadata, user data, and audit logs. Configure encryption and access control for compliance, and set up the database on Azure for scalability.

## Location
- `src/database`

## Dependencies
- None (this is a foundational task).

## Expected Output
- A fully configured PostgreSQL database on Azure Database for PostgreSQL.
- A schema definition for defect metadata, user data, and audit logs.
- Encryption (AES-256) and role-based access control (RBAC) implemented for compliance.
- Read replicas and automated backups configured for scalability and reliability.

## Steps

### Step 1: Design Database Schema
- **Description**: Create a detailed schema for storing all necessary data for DefectXray.
- **Actions**:
  1. Define tables for defect metadata:
     - `defects` (columns: `id`, `test_id`, `failure_details`, `stack_trace`, `environment`, `severity`, `created_at`, `updated_at`)
     - `tests` (columns: `id`, `name`, `framework`, `project_id`, `created_at`)
  2. Define tables for user data:
     - `users` (columns: `id`, `email`, `name`, `role`, `created_at`)
     - `projects` (columns: `id`, `name`, `owner_id`, `created_at`)
  3. Define tables for audit logs:
     - `audit_logs` (columns: `id`, `user_id`, `action`, `target_type`, `target_id`, `details`, `created_at`)
  4. Document the schema in a `schema.sql` file within `src/database`.
- **Validation**: Ensure all necessary fields for defect analysis, user management, and compliance auditing are included. Verify with the requirements in `docs/requirements.md`.

### Step 2: Set Up Azure Database for PostgreSQL
- **Description**: Provision a PostgreSQL instance on Azure for hosting the DefectXray database.
- **Actions**:
  1. Use Azure Portal or CLI to create a new Azure Database for PostgreSQL instance.
  2. Configure the instance with the following settings:
     - Tier: General Purpose (scalable for enterprise needs).
     - Region: Choose a region close to the primary user base or CI/CD infrastructure.
     - Enable high availability for 99.9% uptime.
  3. Set up connection security:
     - Enable TLS 1.3 for data in transit.
     - Configure firewall rules to allow access only from specific IP ranges or Azure services.
- **Validation**: Confirm the database instance is accessible via connection string from a test environment. Ensure high availability is enabled in Azure Portal.

### Step 3: Implement Encryption
- **Description**: Ensure data security by configuring encryption for data at rest and implementing data masking for sensitive information.
- **Actions**:
  1. Enable Azure-managed encryption (AES-256) for the PostgreSQL instance (this is automatic with Azure Database for PostgreSQL).
  2. Verify that sensitive columns (e.g., `failure_details`, `email`) are marked for encryption in the schema design.
  3. Implement data masking using PostgreSQL's `pgcrypto` extension to dynamically mask sensitive fields like `failure_details` and `stack_trace` for non-admin roles.
  4. Create a view `masked_defects_view` for non-admin queries with masked sensitive data.
  5. Document encryption and masking settings in `src/database/security_config.md`.
- **Validation**: Check Azure Portal to confirm encryption is enabled. Test data insertion to ensure sensitive fields are encrypted and masked correctly in views for non-admin access.

### Step 4: Configure Role-Based Access Control (RBAC)
- **Description**: Set up database-level access control to restrict data access based on user roles.
- **Actions**:
  1. Create database roles corresponding to DefectXray user roles (e.g., `admin`, `developer`, `auditor`).
  2. Assign permissions:
     - `admin`: Full access to all tables.
     - `developer`: Read/write access to `defects` and `tests`, read-only for `audit_logs`.
     - `auditor`: Read-only access to all tables.
  3. Use PostgreSQL `GRANT` statements to define these permissions and save them in `src/database/roles.sql`.
  4. Integrate with Azure AD for authentication, mapping AD groups to database roles.
- **Validation**: Test access with dummy user accounts for each role to ensure permissions are correctly enforced.

### Step 5: Configure Scalability Features
- **Description**: Set up read replicas and backups to ensure database scalability and reliability, including disaster recovery planning.
- **Actions**:
  1. Enable read replicas in Azure Database for PostgreSQL to handle high read throughput (e.g., for reporting queries).
  2. Configure automated backups with a retention period of 30 days (adjustable based on enterprise needs).
  3. Set up point-in-time recovery for disaster recovery scenarios.
  4. Configure geo-redundant backups with Azure's cross-region restore for disaster recovery across regions.
  5. Schedule monthly failover tests to validate disaster recovery readiness.
  6. Document disaster recovery plan in `src/database/dr_plan.md`.
- **Validation**: Verify read replicas are active and accessible in Azure Portal. Test a backup restoration to ensure data recovery works as expected. Confirm geo-redundant setup and document failover test results.

### Step 6: Deploy Schema to Database
- **Description**: Apply the designed schema to the provisioned database.
- **Actions**:
  1. Use a database migration tool (e.g., `pgAdmin` or a script with `psql`) to execute the `schema.sql` file on the Azure PostgreSQL instance.
  2. Execute the `roles.sql` script to set up RBAC.
  3. Insert initial test data to verify table structure and relationships.
- **Validation**: Query the database to confirm all tables, indexes, and relationships are correctly created. Ensure test data insertion and retrieval work without errors.

### Step 7: Document Connection Details
- **Description**: Provide secure access instructions for developers and systems to connect to the database.
- **Actions**:
  1. Store connection strings and credentials securely in Azure Key Vault (not in code or documentation).
  2. Document connection instructions (e.g., using environment variables for Node.js backend) in `src/database/connection_guide.md`.
- **Validation**: Ensure backend developers can connect to the database using the provided instructions without exposing sensitive information.

### Step 8: Ensure Data Consistency
- **Description**: Implement mechanisms to prevent race conditions and ensure data consistency during concurrent updates.
- **Actions**:
  1. Use PostgreSQL transactions with `BEGIN`, `COMMIT`, or `ROLLBACK` to ensure atomic updates to the `defects` table.
  2. Test concurrent updates by simulating 100 simultaneous writes to validate consistency.
  3. Document consistency test results and transaction usage in `src/database/consistency_test.md`.
- **Validation**: Run concurrent update tests and query the database to confirm data integrity with no duplicate or inconsistent records. Review test documentation for completeness.

## Conclusion
Completing these steps will establish a secure, scalable PostgreSQL database for DefectXray, ready to support defect metadata storage and user management. This foundational task enables subsequent development of defect detection and analysis modules.

**Version**: 0.1 | **Status**: Draft | **Last Updated**: 2025-05-03 