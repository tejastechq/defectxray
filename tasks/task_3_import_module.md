# Task 3: Develop Import Module for Defect Data Ingestion

## Task Overview
**Task ID**: T3-MVP-IMPORT
**Phase**: Strategy
**Owner**: Backend Developer
**Duration**: 2 Weeks (June-July 2025)
**Priority**: High
**Dependencies**: Task 1 (Severity Mapping Rules and ODC Attribute Logic), Task 2 (PostgreSQL Defect Schema)

This task focuses on developing the Import Module for the DefectXray MVP, which is responsible for ingesting defect data from various CI/CD tools and pipelines, processing it to assign initial severity and ODC attributes, and storing it in the PostgreSQL database. The module must handle diverse input formats and ensure data is prepared for further analysis by the Severity Analysis Engine.

## Objectives
- Create a robust Import Module to ingest defect data from multiple sources (e.g., CI/CD pipelines, test reports) in common formats (e.g., JSON, XML, plain text logs).
- Implement initial processing logic to extract relevant defect information and apply basic ODC classification using keyword matching or predefined tags.
- Integrate with the PostgreSQL database to store processed defect data for further classification and reporting.

## Detailed Steps
1. **Review Requirements and Dependencies**:
   - Study the severity mapping rules and ODC attribute logic from 'tasks/task_1_severity_mapping_rules.md' to understand the data fields and fallback logic for Defect Type, Trigger, and severity.
   - Review the PostgreSQL schema design from 'tasks/task_2_postgresql_defect_schema.md' to ensure data mapping aligns with table structure (e.g., enums for severity, defect_type, trigger).
   - Identify common CI/CD output formats (e.g., JUnit XML, custom JSON from Jenkins, plain text logs) based on enterprise use cases.
   - **Output**: List of supported input formats and mapping to database fields (see Input Format Handling below).

2. **Design Import Module Architecture**:
   - Define the module as a Python-based component (for consistency with likely backend stack and ease of integration with Node.js API layer).
   - Structure the module with sub-components:
     - **Input Parser**: Reads and parses raw data from different formats.
     - **Data Extractor**: Extracts relevant defect information (e.g., description, test suite, failure context).
     - **Initial Classifier**: Applies basic ODC and severity classification using keyword matching or tags as per Task 1 fallback logic.
     - **Database Connector**: Inserts processed data into PostgreSQL 'defects' table.
   - Plan for extensibility to add new input formats post-MVP via plugin or configuration files.
   - **Output**: Architecture diagram or description (see Module Architecture below).

3. **Parse Defect Data for ODC Attributes and Initial Severity**:
   - Extract relevant fields from defect data (e.g., description, stack trace, test name, environment details) to identify potential ODC attributes (Defect Type, Trigger, Activity).
   - Use rule-based keyword matching (from Task 1) to assign initial ODC attributes and severity levels. For example, keywords like 'crash' or 'failure' in descriptions may indicate a 'Function' Defect Type with 'High' severity.
   - Implement logic to handle incomplete or ambiguous data by marking defects for manual review (e.g., flag if no clear Defect Type is identified).
   - Add a configuration option to allow QA engineers to override initial classifications, storing these overrides in a separate `override_log` table for future rule refinement.
   - Clarify that override analysis is manual for MVP, with analysts reviewing logs in July 2025 to refine rules. Automated rule suggestions (e.g., adding keywords based on overrides) are deferred to post-MVP (January 2026).
   - **Output**: Parsing logic and override mechanism in the import module code.

4. **Enhance Classification with Contextual Parsing Rules**:
   - Develop logic to analyze defect context beyond simple keywords, such as metadata from CI/CD pipelines (e.g., build stage, test suite name) or log patterns (e.g., error codes, exception types), to improve ODC attribute assignment.
   - Limit regex-based contextual parsing to 2-3 high-impact cases (e.g., detecting 'timeout' for Timing/Serialization, 'null pointer' for Assignment) to avoid overcomplicating the MVP.
   - Add a configuration toggle to disable metadata parsing if it introduces noise (e.g., inconsistent CI/CD outputs across enterprises), defaulting to keyword priority over metadata (`metadata_priority: false`) for robustness. Use early testing results in July 2025 to validate this choice and adjust if metadata proves reliable for most beta users.
   - **Output**: Contextual parsing rules and configuration toggle in the import module.

5. **Implement Confidence Scoring for Classifications**:
   - Assign a confidence score (0-1) to initial Defect Type, Trigger, and Severity classifications based on the strength of evidence:
     - Explicit tags or metadata (e.g., 'type: Function' in JSON) yield a score of 1.0.
     - Strong keyword matches (e.g., 'crash' for Function) yield 0.8-0.9 based on term specificity.
     - Weak or ambiguous matches (e.g., generic 'error') yield 0.5-0.7.
     - No matches default to 0.3, relying on fallback logic.
   - Set `review_flag=TRUE` in the database for defects with confidence scores below a threshold (e.g., 0.8) to prompt QA review.
   - **Output**: Confidence scoring logic added to classification process (see Code Structure below).

6. **Integrate with PostgreSQL Database**:
   - Use a Python library like `psycopg2` or `SQLAlchemy` to connect to the PostgreSQL instance.
   - Map extracted and classified data to 'defects' table fields, ensuring enum values match schema definitions.
   - Implement batch inserts for efficiency if processing multiple defects at once.
   - Handle insertion errors by logging failed records to a file or error table for recovery.
   - **Output**: Database integration code (see Code Structure below).

7. **Add Logging and Error Handling**:
   - Log ingestion process (e.g., number of defects processed, errors encountered) to a file or monitoring system for debugging.
   - Handle parser failures gracefully by skipping malformed records and logging details for later review.
   - **Output**: Logging setup (see Code Structure below).

8. **Test Import Module with Diverse Defect Data**:
   - Validate the import module using a test suite of 10-15 defect entries per supported format (JUnit XML, JSON, plain text logs), covering various Defect Types, Triggers, and edge cases (e.g., missing metadata, malformed XML, non-English descriptions).
   - Include a batch test with 100 defects to simulate enterprise-scale ingestion, measuring performance (target: process 10,000 defects in 1-3 minutes) and accuracy of ODC attribute extraction.
   - Expand testing scope to handle missing metadata by ensuring fallback logic (from Task 1) is applied correctly, confirming at least 80% of defects are processed without errors.
   - Document test results, including success rates, processing times, and any parsing failures requiring rule adjustments.
   - Plan post-MVP optimization (e.g., database indexing, queue scaling) if performance falls outside the 1-3 minute target for 10,000 defects.
   - **Output**: Test report with performance metrics and identified issues (to be added post-testing).

## Outputs and Deliverables
- **Module Architecture Description**: Overview of Import Module structure and components.
- **Supported Input Formats**: Documentation of handled formats and field mappings.
- **Code Structure and Logic**: Detailed pseudocode or code snippets for parsing, extraction, classification, and database integration.
- **Configuration Format**: Structure for configurable field mappings and regex patterns.
- **Test Results**: Results from running the module on sample data, including database verification (to be added post-testing).

## Module Architecture
The Import Module is a Python-based component with the following sub-components:
- **Input Parser**: Reads raw data from files or streams and parses it based on format (JUnit XML, JSON, plain text).
- **Data Extractor**: Pulls relevant fields (description, source, metadata) from parsed data.
- **Initial Classifier**: Applies basic ODC and severity classification using keyword matching or explicit tags, setting review_flag for uncertain data.
- **Database Connector**: Uses `psycopg2` to insert processed defect data into the PostgreSQL 'defects' table.

**Flow**:
1. Input file/stream → Input Parser identifies format and parses content.
2. Parsed data → Data Extractor maps to internal defect object.
3. Defect object → Initial Classifier assigns Defect Type, Trigger, severity, and review_flag.
4. Classified defect → Database Connector stores in PostgreSQL.
5. Log results and errors at each step.

## Supported Input Formats
| **Format**      | **Key Fields Extracted**                       | **Mapping to Database Fields**                       |
|-----------------|-----------------------------------------------|-----------------------------------------------------|
| JUnit XML       | testcase name, failure message, stack trace   | description (message + trace), source (testcase name), metadata (trace details) |
| JSON Reports    | errorMessage, testName, env                   | description (errorMessage), source (testName), metadata (env as JSON) |
| Plain Text Logs | Lines with ERROR/FAILURE, context lines       | description (error line + context), source (filename or 'log'), metadata (empty or context) |

**Configuration File Structure (YAML example)**:
```yaml
formats:
  json:
    fields:
      description: errorMessage
      source: testName
      metadata: env
  plaintext:
    regex:
      defect_line: ".*(ERROR|FAILURE|CRASH).*"
      context_lines: 2  # lines before/after to include in description
settings:
  metadata_parsing_enabled: true  # Toggle to disable metadata-based parsing for inconsistent CI/CD outputs
```

## Code Structure and Logic
**Target Language**: Python
**Key Libraries**: `xml.etree.ElementTree` (XML parsing), `json` (JSON parsing), `re` (regex for text logs), `psycopg2` (PostgreSQL connection), `yaml` (configuration)

**Project Structure**:
```
src/import_module/
  parsers/
    junit_parser.py        # Logic for JUnit XML parsing
    json_parser.py         # Logic for JSON log parsing
    text_parser.py         # Logic for plain text log parsing
  classifiers/
    odc_classifier.py      # ODC Defect Type and Trigger classification
    severity_classifier.py # Severity mapping based on rules
    confidence_scorer.py   # Confidence scoring for classifications
  config/
    mapping_rules.yaml     # Severity and ODC keyword mappings from Task 1
  db/
    connector.py           # PostgreSQL connection and insertion logic
  cli.py                   # Command-line interface for file or directory input
  main.py                  # Entry point for module execution
```

**confidence_scorer.py (Confidence Scoring)**:
```python
# src/import_module/classifiers/confidence_scorer.py
def calculate_confidence(evidence_type, match_strength):
    """
    Calculate confidence score for a classification based on evidence.
    Args:
        evidence_type (str): Type of evidence ('tag', 'keyword', 'context', 'none')
        match_strength (str): Strength of match ('strong', 'weak', 'none')
    Returns:
        float: Confidence score between 0 and 1
    """
    if evidence_type == 'tag':
        return 1.0  # Explicit metadata or tag
    elif evidence_type == 'keyword':
        return 0.9 if match_strength == 'strong' else 0.6
    elif evidence_type == 'context':
        return 0.7
    else:
        return 0.3  # Fallback or no clear evidence

def flag_for_review(confidence_score, threshold=0.8):
    """
    Determine if classification needs manual review.
    Args:
        confidence_score (float): Confidence in classification
        threshold (float): Minimum confidence to avoid review
    Returns:
        bool: True if review needed
    """
    return confidence_score < threshold
```

**odc_classifier.py (Updated with Contextual Parsing)**:
```python
# src/import_module/classifiers/odc_classifier.py
import re
import yaml

with open('config/mapping_rules.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)

DEFECT_TYPE_KEYWORDS = CONFIG['custom_keywords']['defect_type']
TRIGGER_KEYWORDS = CONFIG['custom_keywords']['trigger']
ACTIVITY_KEYWORDS = CONFIG['custom_keywords']['activity']
METADATA_PARSING_ENABLED = CONFIG.get('metadata_parsing_enabled', True)

def classify_defect_type(description, metadata):
    """
    Classify Defect Type based on keywords and metadata context.
    Returns: tuple of (str, float) - Defect Type and confidence score
    """
    description = description.lower()
    # Check explicit metadata tags first
    if metadata.get('defect_type'):
        return metadata['defect_type'], 1.0
    # Keyword matching
    for defect_type, keywords in DEFECT_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in description:
                return defect_type, calculate_confidence('keyword', 'strong')
    # Contextual hints from metadata (e.g., HTTP status codes) if enabled
    if METADATA_PARSING_ENABLED and metadata.get('http_status') and re.match(r'5\d{2}', metadata['http_status']):
        return 'Interface', calculate_confidence('context', 'strong')
    return 'Unknown', calculate_confidence('none', 'none')

def classify_trigger(description, metadata):
    """
    Classify Trigger based on keywords and environment context.
    Returns: tuple of (str, float) - Trigger and confidence score
    """
    description = description.lower()
    # Check explicit metadata tags
    if metadata.get('trigger'):
        return metadata['trigger'], 1.0
    # Environment context (e.g., 'prod' suggests Stress/Workload) if enabled
    if METADATA_PARSING_ENABLED:
        env = metadata.get('environment', '').lower()
        if env == 'prod' or env == 'production':
            return 'Stress_Workload', calculate_confidence('context', 'strong')
    # Keyword matching
    for trigger, keywords in TRIGGER_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in description:
                return trigger, calculate_confidence('keyword', 'strong')
    # Source context (e.g., test suite name) if enabled
    if METADATA_PARSING_ENABLED:
        source = metadata.get('source', '').lower()
        if 'unit' in source:
            return 'Unit_Test', calculate_confidence('context', 'weak')
    return 'Unknown', calculate_confidence('none', 'none')

def classify_activity(description, metadata):
    """
    Classify Activity based on keywords and phase context.
    Returns: tuple of (str, float) - Activity and confidence score
    """
    description = description.lower()
    text = description + metadata.get('source', '').lower()
    # Check explicit metadata tags
    if metadata.get('activity'):
        return metadata['activity'], 1.0
    # Phase context if enabled
    if METADATA_PARSING_ENABLED:
        phase = metadata.get('phase', '').lower()
        if phase in ['sprint', 'commit', 'code']:
            return 'Coding', calculate_confidence('context', 'strong')
        elif phase in ['test', 'qa']:
            return 'Testing', calculate_confidence('context', 'strong')
        elif phase in ['design', 'spec']:
            return 'Design', calculate_confidence('context', 'strong')
    # Keyword matching
    for activity, keywords in ACTIVITY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                return activity, calculate_confidence('keyword', 'strong')
    return 'Unknown', calculate_confidence('none', 'none')
```

## Timeline and Milestones
- **Start Date**: Late June 2025
- **Completion Date**: Mid-July 2025 (2 weeks duration)
- **Milestone**: Import Module developed and tested by mid-July 2025, ready for integration with Severity Analysis Engine and API endpoints.

## Risks and Mitigation
- **Risk**: Inconsistent defect data formats across enterprise CI/CD tools may lead to parsing errors or missed ODC attributes.
  - **Mitigation**: Implement robust error handling and fallback logic (Step 3) to flag unparseable defects for manual review. Support a limited set of formats for MVP, expanding post-launch based on beta feedback.
- **Risk**: Performance issues with large defect volumes could delay processing in enterprise environments.
  - **Mitigation**: Optimize batch processing (Step 6) with a flexible performance target of 1-3 minutes for 10,000 defects. Defer complex regex patterns or additional format support to post-MVP (January 2026) if needed to meet timeline.
- **Risk**: Contextual parsing may introduce noise if CI/CD metadata is unreliable.
  - **Mitigation**: Limit regex to high-impact cases (Step 5) and provide a disable toggle for metadata parsing, defaulting to keyword priority. Adjust based on July 2025 test results.

## Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for developing the Import Module for DefectXray's MVP, ensuring seamless ingestion of defect data from CI/CD pipelines for severity classification and ODC integration. 