# Task 1: Define Severity Mapping Rules and ODC Attribute Logic

## Task Overview
**Task ID**: T1-MVP-SEV-ODC
**Phase**: Strategy
**Owner**: Technical Lead / Backend Developer
**Duration**: 1 Week (June 2025)
**Priority**: High
**Dependencies**: ODC Knowledge Base from foundational paper review

This task focuses on defining the rules and logic for mapping software defects to severity levels (High, Medium, Low) and integrating Orthogonal Defect Classification (ODC) attributes (Defect Type and Trigger) for the DefectXray MVP. The output will guide the development of the Severity Analysis Engine and Import Module, ensuring consistent and actionable defect classification for enterprise CI/CD workflows.

## Objectives
- Establish clear, deterministic rules for assigning severity levels to defects based on their characteristics and impact.
- Define logic for classifying defects using ODC Defect Type and Trigger attributes to provide process feedback.
- Document mappings and logic in a format usable for coding the Severity Analysis Engine and for user reference.

## Detailed Steps
1. **Review ODC Attribute Definitions**:
   - Revisit key sections of 'Orthogonal Defect Classification - A Concept for In-Process Measurements' to confirm definitions and examples for Defect Type (e.g., Function, Assignment, Interface) and Trigger (e.g., Workload, Recovery, Boundary Conditions).
   - Compile a reference list of Defect Types and Triggers with brief descriptions and associated process stages (e.g., Function with Design).
   - **Output**: Reference table in this document (see below).

2. **Define ODC Defect Type and Activity to Severity Mapping**:
   - Create a mapping table or configuration file linking ODC Defect Types and Activities to default severity levels based on their impact:
     - **Defect Type Mappings**:
       - **Function**: High (affects critical capabilities or new features).
       - **Interface**: Medium (affects interactions between modules).
       - **Build/Package/Merge**: High (can halt development or deployment).
       - **Documentation**: Low (no immediate operational impact).
       - **Assignment**: Low (minor initialization issues).
       - **Checking**: Medium (error handling flaws).
       - **Algorithm**: Medium (logic or efficiency issues).
       - **Timing/Serialization**: High (concurrency or performance-critical issues).
     - **Activity Mappings** (phase of defect introduction):
       - **Coding**: Medium (defects introduced during implementation).
       - **Testing**: Low (defects found but not introduced in testing, often minor).
       - **Design**: High (defects from design flaws, significant impact).
   - Introduce a weighted scoring system for Activity influence, combining Defect Type and Activity to compute a severity score (0-100), then mapping to High (>66), Medium (33-66), or Low (<33). Default weights are 70% for Defect Type and 30% for Activity, configurable by enterprises via YAML (e.g., `defect_type_weight: 0.7, activity_weight: 0.3`).
     ```python
     def calculate_severity_score(defect_type, activity):
         type_weights = {'Function': 100, 'Interface': 50, 'Assignment': 20, 'Build_Package_Merge': 100, 'Documentation': 20, 'Checking': 50, 'Algorithm': 50, 'Timing_Serialization': 100}
         activity_weights = {'Design': 80, 'Coding': 50, 'Testing': 20}
         score = (0.7 * type_weights.get(defect_type, 50) + 
                  0.3 * activity_weights.get(activity, 50))
         if score > 66: return 'High'
         elif score > 33: return 'Medium'
         else: return 'Low'
     ```
   - Document weights and score ranges in the configuration file for enterprise customization, with examples for use cases (e.g., increasing Activity weight for design-heavy projects).
   - **Output**: Configuration file or code snippet for Defect Type and Activity to severity mapping with weighted scoring (see Implementation Specification below).

3. **Define Severity Mapping for Defect Types**:
   - Analyze each ODC Defect Type for its typical impact on software functionality and process stage to assign a default severity level:
     - **High Severity**: Defects with significant impact on core functionality or requiring major design changes (e.g., Function - affects significant capability, often found in design).
     - **Medium Severity**: Defects impacting specific components or interactions, requiring moderate fixes (e.g., Interface - module interaction issues; Timing/Serialization - concurrency issues).
     - **Low Severity**: Defects with minor impact, often localized or documentation-related (e.g., Assignment - few lines of code; Documentation - publications errors).
   - Document rationale for each mapping, considering enterprise priorities (e.g., functionality critical for CI/CD stability).
   - **Output**: Severity mapping table for Defect Types (see below).

4. **Define Trigger Influence on Severity**:
   - Assess how ODC Triggers can modify severity based on the context in which a defect surfaces:
     - **Elevate Severity**: Triggers indicating high-stress or critical conditions (e.g., Workload/Stress - system under load; Recovery - failure recovery scenarios) may increase severity by one level (e.g., Medium to High).
     - **Neutral Impact**: Triggers like Unit Test or Function Test typically do not alter severity as they are expected verification stages.
     - **Lower Severity**: Rare or edge-case triggers (e.g., Rare Situation) may reduce severity if impact is minimal, though rarely applied in MVP.
   - Establish a rule for Trigger adjustment: If a Trigger is associated with field or stress conditions and severity is not already High, increase by one level.
   - **Output**: Trigger influence rules (see below).

5. **Handle Missing or Ambiguous Data**:
   - Define fallback rules for defects lacking clear ODC metadata from CI/CD inputs:
     - Use keyword analysis in defect descriptions (e.g., 'crash' or 'failure' suggests Function/High; 'typo' suggests Documentation/Low).
     - Default to Medium severity if no clear indicators exist, flagging for QA override in the system.
     - For Triggers, default to 'Unknown' if not specified, with no severity adjustment.
   - **Output**: Fallback logic documentation (see below).

6. **Add Custom Keyword Configurations**:
   - Enhance the configuration structure to allow enterprises to define custom keyword lists for Defect Type, Trigger, and Activity mappings, enabling adaptability to specific terminologies.
   - Specify that custom keyword configurations will be managed via a simple admin UI (for enterprise admins to input keywords directly) or config file uploads (for bulk updates), ensuring usability.
   - Add a basic validation script in the admin UI or YAML parser to detect and flag overlapping keywords across categories (e.g., warn if 'crash' appears in both Function and Interface) without blocking configuration saves, to avoid frustrating users. Implement in Python as part of the configuration loading in the Severity Analysis Engine:
     ```python
     def validate_keywords(config):
         keyword_map = {}
         for category, keywords in config['custom_keywords'].items():
             for key, terms in keywords.items():
                 for term in terms:
                     if term in keyword_map and keyword_map[term] != (category, key):
                         print(f"Warning: Keyword '{term}' overlaps in {keyword_map[term]} and {category}:{key}")
                     keyword_map[term] = (category, key)
     ```
   - For MVP, provide a detailed user guide in the documentation with sample YAML files and notes on managing keyword overlaps to minimize classification errors. Plan for stricter enforcement with an advanced UI for conflict resolution in post-MVP (January 2026).
   - Example configuration addition in YAML format:
     ```yaml
     custom_keywords:
       defect_type:
         Function: ["crash", "failure", "critical", "payment"]
         Interface: ["api", "endpoint", "communication"]
       trigger:
         Stress/Workload: ["load", "peak", "traffic"]
         Unit Test: ["unit", "junit", "testcase"]
       activity:
         Coding: ["sprint", "commit", "code"]
         Testing: ["test", "qa", "verify"]
         Design: ["design", "architecture", "spec"]
     ```
   - Ensure these custom keywords can override or supplement default mappings during defect classification.
   - **Output**: Updated configuration specification with custom keyword support and validation warnings (see Implementation Specification below).

7. **Validate Rules with Sample Defects and Pre-Beta Data**:
   - Test the defined rules using an expanded set of 20-30 sample defects covering various Defect Types, Triggers, Activities, and edge cases (e.g., ambiguous descriptions, missing data, multilingual descriptions, truncated logs). Include both synthetic data and real-world defect data from 3-4 enterprise CI/CD pipelines (e.g., Jenkins, GitLab, CircleCI) to simulate variability. Coordinate with potential beta users in June 2025 to collect anonymized data.
   - Develop a data collection plan to engage beta users, targeting outreach by June 1, 2025, to collect data by June 7, 2025. Provide a CSV template (columns: description, source, metadata, expected severity) for standardized submissions.
   - Implement a Python script to automate validation, calculating precision/recall for severity assignments against a manually labeled ground truth, targeting at least 80% precision:
     ```python
     def validate_rules(defects, ground_truth):
         correct = 0
         for defect, expected in zip(defects, ground_truth):
             result = classify_defect(defect)
             if result.severity == expected.severity:
                 correct += 1
         precision = correct / len(defects)
         print(f"Precision: {precision:.2%}")
         return precision
     ```
   - Adjust mappings or fallback logic if precision falls below 80% (e.g., frequent misclassification of 'Function' as 'Interface'). Use statistical analysis to measure rule accuracy.
   - Test configurable severity weights (see Step 3) during validation to ensure flexibility for enterprise use cases.
   - Plan a second validation round in July 2025 with broader data during Task 3 testing to refine rules further.
   - **Output**: Validation report with test results, rule adjustments, and data collection plan (to be documented post-validation).

8. **Document for Implementation**:
   - Format the finalized rules and logic into a clear specification for developers to code into the Severity Analysis Engine.
   - Include configurable parameters (e.g., severity thresholds, Trigger elevation toggle) for enterprise customization.
   - **Output**: Implementation specification section (see below).

## Outputs and Deliverables
- **ODC Reference Table**: A concise table of Defect Types and Triggers with descriptions and process associations.
- **Severity Mapping Table**: Mapping of each Defect Type to a default severity level with rationale.
- **Trigger Influence Rules**: Rules for how Triggers modify severity, with conditions and examples.
- **Fallback Logic**: Guidelines for handling incomplete defect data.
- **Sample Defect Test Results**: Results from applying rules to sample defects, targeting 80% precision (to be added post-validation).
- **Implementation Specification**: Detailed logic and pseudocode for developers to implement in the Severity Analysis Engine.
- **Data Collection Plan**: Plan for coordinating with beta users to collect anonymized defect data for validation.

## ODC Reference Table
| **Attribute**      | **Category**              | **Description**                                      | **Process Association**      |
|--------------------|---------------------------|-----------------------------------------------------|------------------------------|
| Defect Type        | Function                 | Affects significant capability or interfaces        | High-Level Design            |
| Defect Type        | Assignment               | Minor code change (e.g., initialization)            | Low-Level Design/Code        |
| Defect Type        | Interface                | Module interaction errors                          | Low-Level Design             |
| Defect Type        | Checking                 | Failed data/value validation                       | Code                         |
| Defect Type        | Timing/Serialization     | Concurrency or resource management issues          | Low-Level Design             |
| Defect Type        | Build/Package/Merge      | Library or version control errors                  | Library Tools                |
| Defect Type        | Documentation            | Errors in publications or notes                    | Publications                 |
| Defect Type        | Algorithm                | Efficiency/correctness in algorithms               | Low-Level Design             |
| Trigger            | Unit Test                | Found in unit testing                              | Unit Test Stage              |
| Trigger            | Function Test            | Found in feature testing                           | Function Test Stage          |
| Trigger            | System Test              | Found in end-to-end testing                        | System Test Stage            |
| Trigger            | Stress/Workload          | Found under high load or stress                    | System Test/Field            |
| Trigger            | Recovery                 | Found during failure recovery                      | System Test/Field            |
| Trigger            | Boundary Conditions      | Found at edge cases or limits                      | System Test/Field            |
| Trigger            | Rare Situation           | Found in uncommon scenarios                        | Design Review/Field          |
| Trigger            | Unknown                  | Trigger not identified                             | N/A                          |
| Activity           | Coding                   | Defect introduced during implementation            | Coding Phase                 |
| Activity           | Testing                  | Defect found during testing (not introduced)       | Testing Phase                |
| Activity           | Design                   | Defect introduced during design or spec            | Design Phase                 |

## Severity Mapping Table for Defect Types
| **Defect Type**            | **Default Severity** | **Rationale**                                                                 |
|----------------------------|----------------------|------------------------------------------------------------------------------|
| Function                  | High                | Significant impact on core functionality, often requiring design changes.    |
| Interface                 | Medium              | Affects module interactions, moderate scope of impact.                      |
| Checking                  | Medium              | Validation failures can cause operational issues, moderate impact.          |
| Assignment                | Low                 | Localized, minor code fixes with limited impact.                           |
| Timing/Serialization      | Medium              | Concurrency issues can disrupt operations, moderate to high risk.           |
| Build/Package/Merge       | Low                 | Build errors often procedural, low functional impact.                      |
| Documentation             | Low                 | Minimal impact on runtime, affects only reference materials.               |
| Algorithm                 | Medium              | Efficiency issues can degrade performance, moderate impact.                |

## Trigger Influence Rules
- **Elevation Rule**: If Trigger is Stress/Workload, Recovery, or Boundary Conditions AND severity is not already High, increase severity by one level (e.g., Medium to High). Rationale: These conditions indicate critical real-world impact.
- **Neutral Rule**: Triggers like Unit Test, Function Test, or System Test do not modify severity. Rationale: These are expected verification stages, impact already captured by Defect Type.
- **Reduction Rule**: Rare Situation may reduce severity by one level if Defect Type impact is minor (e.g., Medium to Low), but apply cautiously in MVP. Rationale: Rare cases may not warrant high priority.
- **Example**: A defect classified as Interface (Medium) with Trigger Stress/Workload is elevated to High due to real-world stress impact.

## Fallback Logic for Missing/Ambiguous Data
- **Defect Type Fallback**:
  - Scan defect description or title for keywords:
    - High: 'crash', 'failure', 'critical', 'core', 'major' → Function.
    - Medium: 'error', 'bug', 'issue', 'performance', 'timeout' → Interface/Timing/Algorithm.
    - Low: 'typo', 'comment', 'doc', 'minor' → Assignment/Documentation.
  - If no keywords match, default to 'Unknown' Defect Type and assign Medium severity with a flag for QA review.
- **Trigger Fallback**:
  - If no Trigger data available (e.g., no test context), set to 'Unknown' with no severity adjustment.
  - If source indicates field data (e.g., production logs), infer 'Stress/Workload' or 'Recovery' if keywords like 'load' or 'crash' appear.
- **Severity Fallback**: If neither Defect Type nor Trigger can be determined, default to Medium severity to balance risk, flagged for manual override.

## Implementation Specification
**Target Component**: Severity Analysis Engine (Python)
**Logic Overview**:
- Input: Defect object with fields (description, source, tags, metadata).
- Step 1: Assign Defect Type
  - Check for explicit tags (e.g., 'type:function') from CI/CD input; if present, use directly.
  - Else, apply keyword matching on description using fallback logic.
- Step 2: Assign Trigger
  - Check for test stage or context (e.g., 'stage:unit-test') in metadata; map to corresponding Trigger.
  - If field data indicated (e.g., 'source:production'), infer Stress/Workload or Recovery based on keywords.
  - Else, set to Unknown.
- Step 3: Assign Activity
  - Check for phase or sprint context (e.g., 'phase:coding') in metadata; map to corresponding Activity.
  - Else, infer from keywords in description or source (e.g., 'sprint' or 'commit' → Coding).
  - Default to Unknown if unclear.
- Step 4: Determine Base Severity
  - Use Severity Mapping Table to assign base severity from Defect Type, with Activity as a secondary influence (e.g., Design elevates to High if not already).
- Step 5: Adjust Severity by Trigger
  - Apply Trigger Influence Rules: If Trigger in [Stress/Workload, Recovery, Boundary Conditions] and severity < High, increment severity by 1.
- Step 6: Flag for Review
  - If any field is Unknown or fallback logic used, set review_flag = True for QA override.
- Output: Updated defect object with severity, defect_type, trigger, activity, review_flag.

**Pseudocode**:
```python
# Severity Analysis Engine Logic
def classify_defect(defect):
    # Step 1: Assign Defect Type
    if defect.tags.get('type') in defect_type_map:
        defect_type = defect.tags['type']
    else:
        defect_type = keyword_match(defect.description, type_keywords)
        if not defect_type:
            defect_type = 'Unknown'
    
    # Step 2: Assign Trigger
    if defect.metadata.get('stage') in trigger_map:
        trigger = trigger_map[defect.metadata['stage']]
    elif 'production' in defect.source.lower():
        trigger = infer_field_trigger(defect.description)
    else:
        trigger = 'Unknown'
    
    # Step 3: Assign Activity
    if defect.metadata.get('phase') in activity_map:
        activity = activity_map[defect.metadata['phase']]
    else:
        activity = keyword_match(defect.description + defect.source, activity_keywords)
        if not activity:
            activity = 'Unknown'
    
    # Step 4: Base Severity from Defect Type and Activity
    severity = defect_type_severity_map.get(defect_type, 'Medium')
    if activity == 'Design' and severity != 'High':
        severity = 'High'
    elif activity == 'Testing' and severity == 'High':
        severity = 'Medium'
    review_flag = (defect_type == 'Unknown' or activity == 'Unknown')
    
    # Step 5: Adjust Severity by Trigger
    if trigger in ['Stress/Workload', 'Recovery', 'Boundary Conditions'] and severity != 'High':
        severity = increment_severity(severity)
        review_flag = True if trigger inferred else review_flag
    
    # Step 6: Finalize
    defect.severity = severity
    defect.defect_type = defect_type
    defect.trigger = trigger
    defect.activity = activity
    defect.review_flag = review_flag or (trigger == 'Unknown')
    return defect

# Helper Functions
 def keyword_match(text, keywords):
     for category, terms in keywords.items():
         if any(term in text.lower() for term in terms):
             return category
     return None
 
 def increment_severity(current):
     if current == 'Low': return 'Medium'
     if current == 'Medium': return 'High'
     return 'High'
 
 def infer_field_trigger(text):
     if any(term in text.lower() for term in ['load', 'stress', 'crash']):
         return 'Stress/Workload'
     if 'recover' in text.lower():
         return 'Recovery'
     return 'Unknown'
```

**Configurable Parameters**:
- `defect_type_severity_map`: Dictionary mapping Defect Types to default severity, editable by enterprise admins (e.g., change Assignment from Low to Medium).
- `trigger_elevation_list`: List of Triggers that elevate severity, toggleable (e.g., disable Boundary Conditions elevation).
- `keyword_lists`: Adjustable keyword sets for fallback logic to match enterprise terminology.
- `defect_type_weight`: Weight for Defect Type influence in severity calculation.
- `activity_weight`: Weight for Activity influence in severity calculation.

**Configuration File Structure**:
```yaml
severity_mappings:
  defect_type:
    Function: High
    Interface: Medium
    Build_Package_Merge: High
    Documentation: Low
    Assignment: Low
    Checking: Medium
    Algorithm: Medium
    Timing_Serialization: High
  activity:
    Coding: Medium
    Testing: Low
    Design: High
  trigger_influence:
    Stress_Workload: elevate
    Unit_Test: maintain
    Function_Test: maintain
    System_Test: elevate_if_high
    Boundary_Conditions: elevate_if_medium
    Configuration: maintain
    Startup_Shutdown: elevate_if_high
    Recovery: elevate
    Standards_Violation: maintain
  fallback:
    default_severity: Medium
    review_flag: true
  weights:
    defect_type_weight: 0.7
    activity_weight: 0.3
custom_keywords:
  defect_type:
    Function: ["crash", "failure", "critical", "payment"]
    Interface: ["api", "endpoint", "communication"]
    Build_Package_Merge: ["build", "merge", "package", "deploy"]
    Documentation: ["doc", "comment", "readme"]
    Assignment: ["assign", "variable", "init"]
    Checking: ["check", "validation", "if"]
    Algorithm: ["logic", "calculate", "math"]
    Timing_Serialization: ["race", "deadlock", "thread", "sync"]
  trigger:
    Stress_Workload: ["load", "peak", "traffic", "overload"]
    Unit_Test: ["unit", "junit", "testcase", "mock"]
    Function_Test: ["functional", "feature", "spec"]
    System_Test: ["system", "integration", "e2e"]
    Boundary_Conditions: ["boundary", "edge", "limit", "max"]
    Configuration: ["config", "setting", "env", "property"]
    Startup_Shutdown: ["start", "boot", "shutdown", "restart"]
    Recovery: ["recover", "failover", "backup", "restore"]
    Standards_Violation: ["standard", "compliance", "violation", "policy"]
  activity:
    Coding: ["sprint", "commit", "code", "implement"]
    Testing: ["test", "qa", "verify", "validation"]
    Design: ["design", "architecture", "spec", "blueprint"]
```

## Validation and Testing
- Post-definition, apply rules to 5-10 sample defects covering various Defect Types and Triggers.
- Expected outcomes: Function with Stress/Workload = High; Assignment with Unit Test = Low.
- Adjust mappings or rules if outcomes misalign with enterprise impact expectations.
- Document test results in this file under 'Sample Defect Test Results' section (to be added).

## Timeline and Milestones
- **Start Date**: Early June 2025
- **Completion Date**: Mid-June 2025 (1 week duration)
- **Milestone**: Severity mapping rules and custom keyword configurations defined and validated by mid-June 2025, ready for integration into the Severity Analysis Engine and Import Module.

## Risks and Mitigation
- **Risk 1: Over-Simplification of Severity Mapping** - If mappings (e.g., Function always High) do not capture nuanced enterprise impacts, mitigation is to allow rule overrides in the engine and plan for beta feedback to refine mappings.
- **Risk 2: Incomplete ODC Data from CI/CD Tools** - If inputs lack metadata for accurate Defect Type/Trigger assignment, fallback logic ensures a default classification, with flagging for manual review to maintain accuracy.
- **Risk 3: Variability in Enterprise Terminology** - If enterprise defect descriptions use inconsistent or unique terminology, keyword-based classification may fail. Mitigation is to leverage custom keyword configurations and prioritize pre-beta validation with real data from target users to refine mappings early.

## Sample Defect Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for defining the core logic of DefectXray's MVP severity classification and ODC integration, ensuring alignment with enterprise needs and project timelines. 