# Task 6: Create API Endpoints for CI/CD Integration

## Task Overview
**Task ID**: T6-MVP-API
**Phase**: Strategy
**Owner**: Backend Developer
**Duration**: 2 Weeks (August 2025)
**Priority**: High
**Dependencies**: Task 2 (PostgreSQL Defect Schema), Task 4 (Severity Analysis Engine)

This task focuses on designing and implementing API endpoints for the DefectXray MVP using Node.js and Express. These endpoints will enable CI/CD pipelines to submit defect data for classification and retrieve classified defect information, supporting seamless integration with enterprise workflows.

## Objectives
- Develop RESTful API endpoints to accept defect data submissions from CI/CD tools.
- Provide endpoints for retrieving classified defect data, including filtering by severity, Defect Type, and Trigger.
- Ensure security with basic OAuth 2.0 authentication for API access in the MVP.

## Detailed Steps
1. **Review Requirements and Dependencies**:
   - Review the PostgreSQL schema from 'tasks/task_2_postgresql_defect_schema.md' to understand the data structure for defect storage and retrieval.
   - Examine the Severity Analysis Engine capabilities from 'tasks/task_4_severity_analysis_engine.md' to ensure API endpoints can trigger or access classification results.
   - Identify key API functionalities needed for CI/CD integration: submitting defect data, retrieving defect summaries, and filtering defect data for dashboards or reports.
   - **Output**: List of required API endpoints (see API Endpoints Design below).

2. **Set Up Backend Environment**:
   - Initialize a Node.js project with Express for API routing.
   - Add necessary dependencies: `express` for routing, `pg` (PostgreSQL client) for database access, `jsonwebtoken` for OAuth 2.0 token validation.
   - Configure environment variables for database connection and OAuth client credentials using `dotenv`.
   - **Output**: Project setup instructions (see Code Structure below).

3. **Design API Endpoints**:
   - Define RESTful endpoints for core functionalities:
     - **POST /defects**: Submit new defect data for classification (accepts JSON with description, source, metadata).
     - **GET /defects**: Retrieve a list of classified defects with optional query parameters for filtering (severity, defect_type, trigger, date range).
     - **GET /defects/summary**: Retrieve aggregated counts by severity for dashboard cards.
     - **GET /defects/types**: Retrieve defect counts by Defect Type for distribution charts.
     - **GET /defects/triggers**: Retrieve defect counts by Trigger for distribution charts.
   - Specify response formats (JSON) and status codes (e.g., 201 for successful submission, 400 for invalid data).
   - **Output**: API endpoint specifications (see API Endpoints Design below).

4. **Implement Authentication**:
   - Integrate basic OAuth 2.0 authentication middleware using `jsonwebtoken` to validate tokens for all endpoints.
   - Support a simple client ID/secret flow for MVP, with token validation against a hardcoded or environment-stored client list.
   - Return 401 Unauthorized for invalid or missing tokens.
   - **Output**: Authentication middleware code (see Code Structure below).

5. **Develop GET Endpoints for Data Retrieval**:
   - **GET /defects**: Retrieve a list of defects with optional query parameters for filtering:
     - `range`: Date range (e.g., '7d', '30d', 'all').
     - `severity`: Filter by severity level (e.g., 'High', 'Medium', 'Low').
     - `defect_type`: Filter by ODC Defect Type (e.g., 'Function', 'Interface').
     - `trigger`: Filter by ODC Trigger (e.g., 'Stress/Workload').
     - `limit`: Maximum number of results (default: 50).
   - **GET /defects/summary**: Retrieve aggregated counts by severity for dashboard cards (parameters: `range`).
   - **GET /defects/types**: Retrieve aggregated counts by Defect Type (parameters: `range`).
   - **GET /defects/triggers**: Retrieve aggregated counts by Trigger (parameters: `range`).
   - **GET /defects/summary/trend**: Retrieve aggregated defect counts over time for trend visualization (parameters: `range`, `group_by=date` to aggregate daily counts by severity).
   - Return JSON with appropriate structure for dashboard consumption (see Code Structure below).
   - **Output**: GET endpoint implementations.

6. **Secure API with OAuth 2.0 Authentication**:
   - Implement OAuth 2.0 authentication using a library like `passport` with `passport-oauth2` strategy in Express, supporting client credentials and authorization code flows for CI/CD tools and enterprise SSO.
   - Configure scopes to restrict access, focusing on `defects:read` (for GET endpoints) and `defects:write` (for POST endpoints) for MVP to simplify authentication and meet core CI/CD integration needs.
   - Defer additional admin scopes (e.g., for configuration updates) to post-MVP when an admin UI is developed (January 2026).
   - Use environment variables for client ID, secret, and token endpoint to support multiple OAuth providers (e.g., Azure AD, Okta).
   - Add rate limiting to prevent abuse, configurable via environment variables with a default of 100 requests per minute per client, testable up to 500 requests per minute for high-throughput enterprise pipelines. Use a library like `express-rate-limit` with Redis or in-memory store for distributed environments.
   - **Output**: OAuth 2.0 middleware and rate limiting configuration (see Code Structure below).

7. **Add Input Validation and Error Handling**:
   - Validate request payloads (POST /defects) for required fields (e.g., description, source) and acceptable formats using a library like `Joi`.
   - Validate query parameters (GET endpoints) for allowed values (e.g., severity must be 'High', 'Medium', or 'Low').
   - Return appropriate HTTP status codes (e.g., 400 for bad input, 401 for unauthorized, 500 for server errors) with descriptive error messages.
   - Log errors securely for debugging without exposing sensitive data to clients.
   - **Output**: Validation schemas and error handling middleware.

8. **Test API Endpoints**:
   - Write unit tests for each endpoint using a framework like `Jest` or `Mocha`, mocking database interactions to test logic.
   - Test authentication by simulating requests with invalid or expired tokens, expecting 401 responses.
   - Test data retrieval with various filter combinations (e.g., GET /defects?severity=High&range=7d) to ensure correct filtering.
   - Use tools like Postman or automated scripts to simulate CI/CD pipeline submissions.
   - **Output**: Test cases and results (to be documented post-testing).

9. **Add Trend Data Aggregation for Dashboard Visualization**:
   - Defer the implementation of time-based aggregation (e.g., daily defect counts for trend charts) to a post-MVP task (September 2025) to focus on core MVP features within the timeline.
   - For MVP, provide mock trend data or static summaries if requested by the dashboard team (Task 5).
   - Plan for future API support for GET /defects/summary with group_by=date parameter post-MVP.
   - **Output**: Trend aggregation logic deferred to post-MVP (see Code Structure below for placeholder).

10. **Add Audit Logging for Enterprise Compliance**:
   - Log API requests to support enterprise audit requirements, capturing metadata such as client ID (from OAuth token), endpoint, HTTP method, status code, and timestamp.
   - Store logs in a `audit_log` table (schema: id SERIAL PRIMARY KEY, client_id TEXT, endpoint TEXT, method TEXT, status INT, timestamp DATETIME) within the PostgreSQL database for traceability.
   - Limit audit logs to metadata for MVP to minimize storage and privacy concerns (e.g., GDPR). Defer capturing request payloads for debugging to post-MVP with proper anonymization (January 2026).
   - Ensure logging does not impact API performance by using asynchronous writes or buffering if needed.
   - **Output**: Audit logging middleware (see Code Structure below).

## Outputs and Deliverables
- **API Endpoints Design**: Specification of endpoints, methods, parameters, and responses.
- **Code Structure and Logic**: Detailed structure for Node.js/Express setup, authentication, and endpoint implementation.
- **Security Configuration**: OAuth 2.0 setup with `defects:read/write` scopes and configurable rate limiting (default 100/minute).
- **Test Results**: Results from testing API endpoints with sample data and authentication (to be added post-testing).

## API Endpoints Design
| **Endpoint**              | **Method** | **Description**                                      | **Parameters**                              | **Response**                              |
|---------------------------|------------|-----------------------------------------------------|---------------------------------------------|-------------------------------------------|
| /defects                 | POST       | Submit new defect data for classification.          | JSON body: { description, source, metadata } | 201: { id, message: 'Defect submitted' } |
| /defects                 | GET        | Retrieve list of classified defects with filters.   | Query: severity, defect_type, trigger, range, limit, offset | 200: [{ id, severity, defect_type, ... }] |
| /defects/summary         | GET        | Retrieve summary counts by severity.                | Query: range (e.g., '7d', '30d', 'all')     | 200: { total, high, medium, low }        |
| /defects/types           | GET        | Retrieve counts by Defect Type.                     | Query: range                                | 200: [{ type, count }, ...]              |
| /defects/triggers        | GET        | Retrieve counts by Trigger.                         | Query: range                                | 200: [{ trigger, count }, ...]           |
| /defects/summary/trend   | GET        | Retrieve aggregated defect counts over time for trend visualization. | Query: range, group_by=date                | 200: [{ date, high, medium, low }]        |

**Authentication**: All endpoints require a Bearer token in the Authorization header, validated via OAuth 2.0 client credentials.

**Error Responses**:
- 400 Bad Request: Invalid input data or parameters.
- 401 Unauthorized: Missing or invalid token.
- 500 Internal Server Error: Unexpected server issues.

## Code Structure and Logic
**Target Framework**: Node.js with Express and TypeScript
**Key Libraries**: `express` (API framework), `pg` (PostgreSQL client), `joi` (validation), `jsonwebtoken` (OAuth/JWT handling)

**Project Structure**:
```
src/
  api/
    routes/
      defects.ts            # Route handlers for defect endpoints
    middleware/
      auth.ts               # Authentication middleware
      validate.ts           # Validation middleware
    controllers/
      defectController.ts   # Business logic for defect operations
    services/
      db.ts                 # Database connection and queries
    models/
      defect.ts             # Type definitions for defect data
    tests/
      defects.test.ts       # Unit tests for defect endpoints
  app.ts                    # Express app setup
  server.ts                 # Server entry point
```

**Pseudocode**:
```typescript
// src/api/routes/defects.ts
import express, { Router } from 'express';
import * as defectController from '../controllers/defectController';
import authMiddleware from '../middleware/auth';
import validate from '../middleware/validate';
import { defectSchema, summaryQuerySchema, defectQuerySchema } from '../models/defect';

const router: Router = express.Router();

// POST endpoint for submitting defect data
router.post(
  '/defects',
  authMiddleware, // Ensure request is authenticated
  validate(defectSchema), // Validate request body
  defectController.submitDefect
);

// GET endpoint for retrieving defect list with filters
router.get(
  '/defects',
  authMiddleware,
  validate(defectQuerySchema, 'query'), // Validate query params
  defectController.getDefects
);

// GET endpoint for summary by severity
router.get(
  '/defects/summary',
  authMiddleware,
  validate(summaryQuerySchema, 'query'),
  defectController.getSummary
);

// GET endpoint for summary by defect type
router.get(
  '/defects/types',
  authMiddleware,
  validate(summaryQuerySchema, 'query'),
  defectController.getTypesSummary
);

// GET endpoint for summary by trigger
router.get(
  '/defects/triggers',
  authMiddleware,
  validate(summaryQuerySchema, 'query'),
  defectController.getTriggersSummary
);

// GET endpoint for trend data (defect counts over time)
router.get(
  '/defects/summary/trend',
  authMiddleware,
  validate(summaryQuerySchema, 'query'),
  defectController.getTrendSummary
);

export default router;
```

```typescript
// src/api/controllers/defectController.ts
import { Request, Response } from 'express';
import * as db from '../services/db';

// Submit a new defect (from CI/CD pipeline)
export const submitDefect = async (req: Request, res: Response) => {
  try {
    const defectData = req.body;
    // Insert into database
    const insertedDefect = await db.insertDefect(defectData);
    res.status(201).json(insertedDefect);
  } catch (error) {
    console.error('Error submitting defect:', error);
    res.status(500).json({ error: 'Failed to submit defect' });
  }
};

// Get defects with optional filters

export const getDefects = async (req: Request, res: Response) => {
  try {
    const filters = {
      range: req.query.range as string || 'all',
      severity: req.query.severity as string || null,
      defect_type: req.query.defect_type as string || null,
      trigger: req.query.trigger as string || null,
      limit: parseInt(req.query.limit as string) || 50
    };
    const defects = await db.getDefects(filters);
    res.json(defects);
  } catch (error) {
    console.error('Error fetching defects:', error);
    res.status(500).json({ error: 'Failed to fetch defects' });
  }
};

// Get summary by severity

export const getSummary = async (req: Request, res: Response) => {
  try {
    const range = req.query.range as string || 'all';
    const summary = await db.getDefectSummary(range);
    res.json(summary);
  } catch (error) {
    console.error('Error fetching summary:', error);
    res.status(500).json({ error: 'Failed to fetch summary' });
  }
};

// Get summary by defect type

export const getTypesSummary = async (req: Request, res: Response) => {
  try {
    const range = req.query.range as string || 'all';
    const summary = await db.getDefectTypesSummary(range);
    res.json(summary);
  } catch (error) {
    console.error('Error fetching types summary:', error);
    res.status(500).json({ error: 'Failed to fetch types summary' });
  }
};

// Get summary by trigger

export const getTriggersSummary = async (req: Request, res: Response) => {
  try {
    const range = req.query.range as string || 'all';
    const summary = await db.getDefectTriggersSummary(range);
    res.json(summary);
  } catch (error) {
    console.error('Error fetching triggers summary:', error);
    res.status(500).json({ error: 'Failed to fetch triggers summary' });
  }
};

// Get trend summary (defects over time)

export const getTrendSummary = async (req: Request, res: Response) => {
  try {
    const range = req.query.range as string || 'all';
    const groupBy = req.query.group_by as string || 'date';
    if (groupBy !== 'date') {
      return res.status(400).json({ error: 'Invalid group_by parameter. Only "date" is supported.' });
    }
    const trendData = await db.getDefectTrendSummary(range);
    res.json(trendData);
  } catch (error) {
    console.error('Error fetching trend summary:', error);
    res.status(500).json({ error: 'Failed to fetch trend summary' });
  }
};
```

```typescript
// src/api/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

// Environment variable for JWT secret (set in production)
const JWT_SECRET = process.env.JWT_SECRET || 'mock-secret-for-dev';

// Authentication middleware to validate JWT tokens
const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized: Missing or invalid token' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    // Attach decoded token data to request for potential use in controllers
    (req as any).user = decoded;
    next();
  } catch (error) {
    console.error('Token verification failed:', error);
    return res.status(401).json({ error: 'Unauthorized: Invalid or expired token' });
  }
};

export default authMiddleware;
```

```typescript
// src/api/services/db.ts
import { Pool } from 'pg';

// Database connection pool (credentials from environment variables in production)
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  database: process.env.DB_NAME || 'defectxray',
  password: process.env.DB_PASSWORD || 'password',
  port: parseInt(process.env.DB_PORT || '5432'),
});

// Calculate date filter based on range parameter
const getDateFilter = (range: string): string => {
  const now = new Date();
  if (range === '7d') {
    const past = new Date(now);
    past.setDate(now.getDate() - 7);
    return `created_at >= '${past.toISOString()}'`;
  } else if (range === '30d') {
    const past = new Date(now);
    past.setDate(now.getDate() - 30);
    return `created_at >= '${past.toISOString()}'`;
  }
  return 'TRUE'; // 'all' or invalid range returns all records
};

// Insert a new defect

export const insertDefect = async (defect: any) => {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const query = `
      INSERT INTO defects (description, source, metadata, severity, defect_type, trigger)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING *;
    `;
    const values = [
      defect.description,
      defect.source,
      defect.metadata || {},
      defect.severity || 'Medium', // Default if not classified
      defect.defect_type || 'Unknown',
      defect.trigger || 'Unknown'
    ];
    const result = await client.query(query, values);
    await client.query('COMMIT');
    return result.rows[0];
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

// Get defects with filters

export const getDefects = async (filters: { range: string, severity?: string | null, defect_type?: string | null, trigger?: string | null, limit: number }) => {
  const client = await pool.connect();
  try {
    let conditions = [getDateFilter(filters.range)];
    let values: any[] = [];
    let paramIndex = 1;

    if (filters.severity) {
      conditions.push(`severity = $${paramIndex}`);
      values.push(filters.severity);
      paramIndex++;
    }
    if (filters.defect_type) {
      conditions.push(`defect_type = $${paramIndex}`);
      values.push(filters.defect_type);
      paramIndex++;
    }
    if (filters.trigger) {
      conditions.push(`trigger = $${paramIndex}`);
      values.push(filters.trigger);
      paramIndex++;
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';
    const query = `
      SELECT * FROM defects
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT $${paramIndex};
    `;
    values.push(filters.limit);

    const result = await client.query(query, values);
    return result.rows;
  } catch (error) {
    throw error;
  } finally {
    client.release();
  }
};

// Get summary by severity

export const getDefectSummary = async (range: string) => {
  const client = await pool.connect();
  try {
    const dateFilter = getDateFilter(range);
    const query = `
      SELECT 
        COUNT(*) as total,
        COUNT(*) FILTER (WHERE severity = 'High') as high,
        COUNT(*) FILTER (WHERE severity = 'Medium') as medium,
        COUNT(*) FILTER (WHERE severity = 'Low') as low
      FROM defects
      WHERE ${dateFilter};
    `;
    const result = await client.query(query);
    return result.rows[0];
  } catch (error) {
    throw error;
  } finally {
    client.release();
  }
};

// Get summary by defect type

export const getDefectTypesSummary = async (range: string) => {
  const client = await pool.connect();
  try {
    const dateFilter = getDateFilter(range);
    const query = `
      SELECT defect_type as type, COUNT(*) as count
      FROM defects
      WHERE ${dateFilter}
      GROUP BY defect_type
      ORDER BY count DESC;
    `;
    const result = await client.query(query);
    return result.rows;
  } catch (error) {
    throw error;
  } finally {
    client.release();
  }
};

// Get summary by trigger

export const getDefectTriggersSummary = async (range: string) => {
  const client = await pool.connect();
  try {
    const dateFilter = getDateFilter(range);
    const query = `
      SELECT trigger, COUNT(*) as count
      FROM defects
      WHERE ${dateFilter}
      GROUP BY trigger
      ORDER BY count DESC;
    `;
    const result = await client.query(query);
    return result.rows;
  } catch (error) {
    throw error;
  } finally {
    client.release();
  }
};

// Get trend summary (defects over time by severity)

export const getDefectTrendSummary = async (range: string) => {
  const client = await pool.connect();
  try {
    const dateFilter = getDateFilter(range);
    const query = `
      SELECT 
        DATE_TRUNC('day', created_at) as date,
        COUNT(*) FILTER (WHERE severity = 'High') as high,
        COUNT(*) FILTER (WHERE severity = 'Medium') as medium,
        COUNT(*) FILTER (WHERE severity = 'Low') as low
      FROM defects
      WHERE ${dateFilter}
      GROUP BY DATE_TRUNC('day', created_at)
      ORDER BY date ASC;
    `;
    const result = await client.query(query);
    // Format date as YYYY-MM-DD string
    return result.rows.map(row => ({
      date: row.date.toISOString().split('T')[0],
      high: parseInt(row.high),
      medium: parseInt(row.medium),
      low: parseInt(row.low)
    }));
  } catch (error) {
    throw error;
  } finally {
    client.release();
  }
};
```

## Timeline and Milestones
- **Start Date**: Mid-July 2025
- **Completion Date**: Late July 2025 (2 weeks duration)
- **Milestone**: API endpoints for defect ingestion and retrieval developed and tested by late July 2025, ready for integration with Import Module (Task 3) and Dashboard (Task 5). Trend aggregation deferred to post-MVP (September 2025).

## Risks and Mitigation
- **Risk 1: Scalability Issues** - If the API struggles with high defect volumes (e.g., 1,000/hour), mitigation is to implement rate limiting and batch processing for POST requests, and use database indexing (Task 2) for faster GET queries. Pagination added in Step 10 further mitigates this by limiting response sizes.
- **Risk 2: Security Vulnerabilities** - If OAuth 2.0 is misconfigured, unauthorized access could occur. Mitigation is to use established libraries (e.g., passport.js) for token validation and test authentication flows before launch.
- **Risk 3: Integration Delays** - If dependent tasks (e.g., Task 3 Import Module) are delayed, API testing may be incomplete. Mitigation is to use mock data for initial testing and coordinate closely with other task leads for integration timelines.
- **Risk 4: Data Inconsistency** - If ingested data has inconsistent formats or missing fields, API responses may be unreliable. Mitigation is to enforce validation schemas on POST requests (returning 400 Bad Request for invalid data) and ensure Task 3 preprocessing aligns with API expectations.
- **Risk**: Authentication complexity may delay integration for enterprise clients with diverse SSO setups.
  - **Mitigation**: Support standard OAuth 2.0 flows (Step 6) and document setup for common providers (Azure AD, Okta). Limit scopes to `defects:read/write` for MVP, expanding post-MVP based on beta feedback.
- **Risk**: High request volumes from CI/CD pipelines may overwhelm the API, causing downtime.
  - **Mitigation**: Implement pagination (Step 5) and configurable rate limiting (default 100/minute, up to 500/minute, Step 6) to manage load. Test with simulated pipeline traffic (Step 8).
- **Risk**: Audit logging may introduce performance overhead or privacy concerns.
  - **Mitigation**: Limit logs to metadata (Step 10) for MVP, using async writes to reduce latency. Defer payload logging to post-MVP with anonymization for GDPR compliance.

## Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for creating API Endpoints for CI/CD Integration in DefectXray's MVP, ensuring seamless data submission and retrieval for enterprise workflows. 