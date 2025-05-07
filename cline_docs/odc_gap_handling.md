# ODC Gap Handling Strategy for DefectXray

## Purpose
This document outlines the strategy for handling gaps in Orthogonal Defect Classification (ODC) metadata during the MVP phase (August 2025) and post-MVP phases (November 2025 onward) of DefectXray. The goal is to ensure reliable classification despite incomplete data from enterprise tools like Jira and Sentry, addressing challenges identified in planning discussions.

## MVP Phase: Heuristic Rules (August 2025)
For the MVP, simple heuristic rules will be applied to handle missing ODC attributes during defect import (Task 3: Import Module). These rules prioritize usability and minimal user disruption:
- **Defect Type**: If missing, set to 'Unknown' and prompt user via dashboard notification to specify (e.g., 'Functional', 'Performance'). Default to 'Functional' if no input within 48 hours for reporting continuity.
- **Activity**: If missing, infer from defect description using keyword matching (e.g., 'test' or 'QA' suggests 'Testing'; 'deploy' suggests 'Deployment'). If no match, set to 'Unknown' and prompt user.
- **Source**: If missing, set to the originating tool (e.g., 'Jira', 'Sentry') as detected during import. If manual upload (CSV/JSON), set to 'Manual' and prompt user for clarification.

These rules will be implemented in the Import Module (Task 3) to ensure at least basic ODC metadata is available for severity analysis and reporting.

## Validation Plan
- **Beta Testing (July 2025)**: Validate heuristic rules with 1-2 beta users using real defect data (target: <10% misclassification rate for inferred attributes). Adjust keyword lists and default behaviors based on feedback.
- **Metrics**: Track user override frequency for defaults (target: <20% overrides) and accuracy of inferred values (target: 80% match with user corrections).

## Post-MVP Phase: Machine Learning Inference (November 2025 Onward)
Post-MVP, machine learning (ML) models will be trained on beta user data to infer missing ODC attributes more accurately, reducing user prompts and improving automation:
- **Priority Attributes for ML**: Focus on inferring 'Trigger' and 'Impact' based on defect description, severity, and other metadata. Use beta feedback to identify most impactful attributes for enterprise process insights.
- **Training Data**: Collect anonymized defect data from beta phase (August-October 2025), targeting 10,000+ defects with user-corrected ODC labels for model training.
- **Integration**: Deploy ML inference as an optional feature in the Severity Analysis Engine (Task 1), allowing users to toggle between heuristic and ML-based gap filling by Q1 2026.

## Timeline
- **May 2025**: Finalize heuristic rules in this document and integrate into Task 3 requirements.
- **July 2025**: Validate rules during beta prototype demo, refine based on feedback.
- **August 2025**: Deploy heuristic-based gap handling in MVP.
- **November 2025**: Begin ML model training for advanced inference, targeting deployment by March 2026.

## Dependencies
- **Task 3 (Import Module)**: Must implement heuristic rules for data ingestion.
- **Task 1 (Severity Analysis Engine)**: Must support user overrides for ODC attributes and integrate ML inference post-MVP.
- **Beta Feedback**: Critical for refining heuristics and prioritizing ML attributes.

## Changelog
- May 2025: Initial draft created during Strategy phase based on user feedback for ODC integration. 