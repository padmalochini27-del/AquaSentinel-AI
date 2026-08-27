import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AquaSentinel AI",
    page_icon="💧",
    layout="wide"
)

# Title
st.title("💧 AquaSentinel AI")
st.subheader("AI-Powered Water Leak Detection & Monitoring System")

st.write(
    "Monitor water flow and pressure, detect abnormal patterns, "
    "and identify potential leaks using AI."
)

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Water Flow", "42 L/min")

with col2:
    st.metric("Pressure", "3.2 bar")

with col3:
    st.metric("Leak Probability", "8%")

with col4:
    st.metric("System Status", "🟢 Normal")

st.divider()

# Sensor monitoring section
st.header("📊 Sensor Monitoring")

flow = st.slider(
    "Water Flow (L/min)",
    min_value=0,
    max_value=100,
    value=42
)

pressure = st.slider(
    "Water Pressure (bar)",
    min_value=0.0,
    max_value=10.0,
    value=3.2
)

st.write("### Current Sensor Readings")

sensor_data = pd.DataFrame({
    "Sensor": ["Water Flow", "Water Pressure"],
    "Value": [flow, pressure],
    "Unit": ["L/min", "bar"]
})

st.dataframe(sensor_data, use_container_width=True)

# Simple initial leak logic
st.header("🚨 Leak Detection")

if flow > 75 and pressure < 2.5:
    st.error("🚨 Possible Water Leak Detected!")
    st.warning("Abnormal combination of high flow and low pressure.")
elif flow > 60:
    st.warning("⚠️ Unusual Water Flow Detected")
else:
    st.success("✅ No Leak Detected")

# Information section
st.divider()

st.header("ℹ️ About AquaSentinel AI")

st.write(
    """
    AquaSentinel AI is an intelligent water monitoring system designed
    to detect possible pipeline leaks by analyzing sensor data such as
    water flow and pressure.

    The system can later be enhanced with a machine learning model
    trained on historical sensor data to detect abnormal patterns.
    """
)
