import streamlit as st
import sqlite3
import plotly.graph_objects as go
import os
import subprocess
import datetime

st.set_page_config(
    page_title="Project Finance AI Controller",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SQLite Database connection helper
DB_PATH = os.path.join("data", "project_finance.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def load_table(table_name):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        st.error(f"Error loading {table_name}: {e}")
        return []
    finally:
        conn.close()

def render_html_table(data, headers=None):
    if not data:
        st.write("No data available.")
        return
    
    if not headers:
        headers = list(data[0].keys())
        
    html = "<table style='width:100%; border-collapse: collapse; border: 1px solid #b0bec5; font-size:14px; text-align:left; background-color: #ffffff;'>"
    html += "<tr style='background-color: #cfd8dc;'>"
    for h in headers:
        html += f"<th style='padding: 8px; border: 1px solid #b0bec5; color: #000000; font-weight: bold;'>{str(h).replace('_', ' ').title()}</th>"
    html += "</tr>"
    
    for row in data:
        html += "<tr>"
        for h in headers:
            val = row.get(h, '')
            html += f"<td style='padding: 8px; border: 1px solid #cfd8dc; color: #000000;'>{val}</td>"
        html += "</tr>"
    html += "</table><br>"
    st.markdown(html, unsafe_allow_html=True)

# Custom CSS for custom styling matching 'Storytelling with Data'
st.markdown("""
<style>
    .kpi-card {
        background-color: #1e2630;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        border-left: 5px solid #1565C0;
    }
    .kpi-val {
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
    }
    .kpi-lbl {
        font-size: 14px;
        color: #90a4ae;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Project Finance AI Controller Dashboard")
st.markdown("---")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to page:",
    [
        "📊 Executive Overview",
        "📈 EVM Trends & Waterfall",
        "⚠️ Risk & Action Registry",
        "💼 Bidding & Post-Calc",
        "📅 Project Gantt Schedule",
        "⚙️ Orchestrate Agents"
    ]
)

# Project filter selection
st.sidebar.markdown("---")
st.sidebar.subheader("Project Filter")
project_list = ["P-1023"]
selected_project = st.sidebar.selectbox("Select Project ID:", project_list)

# ----------------- PAGE 1: EXECUTIVE OVERVIEW -----------------
if page == "📊 Executive Overview":
    st.header("Executive Overview — Portfolio Status")
    st.markdown("### *How is the project performing at a glance?*")
    
    # Load data
    validated = load_table("validated_dataset")
    forecast = load_table("forecast_output")
    variance = load_table("variance_risk_report")
    
    if validated and forecast and variance:
        # Filter for selected project
        val_row = [r for r in validated if r['project_id'] == selected_project][0]
        fore_row = [r for r in forecast if r['project_id'] == selected_project][0]
        var_row = [r for r in variance if r['project_id'] == selected_project][0]
        
        # Display KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f'<div class="kpi-card" style="border-left: 5px solid #546E7A;"><div class="kpi-lbl">PROJECT ID</div><div class="kpi-val">{selected_project}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="kpi-card" style="border-left: 5px solid #1565C0;"><div class="kpi-lbl">TOTAL BUDGET COST</div><div class="kpi-val">${int(float(val_row["total_budget_cost"])):,}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="kpi-card" style="border-left: 5px solid #00838F;"><div class="kpi-lbl">TOTAL ACTUAL COST</div><div class="kpi-val">${int(float(val_row["total_actual_cost"])):,}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="kpi-card" style="border-left: 5px solid #6A1B9A;"><div class="kpi-lbl">ESTIMATE AT COMPLETION</div><div class="kpi-val">${int(float(fore_row["eac_cost"])):,}</div></div>', unsafe_allow_html=True)
        
        # Color coding for Risk level
        risk_color = "#2E7D32" # Green
        if var_row["risk_level"] == "High":
            risk_color = "#C62828"
        elif var_row["risk_level"] == "Medium":
            risk_color = "#F9A825"
            
        with col5:
            st.markdown(f'<div class="kpi-card" style="border-left: 5px solid {risk_color};"><div class="kpi-lbl">RISK LEVEL</div><div class="kpi-val" style="color: {risk_color};">{var_row["risk_level"]}</div></div>', unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Comparison chart
        st.subheader("Budget vs Actual vs Estimate at Completion (EAC)")
        raw_erp = load_table("erp_raw_data")
        raw_erp = [r for r in raw_erp if r['project_id'] == selected_project]
        
        descriptions = [r['description'] for r in raw_erp]
        budget_costs = [float(r['budget_cost']) for r in raw_erp]
        actual_costs = [float(r['actual_cost']) for r in raw_erp]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=descriptions,
            y=budget_costs,
            name='Budget Cost',
            marker_color='#546E7A'
        ))
        fig.add_trace(go.Bar(
            x=descriptions,
            y=actual_costs,
            name='Actual Cost',
            marker_color='#00838F'
        ))
        
        fig.update_layout(
            barmode='group',
            template="plotly_dark",
            xaxis_title="Cost Category",
            yaxis_title="Amount ($)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Executive Summary Message
        st.info(f"👉 **Headline Insight**: The project is tracking at high risk with a cost variance of **${int(float(var_row['cost_variance_abs'])):,} ({var_row['cost_variance_pct']}%)** overbudget. EAC stands at **${int(float(fore_row['eac_cost'])):,}** against a budget of **${int(float(val_row['total_budget_cost'])):,}**.")

# ----------------- PAGE 2: EVM TRENDS & WATERFALL -----------------
elif page == "📈 EVM Trends & Waterfall":
    st.header("Earned Value Management (EVM) Trends")
    st.markdown("### *What is the earned value trend over time?*")
    
    # Cumulative monthly data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    pv_vals = [200000, 450000, 700000, 950000, 1100000, 1170000]
    ev_vals = [180000, 400000, 650000, 880000, 1020000, 1080000]
    ac_vals = [190000, 420000, 710000, 990000, 1150000, 1259000]
    
    cpi_vals = [ev / ac for ev, ac in zip(ev_vals, ac_vals)]
    spi_vals = [ev / pv for ev, pv in zip(ev_vals, pv_vals)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("EVM S-Curve (PV vs EV vs AC)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=pv_vals, name="Planned Value (PV)", line=dict(color="#6A1B9A", width=3)))
        fig.add_trace(go.Scatter(x=months, y=ev_vals, name="Earned Value (EV)", line=dict(color="#1565C0", width=3)))
        fig.add_trace(go.Scatter(x=months, y=ac_vals, name="Actual Cost (AC)", line=dict(color="#00838F", width=3)))
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Reporting Period",
            yaxis_title="Cumulative Cost ($)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Performance Indices (CPI & SPI)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=cpi_vals, name="CPI", line=dict(color="#2E7D32", width=3)))
        fig.add_trace(go.Scatter(x=months, y=spi_vals, name="SPI", line=dict(color="#F9A825", width=3)))
        # Reference line
        fig.add_shape(type="line", x0="Jan", y0=1.0, x1="Jun", y1=1.0, line=dict(color="grey", width=1, dash="dash"))
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Reporting Period",
            yaxis_title="Index Value",
            yaxis_range=[0.7, 1.2],
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("---")
    
    # Waterfall Chart
    st.subheader("Variance Bridge (BAC to EAC)")
    
    validated = load_table("validated_dataset")
    forecast = load_table("forecast_output")
    
    if validated and forecast:
        val_row = [r for r in validated if r['project_id'] == selected_project][0]
        fore_row = [r for r in forecast if r['project_id'] == selected_project][0]
        
        bac = float(val_row["total_budget_cost"])
        eac = float(fore_row["eac_cost"])
        
        mat_overrun = 52000
        lab_overrun = 60000
        eqp_overrun = 22000
        sub_overrun = 25000
        
        fig = go.Figure(go.Waterfall(
            name = "Variance",
            orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
            x = ["Budget (BAC)", "Material Overrun", "Labor Overrun", "Equipment Overrun", "Subcontractor Overrun", "Forecast (EAC)"],
            textposition = "outside",
            text = [f"${int(bac):,}", f"+${mat_overrun:,}", f"+${lab_overrun:,}", f"+${eqp_overrun:,}", f"+${sub_overrun:,}", f"${int(eac):,}"],
            y = [bac, mat_overrun, lab_overrun, eqp_overrun, sub_overrun, eac],
            connector = dict(line = dict(color = "rgb(127, 127, 127)")),
            increasing = dict(marker = dict(color = "#C62828")),
            totals = dict(marker = dict(color = "#6A1B9A"))
        ))
        
        fig.update_layout(
            template="plotly_dark",
            yaxis_title="Amount ($)",
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ----------------- PAGE 3: RISK & ACTION REGISTRY -----------------
elif page == "⚠️ Risk & Action Registry":
    st.header("Risk Registry & Challenge Questions")
    st.markdown("### *What are the specific issues and what should we do?*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 Identified Risk Items")
        risks = load_table("risk_items")
        if risks:
            risks_filtered = [r for r in risks if r['project_id'] == selected_project]
            render_html_table(risks_filtered)
            
    with col2:
        st.subheader("💡 Variance Drivers")
        drivers = load_table("variance_drivers")
        if drivers:
            drivers_filtered = [r for r in drivers if r['project_id'] == selected_project]
            render_html_table(drivers_filtered)
            
    st.markdown("---")
    
    st.subheader("💬 Challenge Questions for Project Review Meetings")
    st.info("⚡ *Use these questions to challenge project managers on schedule slippage and cost controls.*")
    
    questions = [
        "Why are materials costs experiencing a 4.9% spike ($472k vs $450k) in this reporting period?",
        "What schedule recovery steps are planned to improve the declining SPI (0.92)?",
        "Why was the equipment downtime not covered in the original contingency budget calculations?",
        "Are subcontractors tracking to their revised milestones to avoid further late penalties?"
    ]
    for q in questions:
        st.write(f"- **{q}**")

# ----------------- PAGE 4: LEADERSHIP & SUMMARY -----------------
elif page == "💼 Bidding & Post-Calc":
    st.header("Bidding, Benchmarks & Post-Calculation Summary")
    st.markdown("### *What do leaders need to know and decide?*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Post-Calculation: Bid vs Actual Value")
        postcalc = load_table("postcalc_comparison")
        if postcalc:
            items = [r['item'] for r in postcalc]
            bid_vals = [float(r['bid_value']) for r in postcalc]
            actual_vals = [float(r['actual_value']) for r in postcalc]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=items,
                y=bid_vals,
                name='Bid Value',
                marker_color='#546E7A'
            ))
            fig.add_trace(go.Bar(
                x=items,
                y=actual_vals,
                name='Actual Value',
                marker_color='#00838F'
            ))
            fig.update_layout(
                barmode='group',
                template="plotly_dark",
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.subheader("📑 Lessons Learned")
        lessons = load_table("lessons_learned")
        if lessons:
            for row in lessons:
                st.warning(f"📝 {row['lesson']}")
                
    st.markdown("---")
    
    st.subheader("🔄 Suggested Bidding Model Parameter Updates")
    updates = load_table("suggested_updates")
    if updates:
        for row in updates:
            st.success(f"🔧 {row['update']}")

# ----------------- PAGE 5: GANTT CHART SCHEDULE -----------------
elif page == "📅 Project Gantt Schedule":
    st.header("Project Gantt Chart Schedule")
    st.markdown("### *Milestone Schedule & Execution Timeline*")
    
    # Define Gantt tasks for P-1023 using standard dicts
    gantt_tasks = [
        {"Task": "1. Engineering & Design", "Start": "2026-01-01", "Finish": "2026-03-15", "Status": "Completed", "Progress": 100},
        {"Task": "2. Procurement Phase", "Start": "2026-02-15", "Finish": "2026-05-01", "Status": "Completed", "Progress": 100},
        {"Task": "3. Subcontractor Setup", "Start": "2026-04-01", "Finish": "2026-06-10", "Status": "Delayed", "Progress": 85},
        {"Task": "4. Core Fabrication", "Start": "2026-04-15", "Finish": "2026-08-30", "Status": "Underway", "Progress": 65},
        {"Task": "5. Testing & Verification", "Start": "2026-08-15", "Finish": "2026-10-30", "Status": "Not Started", "Progress": 0}
    ]
    
    fig = go.Figure()
    colors = {
        "Completed": "#2E7D32",
        "Delayed": "#C62828",
        "Underway": "#1565C0",
        "Not Started": "#546E7A"
    }
    
    for task in gantt_tasks:
        start_dt = datetime.datetime.strptime(task["Start"], "%Y-%m-%d")
        finish_dt = datetime.datetime.strptime(task["Finish"], "%Y-%m-%d")
        duration = (finish_dt - start_dt).days
        
        fig.add_trace(go.Bar(
            y=[task["Task"]],
            x=[duration],
            base=task["Start"],
            orientation="h",
            marker_color=colors.get(task["Status"], "#546E7A"),
            name=task["Status"],
            text=f"{task['Status']} ({task['Progress']}%)",
            textposition="inside",
            showlegend=False
        ))
        
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Timeline Calendar",
        xaxis=dict(type='date'),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detail Table
    render_html_table(gantt_tasks)

# ----------------- PAGE 6: ORCHESTRATE AGENTS -----------------
elif page == "⚙️ Orchestrate Agents":
    st.header("Orchestrate AI Agents")
    st.markdown("### *Trigger multi-agent pipeline ingestion and feedback cycles.*")
    
    # Button to run pipeline
    if st.button("🚀 Run Multi-Agent Ingestion Pipeline"):
        st.write("Running pipeline script `simulate_pipeline.py`...")
        
        try:
            # Execute python simulation script
            res = subprocess.run(["python", "simulate_pipeline.py"], capture_output=True, text=True, check=True)
            st.success("Pipeline executed successfully!")
            
            # Print execution logs
            st.subheader("Execution Logs:")
            st.code(res.stdout)
        except Exception as e:
            st.error(f"Error running pipeline: {e}")
            
    st.markdown("---")
    st.subheader("🔍 SQLite Tables Inspector")
    table_to_inspect = st.selectbox(
        "Select Database Table to View:",
        [
            "erp_raw_data", "validated_dataset", "forecast_input", "forecast_output", 
            "rolling_forecast", "variance_risk_report", "variance_drivers", "risk_items",
            "powerbi_kpis", "standardized_report", "decision_support", "postcalc_comparison",
            "lessons_learned", "suggested_updates"
        ]
    )
    
    table_data = load_table(table_to_inspect)
    if table_data:
        render_html_table(table_data)
