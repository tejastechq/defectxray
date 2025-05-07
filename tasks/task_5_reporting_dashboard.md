# Task 5: Reporting Dashboard for DefectXray MVP

## Objective
Create an interactive web-based dashboard for visualizing defect severity and ODC metadata, enabling enterprise users to analyze and prioritize defects for the DefectXray MVP by August 2025, with a focus on usability and scalability.

## Scope
- Display defect counts by severity (Low, Medium, High) and basic ODC attributes (Defect Type, Activity).
- Provide interactive filtering and drill-down capabilities for detailed analysis.
- Ensure performance and scalability for large enterprise datasets.

## Steps
1. **UI Design**: Develop a responsive dashboard layout using a framework like React, with charts (e.g., bar, pie) for severity and ODC attribute distribution.
2. **Data Visualization**: Implement visualizations for defect trends (e.g., severity over time) using libraries like Chart.js, with dynamic data loading.
3. **Filtering**: Add filters for severity, ODC attributes, date range, and source tool (e.g., Jira, Sentry) to allow targeted analysis.
4. **Drill-Down**: Enable drill-down into defect subsets (e.g., click 'High Severity' to view details), with table sorting by Severity (DESC) and Created At (DESC).
5. **Feedback Widget**: Include a simplified feedback widget (single rating 1-5, target 75% satisfaction) for users to rate classification accuracy, with optional comments.
6. **Performance Optimization**: Set scalability thresholds (e.g., handle 10,000 defects with <2-second load time) using pagination or lazy loading, and limit chart data points (e.g., top 5 categories, 'Other' for rest) with a UI note.
7. **Accessibility**: Implement basic accessibility (e.g., ARIA labels for charts), deferring full WCAG 2.1 compliance to post-MVP (January 2026).

## Dependencies
- **Task 2 (PostgreSQL Defect Schema)**: Requires access to stored defect data and metadata.
- **Task 4 (Severity Analysis Engine)**: Relies on processed severity and ODC data for visualization.
- **Task 6 (API Endpoints)**: Needs secure API endpoints to fetch dashboard data.

## Deliverables
- **Dashboard Prototype**: Functional UI with severity and ODC visualizations, filters, and drill-down.
- **Feedback Widget**: Integrated rating system for user input on classification accuracy.
- **Performance Spec**: Documentation of scalability thresholds and load time targets (e.g., <2 seconds for 10,000 defects).

## Timeline
- **June 2025**: Complete UI design and initial data visualization.
- **July 2025**: Implement filtering, drill-down, feedback widget, and test scalability with large datasets (10,000+ defects).
- **August 2025**: Finalize integration with API endpoints for MVP launch.

## Notes
- Usability features like drill-down sorting and simplified feedback enhance enterprise user experience.
- Scalability measures (pagination, data limits) ensure performance with large defect volumes.

## Changelog
- May 2025: Updated task with drill-down sorting, simplified feedback widget, chart performance limits with 'Other' category, and scalability thresholds.

## Task Overview
**Task ID**: T5-MVP-DASHBOARD
**Phase**: Strategy
**Owner**: Frontend Developer
**Duration**: 2 Weeks (July-August 2025)
**Priority**: Medium
**Dependencies**: Task 2 (PostgreSQL Defect Schema), Task 4 (Severity Analysis Engine)

This task focuses on developing a basic Reporting Dashboard for the DefectXray MVP using React and Tailwind CSS. The dashboard will visualize defect distributions by severity and Orthogonal Defect Classification (ODC) attributes (Defect Type and Trigger), providing enterprise stakeholders with actionable insights into CI/CD workflow issues.

## Objectives
- Create a user-friendly dashboard interface to display defect counts and distributions by severity (High, Medium, Low).
- Visualize ODC attributes (Defect Type and Trigger) to highlight process issues (e.g., high Function defects in design).
- Ensure the dashboard is functional for MVP, prioritizing data clarity over extensive UI polish, with scalability for future enhancements.

## Detailed Steps
1. **Review Requirements and Dependencies**:
   - Review the PostgreSQL schema from 'tasks/task_2_postgresql_defect_schema.md' to understand data structure (e.g., enum fields for severity, defect_type, trigger).
   - Examine the Severity Analysis Engine output from 'tasks/task_4_severity_analysis_engine.md' to confirm data availability for visualization.
   - Identify key metrics for enterprise stakeholders: total defect count, severity distribution, top Defect Types, and Trigger distributions.
   - **Output**: List of metrics and visualizations to implement (see Visualization Plan below).

2. **Set Up Frontend Environment**:
   - Initialize a React project with TypeScript for type safety, using Create React App or Vite.
   - Integrate Tailwind CSS for rapid styling, following a utility-first approach for responsive design.
   - Add necessary libraries: `recharts` for charts, `axios` for API calls to fetch defect data.
   - **Output**: Project setup instructions (see Code Structure below).

3. **Design Dashboard Layout**:
   - Create a single-page layout with:
     - Header: Title ("DefectXray Dashboard") and date range selector for data filtering.
     - Summary Section: Total defect count and severity breakdown (e.g., cards showing High: X, Medium: Y, Low: Z).
     - Charts Section: Bar charts for severity distribution, Defect Type distribution, and Trigger distribution.
   - Use Tailwind CSS for a clean, modern look with responsive grid layout (e.g., cards stack on mobile).
   - Prioritize simplicity for MVP: static data fetch on load, minimal interactivity (e.g., no drill-downs yet).
   - **Output**: Layout wireframe or description (see Visualization Plan below).

4. **Implement Data Fetching**:
   - Create a service to fetch defect data from the backend API (to be developed in Task 6) or mock data for initial development.
   - Fetch aggregated data for:
     - Total count and severity breakdown.
     - Counts by Defect Type and Trigger for respective charts.
   - Handle loading and error states (e.g., spinner while fetching, error message if API fails).
   - **Output**: Data fetching logic (see Code Structure below).

5. **Develop Visualization Components**:
   - Use `recharts` to create:
     - **Severity Bar Chart**: X-axis as severity levels (High, Medium, Low), Y-axis as count.
     - **Defect Type Bar Chart**: X-axis as Defect Types (e.g., Function, Interface), Y-axis as count, sorted by frequency.
     - **Trigger Bar Chart**: X-axis as Triggers (e.g., Stress/Workload, Unit Test), Y-axis as count.
   - Style charts with Tailwind CSS for consistency (e.g., color coding: High=Red, Medium=Yellow, Low=Green).
   - Add tooltips to show exact counts on hover.
   - **Output**: Chart component code (see Code Structure below).

6. **Add Basic Filtering**:
   - Implement a simple date range selector (e.g., last 7 days, last 30 days, all time) to filter data fetched from API.
   - Update charts dynamically based on selected range (re-fetch or filter client-side for MVP).
   - **Output**: Filtering logic (see Code Structure below).

7. **Implement Drill-Down Functionality for Detailed Insights**:
   - Add interactivity to charts allowing users to click on a severity level (e.g., 'High') or ODC attribute (e.g., 'Function') to view a filtered table of corresponding defects below the visualizations.
   - Develop a `DefectTable.tsx` component to display filtered defect lists with columns for ID, Description (truncated), Severity, Defect Type, Trigger, Activity, Created At, and a 'Details' link to a full defect view.
   - Set default sorting for the table to prioritize Severity (High to Low) for focusing on critical defects, followed by Created At (newest first) for equal severities, to reflect recent issues.
   - Enable client-side sorting and filtering on Severity, Defect Type, and Created At columns to support quick data exploration without additional server requests.
   - Include pagination controls if result sets exceed 10-15 entries per page, ensuring performance with large defect volumes.
   - **Output**: Interactive drill-down table component with default sorting (Severity DESC, Created At DESC).

8. **Implement Client-Side Filtering for Enhanced Usability**:
   - Add dropdowns or buttons above charts to filter data by Severity, Defect Type, or Trigger without re-fetching from the API.
   - Store fetched data in React state or context to enable quick client-side filtering, improving user experience.
   - Example: Add a severity filter dropdown to update all charts to show only High severity defects.
   - **Output**: Client-side filtering logic (see Code Structure below).

9. **Optimize Chart Performance for Large Datasets**:
   - Ensure charts handle enterprise-scale data (e.g., thousands of defects) by aggregating counts server-side (via Task 6 API endpoints) before passing to the frontend, minimizing client-side processing.
   - Limit chart visualizations to the top 5-7 categories per attribute (e.g., top Defect Types by count) with remaining categories grouped as 'Other' to maintain clarity and performance.
   - Add a UI note or tooltip in `SeverityChart.tsx`, `DefectTypeChart.tsx`, and `TriggerChart.tsx` to inform users that minor categories are grouped as 'Other', with full data available via CSV export. Defer a toggle for full data display to post-MVP.
   - Use lazy loading or virtualization for the drill-down table if rendering hundreds of rows to prevent UI lag.
   - **Output**: Optimized chart components with aggregation and 'Other' category handling.

10. **Ensure Accessibility and Usability**:
    - Add ARIA labels to charts and UI elements for screen reader support.
    - Use high-contrast colors for readability (e.g., distinct colors for severity levels).
    - Implement keyboard navigation for chart interactions (e.g., Tab to select bars, Enter to drill down).
    - Ensure colorblind-friendly palettes (e.g., use patterns or distinct hues for severity levels).
    - Test with tools like Lighthouse to achieve a minimum accessibility score of 85 for MVP, with full compliance (score of 90+) targeted for beta (January 2026).
    - Keep navigation minimal for MVP, focusing on data visibility.
    - **Output**: Accessibility considerations (documented in code comments, see Code Structure below).

11. **Add CSV Export Feature for Pilot Usability**:
    - Implement a basic export feature to allow users to download defect data (e.g., from drill-down tables) as a CSV file.
    - Leverage existing API data or client-side state to generate the CSV, including fields like ID, Description, Source, Severity, Defect Type, and Trigger.
    - Ensure the feature is simple for MVP, with a button or link to trigger the download.
    - **Output**: CSV export logic and UI component (see Code Structure below).

12. **Add In-App Feedback Widget for Beta Users**:
    - Include a simple feedback widget in the dashboard UI (e.g., fixed button or modal) to collect usability feedback from beta users, aiding rapid iteration.
    - Implement a `FeedbackWidget.tsx` component with a single overall rating (1-5 scale) and a free-text comment field to reduce development time for MVP. Target a minimum 75% user satisfaction rate (ratings of 4/5 or higher).
    - Store feedback in a separate `feedback` table or file for analysis (schema: rating INT, comment TEXT, timestamp DATETIME, optional user_id if authenticated).
    - Defer component-specific feedback (e.g., separate ratings for charts vs. filters) to post-MVP based on beta insights (January 2026).
    - Analyze feedback during beta (November-December 2025) to identify UI pain points, prioritizing fixes for post-MVP enhancements.
    - **Output**: Feedback widget component with single rating and comment field.

## Outputs and Deliverables
- **Visualization Plan**: List of metrics and chart types for the dashboard.
- **Code Structure and Logic**: Detailed structure for React components, data fetching, and chart rendering.
- **Test Results**: Results from testing dashboard with mock or real data (to be added post-testing).
- **Enhanced Usability Features**: Documentation of drill-down, client-side filtering, trend lines, and accessibility features.
- **Dashboard UI**: Functional React components for charts and tables.
- **Visualization Plan**: Design for Severity, Defect Type, and Trigger charts with drill-down and export features.
- **Accessibility Report**: Documentation of ARIA labels, keyboard navigation, and color contrast adjustments, targeting a Lighthouse accessibility score of 85 for MVP.
- **Test Results**: Results from usability and performance testing, tracking 75% user satisfaction rate (to be added post-testing).
- **Feedback Analysis**: Summary of beta user feedback for UI improvements (to be added post-beta).

## Visualization Plan
| **Metric**                | **Visualization Type** | **Description**                                      |
|---------------------------|------------------------|-----------------------------------------------------|
| Total Defect Count        | Summary Card           | Display total number of defects in selected range.  |
| Severity Distribution     | Bar Chart              | Count of defects by severity (High, Medium, Low).   |
| Defect Type Distribution  | Bar Chart              | Count of defects by ODC Defect Type, sorted by frequency. |
| Trigger Distribution      | Bar Chart              | Count of defects by ODC Trigger, sorted by frequency. |
| Defect Trend Over Time    | Line Chart             | Daily defect counts over selected date range to identify trends. |

**Layout Description**:
- **Header**: Title and date range dropdown (e.g., "Last 7 Days", "Last 30 Days", "All Time").
- **Summary Section**: Three cards for severity counts (High, Medium, Low) with color coding.
- **Filter Section**: Dropdowns or buttons for Severity, Defect Type, and Trigger filtering.
- **Charts Section**: Four charts stacked vertically (Severity, Defect Type, Trigger Bar Charts, and Trend Line Chart), each with a title, tooltips, and drill-down capability.

## Code Structure and Logic
**Target Framework**: React with TypeScript
**Key Libraries**: `recharts` (charts), `axios` (API calls), `tailwindcss` (styling)

**Project Structure**:
```
src/
  components/
    Dashboard.tsx          # Main dashboard component
    SummaryCard.tsx        # Card for severity counts
    SeverityChart.tsx      # Bar chart for severity distribution
    DefectTypeChart.tsx    # Bar chart for Defect Type distribution
    TriggerChart.tsx       # Bar chart for Trigger distribution
    TrendChart.tsx         # Line chart for defect trends over time
    DefectTable.tsx        # Table for drill-down defect details
    DateRangeSelector.tsx  # Dropdown for date range filtering
    FilterSelector.tsx     # Dropdowns for severity, type, trigger filtering
    CSVExportButton.tsx    # Button for CSV export of defect data
    FeedbackWidget.tsx     # Feedback widget component
  services/
    api.ts                 # API fetching logic
  types/
    defect.ts              # Type definitions for defect data
  App.tsx                  # Entry point integrating dashboard
  index.css                # Tailwind CSS import
```

**Pseudocode**:
```typescript
// src/components/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import SummaryCard from './SummaryCard';
import SeverityChart from './SeverityChart';
import DefectTypeChart from './DefectTypeChart';
import TriggerChart from './TriggerChart';
import TrendChart from './TrendChart';
import DefectTable from './DefectTable';
import DateRangeSelector from './DateRangeSelector';
import FilterSelector from './FilterSelector';
import CSVExportButton from './CSVExportButton';
import FeedbackWidget from './FeedbackWidget';
import { fetchDefectSummary, fetchDefectTypes, fetchDefectTriggers, fetchDefects } from '../services/api';
import { DefectSummary, DefectTypeData, TriggerData, Defect } from '../types/defect';

interface DateRange {
  label: string;
  value: string; // e.g., '7d', '30d', 'all'
}

interface FilterOptions {
  severity: string | null; // e.g., 'High', 'Medium', 'Low', or null for all
  defectType: string | null;
  trigger: string | null;
}

const Dashboard: React.FC = () => {
  const [dateRange, setDateRange] = useState<DateRange>({ label: 'Last 7 Days', value: '7d' });
  const [filters, setFilters] = useState<FilterOptions>({ severity: null, defectType: null, trigger: null });
  const [summary, setSummary] = useState<DefectSummary>({ total: 0, high: 0, medium: 0, low: 0 });
  const [defectTypes, setDefectTypes] = useState<DefectTypeData[]>([]);
  const [triggers, setTriggers] = useState<TriggerData[]>([]);
  const [selectedDefects, setSelectedDefects] = useState<Defect[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<{ type: string, value: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const summaryData = await fetchDefectSummary(dateRange.value);
        const typeData = await fetchDefectTypes(dateRange.value);
        const triggerData = await fetchDefectTriggers(dateRange.value);
        setSummary(summaryData);
        setDefectTypes(typeData);
        setTriggers(triggerData);
        setSelectedDefects([]); // Reset drill-down on data refresh
        setSelectedCategory(null);
      } catch (err) {
        setError('Failed to load defect data. Please try again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [dateRange]);

  const handleRangeChange = (newRange: DateRange) => {
    setDateRange(newRange);
  };

  const handleFilterChange = (filterType: keyof FilterOptions, value: string | null) => {
    setFilters(prev => ({ ...prev, [filterType]: value }));
    // Optionally re-fetch data with filters applied if client-side filtering is insufficient
  };

  const handleChartClick = async (categoryType: string, value: string) => {
    setSelectedCategory({ type: categoryType, value });
    try {
      const filterParams: any = { range: dateRange.value };
      if (categoryType === 'severity') filterParams.severity = value;
      if (categoryType === 'defectType') filterParams.defect_type = value;
      if (categoryType === 'trigger') filterParams.trigger = value;
      const defects = await fetchDefects(filterParams);
      setSelectedDefects(defects);
    } catch (err) {
      console.error('Failed to fetch defects for category', err);
      setSelectedDefects([]);
    }
  };

  // Apply client-side filtering to chart data if filters are set
  const filteredSummary = filters.severity ? {
    ...summary,
    high: filters.severity === 'High' ? summary.high : 0,
    medium: filters.severity === 'Medium' ? summary.medium : 0,
    low: filters.severity === 'Low' ? summary.low : 0
  } : summary;

  const filteredDefectTypes = filters.defectType ? defectTypes.filter(d => d.type === filters.defectType) : defectTypes;
  const filteredTriggers = filters.trigger ? triggers.filter(t => t.trigger === filters.trigger) : triggers;

  if (error) {
    return <div className="text-center text-red-500 p-4">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4 bg-gray-50 min-h-screen">
      <header className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">DefectXray Dashboard</h1>
        <DateRangeSelector 
          currentRange={dateRange} 
          onChange={handleRangeChange} 
          options=[
            { label: 'Last 7 Days', value: '7d' },
            { label: 'Last 30 Days', value: '30d' },
            { label: 'All Time', value: 'all' }
          ] 
        />
      </header>

      <section className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FilterSelector 
            label="Severity" 
            options={['High', 'Medium', 'Low'].map(v => ({ label: v, value: v }))}
            currentValue={filters.severity}
            onChange={(val) => handleFilterChange('severity', val)}
            allowClear={true}
          />
          <FilterSelector 
            label="Defect Type" 
            options={defectTypes.map(d => ({ label: d.type, value: d.type }))}
            currentValue={filters.defectType}
            onChange={(val) => handleFilterChange('defectType', val)}
            allowClear={true}
          />
          <FilterSelector 
            label="Trigger" 
            options={triggers.map(t => ({ label: t.trigger, value: t.trigger }))}
            currentValue={filters.trigger}
            onChange={(val) => handleFilterChange('trigger', val)}
            allowClear={true}
          />
        </div>
      </section>

      {loading ? (
        <div className="text-center p-8">Loading data...</div>
      ) : (
        <>
          <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <SummaryCard title="High Severity" count={filteredSummary.high} color="bg-red-100 border-red-500" />
            <SummaryCard title="Medium Severity" count={filteredSummary.medium} color="bg-yellow-100 border-yellow-500" />
            <SummaryCard title="Low Severity" count={filteredSummary.low} color="bg-green-100 border-green-500" />
          </section>

          <section className="space-y-6">
            <div className="bg-white p-4 rounded shadow">
              <h2 className="text-xl font-semibold mb-2">Severity Distribution</h2>
              <SeverityChart data=[
                { severity: 'High', count: filteredSummary.high, fill: 'rgb(239, 68, 68)' },
                { severity: 'Medium', count: filteredSummary.medium, fill: 'rgb(234, 179, 8)' },
                { severity: 'Low', count: filteredSummary.low, fill: 'rgb(34, 197, 94)' }
              ]} onBarClick={(data) => handleChartClick('severity', data.severity)} />
              {selectedCategory?.type === 'severity' && selectedDefects.length > 0 && (
                <>
                  <DefectTable defects={selectedDefects} title={`Defects for ${selectedCategory.value} Severity`} />
                  <CSVExportButton data={selectedDefects} filename={`defects_${selectedCategory.value.toLowerCase()}_severity.csv`} />
                </>
              )}
            </div>

            <div className="bg-white p-4 rounded shadow">
              <h2 className="text-xl font-semibold mb-2">Defect Type Distribution</h2>
              <DefectTypeChart data={filteredDefectTypes} onBarClick={(data) => handleChartClick('defectType', data.type)} />
              {selectedCategory?.type === 'defectType' && selectedDefects.length > 0 && (
                <>
                  <DefectTable defects={selectedDefects} title={`Defects for ${selectedCategory.value} Type`} />
                  <CSVExportButton data={selectedDefects} filename={`defects_${selectedCategory.value.toLowerCase()}_type.csv`} />
                </>
              )}
            </div>

            <div className="bg-white p-4 rounded shadow">
              <h2 className="text-xl font-semibold mb-2">Trigger Distribution</h2>
              <TriggerChart data={filteredTriggers} onBarClick={(data) => handleChartClick('trigger', data.trigger)} />
              {selectedCategory?.type === 'trigger' && selectedDefects.length > 0 && (
                <>
                  <DefectTable defects={selectedDefects} title={`Defects for ${selectedCategory.value} Trigger`} />
                  <CSVExportButton data={selectedDefects} filename={`defects_${selectedCategory.value.toLowerCase()}_trigger.csv`} />
                </>
              )}
            </div>
          </section>
        </>
      )}

      <section className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Feedback</h2>
        <FeedbackWidget />
      </section>
    </div>
  );
};

export default Dashboard;
```

**SeverityChart.tsx Example (Updated with Drill-Down)**:
```typescript
// src/components/SeverityChart.tsx
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface SeverityData {
  severity: string;
  count: number;
  fill: string;
}

interface SeverityChartProps {
  data: SeverityData[];
  onBarClick?: (data: SeverityData) => void;
}

const SeverityChart: React.FC<SeverityChartProps> = ({ data, onBarClick }) => {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} aria-label="Severity distribution chart" onClick={(e, data) => onBarClick && onBarClick(data.payload)}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="severity" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SeverityChart;
```

**DefectTable.tsx Example (Drill-Down Table)**:
```typescript
// src/components/DefectTable.tsx
import React from 'react';
import { Defect } from '../types/defect';

interface DefectTableProps {
  defects: Defect[];
  title: string;
}

const DefectTable: React.FC<DefectTableProps> = ({ defects, title }) => {
  return (
    <div className="mt-4">
      <h3 className="text-lg font-medium text-gray-700 mb-2">{title}</h3>
      <div className="overflow-x-auto max-h-64 overflow-y-auto border border-gray-200 rounded">
        <table className="min-w-full bg-white">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-600 border-b">ID</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-600 border-b">Description</th>
              <th className="px-4 py-2 text-left text-sm font-semibold text-gray-600 border-b">Source</th>
            </tr>
          </thead>
          <tbody>
            {defects.length > 0 ? (
              defects.map(defect => (
                <tr key={defect.id} className="hover:bg-gray-50 border-b">
                  <td className="px-4 py-2 text-sm text-gray-700">{defect.id}</td>
                  <td className="px-4 py-2 text-sm text-gray-700 truncate max-w-xs">{defect.description}</td>
                  <td className="px-4 py-2 text-sm text-gray-700">{defect.source}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3} className="px-4 py-2 text-center text-gray-500">No defects found for this category.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DefectTable;
```

**FilterSelector.tsx Example (Client-Side Filtering)**:
```typescript
// src/components/FilterSelector.tsx
import React from 'react';

interface FilterOption {
  label: string;
  value: string;
}

interface FilterSelectorProps {
  label: string;
  options: FilterOption[];
  currentValue: string | null;
  onChange: (value: string | null) => void;
  allowClear: boolean;
}

const FilterSelector: React.FC<FilterSelectorProps> = ({ label, options, currentValue, onChange, allowClear }) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value === '' ? null : e.target.value;
    onChange(value);
  };

  return (
    <div className="flex flex-col">
      <label className="text-sm font-medium text-gray-700 mb-1">{label}</label>
      <select 
        className="p-2 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
        value={currentValue || ''}
        onChange={handleChange}
        aria-label={`Filter by ${label}`}
      >
        <option value="">All {label}s</option>
        {options.map(opt => (
          <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
    </div>
  );
};

export default FilterSelector;
```

**TrendChart.tsx Example (Trend Line Visualization)**:
```typescript
// src/components/TrendChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface TrendData {
  date: string; // e.g., '2025-07-01'
  high: number;
  medium: number;
  low: number;
}

interface TrendChartProps {
  data: TrendData[];
}

const TrendChart: React.FC<TrendChartProps> = ({ data }) => {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} aria-label="Defect trend over time chart">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="high" stroke="rgb(239, 68, 68)" name="High Severity" />
          <Line type="monotone" dataKey="medium" stroke="rgb(234, 179, 8)" name="Medium Severity" />
          <Line type="monotone" dataKey="low" stroke="rgb(34, 197, 94)" name="Low Severity" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendChart;
```

**CSVExportButton.tsx Example (CSV Export Feature)**:
```typescript
// src/components/CSVExportButton.tsx
import React from 'react';
import { Defect } from '../types/defect';

interface CSVExportButtonProps {
  data: Defect[];
  filename: string;
}

const CSVExportButton: React.FC<CSVExportButtonProps> = ({ data, filename }) => {
  const exportToCSV = () => {
    if (!data || data.length === 0) return;
    
    const headers = ['ID', 'Description', 'Source', 'Severity', 'Defect Type', 'Trigger', 'Created At'];
    const csvRows = [headers];
    
    data.forEach(defect => {
      const row = [
        defect.id,
        `"${defect.description.replace(/"/g, '""')}"`, // Escape quotes in description
        defect.source,
        defect.severity,
        defect.defect_type,
        defect.trigger,
        defect.created_at
      ];
      csvRows.push(row);
    });
    
    const csvContent = csvRows.map(row => row.join(',')).join('
');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };
  
  return (
    <button 
      onClick={exportToCSV}
      className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      aria-label="Export defects to CSV"
    >
      Export to CSV
    </button>
  );
};

export default CSVExportButton;
```

**api.ts Example (Updated with Trend Data Fetching Deferred)**:
```typescript
// src/services/api.ts
import axios from 'axios';

// Mock API base URL (to be replaced with Task 6 API endpoint)
const API_BASE_URL = 'http://localhost:3000/api';

// Interfaces for data structure

export interface DefectSummary {
  total: number;
  high: number;
  medium: number;
  low: number;
}

export interface DefectTypeData {
  type: string;
  count: number;
}

export interface TriggerData {
  trigger: string;
  count: number;
}

export interface TrendData {
  date: string;
  high: number;
  medium: number;
  low: number;
}

export interface Defect {
  id: string;
  description: string;
  source: string;
  severity: string;
  defect_type: string;
  trigger: string;
  created_at: string;
}

// Fetch summary data for severity cards
export const fetchDefectSummary = async (range: string): Promise<DefectSummary> => {
  // Mock data for development until API is ready
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        total: 150,
        high: range === '7d' ? 20 : range === '30d' ? 50 : 75,
        medium: range === '7d' ? 30 : range === '30d' ? 60 : 50,
        low: range === '7d' ? 10 : range === '30d' ? 40 : 25,
      });
    }, 500);
  });
  // Replace with actual API call post-Task 6
  // const response = await axios.get(`${API_BASE_URL}/defects/summary?range=${range}`);
  // return response.data;
};

// Fetch Defect Type distribution
export const fetchDefectTypes = async (range: string): Promise<DefectTypeData[]> => {
  // Mock data
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { type: 'Function', count: range === '7d' ? 15 : 40 },
        { type: 'Interface', count: range === '7d' ? 10 : 30 },
        { type: 'Assignment', count: range === '7d' ? 5 : 20 },
        { type: 'Timing', count: range === '7d' ? 8 : 15 },
        { type: 'Documentation', count: range === '7d' ? 2 : 10 },
      ]);
    }, 500);
  });
  // Replace with actual API call post-Task 6
  // const response = await axios.get(`${API_BASE_URL}/defects/types?range=${range}`);
  // return response.data;
};

// Fetch Trigger distribution
export const fetchDefectTriggers = async (range: string): Promise<TriggerData[]> => {
  // Mock data
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { trigger: 'Stress/Workload', count: range === '7d' ? 10 : 30 },
        { trigger: 'Unit Test', count: range === '7d' ? 15 : 40 },
        { trigger: 'Function Test', count: range === '7d' ? 8 : 25 },
        { trigger: 'Boundary Conditions', count: range === '7d' ? 5 : 15 },
        { trigger: 'Recovery', count: range === '7d' ? 2 : 10 },
      ]);
    }, 500);
  });
  // Replace with actual API call post-Task 6
  // const response = await axios.get(`${API_BASE_URL}/defects/triggers?range=${range}`);
  // return response.data;
};

// Fetch detailed defects for drill-down
export const fetchDefects = async (filters: { range: string, severity?: string, defect_type?: string, trigger?: string, limit?: number }): Promise<Defect[]> => {
  // Mock data
  return new Promise((resolve) => {
    setTimeout(() => {
      const mockDefects: Defect[] = [];
      const count = filters.limit || 10;
      for (let i = 0; i < count; i++) {
        mockDefects.push({
          id: `DEF-${Math.floor(Math.random() * 10000)}`,
          description: `Mock defect description ${i + 1} for ${filters.severity || 'Any'} severity`,
          source: `Test Suite ${Math.floor(Math.random() * 10)}`,
          severity: filters.severity || (['High', 'Medium', 'Low'][Math.floor(Math.random() * 3)]), 
          defect_type: filters.defect_type || (['Function', 'Interface', 'Assignment'][Math.floor(Math.random() * 3)]), 
          trigger: filters.trigger || (['Stress/Workload', 'Unit Test', 'Function Test'][Math.floor(Math.random() * 3)]), 
          created_at: new Date().toISOString()
        });
      }
      resolve(mockDefects);
    }, 500);
  });
  // Replace with actual API call post-Task 6
  // const query = new URLSearchParams({ range: filters.range, limit: (filters.limit || 50).toString() });
  // if (filters.severity) query.append('severity', filters.severity);
  // if (filters.defect_type) query.append('defect_type', filters.defect_type);
  // if (filters.trigger) query.append('trigger', filters.trigger);
  // const response = await axios.get(`${API_BASE_URL}/defects?${query.toString()}`);
  // return response.data;
};
```

## Timeline and Milestones
- **Start Date**: Late July 2025
- **Completion Date**: Early August 2025 (2 weeks duration)
- **Milestone**: Basic Reporting Dashboard with drill-down, client-side filtering, CSV export, and accessibility features developed and tested by mid-August 2025, ready for integration with API endpoints. Trend visualization deferred to post-MVP (September 2025).

## Risks and Mitigation
- **Risk 1: Data Fetching Delays** - If API calls (post-Task 6) are slow, affecting dashboard responsiveness, mitigation is to implement caching or client-side data aggregation for MVP, with asynchronous loading indicators to maintain UX.
- **Risk 2: Visualization Overload** - If large datasets cause chart rendering issues, mitigation is to limit data to top N categories (e.g., top 5 Defect Types) with an 'Other' category, adjusting post-beta based on feedback.
- **Risk 3: Usability Gaps** - If stakeholders find the basic UI insufficient for decision-making, mitigation is to prioritize beta feedback for adding specific interactivity (e.g., click-to-filter) in post-MVP updates, keeping MVP focused on core data display. With added drill-down, filtering, and CSV export, this risk is partially mitigated, but further enhancements may still be needed based on user input.
- **Risk 4: Accessibility Challenges** - If enhanced accessibility features (e.g., keyboard navigation) are incomplete or ineffective, mitigation is to use testing tools like Lighthouse during development to ensure a minimum score of 85 for MVP and allocate additional time post-beta for full compliance.
- **Risk 5: Large Defect Datasets** - If defect datasets are large, they may slow down dashboard rendering, frustrating users.
  - **Mitigation**: Optimize data aggregation server-side (Step 9) and use pagination or virtualization for tables. Limit charts to top categories with an 'Other' grouping and UI note for clarity.

## Test Results
*(To be added post-validation)*

This task instruction provides a comprehensive guide for building the basic Reporting Dashboard for DefectXray's MVP, ensuring stakeholders gain actionable insights from defect severity and ODC data. 