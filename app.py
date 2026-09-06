import streamlit as st
from agent_workflow import (
    run_aquasentinel_workflow,
    seed_historical_incidents
)
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AquaSentinel AI",
    page_icon="💧",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("💧 AquaSentinel AI")
st.subheader("AI-Powered Water Leak Detection & Monitoring System")

st.write(
    "A smart monitoring platform that analyzes water flow and pressure "
    "to identify abnormal patterns and detect potential pipeline leaks."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.header("⚙️ Monitoring Controls")

simulation = st.sidebar.selectbox(
    "Simulation Mode",
    ["Normal Operation", "Simulate Leak", "High Flow Warning"]
)

st.sidebar.info(
    "Use Simulation Mode to demonstrate how AquaSentinel AI "
    "responds to abnormal water conditions."
)

# --------------------------------------------------
# SENSOR VALUES
# --------------------------------------------------
if simulation == "Normal Operation":
    flow = 42
    pressure = 3.2
    leak_probability = 8
    status = "🟢 NORMAL"

elif simulation == "Simulate Leak":
    flow = 87
    pressure = 1.8
    leak_probability = 94
    status = "🔴 LEAK DETECTED"

else:
    flow = 68
    pressure = 3.0
    leak_probability = 38
    status = "🟡 WARNING"

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------
st.header("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Water Flow",
        f"{flow} L/min",
        "Normal: 30–60 L/min"
    )

with col2:
    st.metric(
        "Pipeline Pressure",
        f"{pressure} bar",
        "Expected: 2.5–4.5 bar"
    )

with col3:
    st.metric(
        "Leak Probability",
        f"{leak_probability}%"
    )

with col4:
    st.metric(
        "System Status",
        status
    )

st.divider()

# --------------------------------------------------
# SENSOR MONITORING
# --------------------------------------------------
st.header("🌊 Sensor Monitoring")

sensor_data = pd.DataFrame({
    "Sensor": [
        "Water Flow Sensor",
        "Pressure Sensor",
        "Leak Detection Engine"
    ],
    "Reading": [
        f"{flow} L/min",
        f"{pressure} bar",
        f"{leak_probability}% probability"
    ],
    "Status": [
        "Normal" if flow <= 60 else "Abnormal",
        "Normal" if pressure >= 2.5 else "Abnormal",
        status
    ]
})

st.dataframe(
    sensor_data,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# AI AGENT INCIDENT ASSESSMENT
# --------------------------------------------------
st.divider()

st.header("🧠 AI Agent Incident Assessment")

st.write(
    "The AI workflow combines anomaly analysis, rule-based detection, "
    "historical incident context, AI reasoning, and security guardrails."
)

if st.button("🔍 Run AI Assessment", use_container_width=True):

    with st.spinner("Loading historical incident memory..."):

        seed_result = seed_historical_incidents()

    with st.spinner("Analyzing sensor conditions..."):

        workflow_result = run_aquasentinel_workflow(
            flow,
            pressure
        )

    final_status = workflow_result["final_status"]

    # ----------------------------------------------
    # FINAL STATUS
    # ----------------------------------------------
    if final_status == "NORMAL":

        st.success(
            f"✅ System Assessment: {final_status}"
        )

    elif final_status == "HUMAN REVIEW REQUIRED":

        st.warning(
            f"⚠️ System Assessment: {final_status}"
        )

    elif final_status == "BLOCKED BY SECURITY GUARDRAIL":

        st.error(
            f"🛡️ System Assessment: {final_status}"
        )

    else:

        st.error(
            f"🚨 System Assessment: {final_status}"
        )

    # ----------------------------------------------
    # WORKFLOW METRICS
    # ----------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ML Anomaly Score",
            f'{workflow_result["ml_result"]["anomaly_score"]}%'
        )

    with col2:
        st.metric(
            "Rule Engine",
            workflow_result["rule_result"]["status"]
        )

    with col3:

        security_status = (
            "SAFE"
            if workflow_result["enkrypt"]["safe"]
            else "BLOCKED"
        )

        st.metric(
            "Enkrypt Security",
            security_status
        )

    # ----------------------------------------------
    # AI WORKFLOW DETAILS
    # ----------------------------------------------
    with st.expander("🔎 View AI Workflow Details"):

        st.write("### 1️⃣ ML Anomaly Detection")
        st.json(
            workflow_result["ml_result"]
        )

        st.write("### 2️⃣ Rule-Based Detection")
        st.json(
            workflow_result["rule_result"]
        )

        st.write("### 3️⃣ Qdrant Historical Memory")

        if workflow_result["qdrant_memory"]["available"]:

            st.success(
                "Historical incident context retrieved from Qdrant."
            )

        else:

            st.info(
                "Qdrant memory is not configured or no historical "
                "incident collection is available."
            )

        st.json(
            workflow_result["qdrant_memory"]
        )
         st.write("### 🧠 Qdrant Memory Write-Back")

        if workflow_result["memory_write"]["stored"]:
            st.success(
                "New incident successfully stored in Qdrant memory."
            )
            st.json(
                workflow_result["memory_write"]
            )
        else:
            st.info(
                workflow_result["memory_write"]["message"]
            )

        st.write("### 4️⃣ Lyzr Decision Agent")

        if workflow_result["lyzr"]["available"]:

            st.success(
                "Lyzr AI decision agent completed the assessment."
            )

        else:

            st.info(
                "Lyzr is not configured yet."
            )

        st.write(
            workflow_result["lyzr"]["assessment"]
        )

        st.write("### 5️⃣ Enkrypt Security Guardrail")

        if workflow_result["enkrypt"]["available"]:

            if workflow_result["enkrypt"]["safe"]:

                st.success(
                    "Enkrypt security check passed."
                )

            else:

                st.error(
                    "Enkrypt security guardrail blocked the response."
                )

        else:

            st.info(
                "Enkrypt is not configured yet."
            )

        st.json(
            workflow_result["enkrypt"]
        )

# --------------------------------------------------
# LEAK DETECTION ENGINE
# --------------------------------------------------
st.header("🤖 AI Leak Detection")

if simulation == "Simulate Leak":

    st.error("🚨 PIPELINE LEAK DETECTED")

    st.write(
        "The system identified an abnormal combination of "
        "high water flow and reduced pipeline pressure."
    )

    st.warning(
        "Recommended Action: Inspect the affected pipeline section "
        "and isolate the water supply if necessary."
    )

elif simulation == "High Flow Warning":

    st.warning("⚠️ ABNORMAL WATER FLOW")

    st.write(
        "Water flow is higher than the expected operating range. "
        "The system recommends continued monitoring."
    )

else:

    st.success("✅ SYSTEM OPERATING NORMALLY")

    st.write(
        "Current flow and pressure values are within the expected "
        "operating range."
    )

# --------------------------------------------------
# ANOMALY SCORE
# --------------------------------------------------
st.header("📈 Anomaly Analysis")

normal_flow = 45
normal_pressure = 3.5

flow_anomaly = abs(flow - normal_flow) / normal_flow
pressure_anomaly = abs(pressure - normal_pressure) / normal_pressure

anomaly_score = min(
    100,
    int((flow_anomaly + pressure_anomaly) * 50)
)

st.progress(anomaly_score / 100)

st.write(f"**Anomaly Score: {anomaly_score}/100**")

if anomaly_score >= 60:

    st.error(
        "High anomaly detected — immediate inspection recommended."
    )

elif anomaly_score >= 30:

    st.warning(
        "Moderate anomaly detected — continue monitoring."
    )

else:

    st.success(
        "Low anomaly — system conditions appear normal."
    )

# --------------------------------------------------
# SIMULATED SENSOR TREND
# --------------------------------------------------
st.header("📉 Sensor Trend")

time = pd.date_range(
    start="2026-08-27 18:00",
    periods=20,
    freq="5min"
)

if simulation == "Simulate Leak":

    flow_values = np.concatenate([
        np.random.normal(42, 2, 12),
        np.random.normal(85, 4, 8)
    ])

    pressure_values = np.concatenate([
        np.random.normal(3.4, 0.15, 12),
        np.random.normal(1.8, 0.15, 8)
    ])

elif simulation == "High Flow Warning":

    flow_values = np.random.normal(68, 3, 20)
    pressure_values = np.random.normal(3.0, 0.15, 20)

else:

    flow_values = np.random.normal(42, 2, 20)
    pressure_values = np.random.normal(3.3, 0.15, 20)

trend_data = pd.DataFrame({
    "Time": time,
    "Water Flow (L/min)": flow_values,
    "Pressure (bar)": pressure_values
})

st.line_chart(
    trend_data.set_index("Time")
)

# --------------------------------------------------
# ALERT CENTER
# --------------------------------------------------
st.header("🚨 Alert Center")

if simulation == "Simulate Leak":

    alert_data = pd.DataFrame({
        "Time": ["Current"],
        "Alert": ["Pipeline Leak Detected"],
        "Severity": ["CRITICAL"],
        "Action": ["Inspect Pipeline"]
    })

    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )

elif simulation == "High Flow Warning":

    alert_data = pd.DataFrame({
        "Time": ["Current"],
        "Alert": ["High Water Flow"],
        "Severity": ["MEDIUM"],
        "Action": ["Monitor System"]
    })

    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No active alerts.")

# --------------------------------------------------
# SYSTEM ARCHITECTURE
# --------------------------------------------------
st.divider()

st.header("🏗️ AquaSentinel AI Architecture")

st.write(
    """
    **Sensor Layer → Data Processing → Anomaly Detection →
    Leak Probability → Alert System → User Dashboard**
    """
)

st.write(
    "The prototype currently uses simulated sensor data. "
    "The architecture is designed to support real flow and pressure "
    "sensors in a future deployment."
)

# --------------------------------------------------
# ABOUT
# --------------------------------------------------
st.divider()

st.header("ℹ️ About AquaSentinel AI")

st.write(
    """
    AquaSentinel AI is an intelligent water monitoring solution
    designed to detect potential pipeline leaks by analyzing
    water-flow and pressure patterns.

    Instead of relying only on manual inspection, the system
    continuously evaluates sensor readings and identifies
    abnormal conditions that may indicate a leak.

    The prototype includes simulated sensor data, anomaly scoring,
    leak probability estimation, trend visualization, an automated
    alert mechanism, and an AI-assisted incident assessment workflow.
    """
)
