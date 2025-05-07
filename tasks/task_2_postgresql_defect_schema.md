# Task 2: Design and Deploy PostgreSQL Defect Schema

## Task Overview
**Task ID**: T2-MVP-DB-SCHEMA
**Phase**: Strategy
**Owner**: Database Engineer / Backend Developer
**Duration**: 1 Week (June 2025)
**Priority**: High
**Dependencies**: Task 1 (Severity Mapping Rules and ODC Attribute Logic)

This task focuses on designing and deploying a PostgreSQL database schema for storing defect data in the DefectXray MVP. The schema must support severity classification (High, Medium, Low) and Orthogonal Defect Classification (ODC) attributes (Defect Type and Trigger), enabling efficient storage, querying, and reporting for enterprise CI/CD workflows.

## Objectives
- Design a robust and scalable database schema to store defect data with associated severity and ODC metadata.
- Define appropriate data types, constraints, and indexes to ensure data integrity and query performance.
- Deploy the schema to a PostgreSQL instance for initial testing and integration with other MVP components.

## Detailed Steps
1. **Review Requirements and Outputs from Task 1**:
   - Examine the severity mapping rules and ODC attribute logic defined in 'tasks/task_1_severity_mapping_rules.md' to understand the data fields required (e.g., severity as enum, Defect Type, Trigger).
   - Identify additional fields needed for defect tracking, such as unique identifiers, timestamps, source information, and review flags.
   - **Output**: List of required fields with data types (see Schema Design section below).

2. **Design Schema Structure**:
   - Create a primary table 'defects' to store core defect information:
     - `id`: UUID or serial primary key for unique identification.
     - `severity`: Enum type (High, Medium, Low) for classification.
     - `defect_type`: Enum type for ODC Defect Type (e.g., Function, Assignment).
     - `trigger`: Enum type for ODC Trigger (e.g., Stress/Workload, Unit Test).
     - `description`: Text field for defect details.
     - `source`: Varchar for origin of defect (e.g., CI/CD pipeline, test suite name).
     - `created_at`: Timestamp for defect logging time.
     - `updated_at`: Timestamp for last modification.
     - `review_flag`: Boolean to indicate if manual review is needed.
     - `metadata`: JSONB for additional unstructured data (e.g., test context, tags).
   - Consider normalization for frequently queried fields if needed (e.g., separate table for sources if many-to-one relationships emerge), but prioritize simplicity for MVP.
   - **Output**: SQL schema definition with comments (see below).

3. **Define Enums for Structured Data**:
   - Create custom enum types in PostgreSQL for `severity`, `defect_type`, and `trigger` to enforce data consistency:
     - `severity_enum`: ('High', 'Medium', 'Low')
     - `defect_type_enum`: ('Function', 'Assignment', 'Interface', 'Checking', 'Timing/Serialization', 'Build/Package/Merge', 'Documentation', 'Algorithm', 'Unknown')
     - `trigger_enum`: ('Unit Test', 'Function Test', 'System Test', 'Stress/Workload', 'Recovery', 'Boundary Conditions', 'Rare Situation', 'Unknown')
   - **Output**: Enum creation SQL statements (see below).

4. **Add Indexes for Performance**:
   - Create indexes on frequently queried fields to optimize dashboard and API performance:
     - Index on `severity` for quick severity distribution queries.
     - Index on `defect_type` and `trigger` for ODC attribute analysis.
     - Index on `created_at` for time-based filtering.
     - Composite index on `(severity, defect_type)` for combined distribution reports.
   - Avoid over-indexing in MVP to minimize write overhead; refine based on beta usage patterns.
   - **Output**: Index creation SQL statements (see below).

5. **Define Constraints and Data Integrity Rules**:
   - Set `id` as primary key.
   - Set `severity`, `defect_type`, and `trigger` as NOT NULL with default values ('Medium', 'Unknown', 'Unknown') to handle incomplete data gracefully.
   - Set `created_at` to default to current timestamp.
   - **Output**: Constraints included in table definition (see below).

6. **Write Deployment Script**:
   - Create a SQL script to deploy the schema, including enum definitions, table creation, and index setup.
   - Include initial seed data if applicable (e.g., a few sample defects for testing).
   - Ensure script is idempotent (e.g., DROP IF EXISTS for re-runs during development).
   - **Output**: Complete deployment script (see below).

7. **Test Schema Deployment**:
   - Deploy the schema to a local or development PostgreSQL instance (e.g., using Docker for quick setup if no instance exists).
   - Insert 5-10 sample defect records covering various severity levels, Defect Types, and Triggers.
   - Run basic queries to verify data retrieval (e.g., count by severity, filter by defect_type).
   - **Output**: Test results and sample queries (to be documented post-testing).

## Outputs and Deliverables
- **Schema Design Documentation**: Detailed structure of the 'defects' table with field descriptions and rationale.
- **Enum Definitions**: SQL for creating custom enum types for severity and ODC attributes.
- **Index Definitions**: SQL for performance-enhancing indexes.
- **Deployment Script**: Complete SQL script for schema creation and initial data seeding.
- **Test Results**: Results from schema deployment and sample data queries (to be added post-testing).

## Schema Design Documentation
| **Field Name**     | **Data Type**          | **Constraints**               | **Description**                                      |
|--------------------|------------------------|-------------------------------|-----------------------------------------------------|
| id                | UUID or SERIAL         | PRIMARY KEY                  | Unique identifier for each defect.                 |
| severity          | severity_enum          | NOT NULL, DEFAULT 'Medium'   | Severity level (High, Medium, Low).                |
| defect_type       | defect_type_enum       | NOT NULL, DEFAULT 'Unknown'  | ODC Defect Type (e.g., Function, Assignment).      |
| trigger           | trigger_enum           | NOT NULL, DEFAULT 'Unknown'  | ODC Trigger (e.g., Stress/Workload, Unit Test).    |
| description       | TEXT                   |                              | Detailed description of the defect.                |
| source            | VARCHAR(255)           |                              | Origin of defect (e.g., pipeline name, test suite).|
| created_at        | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW()    | Timestamp when defect was logged.                  |
| updated_at        | TIMESTAMP WITH TIME ZONE |                            | Timestamp of last update to defect record.         |
| review_flag       | BOOLEAN                | DEFAULT FALSE                | Flag indicating if manual review is needed.        |
| metadata          | JSONB                  |                              | Additional unstructured data (e.g., tags, context).|

**Rationale**:
- **Enums**: Used for `severity`, `defect_type`, and `trigger` to enforce data consistency and simplify querying for dashboards.
- **JSONB for metadata**: Allows flexibility to store varying CI/CD metadata without schema changes in MVP, supporting future extensions.
- **Timestamps**: Essential for tracking defect history and filtering by recency in reporting.
- **Review Flag**: Supports QA processes by marking defects with uncertain classifications for manual override.

## SQL Definitions and Deployment Script
```sql
-- Drop existing objects if they exist (idempotent for development)
DROP TABLE IF EXISTS defects;
DROP TYPE IF EXISTS severity_enum;
DROP TYPE IF EXISTS defect_type_enum;
DROP TYPE IF EXISTS trigger_enum;

-- Create Enum Types for structured data
CREATE TYPE severity_enum AS ENUM ('High', 'Medium', 'Low');
CREATE TYPE defect_type_enum AS ENUM ('Function', 'Assignment', 'Interface', 'Checking', 'Timing/Serialization', 'Build/Package/Merge', 'Documentation', 'Algorithm', 'Unknown');
CREATE TYPE trigger_enum AS ENUM ('Unit Test', 'Function Test', 'System Test', 'Stress/Workload', 'Recovery', 'Boundary Conditions', 'Rare Situation', 'Unknown');

-- Create Defects Table
CREATE TABLE defects (
    id SERIAL PRIMARY KEY,
    severity severity_enum NOT NULL DEFAULT 'Medium',
    defect_type defect_type_enum NOT NULL DEFAULT 'Unknown',
    trigger trigger_enum NOT NULL DEFAULT 'Unknown',
    description TEXT,
    source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    review_flag BOOLEAN DEFAULT FALSE,
    metadata JSONB
);

-- Create Indexes for performance
CREATE INDEX idx_defects_severity ON defects(severity);
CREATE INDEX idx_defects_defect_type ON defects(defect_type);
CREATE INDEX idx_defects_trigger ON defects(trigger);
CREATE INDEX idx_defects_created_at ON defects(created_at);
CREATE INDEX idx_defects_sev_type ON defects(severity, defect_type);

-- Insert Sample Data for Testing (optional, can be expanded)
INSERT INTO defects (severity, defect_type, trigger, description, source, review_flag, metadata)
VALUES 
    ('High', 'Function', 'Stress/Workload', 'Application crashes under high load during payment processing.', 'CI Pipeline - Payment Tests', FALSE, '{"test_suite": "payment", "env": "prod-sim"}'::jsonb),
    ('Medium', 'Interface', 'Function Test', 'API endpoint returns incorrect status code for invalid input.', 'CI Pipeline - API Tests', FALSE, '{"endpoint": "/api/user", "status": 500}'::jsonb),
    ('Low', 'Documentation', 'Unit Test', 'Typo in internal API documentation.', 'Manual Report', FALSE, '{"doc": "internal-api.md"}'::jsonb);

-- Comment for documentation
COMMENT ON TABLE defects IS 'Stores defect data with severity and ODC attributes for DefectXray MVP.';
COMMENT ON COLUMN defects.severity IS 'Severity classification of the defect (High, Medium, Low).';
COMMENT ON COLUMN defects.defect_type IS 'ODC Defect Type indicating nature of fix.';
COMMENT ON COLUMN defects.trigger IS 'ODC Trigger indicating condition under which defect was found.';
```

## Validation and Testing
- Deploy the above script to a PostgreSQL instance (local or cloud-based).
- Verify enum types are created and usable in table structure.
- Insert sample data (beyond the initial 3 records if needed) covering all severity levels, Defect Types, and Triggers.
- Run test queries to ensure data retrieval works as expected:
  - `SELECT severity, COUNT(*) FROM defects GROUP BY severity;`
  - `SELECT defect_type, COUNT(*) FROM defects WHERE severity = 'High' GROUP BY defect_type;`
  - `SELECT * FROM defects WHERE review_flag = TRUE ORDER BY created_at DESC;`
- Confirm indexes are applied by checking query plans with `EXPLAIN`.
- **Output**: Document test results and any schema adjustments below (to be added post-testing).

## Timeline and Milestones
- **Start Date**: Mid-June 2025
- **Completion Date**: Late June 2025 (1 week duration)
- **Milestone**: PostgreSQL schema designed, deployed, and tested by late June 2025, ready for integration with Import Module and API development.

## Risks and Mitigation
- **Risk 1: Performance Issues with Large Data Volumes** - If defect data grows beyond MVP expectations, mitigation is to implement pagination in API queries and limit dashboard data to recent or filtered subsets. Additional indexes can be added post-beta based on query patterns.
- **Risk 2: Schema Evolution Needs** - If new ODC attributes or fields are needed post-MVP, use `ALTER TABLE` for additive changes and store temporary data in `metadata` JSONB field to avoid immediate schema redesign. Plan for schema migration strategy in beta feedback phase.
- **Risk 3: Data Integrity Failures** - If enum constraints or defaults lead to data loss (e.g., invalid severity values rejected), mitigation is to log rejected data to a temporary table or log file for recovery, with alerts for schema adjustment needs.

## Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for designing and deploying the PostgreSQL schema for DefectXray's MVP, ensuring data structure supports severity classification and ODC integration for enterprise needs. 