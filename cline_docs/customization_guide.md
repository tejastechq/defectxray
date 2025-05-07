# Customization Guide for DefectXray MVP

## Purpose
This document outlines customization options for enterprise users of DefectXray, enabling tailored defect severity analysis and ODC integration to meet diverse CI/CD workflow needs for the MVP launch in August 2025.

## Customization Areas
The following components of DefectXray can be customized to align with enterprise-specific requirements:

### 1. Severity Mapping Rules (Task 1)
- **Custom Rules**: Users can define custom severity mapping rules based on defect attributes (e.g., description keywords, ODC Defect Type) beyond predefined rules.
- **Weight Adjustments**: Modify the weighting of ODC attributes in severity calculation (default: 70% Defect Type, 30% Activity) to reflect enterprise priorities (e.g., increase Activity weight to 50% for testing-heavy workflows).
- **Validation Warnings**: System alerts users to potential rule conflicts (e.g., overlapping keywords for High and Medium severity) during customization.

### 2. Import Module Settings (Task 3)
- **Batch Size Configuration**: Adjust batch processing sizes (range: 100-10,000 defects per batch) to balance speed and system load based on enterprise data volume.
- **Metadata Parsing Options**: Enable or disable complex metadata parsing (e.g., skip ODC Trigger extraction) for faster import during MVP, with toggle available in settings.
- **Tool-Specific Mapping**: Define custom field mappings for supported tools (e.g., map Jira 'Priority' to DefectXray 'Severity Hint') to improve import accuracy.

### 3. Reporting Dashboard (Task 5)
- **Filter Presets**: Save frequently used filter combinations (e.g., 'High Severity + Jira') as presets for quick access during defect analysis.
- **Chart Customization**: Select preferred chart types (e.g., bar vs. pie for severity distribution) and set data display limits (e.g., top 5 categories) to optimize dashboard readability.

### 4. API Integration (Task 6)
- **Rate Limit Adjustment**: Enterprise admins can request higher rate limits (default: 100/minute, up to 500/minute) for API endpoints to support larger automation workflows.
- **Custom Scopes**: Define specific OAuth scopes for API access (e.g., read-only for reporting, write for import) to restrict third-party tool permissions.

## Implementation in MVP
- **UI/Configuration File**: Customization will be accessible via a settings panel in the dashboard UI or through a configuration file (e.g., JSON) for API-driven setups, targeting implementation by July 2025.
- **Documentation**: Each customization option will include inline help or a linked guide to explain impact (e.g., increasing batch size may slow processing but reduce system strain).
- **Validation**: System will validate custom inputs (e.g., ensure weight percentages sum to 100%) to prevent configuration errors.

## Testing and Feedback
- **Beta Phase (July 2025)**: Test customization options with a simulated enterprise dataset (5,000 defects, varied CI/CD tools) to ensure usability and performance.
- **Feedback Collection**: Gather beta user input on customization utility and ease of use, targeting 75% satisfaction rate, with iterative refinements before MVP launch.

## Post-MVP Enhancements (January 2026 Onward)
- **Advanced Rule Editor**: Introduce a drag-and-drop interface for severity rule creation with real-time preview of classification impact.
- **Profile Templates**: Offer pre-configured customization profiles for common enterprise types (e.g., Agile, DevOps) to simplify onboarding.
- **API-Driven Customization**: Enable full customization via API for automated provisioning in large-scale deployments.

## Timeline
- **May 2025**: Finalize customization options in this guide.
- **June 2025**: Integrate customization specs into task deliverables (Tasks 1, 3, 5, 6).
- **July 2025**: Test customization features with beta users, refine based on feedback.
- **August 2025**: Deploy customization options in MVP.

## Dependencies
- **Task 1 (Severity Mapping Rules)**: Must support custom rules and weight adjustments.
- **Task 3 (Import Module)**: Must allow batch size and parsing configurations.
- **Task 5 (Reporting Dashboard)**: Must include filter presets and chart options.
- **Task 6 (API Endpoints)**: Must support rate limit and scope customization.

## Changelog
- May 2025: Initial draft created during Strategy phase to address enterprise customization needs. 