import streamlit as st
from agent_workflow import (
    run_aquasentinel_workflow,
    seed_historical_incidents
)

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AquaSentinel AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0, 174, 255, 0.16), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(0, 119, 255, 0.13), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(0, 220, 255, 0.10), transparent 35%),
        linear-gradient(135deg, #020b18 0%, #03152b 45%, #02101f 100%);
    color: #eaf7ff;
}

/* Water-like animated glow */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 150px;
    pointer-events: none;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(0, 198, 255, 0.25), transparent 45%),
        radial-gradient(ellipse at 70% 30%, rgba(0, 125, 255, 0.22), transparent 50%);
    filter: blur(25px);
    z-index: 0;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(2, 17, 38, 0.98),
            rgba(1, 10, 24, 0.98)
        );
    border-right: 1px solid rgba(0, 183, 255, 0.25);
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #e8f7ff;
}

/* Cards */
.dashboard-card {
    background:
        linear-gradient(
            145deg,
            rgba(9, 42, 76, 0.88),
            rgba(2, 21, 42, 0.92)
        );
    border: 1px solid rgba(0, 185, 255, 0.25);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

/* KPI cards */
.kpi-card {
    background:
        linear-gradient(
            145deg,
            rgba(9, 52, 91, 0.92),
            rgba(3, 24, 48, 0.95)
        );
    border: 1px solid rgba(0, 190, 255, 0.32);
    border-radius: 18px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    transition: transform 0.2s ease, border 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(0, 220, 255, 0.7);
}

.kpi-title {
    color: #a9d9ef;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    color: #f3fbff;
    font-size: 31px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-sub {
    color: #6fdcff;
    font-size: 12px;
    margin-top: 5px;
}

/* Status badges */
.status-online {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: rgba(0, 220, 150, 0.12);
    border: 1px solid rgba(0, 255, 170, 0.45);
    color: #35f2b0;
    font-weight: 700;
    font-size: 13px;
}

.status-critical {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 20px;
    background: rgba(255, 55, 85, 0.13);
    border: 1px solid rgba(255, 70, 95, 0.5);
    color: #ff6c80;
    font-weight: 700;
}

.status-warning {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 20px;
    background: rgba(255, 180, 0, 0.12);
    border: 1px solid rgba(255, 190, 0, 0.5);
    color: #ffc44d;
    font-weight: 700;
}

.status-normal {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 20px;
    background: rgba(0, 220, 150, 0.12);
    border: 1px solid rgba(0, 255, 170, 0.45);
    color: #35f2b0;
    font-weight: 700;
}

/* AI pipeline */
.pipeline-step {
    background: linear-gradient(
        135deg,
        rgba(5, 42, 74, 0.92),
        rgba(3, 21, 43, 0.95)
    );
    border: 1px solid rgba(0, 190, 255, 0.24);
    border-radius: 13px;
    padding: 13px 15px;
    margin: 7px 0;
}

.pipeline-title {
    color: #dff7ff;
    font-weight: 700;
    font-size: 14px;
}

.pipeline-result {
    color: #62dfff;
    font-size: 12px;
    margin-top: 3px;
}

/* Section headings */
.section-title {
    color: #f0fbff;
    font-size: 21px;
    font-weight: 800;
    margin: 18px 0 12px 0;
}

.section-caption {
    color: #86b9cc;
    font-size: 13px;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(0, 198, 255, 0.45);
    background: linear-gradient(
        90deg,
        #007cff,
        #00bfff
    );
    color: white;
    font-weight: 700;
    min-height: 46px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #5fe9ff;
    box-shadow: 0 0 22px rgba(0, 191, 255, 0.35);
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(4, 31, 56, 0.8);
    border-radius: 12px;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(4, 30, 53, 0.72);
    border: 1px solid rgba(0, 180, 255, 0.18);
    padding: 14px;
    border-radius: 14px;
}

/* Progress bar */
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #00aaff, #00e6ff);
}

/* Divider */
hr {
    border-color: rgba(0, 190, 255, 0.15);
}

/* Water wave decoration */
.water-wave {
    height: 5px;
    margin: 8px 0 20px 0;
    border-radius: 50%;
    background: linear-gradient(
        90deg,
        transparent,
        #00bfff,
        #47e9ff,
        #008cff,
        transparent
    );
    box-shadow: 0 0 18px rgba(0, 200, 255, 0.55);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "last_flow" not in st.session_state:
    st.session_state.last_flow = None

if "last_pressure" not in st.session_state:
    st.session_state.last_pressure = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px 0 20px 0;">
            <div style="font-size:55px;">💧</div>
            <div style="font-size:23px; font-weight:800; color:#55ddff;">
                AquaSentinel AI
            </div>
            <div style="font-size:12px; color:#82b8ca;">
                Intelligent Water Monitoring
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🎛️ Simulation Controls")

    simulation = st.selectbox(
        "Simulation Mode",
        [
            "Normal Operation",
            "High Flow Warning",
            "Simulate Leak",
            "Custom Sensor Input"
        ]
    )

    if simulation == "Normal Operation":

        default_flow = 42
        default_pressure = 3.2

    elif simulation == "High Flow Warning":

        default_flow = 68
        default_pressure = 3.0

    elif simulation == "Simulate Leak":

        default_flow = 87
        default_pressure = 1.8

    else:

        default_flow = 55
        default_pressure = 3.2


    st.markdown("#### 🌊 Flow Sensor")

    if simulation == "Custom Sensor Input":

        flow = st.slider(
            "Water Flow (L/min)",
            min_value=20,
            max_value=120,
            value=default_flow
        )

        pressure = st.slider(
            "Pipeline Pressure (bar)",
            min_value=1.0,
            max_value=5.0,
            value=float(default_pressure),
            step=0.1
        )

    else:

        flow = default_flow
        pressure = default_pressure

        st.info(
            f"Flow: **{flow} L/min**  \n"
            f"Pressure: **{pressure} bar**"
        )


    zone = st.selectbox(
        "Monitoring Zone",
        ["Zone A", "Zone B", "Zone C"]
    )

    st.markdown("---")

    if st.button("🔍 Run AI Assessment"):

        with st.spinner("Connecting to historical memory..."):

            seed_historical_incidents()

        with st.spinner("Running AquaSentinel AI..."):

            result = run_aquasentinel_workflow(
                flow,
                pressure
            )

        st.session_state.workflow_result = result
        st.session_state.last_flow = flow
        st.session_state.last_pressure = pressure

        st.success("AI assessment completed!")


    if st.button("🔄 Reset Dashboard"):

        st.session_state.workflow_result = None
        st.session_state.last_flow = None
        st.session_state.last_pressure = None
        st.rerun()


    st.markdown("---")

    st.markdown(
        """
        <div class="status-online">
        ● SYSTEM ONLINE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Monitoring Zone A • Live sensor simulation")


# ============================================================
# CALCULATED DISPLAY VALUES
# ============================================================

if simulation == "Normal Operation":

    leak_probability = 8
    status = "NORMAL"

elif simulation == "High Flow Warning":

    leak_probability = 38
    status = "WARNING"

elif simulation == "Simulate Leak":

    leak_probability = 94
    status = "LEAK DETECTED"

else:

    risk = 0

    if flow > 60:
        risk += 35

    if pressure < 2.5:
        risk += 35

    if flow > 80 and pressure < 2.2:
        risk += 30

    leak_probability = min(risk, 100)

    if leak_probability >= 70:
        status = "LEAK DETECTED"
    elif leak_probability >= 30:
        status = "WARNING"
    else:
        status = "NORMAL"


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns([4, 1])

with header_col1:

    st.markdown(
        """
        <div style="padding-top:8px;">
            <div style="
                font-size:38px;
                font-weight:800;
                color:#f2fbff;
            ">
                💧 AquaSentinel <span style="color:#22cfff;">AI</span>
            </div>

            <div style="
                font-size:15px;
                color:#88bdd0;
                margin-top:-5px;
            ">
                AI-Powered Water Infrastructure Monitoring & Leak Detection
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:

    st.markdown(
        """
        <div style="text-align:right; padding-top:12px;">
            <span class="status-online">
                ● SYSTEM ONLINE
            </span>
            <br>
            <span style="font-size:11px; color:#719caf;">
                Live Sensor Simulation
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="water-wave"></div>', unsafe_allow_html=True)


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Live System Overview</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)


with k1:

    flow_state = "HIGH" if flow > 60 else "NORMAL"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💧 WATER FLOW</div>
            <div class="kpi-value">{flow} <span style="font-size:15px;">L/min</span></div>
            <div class="kpi-sub">Normal range: 30–60 L/min</div>
            <div style="margin-top:9px;">
                <span class="{'status-warning' if flow > 60 else 'status-normal'}">
                    {flow_state}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    pressure_state = "LOW" if pressure < 2.5 else "NORMAL"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📡 PIPELINE PRESSURE</div>
            <div class="kpi-value">{pressure} <span style="font-size:15px;">bar</span></div>
            <div class="kpi-sub">Expected: 2.5–4.5 bar</div>
            <div style="margin-top:9px;">
                <span class="{'status-critical' if pressure < 2.5 else 'status-normal'}">
                    {pressure_state}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    risk_class = (
        "status-critical"
        if leak_probability >= 70
        else "status-warning"
        if leak_probability >= 30
        else "status-normal"
    )

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⚠️ LEAK PROBABILITY</div>
            <div class="kpi-value">{leak_probability}%</div>
            <div class="kpi-sub">AI estimated incident risk</div>
            <div style="margin-top:9px;">
                <span class="{risk_class}">
                    {status}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    status_class = (
        "status-critical"
        if status == "LEAK DETECTED"
        else "status-warning"
        if status == "WARNING"
        else "status-normal"
    )

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛡️ SYSTEM STATUS</div>
            <div class="kpi-value" style="font-size:24px;">
                {status}
            </div>
            <div class="kpi-sub">{zone} monitoring</div>
            <div style="margin-top:9px;">
                <span class="{status_class}">
                    ● LIVE
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Live Sensor Analytics</div>',
    unsafe_allow_html=True
)

chart_col, incident_col = st.columns([2.2, 1])


# ============================================================
# SENSOR TREND
# ============================================================

with chart_col:

    np.random.seed(42)

    times = [
        datetime.now() - timedelta(minutes=5 * (19 - i))
        for i in range(20)
    ]

    if simulation == "Simulate Leak":

        flow_values = np.concatenate([
            np.random.normal(42, 2, 12),
            np.random.normal(85, 4, 8)
        ])

        pressure_values = np.concatenate([
            np.random.normal(3.4, 0.12, 12),
            np.random.normal(1.8, 0.12, 8)
        ])

    elif simulation == "High Flow Warning":

        flow_values = np.random.normal(68, 3, 20)
        pressure_values = np.random.normal(3.0, 0.12, 20)

    elif simulation == "Custom Sensor Input":

        flow_values = np.random.normal(flow, max(flow * 0.035, 1), 20)
        pressure_values = np.random.normal(
            pressure,
            max(pressure * 0.035, 0.05),
            20
        )

    else:

        flow_values = np.random.normal(42, 2, 20)
        pressure_values = np.random.normal(3.3, 0.12, 20)


    trend_data = pd.DataFrame({
        "Time": times,
        "Flow": flow_values,
        "Pressure": pressure_values
    })


    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend_data["Time"],
            y=trend_data["Flow"],
            mode="lines",
            name="Flow (L/min)",
            line=dict(width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend_data["Time"],
            y=trend_data["Pressure"],
            mode="lines",
            name="Pressure (bar)",
            yaxis="y2",
            line=dict(width=3)
        )
    )

    fig.update_layout(
        height=390,
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,18,35,0.5)",
        font=dict(color="#ccefff"),
        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(100,180,220,0.08)"
        ),
        yaxis=dict(
            title="Flow",
            showgrid=True,
            gridcolor="rgba(100,180,220,0.08)"
        ),
        yaxis2=dict(
            title="Pressure",
            overlaying="y",
            side="right",
            showgrid=False
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False
        }
    )


# ============================================================
# INCIDENT CARD
# ============================================================

with incident_col:

    if status == "LEAK DETECTED":

        incident_class = "status-critical"
        incident_icon = "🚨"
        incident_text = "PIPELINE LEAK"

    elif status == "WARNING":

        incident_class = "status-warning"
        incident_icon = "⚠️"
        incident_text = "HIGH FLOW WARNING"

    else:

        incident_class = "status-normal"
        incident_icon = "✅"
        incident_text = "SYSTEM NORMAL"


    st.markdown(
        f"""
        <div class="dashboard-card" style="min-height:340px;">

            <div style="
                color:#b6e7f7;
                font-size:15px;
                font-weight:700;
            ">
                🚨 CURRENT INCIDENT
            </div>

            <hr style="border-color:rgba(0,190,255,0.15);">

            <div style="
                font-size:24px;
                font-weight:800;
                color:#f4fbff;
                margin:20px 0 8px 0;
            ">
                {incident_icon} {incident_text}
            </div>

            <span class="{incident_class}">
                {status}
            </span>

            <div style="margin-top:25px;">

                <div style="display:flex; justify-content:space-between; margin:12px 0;">
                    <span style="color:#83b6c9;">Flow</span>
                    <b>{flow} L/min</b>
                </div>

                <div style="display:flex; justify-content:space-between; margin:12px 0;">
                    <span style="color:#83b6c9;">Pressure</span>
                    <b>{pressure} bar</b>
                </div>

                <div style="display:flex; justify-content:space-between; margin:12px 0;">
                    <span style="color:#83b6c9;">Leak Risk</span>
                    <b>{leak_probability}%</b>
                </div>

                <div style="display:flex; justify-content:space-between; margin:12px 0;">
                    <span style="color:#83b6c9;">Zone</span>
                    <b>{zone}</b>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AI DECISION PIPELINE
# ============================================================

st.markdown(
    '<div class="section-title">🧠 AI Decision Pipeline</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-caption">
    Multi-layer incident intelligence: sensor analysis → historical memory →
    AI reasoning → security validation → action.
    </div>
    """,
    unsafe_allow_html=True
)


if st.session_state.workflow_result:

    result = st.session_state.workflow_result

    ml = result["ml_result"]
    rules = result["rule_result"]
    memory = result["qdrant_memory"]
    lyzr = result["lyzr"]
    enkrypt = result["enkrypt"]


    p1, p2, p3, p4, p5 = st.columns(5)


    with p1:

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center; min-height:130px;">
                <div style="font-size:25px;">🧠</div>
                <b>ML ANALYSIS</b>
                <div style="font-size:23px; color:#37d8ff; margin-top:8px;">
                    {ml["anomaly_score"]}%
                </div>
                <small style="color:#8eb9ca;">
                    Anomaly Score
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with p2:

        rule_status = rules["status"]

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center; min-height:130px;">
                <div style="font-size:25px;">⚙️</div>
                <b>RULE ENGINE</b>
                <div style="
                    font-size:21px;
                    color:{'#ff647c' if rule_status == 'ALERT' else '#35f2b0'};
                    margin-top:8px;
                ">
                    {rule_status}
                </div>
                <small style="color:#8eb9ca;">
                    {len(rules["alerts"])} conditions
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with p3:

        matches = memory.get("matches", [])

        best_score = (
            matches[0]["score"]
            if matches
            else 0
        )

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center; min-height:130px;">
                <div style="font-size:25px;">🗄️</div>
                <b>QDRANT MEMORY</b>
                <div style="font-size:21px; color:#37d8ff; margin-top:8px;">
                    {best_score:.3f}
                </div>
                <small style="color:#8eb9ca;">
                    Best similarity
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with p4:

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center; min-height:130px;">
                <div style="font-size:25px;">🤖</div>
                <b>LYZR AGENT</b>
                <div style="font-size:20px; color:#ff657c; margin-top:8px;">
                    {"READY" if lyzr["available"] else "UNAVAILABLE"}
                </div>
                <small style="color:#8eb9ca;">
                    Decision Layer
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with p5:

        safe = enkrypt["safe"]

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center; min-height:130px;">
                <div style="font-size:25px;">🛡️</div>
                <b>ENKRYPT</b>
                <div style="
                    font-size:21px;
                    color:{'#35f2b0' if safe else '#ff647c'};
                    margin-top:8px;
                ">
                    {"SAFE" if safe else "BLOCKED"}
                </div>
                <small style="color:#8eb9ca;">
                    Security Guardrail
                </small>
            </div>
            """,
            unsafe_allow_html=True
        )


else:

    st.info(
        "Run **AI Assessment** from the sidebar to activate the complete "
        "ML → Rules → Qdrant → Lyzr → Enkrypt pipeline."
    )


# ============================================================
# AI ASSESSMENT RESULT
# ============================================================

if st.session_state.workflow_result:

    result = st.session_state.workflow_result

    st.markdown(
        '<div class="section-title">🤖 AI Incident Assessment</div>',
        unsafe_allow_html=True
    )

    final_status = result["final_status"]


    if final_status == "NORMAL":

        st.success(
            f"✅ System Assessment: **{final_status}**"
        )

    elif final_status == "HUMAN REVIEW REQUIRED":

        st.warning(
            f"⚠️ System Assessment: **{final_status}**"
        )

    elif final_status == "BLOCKED BY SECURITY GUARDRAIL":

        st.error(
            f"🛡️ System Assessment: **{final_status}**"
        )

    else:

        st.error(
            f"🚨 System Assessment: **{final_status}**"
        )


    st.markdown(
        f"""
        <div class="dashboard-card">

            <div style="
                font-size:18px;
                color:#56ddff;
                font-weight:800;
            ">
                🧠 LYZR DECISION AGENT
            </div>

            <div style="
                margin-top:18px;
                color:#d8f4ff;
                font-size:15px;
                line-height:1.7;
            ">
                {lyzr["assessment"].replace(chr(10), "<br>")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ALERT CENTER
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Alert Center</div>',
    unsafe_allow_html=True
)

if status == "LEAK DETECTED":

    alert_data = pd.DataFrame({
        "Time": ["Current"],
        "Alert": ["Pipeline Leak Detected"],
        "Severity": ["CRITICAL"],
        "Zone": [zone],
        "Recommended Action": ["Inspect Pipeline"]
    })

    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )

elif status == "WARNING":

    alert_data = pd.DataFrame({
        "Time": ["Current"],
        "Alert": ["High Water Flow"],
        "Severity": ["MEDIUM"],
        "Zone": [zone],
        "Recommended Action": ["Monitor System"]
    })

    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("✅ No active critical alerts.")


# ============================================================
# HISTORICAL MEMORY
# ============================================================

if st.session_state.workflow_result:

    memory = st.session_state.workflow_result["qdrant_memory"]

    st.markdown(
        '<div class="section-title">🗄️ Qdrant Historical Context</div>',
        unsafe_allow_html=True
    )

    matches = memory.get("matches", [])

    if matches:

        history_rows = []

        for match in matches:

            incident = match["incident"]

            history_rows.append({
                "Similarity": round(match["score"], 3),
                "Incident": incident.get("incident_type", "Unknown"),
                "Severity": incident.get("severity", "Unknown"),
                "Flow": f'{incident.get("flow_lpm", "-")} L/min',
                "Pressure": f'{incident.get("pressure_bar", "-")} bar',
                "Zone": incident.get("zone", "-")
            })

        history_df = pd.DataFrame(history_rows)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No historical incidents were retrieved.")


# ============================================================
# TECHNICAL WORKFLOW DETAILS
# ============================================================

if st.session_state.workflow_result:

    result = st.session_state.workflow_result

    with st.expander("🔎 View Full AI Workflow Details"):

        st.markdown("### 1️⃣ ML Anomaly Detection")

        st.json(
            result["ml_result"]
        )


        st.markdown("### 2️⃣ Rule-Based Detection")

        st.json(
            result["rule_result"]
        )


        st.markdown("### 3️⃣ Qdrant Historical Memory")

        if result["qdrant_memory"]["available"]:

            st.success(
                "Historical incident context successfully retrieved from Qdrant."
            )

        st.json(
            result["qdrant_memory"]
        )


        st.markdown("### 🧠 Qdrant Memory Write-Back")

        if result["memory_write"]["stored"]:

            st.success(
                "New incident successfully stored in Qdrant memory."
            )

        st.json(
            result["memory_write"]
        )


        st.markdown("### 4️⃣ Lyzr Decision Agent")

        if result["lyzr"]["available"]:

            st.success(
                "Lyzr AI decision agent completed the assessment."
            )

        st.write(
            result["lyzr"]["assessment"]
        )


        st.markdown("### 5️⃣ Enkrypt Security Guardrail")

        if result["enkrypt"]["available"]:

            if result["enkrypt"]["safe"]:

                st.success(
                    "Enkrypt security check passed."
                )

            else:

                st.error(
                    "Enkrypt security guardrail blocked the response."
                )

        st.json(
            result["enkrypt"]
        )


# ============================================================
# ARCHITECTURE
# ============================================================

st.markdown(
    '<div class="section-title">🏗️ AquaSentinel AI Architecture</div>',
    unsafe_allow_html=True
)

a1, a2, a3, a4, a5 = st.columns(5)

architecture = [
    ("🌊", "Sensors", "Flow + Pressure"),
    ("🧠", "ML + Rules", "Anomaly Detection"),
    ("🗄️", "Qdrant", "Historical Memory"),
    ("🤖", "Lyzr", "AI Decision"),
    ("🛡️", "Enkrypt", "Security Guardrail")
]

for col, item in zip(
    [a1, a2, a3, a4, a5],
    architecture
):

    with col:

        st.markdown(
            f"""
            <div class="dashboard-card" style="text-align:center;">
                <div style="font-size:30px;">
                    {item[0]}
                </div>

                <div style="
                    font-weight:800;
                    color:#e9faff;
                    margin-top:8px;
                ">
                    {item[1]}
                </div>

                <div style="
                    color:#72b8cc;
                    font-size:12px;
                    margin-top:5px;
                ">
                    {item[2]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    """
    <div class="dashboard-card" style="text-align:center;">

        <div style="
            font-size:15px;
            color:#70dcff;
            font-weight:700;
        ">
            SENSOR DATA
            &nbsp; → &nbsp;
            INTELLIGENCE
            &nbsp; → &nbsp;
            MEMORY
            &nbsp; → &nbsp;
            AI DECISION
            &nbsp; → &nbsp;
            SECURITY
            &nbsp; → &nbsp;
            ACTION
        </div>

        <div style="
            color:#7eaabd;
            font-size:12px;
            margin-top:10px;
        ">
            Confirmed incidents are written back into Qdrant
            for future contextual retrieval.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ABOUT
# ============================================================

with st.expander("ℹ️ About AquaSentinel AI"):

    st.write(
        """
        **AquaSentinel AI** is an intelligent water infrastructure
        monitoring solution designed to detect potential pipeline
        leaks by analyzing water-flow and pressure patterns.

        The system combines deterministic rules, anomaly analysis,
        historical incident memory through Qdrant, AI-assisted
        decision making through Lyzr, and security validation
        through Enkrypt AI.

        The current prototype uses simulated sensor data and is
        designed to support real flow and pressure sensors in a
        future deployment.
        """
    )

st.markdown(
    """
    <div style="
        text-align:center;
        color:#537f91;
        font-size:11px;
        padding:30px 0 10px 0;
    ">
        AquaSentinel AI • Intelligent Water Infrastructure Monitoring
    </div>
    """,
    unsafe_allow_html=True
)
