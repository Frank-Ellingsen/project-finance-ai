# SQLite Database Schema Relation Map

This document outlines the entity relationships and schema details for `project_finance.db` used in the Project Finance AI agentic workflow.

![Database Schema Relation](file:///d:/Toolstack/project-finance-ai/docs/data_models/db_schema_relation.png)

## Entity Relationship Diagram

```mermaid
erDiagram
    erp_raw_data {
        string project_id PK, FK
        string period PK, FK
        string cost_code PK
        string description
        real budget_cost
        real actual_cost
        real budget_revenue
        real actual_revenue
        real hours_booked
        real qty_installed
    }

    validated_dataset {
        string project_id PK
        string period PK
        real total_budget_cost
        real total_actual_cost
        real total_budget_revenue
        real total_actual_revenue
        real remaining_work_estimate
        real risk_adjustment
    }

    forecast_input {
        string project_id PK, FK
        string period PK, FK
        real budget_cost
        real actual_cost
        real budget_revenue
        real actual_revenue
        real remaining_work
        real risk_adjustment
    }

    forecast_output {
        string project_id PK, FK
        string period PK, FK
        real eac_cost
        real eac_revenue
        real eac_margin
        real etc_cost
        real etc_revenue
        real etc_margin
    }

    rolling_forecast {
        string project_id PK, FK
        string period PK
        real forecast_cost
        real forecast_revenue
        real forecast_margin
    }

    variance_risk_report {
        string project_id PK, FK
        string period PK, FK
        real cost_variance_abs
        real cost_variance_pct
        real revenue_variance_abs
        real revenue_variance_pct
        real margin_variance_abs
        real margin_variance_pct
        string risk_level
    }

    variance_drivers {
        string project_id PK, FK
        string period PK, FK
        string driver_name PK
        string driver_type
        real impact_on_margin
    }

    risk_items {
        string project_id PK, FK
        string period PK, FK
        string description PK
        real probability
        real impact
    }

    decision_support {
        string project_id PK, FK
        string period PK, FK
        string option_name PK
        real financial_impact
        string risk_impact
        string recommendation
    }

    validated_dataset ||--o{ erp_raw_data : "aggregates"
    validated_dataset ||--|| forecast_input : "feeds"
    forecast_input ||--|| forecast_output : "predicts"
    forecast_output ||--o{ rolling_forecast : "projects out"
    forecast_output ||--|| variance_risk_report : "compares"
    variance_risk_report ||--o{ variance_drivers : "explained by"
    variance_risk_report ||--o{ risk_items : "contains"
    variance_risk_report ||--o{ decision_support : "informs"
```

## Primary Key Mapping & Relations

Most tables in the project finance database use a composite key consisting of `(project_id, period)` to uniquely identify data rows in time-phased project management:

| Table | Composite Keys / Identifiers | Type | Relationship / Description |
|---|---|---|---|
| `validated_dataset` | `(project_id, period)` | Fact (Cleaned) | Parent record for a project's monthly period reporting. |
| `erp_raw_data` | `(project_id, period, cost_code)` | Fact (Raw) | Many-to-one with `validated_dataset` via `(project_id, period)`. |
| `forecast_input` | `(project_id, period)` | Input Parameter | One-to-one with `validated_dataset`. |
| `forecast_output` | `(project_id, period)` | Calculation Output | One-to-one with `forecast_input`. |
| `rolling_forecast` | `(project_id, period)` | Future Projections | One-to-many from `forecast_output` for future periods. |
| `variance_risk_report`| `(project_id, period)` | Analysis Output | One-to-one with `forecast_output`. |
| `variance_drivers` | `(project_id, period, driver_name)`| Drivers Breakdown | Many-to-one with `variance_risk_report`. |
| `risk_items` | `(project_id, period, description)`| Risk Registry | Many-to-one with `variance_risk_report`. |
| `decision_support` | `(project_id, period, option_name)`| Decision Alternatives| Many-to-one with `variance_risk_report`. |

## Reference & Configuration Tables

The following tables are standalone lookups or configuration data without direct relational foreign keys:

- `powerbi_kpis`: Contains business logic specifications (`kpi_name`, `dax_expression`) for the Power BI Agent.
- `standardized_report`: Configuration table mapping the output sections to fields (`section`, `field`).
- `postcalc_comparison`: Cost structure evaluation metrics (`item`, `bid_value`, `actual_value`, `variance`).
- `lessons_learned`: Text observations of project failures/successes (`lesson`).
- `suggested_updates`: Parameter adjustment suggestions (`update`) fed back to the bidding/ERP systems.
