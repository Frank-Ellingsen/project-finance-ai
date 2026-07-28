# Project Finance AI: User Guide

Welcome to the **Project Finance AI** system documentation. This guide details how to navigate the workspace, interact with the SQLite database, run the multi-agent simulation workflow, and run tests.

---

## 1. Getting Started

### Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### Workspace Setup
1. Open VS Code.
2. Select **File** -> **Open Workspace from File...**
3. Choose the [workspace.code-workspace](file:///d:/Toolstack/project-finance-ai/workspace.code-workspace) configuration file to load the folder layout.

---

## 2. Directory Layout

Here is the directory structure for your Project Finance workflow:

```text
d:\Toolstack\project-finance-ai
 ├── agents/                      # Specialized agent classes
 │   ├── forecast/                # EAC/ETC calculations
 │   ├── variance_risk/           # Deviation and risk identification
 │   ├── power_bi/                # DAX metrics generation
 │   ├── reporting_standardization/ # Template processing
 │   ├── decision_support/        # Executive briefing creation
 │   ├── erp_data_foundation/     # Raw data ingestion
 │   └── calc_postcalc/           # Bid-vs-actual feedback loop
 ├── data/
 │   └── project_finance.db       # SQLite Database containing mock data
 ├── mock_data/                   # CSV copies of database tables
 ├── docs/                        # Architecture, schemas, and user guide
 ├── scripts/                     # Operational execution scripts
 ├── tests/                       # Unit tests for agent evaluation
 └── simulate_pipeline.py         # Main execution entrypoint script
```

---

## 3. Database & Schema Relation

The system runs on the `project_finance.db` SQLite database.

### Viewing the Schema

For a detailed view of the database entities and how they link via composite keys `(project_id, period)`, refer to the [Schema Relation Guide](file:///d:/Toolstack/project-finance-ai/docs/data_models/schema_relation.md).

![Database Schema](file:///d:/Toolstack/project-finance-ai/docs/data_models/db_schema_relation.png)

### Querying with Python

You can easily query the SQLite database inside python:

```python
import sqlite3

# Connect to the DB
conn = sqlite3.connect("data/project_finance.db")
cursor = conn.cursor()

# Query the raw ERP data
cursor.execute("SELECT * FROM erp_raw_data LIMIT 5")
rows = cursor.fetchall()
for r in rows:
    print(r)

conn.close()
```

---

## 4. Multi-Agent Workflow Simulation

The workflow processes project metrics from raw ERP ingestion up to final decision briefs.

![Agentic Workflow](file:///d:/Toolstack/project-finance-ai/docs/architecture/agent_workflow_diagram.png)

### Running the Simulation
To execute the entire multi-agent cycle using the synthetic datasets, run the following command from the root project folder:

```powershell
python simulate_pipeline.py
```

This runs the agents sequentially:
1. **ERP Agent**: Cleans and validates incoming transaction figures.
2. **Forecast Agent**: Estimates EAC, ETC, and project margins.
3. **Variance & Risk Agent**: Flags overruns and identifies variance driver categories.
4. **Power BI Agent**: Formulates DAX measures.
5. **Reporting Agent**: Places metrics into standard sections.
6. **Decision Agent**: Suggests choices (e.g. subcontractors vs. overtime).
7. **Post-Calc Agent**: Completes the loop to suggest bidding parameter adjustments.

---

## 5. Running Tests

To verify that all components are fully functional:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

---

## 6. Streamlit Dashboard

To run the interactive reporting dashboard featuring EVM charts, S-Curves, waterfall variance bridges, and Gantt charts:

### Install Requirements
```powershell
pip install -r requirements.txt
```

### Start Dashboard App
```powershell
streamlit run app.py
```

