# Task 4: Implement Severity Analysis Engine

## Task Overview
**Task ID**: T4-MVP-SEV-ENGINE
**Phase**: Strategy
**Owner**: Backend Developer
**Duration**: 2 Weeks (July 2025)
**Priority**: High
**Dependencies**: Task 1 (Severity Mapping Rules and ODC Attribute Logic), Task 2 (PostgreSQL Defect Schema), Task 3 (Import Module)

This task focuses on implementing the Severity Analysis Engine for the DefectXray MVP, which is responsible for classifying defects into severity levels (High, Medium, Low) based on predefined rules and Orthogonal Defect Classification (ODC) attributes (Defect Type and Trigger). The engine refines initial classifications from the Import Module, ensuring accurate and actionable defect prioritization for enterprise CI/CD workflows.

## Objectives
- Develop a rules-based Severity Analysis Engine to assign severity levels to defects using ODC attributes and predefined logic.
- Enable configurability for enterprise customization of severity mappings and trigger influences.
- Integrate with the PostgreSQL database to read initial defect data and update classifications, supporting review flagging for QA oversight.

## Detailed Steps
1. **Review Requirements and Dependencies**:
   - Study the severity mapping rules and ODC attribute logic from 'tasks/task_1_severity_mapping_rules.md', focusing on Defect Type to severity mappings, Trigger influence rules, and fallback logic.
   - Review the PostgreSQL schema from 'tasks/task_2_postgresql_defect_schema.md' to understand data structure (e.g., enum fields for severity, defect_type, trigger).
   - Examine the Import Module output from 'tasks/task_3_import_module.md' to ensure the engine processes initial classifications and review flags correctly.
   - **Output**: Summary of input data expectations and rules to implement (see Rules Implementation below).

2. **Design Severity Analysis Engine Architecture**:
   - Define the engine as a Python-based component (for consistency with Import Module and ease of database integration).
   - Structure the engine with sub-components:
     - **Data Reader**: Retrieves unprocessed or flagged defects from PostgreSQL.
     - **Rules Processor**: Applies severity mapping and Trigger influence rules to assign final severity.
     - **Configuration Manager**: Loads and applies enterprise-specific configurations for mappings and rules.
     - **Data Updater**: Updates defect records in PostgreSQL with final classifications and review status.
   - Plan for scalability to handle batch processing of defects for large CI/CD pipelines.
   - **Output**: Architecture description (see Engine Architecture below).

3. **Implement Data Reader**:
   - Use `psycopg2` or `SQLAlchemy` to query the 'defects' table for records needing analysis:
     - Select defects where `review_flag = TRUE` or a specific processing flag (if added) indicates initial classification needs refinement.
     - Optionally, allow reprocessing of all defects for rule updates via a parameter.
   - Fetch relevant fields: `id`, `severity`, `defect_type`, `trigger`, `description`, `source`, `metadata`, `review_flag`.
   - **Output**: Data retrieval logic (see Code Structure below).

4. **Implement Rules Processor**:
   - Code the logic from Task 1 to assign severity based on Defect Type and adjust with Trigger influence:
     - Map Defect Type to base severity (e.g., Function → High, Assignment → Low) using a configurable dictionary.
     - Adjust severity based on Trigger (e.g., Stress/Workload elevates Medium to High if not already High).
     - Retain initial severity if explicitly tagged (e.g., metadata indicates manual override) and configuration allows.
   - Apply fallback logic if Defect Type or Trigger is 'Unknown', scanning `description` for keywords to reassign values, updating `review_flag` if fallback is used.
   - **Output**: Rules processing logic (see Code Structure below).

5. **Implement Configuration Manager**:
   - Load configuration from a file (e.g., YAML or JSON) to allow enterprise customization:
     - `defect_type_severity_map`: Mapping of Defect Types to default severity levels.
     - `trigger_elevation_list`: List of Triggers that elevate severity (e.g., Stress/Workload).
     - `keyword_lists`: Keywords for fallback classification if Defect Type/Trigger are Unknown.
     - `allow_override`: Boolean to respect manual or tagged classifications over rules.
   - Provide default configuration matching Task 1 mappings for out-of-the-box functionality.
   - **Output**: Configuration structure and loading logic (see Code Structure below).

6. **Implement Data Updater**:
   - Update processed defects in PostgreSQL with final `severity`, `defect_type`, `trigger`, and `review_flag` values.
   - Set `updated_at` timestamp to current time for tracking changes.
   - Optionally, log changes to a history table or file if audit tracking is needed in MVP.
   - Handle update failures by logging errors and marking records for retry.
   - **Output**: Update logic (see Code Structure below).

7. **Add Logging and Error Handling**:
   - Log processing details (e.g., number of defects analyzed, rule application outcomes, errors) to a file or monitoring system.
   - Handle rule application errors (e.g., invalid enum values) by skipping records, logging issues, and flagging for review.
   - **Output**: Logging setup (see Code Structure below).

8. **Test Severity Analysis Engine**:
   - Use sample defect data from Task 3 (or create new set with 10-15 records) covering various Defect Types, Triggers, and initial review_flag states.
   - Run the engine with default and custom configurations to verify:
     - Correct severity assignment per Task 1 rules (e.g., Function with Stress/Workload → High).
     - Proper handling of Unknown values with fallback logic (e.g., 'crash' in description updates Unknown to Function/High).
     - Database updates reflect final classifications and timestamps.
   - Adjust logic or configuration defaults based on test outcomes.
   - **Output**: Test results and sample data scenarios (to be documented post-testing).

## Outputs and Deliverables
- **Engine Architecture Description**: Overview of Severity Analysis Engine structure and components.
- **Rules Implementation Summary**: Documentation of implemented severity and ODC rules from Task 1.
- **Code Structure and Logic**: Detailed pseudocode or code snippets for data reading, rules processing, configuration, and updating.
- **Configuration Format**: Structure for customizable severity mappings and rules.
- **Test Results**: Results from running the engine on sample data, verifying rule application and database updates (to be added post-testing).

## Engine Architecture
The Severity Analysis Engine is a Python-based component with the following sub-components:
- **Data Reader**: Queries PostgreSQL for defects needing analysis (e.g., `review_flag = TRUE`).
- **Rules Processor**: Applies severity mapping and Trigger influence rules, with fallback logic for Unknown values.
- **Configuration Manager**: Loads enterprise-specific mappings and rules from a configuration file.
- **Data Updater**: Updates defect records in PostgreSQL with final classifications.

**Flow**:
1. Data Reader fetches unprocessed or flagged defects from PostgreSQL.
2. Rules Processor applies Task 1 rules using loaded configuration to assign final severity and ODC attributes.
3. Data Updater stores updated classifications back to PostgreSQL.
4. Log results and errors at each step for monitoring.

## Rules Implementation Summary
| **Rule Type**            | **Logic**                                                                 | **Source** (Task 1)          |
|--------------------------|---------------------------------------------------------------------------|------------------------------|
| Defect Type Mapping      | Function → High; Interface, Checking, Timing/Serialization, Algorithm → Medium; Assignment, Build/Package/Merge, Documentation → Low | Severity Mapping Table       |
| Trigger Influence        | Stress/Workload, Recovery, Boundary Conditions elevate severity by 1 if not High; Unit Test, Function Test, System Test neutral; Rare Situation may lower if minor | Trigger Influence Rules      |
| Fallback for Unknown     | Scan description for keywords (e.g., 'crash' → Function/High); default Medium if no match; set review_flag = True | Fallback Logic               |

**Configuration Overrides**: Allow enterprises to remap Defect Type severity (e.g., Assignment → Medium) and toggle Trigger elevation list via config file.

## Code Structure and Logic
**Target Language**: Python
**Key Libraries**: `psycopg2` (for PostgreSQL), `yaml` or `json` (for configuration)

**Pseudocode**:
```python
# Severity Analysis Engine Main Logic
import psycopg2
import yaml
from typing import List, Dict, Any

# Default Configuration (can be overridden by file)
DEFAULT_CONFIG = {
    'defect_type_severity_map': {
        'Function': 'High',
        'Interface': 'Medium',
        'Checking': 'Medium',
        'Assignment': 'Low',
        'Timing/Serialization': 'Medium',
        'Build/Package/Merge': 'Low',
        'Documentation': 'Low',
        'Algorithm': 'Medium',
        'Unknown': 'Medium'
    },
    'trigger_elevation_list': ['Stress/Workload', 'Recovery', 'Boundary Conditions'],
    'keyword_lists': {
        'high': ['crash', 'failure', 'critical', 'core', 'major'],
        'medium': ['error', 'bug', 'issue', 'performance', 'timeout'],
        'low': ['typo', 'comment', 'doc', 'minor']
    },
    'allow_override': True
}

class SeverityAnalysisEngine:
    def __init__(self, db_config: Dict, config_file: str = None):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.config = self._load_config(config_file)
        self.logs = []

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from file or use default."""
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f) or DEFAULT_CONFIG
            except Exception as e:
                self.logs.append(f"Config load error: {str(e)}, using default")
        return DEFAULT_CONFIG

    def analyze_defects(self, batch_size: int = 100, reprocess_all: bool = False) -> int:
        """Analyze defects needing classification. Returns count of processed defects."""
        defects = self._read_defects(batch_size, reprocess_all)
        processed_count = 0
        for defect in defects:
            updated_defect = self._process_rules(defect)
            if self._update_defect(updated_defect):
                processed_count += 1
            else:
                self.logs.append(f"Failed to update defect ID {defect['id']}")
        self.conn.commit()
        self.logs.append(f"Processed {processed_count} defects")
        return processed_count

    def _read_defects(self, batch_size: int, reprocess_all: bool) -> List[Dict]:
        """Read defects from database for analysis."""
        try:
            query = "SELECT id, severity, defect_type, trigger, description, source, metadata, review_flag FROM defects WHERE review_flag = TRUE"
            if reprocess_all:
                query = "SELECT id, severity, defect_type, trigger, description, source, metadata, review_flag FROM defects"
            query += f" LIMIT {batch_size}"
            self.cursor.execute(query)
            columns = ['id', 'severity', 'defect_type', 'trigger', 'description', 'source', 'metadata', 'review_flag']
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            self.logs.append(f"Read error: {str(e)}")
            return []

    def _process_rules(self, defect: Dict) -> Dict:
        """Apply severity and ODC classification rules."""
        # Check for manual override if allowed
        if self.config['allow_override'] and 'override' in defect['metadata'].get('tags', {}):
            severity = defect['metadata']['tags'].get('override_severity', defect['severity'])
            defect_type = defect['metadata']['tags'].get('override_type', defect['defect_type'])
            trigger = defect['metadata']['tags'].get('override_trigger', defect['trigger'])
            review_flag = False
        else:
            # Handle Unknown Defect Type with fallback
            defect_type = defect['defect_type']
            severity = defect['severity']
            trigger = defect['trigger']
            review_flag = defect['review_flag']
            
            if defect_type == 'Unknown':
                defect_type, severity = self._fallback_defect_type(defect['description'])
                review_flag = True
            else:
                severity = self.config['defect_type_severity_map'].get(defect_type, 'Medium')
            
            # Handle Unknown Trigger with fallback
            if trigger == 'Unknown':
                trigger = self._fallback_trigger(defect['description'], defect['source'])
                review_flag = True
            
            # Apply Trigger influence on severity
            if trigger in self.config['trigger_elevation_list'] and severity != 'High':
                severity = 'High' if severity == 'Medium' else 'Medium'

        defect.update({
            'severity': severity,
            'defect_type': defect_type,
            'trigger': trigger,
            'review_flag': review_flag
        })
        return defect

    def _fallback_defect_type(self, description: str) -> tuple:
        """Fallback logic for Unknown Defect Type."""
        desc = description.lower()
        for sev, keywords in self.config['keyword_lists'].items():
            if any(k in desc for k in keywords):
                if sev == 'high':
                    return 'Function', 'High'
                elif sev == 'medium':
                    return 'Interface', 'Medium'
                elif sev == 'low':
                    return 'Assignment', 'Low'
        return 'Unknown', 'Medium'

    def _fallback_trigger(self, description: str, source: str) -> str:
        """Fallback logic for Unknown Trigger."""
        desc = description.lower()
        src = source.lower()
        if 'test' in src or 'test' in desc:
            if 'unit' in src or 'unit' in desc:
                return 'Unit Test'
            elif 'function' in src or 'feature' in desc:
                return 'Function Test'
            return 'System Test'
        elif 'prod' in src or 'load' in desc or 'stress' in desc:
            return 'Stress/Workload'
        elif 'recover' in desc:
            return 'Recovery'
        return 'Unknown'

    def _update_defect(self, defect: Dict) -> bool:
        """Update defect record in database with final classification."""
        try:
            self.cursor.execute("""
                UPDATE defects
                SET severity = %s, defect_type = %s, trigger = %s, review_flag = %s, updated_at = NOW()
                WHERE id = %s
            """, (
                defect['severity'],
                defect['defect_type'],
                defect['trigger'],
                defect['review_flag'],
                defect['id']
            ))
            return True
        except Exception as e:
            self.logs.append(f"Update error for ID {defect['id']}: {str(e)}")
            return False

    def save_logs(self, log_file: str):
        """Save processing logs to file."""
        with open(log_file, 'a') as f:
            f.write('\n'.join(self.logs) + '\n')
        self.logs = []

# Usage Example
if __name__ == "__main__":
    db_config = {'dbname': 'defectxray', 'user': 'user', 'password': 'pass', 'host': 'localhost'}
    engine = SeverityAnalysisEngine(db_config, config_file='severity_config.yaml')
    count = engine.analyze_defects(batch_size=100)
    engine.save_logs('analysis_log.txt')
    print(f"Analyzed {count} defects")
```

## Timeline and Milestones
- **Start Date**: Early July 2025
- **Completion Date**: Mid-July 2025 (2 weeks duration)
- **Milestone**: Severity Analysis Engine implemented and tested by mid-July 2025, ready for integration with Import Module and Reporting Dashboard.

## Risks and Mitigation
- **Risk 1: Rule Misalignment with Enterprise Needs** - If default severity mappings do not match enterprise priorities, mitigation is to rely on configuration overrides and gather beta feedback for rule refinement. Ensure configuration is well-documented for admins.
- **Risk 2: Performance with Large Defect Volumes** - If processing large batches impacts CI/CD feedback loops, mitigation is to implement batch size limits and asynchronous processing, prioritizing recent or high-severity defects. Optimize queries during testing.
- **Risk 3: Incorrect Fallback Classifications** - If keyword-based fallback logic misclassifies defects, mitigation is to flag such records for review (`review_flag = TRUE`) and iteratively improve keyword lists based on test and beta results.

## Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for implementing the Severity Analysis Engine for DefectXray's MVP, ensuring accurate defect classification for enterprise CI/CD workflows. 