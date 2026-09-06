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
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AquaSentinel AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM UI / CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    /* ======================================================
       MAIN WATER-THEMED BACKGROUND
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                ellipse at 50% -10%,
                rgba(0, 194, 255, 0.32),
                transparent 38%
            ),
            radial-gradient(
                ellipse at 10% 30%,
                rgba(0, 105, 255, 0.16),
                transparent 35%
            ),
            radial-gradient(
                ellipse at 90% 70%,
                rgba(0, 220, 255, 0.10),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #010914 0%,
                #02172c 38%,
                #021226 70%,
                #010914 100%
            );

        color: #ecfaff;
    }


    /* Water glow at top */

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 190px;

        background:
            radial-gradient(
                ellipse at 20% 50%,
                rgba(0, 211, 255, 0.22),
                transparent 42%
            ),
            radial-gradient(
                ellipse at 50% 30%,
                rgba(0, 130, 255, 0.25),
                transparent 48%
            ),
            radial-gradient(
                ellipse at 80% 60%,
                rgba(0, 215, 255, 0.18),
                transparent 42%
            );

        filter: blur(25px);
        pointer-events: none;
        z-index: 0;
    }


    /* Subtle wave lines */

    .stApp::after {
        content: "";
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        height: 85px;

        background:
            repeating-radial-gradient(
                ellipse at 50% 100%,
                transparent 0px,
                transparent 12px,
                rgba(0, 201, 255, 0.05) 13px,
                transparent 25px
            );

        pointer-events: none;
        z-index: 0;
    }


    /* ======================================================
       STREAMLIT CLEANUP
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(1, 18, 38, 0.98),
                rgba(1, 9, 22, 0.99)
            );

        border-right: 1px solid rgba(0, 196, 255, 0.28);
    }


    section[data-testid="stSidebar"] * {
        color: #e7f8ff;
    }


    /* ======================================================
       DASHBOARD CARDS
       ====================================================== */

    .dashboard-card {

        background:
            linear-gradient(
                145deg,
                rgba(7, 47, 82, 0.88),
                rgba(2, 20, 40, 0.94)
            );

        border: 1px solid rgba(0, 194, 255, 0.25);

        border-radius: 18px;

        padding: 20px;

        margin-bottom: 14px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }


    /* ======================================================
       KPI CARDS
       ====================================================== */

    .kpi-card {

        background:
            linear-gradient(
                145deg,
                rgba(8, 56, 96, 0.94),
                rgba(2, 25, 49, 0.97)
            );

        border: 1px solid rgba(0, 197, 255, 0.34);

        border-radius: 18px;

        padding: 20px;

        min-height: 158px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.26);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }


    .kpi-card:hover {

        transform: translateY(-4px);

        border-color:
            rgba(0, 221, 255, 0.72);

        box-shadow:
            0 12px 38px rgba(0, 177, 255, 0.16);
    }


    .kpi-title {

        color: #a9dcec;

        font-size: 13px;

        font-weight: 700;

        letter-spacing: 0.4px;
    }


    .kpi-value {

        color: #f3fbff;

        font-size: 32px;

        font-weight: 800;

        margin-top: 9px;
    }


    .kpi-sub {

        color: #70c9e5;

        font-size: 11px;

        margin-top: 5px;
    }


    /* ======================================================
       STATUS BADGES
       ====================================================== */

    .status-online {

        display: inline-block;

        padding: 8px 16px;

        border-radius: 30px;

        background:
            rgba(0, 230, 160, 0.10);

        border:
            1px solid rgba(0, 255, 175, 0.45);

        color: #36f2b2;

        font-weight: 800;

        font-size: 12px;
    }


    .status-critical {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 20px;

        background:
            rgba(255, 55, 85, 0.13);

        border:
            1px solid rgba(255, 80, 105, 0.50);

        color: #ff6c82;

        font-weight: 800;

        font-size: 11px;
    }


    .status-warning {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 20px;

        background:
            rgba(255, 183, 0, 0.12);

        border:
            1px solid rgba(255, 190, 0, 0.50);

        color: #ffc64f;

        font-weight: 800;

        font-size: 11px;
    }


    .status-normal {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 20px;

        background:
            rgba(0, 230, 160, 0.10);

        border:
            1px solid rgba(0, 255, 175, 0.45);

        color: #35f2b0;

        font-weight: 800;

        font-size: 11px;
    }


    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-title {

        color: #f2fbff;

        font-size: 21px;

        font-weight: 800;

        margin-top: 18px;

        margin-bottom: 10px;
    }


    .section-caption {

        color: #7fb4c8;

        font-size: 12px;

        margin-bottom: 12px;
    }


    /* ======================================================
       WATER WAVE DIVIDER
       ====================================================== */

    .water-wave {

        height: 5px;

        margin: 10px 0 22px 0;

        border-radius: 50%;

        background:
            linear-gradient(
                90deg,
                transparent,
                #008cff,
                #29e4ff,
                #00aaff,
                transparent
            );

        box-shadow:
            0 0 20px rgba(0, 207, 255, 0.65);
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        width: 100%;

        min-height: 45px;

        border-radius: 12px;

        border:
            1px solid rgba(0, 205, 255, 0.45);

        background:
            linear-gradient(
                90deg,
                #007bff,
                #00bfff
            );

        color: white;

        font-weight: 800;

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        border-color: #64ebff;

        box-shadow:
            0 0 22px rgba(0, 191, 255, 0.38);
    }


    /* ======================================================
       STREAMLIT METRICS
       ====================================================== */

    [data-testid="stMetric"] {

        background:
            rgba(4, 31, 55, 0.75);

        border:
            1px solid rgba(0, 190, 255, 0.18);

        padding: 13px;

        border-radius: 14px;
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {

        border:
            1px solid rgba(0, 188, 255, 0.20);

        border-radius: 14px;

        background:
            rgba(2, 22, 41, 0.65);
    }


    /* ======================================================
       DATAFRAMES
       ====================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {

        border-color:
            rgba(0, 190, 255, 0.14);
    }

    </style>
    """,
    unsafe_allow_html=True
)


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
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">

            <div style="font-size:52px;">
                💧
            </div>

            <div style="
                font-size:23px;
                font-weight:800;
                color:#4cddff;
            ">
                AquaSentinel AI
            </div>

            <div style="
                font-size:11px;
                color:#78aabd;
                margin-top:3px;
            ">
                Intelligent Water Infrastructure
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


    # --------------------------------------------------------
    # PRESET VALUES
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SENSOR CONTROLS
    # --------------------------------------------------------

    if simulation == "Custom Sensor Input":

        st.markdown("#### 💧 Water Flow")

        flow = st.slider(
            "Flow (L/min)",
            min_value=20,
            max_value=120,
            value=default_flow
        )


        st.markdown("#### 📡 Pipeline Pressure")

        pressure = st.slider(
            "Pressure (bar)",
            min_value=1.0,
            max_value=5.0,
            value=float(default_pressure),
            step=0.1
        )

    else:

        flow = default_flow
        pressure = default_pressure

        st.markdown(
            f"""
            <div style="
                background:rgba(8,48,83,0.72);
                border:1px solid rgba(0,180,255,0.18);
                border-radius:12px;
                padding:13px;
                margin-top:10px;
                margin-bottom:15px;
            ">

                <div style="
                    color:#89bfd2;
                    font-size:12px;
                ">
                    Current Sensor Values
                </div>

                <div style="
                    font-size:17px;
                    font-weight:700;
                    margin-top:7px;
                ">
                    💧 {flow} L/min
                </div>

                <div style="
                    font-size:17px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    📡 {pressure} bar
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # MONITORING ZONE
    # --------------------------------------------------------
    # Backend currently processes Zone A, so keep UI aligned.

    st.markdown("#### 📍 Monitoring Zone")

    st.selectbox(
        "Zone",
        ["Zone A"],
        label_visibility="collapsed"
    )


    st.markdown("---")


    # --------------------------------------------------------
    # RUN AI
    # --------------------------------------------------------

    if st.button(
        "🔍 Run AI Assessment",
        use_container_width=True
    ):

        with st.spinner(
            "Loading historical incident memory..."
        ):

            seed_historical_incidents()


        with st.spinner(
            "Running AquaSentinel AI analysis..."
        ):

            workflow_result = run_aquasentinel_workflow(
                flow,
                pressure
            )


        st.session_state.workflow_result = workflow_result

        st.session_state.last_flow = flow

        st.session_state.last_pressure = pressure

        st.success(
            "AI assessment completed!"
        )


    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if st.button(
        "🔄 Reset Dashboard",
        use_container_width=True
    ):

        st.session_state.workflow_result = None

        st.session_state.last_flow = None

        st.session_state.last_pressure = None

        st.rerun()


    st.markdown("---")


    st.markdown(
        """
        <div style="text-align:center;">

            <span class="status-online">
                ● SYSTEM ONLINE
            </span>

            <div style="
                color:#638fa2;
                font-size:10px;
                margin-top:8px;
            ">
                Sensor simulation active
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY STATUS
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

header_col1, header_col2 = st.columns(
    [4, 1]
)


with header_col1:

    st.markdown(
        """
        <div style="
            padding-top:8px;
            margin-bottom:2px;
        ">

            <div style="
                font-size:38px;
                font-weight:800;
                color:#f2fbff;
                line-height:1.1;
            ">
                💧 AquaSentinel
                <span style="color:#22cfff;">
                    AI
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div style="
            font-size:15px;
            color:#88bdd0;
            margin-top:0px;
        ">
            AI-Powered Water Infrastructure Monitoring
            &amp; Leak Detection
        </div>
        """,
        unsafe_allow_html=True
    )


with header_col2:

    st.markdown(
        """
        <div style="
            text-align:right;
            padding-top:12px;
        ">

            <span class="status-online">
                ● SYSTEM ONLINE
            </span>

            <div style="
                font-size:10px;
                color:#719caf;
                margin-top:7px;
            ">
                Live Sensor Simulation
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="water-wave"></div>',
    unsafe_allow_html=True
)


# ============================================================
# LIVE SYSTEM OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📊 Live System Overview
    </div>
    """,
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


# ============================================================
# FLOW KPI
# ============================================================

with k1:

    flow_state = (
        "HIGH"
        if flow > 60
        else "NORMAL"
    )

    flow_class = (
        "status-warning"
        if flow > 60
        else "status-normal"
    )

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                💧 WATER FLOW
            </div>

            <div class="kpi-value">
                {flow}
                <span style="font-size:14px;">
                    L/min
                </span>
            </div>

            <div class="kpi-sub">
                Normal range: 30–60 L/min
            </div>

            <div style="margin-top:10px;">
                <span class="{flow_class}">
                    {flow_state}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PRESSURE KPI
# ============================================================

with k2:

    pressure_state = (
        "LOW"
        if pressure < 2.5
        else "NORMAL"
    )

    pressure_class = (
        "status-critical"
        if pressure < 2.5
        else "status-normal"
    )

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                📡 PIPELINE PRESSURE
            </div>

            <div class="kpi-value">
                {pressure}
                <span style="font-size:14px;">
                    bar
                </span>
            </div>

            <div class="kpi-sub">
                Expected: 2.5–4.5 bar
            </div>

            <div style="margin-top:10px;">
                <span class="{pressure_class}">
                    {pressure_state}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LEAK RISK KPI
# ============================================================

with k3:

    if leak_probability >= 70:

        risk_class = "status-critical"

    elif leak_probability >= 30:

        risk_class = "status-warning"

    else:

        risk_class = "status-normal"


    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                ⚠️ LEAK PROBABILITY
            </div>

            <div class="kpi-value">
                {leak_probability}%
            </div>

            <div class="kpi-sub">
                Estimated incident risk
            </div>

            <div style="margin-top:10px;">
                <span class="{risk_class}">
                    {status}
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SYSTEM STATUS KPI
# ============================================================

with k4:

    if status == "LEAK DETECTED":

        status_class = "status-critical"

    elif status == "WARNING":

        status_class = "status-warning"

    else:

        status_class = "status-normal"


    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                🛡️ SYSTEM STATUS
            </div>

            <div class="kpi-value"
                 style="font-size:23px;">
                {status}
            </div>

            <div class="kpi-sub">
                Monitoring Zone A
            </div>

            <div style="margin-top:10px;">
                <span class="{status_class}">
                    ● LIVE
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SENSOR ANALYTICS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📈 Live Sensor Analytics
    </div>

    <div class="section-caption">
        Interactive flow and pressure monitoring
    </div>
    """,
    unsafe_allow_html=True
)


chart_col, incident_col = st.columns(
    [2.1, 1]
)


# ============================================================
# INTERACTIVE PLOTLY CHART
# ============================================================

with chart_col:

    np.random.seed(42)

    times = [
        datetime.now()
        - timedelta(minutes=5 * (19 - i))
        for i in range(20)
    ]


    if simulation == "Simulate Leak":

        flow_values = np.concatenate(
            [
                np.random.normal(42, 2, 12),
                np.random.normal(85, 4, 8)
            ]
        )

        pressure_values = np.concatenate(
            [
                np.random.normal(3.4, 0.12, 12),
                np.random.normal(1.8, 0.12, 8)
            ]
        )


    elif simulation == "High Flow Warning":

        flow_values = np.random.normal(
            68,
            3,
            20
        )

        pressure_values = np.random.normal(
            3.0,
            0.12,
            20
        )


    elif simulation == "Custom Sensor Input":

        flow_values = np.random.normal(
            flow,
            max(flow * 0.035, 1),
            20
        )

        pressure_values = np.random.normal(
            pressure,
            max(pressure * 0.035, 0.05),
            20
        )


    else:

        flow_values = np.random.normal(
            42,
            2,
            20
        )

        pressure_values = np.random.normal(
            3.3,
            0.12,
            20
        )


    trend_data = pd.DataFrame(
        {
            "Time": times,
            "Flow": flow_values,
            "Pressure": pressure_values
        }
    )


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=trend_data["Time"],
            y=trend_data["Flow"],
            mode="lines+markers",
            name="Flow (L/min)",
            line=dict(
                width=3
            ),
            marker=dict(
                size=5
            )
        )
    )


    fig.add_trace(
        go.Scatter(
            x=trend_data["Time"],
            y=trend_data["Pressure"],
            mode="lines+markers",
            name="Pressure (bar)",
            yaxis="y2",
            line=dict(
                width=3
            ),
            marker=dict(
                size=4
            )
        )
    )


    fig.update_layout(

        height=385,

        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(1,19,38,0.62)",

        font=dict(
            color="#ccefff"
        ),

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),

        hovermode="x unified",

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(100,180,220,0.08)"
        ),

        yaxis=dict(
            title="Flow (L/min)",
            showgrid=True,
            gridcolor="rgba(100,180,220,0.08)"
        ),

        yaxis2=dict(
            title="Pressure (bar)",
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
            "displaylogo": False,
            "scrollZoom": True
        }
    )


# ============================================================
# CURRENT INCIDENT
# ============================================================

with incident_col:

    if status == "LEAK DETECTED":

        incident_icon = "🚨"
        incident_title = "PIPELINE LEAK"
        incident_class = "status-critical"

    elif status == "WARNING":

        incident_icon = "⚠️"
        incident_title = "HIGH FLOW WARNING"
        incident_class = "status-warning"

    else:

        incident_icon = "✅"
        incident_title = "SYSTEM NORMAL"
        incident_class = "status-normal"


    st.markdown(
        f"""
        <div class="dashboard-card"
             style="min-height:340px;">

            <div style="
                color:#b7e8f8;
                font-size:14px;
                font-weight:800;
            ">
                🚨 CURRENT INCIDENT
            </div>

            <hr>

            <div style="
                font-size:22px;
                font-weight:800;
                color:#f4fbff;
                margin:20px 0 9px 0;
            ">
                {incident_icon}
                {incident_title}
            </div>

            <span class="{incident_class}">
                {status}
            </span>


            <div style="margin-top:25px;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin:13px 0;
                ">
                    <span style="color:#83b6c9;">
                        Flow
                    </span>

                    <b>
                        {flow} L/min
                    </b>
                </div>


                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin:13px 0;
                ">
                    <span style="color:#83b6c9;">
                        Pressure
                    </span>

                    <b>
                        {pressure} bar
                    </b>
                </div>


                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin:13px 0;
                ">
                    <span style="color:#83b6c9;">
                        Leak Risk
                    </span>

                    <b>
                        {leak_probability}%
                    </b>
                </div>


                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin:13px 0;
                ">
                    <span style="color:#83b6c9;">
                        Zone
                    </span>

                    <b>
                        Zone A
                    </b>
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
    """
    <div class="section-title">
        🧠 AI Decision Pipeline
    </div>

    <div class="section-caption">
        Sensor intelligence → historical memory →
        AI reasoning → security validation → action
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


    # --------------------------------------------------------
    # ML
    # --------------------------------------------------------

    with p1:

        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center; min-height:130px;">

                <div style="font-size:26px;">
                    🧠
                </div>

                <b>ML ANALYSIS</b>

                <div style="
                    font-size:22px;
                    color:#36d8ff;
                    margin-top:8px;
                ">
                    {ml["anomaly_score"]}%
                </div>

                <small style="color:#8eb9ca;">
                    Anomaly Score
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # RULE ENGINE
    # --------------------------------------------------------

    with p2:

        rule_status = rules["status"]

        rule_color = (
            "#ff647c"
            if rule_status == "ALERT"
            else "#35f2b0"
        )


        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center; min-height:130px;">

                <div style="font-size:26px;">
                    ⚙️
                </div>

                <b>RULE ENGINE</b>

                <div style="
                    font-size:21px;
                    color:{rule_color};
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


    # --------------------------------------------------------
    # QDRANT
    # --------------------------------------------------------

    with p3:

        matches = memory.get(
            "matches",
            []
        )


        best_score = (
            matches[0]["score"]
            if matches
            else 0
        )


        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center; min-height:130px;">

                <div style="font-size:26px;">
                    🗄️
                </div>

                <b>QDRANT MEMORY</b>

                <div style="
                    font-size:21px;
                    color:#36d8ff;
                    margin-top:8px;
                ">
                    {best_score:.3f}
                </div>

                <small style="color:#8eb9ca;">
                    Best Similarity
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # LYZR
    # --------------------------------------------------------

    with p4:

        lyzr_status = (
            "READY"
            if lyzr["available"]
            else "UNAVAILABLE"
        )


        lyzr_color = (
            "#35f2b0"
            if lyzr["available"]
            else "#ff647c"
        )


        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center; min-height:130px;">

                <div style="font-size:26px;">
                    🤖
                </div>

                <b>LYZR AGENT</b>

                <div style="
                    font-size:20px;
                    color:{lyzr_color};
                    margin-top:8px;
                ">
                    {lyzr_status}
                </div>

                <small style="color:#8eb9ca;">
                    Decision Layer
                </small>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ENKRYPT
    # --------------------------------------------------------

    with p5:

        safe = enkrypt["safe"]

        enkrypt_color = (
            "#35f2b0"
            if safe
            else "#ff647c"
        )


        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center; min-height:130px;">

                <div style="font-size:26px;">
                    🛡️
                </div>

                <b>ENKRYPT</b>

                <div style="
                    font-size:21px;
                    color:{enkrypt_color};
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
        "Run **AI Assessment** from the sidebar to activate "
        "the complete ML → Rules → Qdrant → Lyzr → Enkrypt pipeline."
    )


# ============================================================
# AI INCIDENT ASSESSMENT
# ============================================================

if st.session_state.workflow_result:

    result = st.session_state.workflow_result

    st.markdown(
        """
        <div class="section-title">
            🤖 AI Incident Assessment
        </div>
        """,
        unsafe_allow_html=True
    )


    final_status = result["final_status"]


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


    # --------------------------------------------------------
    # IMPORTANT:
    # Use normal Streamlit text for Lyzr output instead of
    # unsafe HTML, so model output cannot accidentally break UI.
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="dashboard-card">

            <div style="
                font-size:18px;
                color:#56ddff;
                font-weight:800;
            ">
                🧠 LYZR DECISION AGENT
            </div>

            <div style="
                color:#91c6d8;
                font-size:12px;
                margin-top:4px;
            ">
                Explainable AI incident reasoning
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write(
        result["lyzr"]["assessment"]
    )


# ============================================================
# ALERT CENTER
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🚨 Alert Center
    </div>
    """,
    unsafe_allow_html=True
)


if status == "LEAK DETECTED":

    alert_data = pd.DataFrame(
        {
            "Time": ["Current"],
            "Alert": ["Pipeline Leak Detected"],
            "Severity": ["CRITICAL"],
            "Zone": ["Zone A"],
            "Recommended Action": [
                "Inspect Pipeline"
            ]
        }
    )


    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )


elif status == "WARNING":

    alert_data = pd.DataFrame(
        {
            "Time": ["Current"],
            "Alert": ["High Water Flow"],
            "Severity": ["MEDIUM"],
            "Zone": ["Zone A"],
            "Recommended Action": [
                "Monitor System"
            ]
        }
    )


    st.dataframe(
        alert_data,
        use_container_width=True,
        hide_index=True
    )


else:

    st.success(
        "✅ No active critical alerts."
    )


# ============================================================
# QDRANT HISTORICAL CONTEXT
# ============================================================

if st.session_state.workflow_result:

    memory = (
        st.session_state
        .workflow_result["qdrant_memory"]
    )


    st.markdown(
        """
        <div class="section-title">
            🗄️ Qdrant Historical Context
        </div>

        <div class="section-caption">
            Similar historical incidents retrieved from
            AquaSentinel memory.
        </div>
        """,
        unsafe_allow_html=True
    )


    matches = memory.get(
        "matches",
        []
    )


    if matches:

        history_rows = []


        for match in matches:

            incident = match["incident"]


            history_rows.append(
                {
                    "Similarity": round(
                        match["score"],
                        3
                    ),

                    "Incident": incident.get(
                        "incident_type",
                        "Unknown"
                    ),

                    "Severity": incident.get(
                        "severity",
                        "Unknown"
                    ),

                    "Flow": (
                        f'{incident.get("flow_lpm", "-")}'
                        ' L/min'
                    ),

                    "Pressure": (
                        f'{incident.get("pressure_bar", "-")}'
                        ' bar'
                    ),

                    "Zone": incident.get(
                        "zone",
                        "-"
                    )
                }
            )


        history_df = pd.DataFrame(
            history_rows
        )


        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "No historical incidents were retrieved."
        )


# ============================================================
# SENSOR DATA TABLE
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🌊 Sensor Monitoring
    </div>
    """,
    unsafe_allow_html=True
)


sensor_data = pd.DataFrame(
    {
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
            "Normal"
            if flow <= 60
            else "Abnormal",

            "Normal"
            if pressure >= 2.5
            else "Abnormal",

            status
        ]
    }
)


st.dataframe(
    sensor_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FULL TECHNICAL WORKFLOW
# ============================================================

if st.session_state.workflow_result:

    result = st.session_state.workflow_result


    with st.expander(
        "🔎 View Full AI Workflow Details"
    ):


        st.markdown(
            "### 1️⃣ ML Anomaly Detection"
        )

        st.json(
            result["ml_result"]
        )


        st.markdown(
            "### 2️⃣ Rule-Based Detection"
        )

        st.json(
            result["rule_result"]
        )


        st.markdown(
            "### 3️⃣ Qdrant Historical Memory"
        )


        if result["qdrant_memory"]["available"]:

            st.success(
                "Historical incident context successfully "
                "retrieved from Qdrant."
            )


        else:

            st.info(
                "Qdrant memory is not available."
            )


        st.json(
            result["qdrant_memory"]
        )


        st.markdown(
            "### 🧠 Qdrant Memory Write-Back"
        )


        if result["memory_write"]["stored"]:

            st.success(
                "New incident successfully stored "
                "in Qdrant memory."
            )

        else:

            st.info(
                result["memory_write"]["message"]
            )


        st.json(
            result["memory_write"]
        )


        st.markdown(
            "### 4️⃣ Lyzr Decision Agent"
        )


        if result["lyzr"]["available"]:

            st.success(
                "Lyzr AI decision agent completed "
                "the assessment."
            )

        else:

            st.info(
                "Lyzr is not configured."
            )


        st.write(
            result["lyzr"]["assessment"]
        )


        st.markdown(
            "### 5️⃣ Enkrypt Security Guardrail"
        )


        if result["enkrypt"]["available"]:

            if result["enkrypt"]["safe"]:

                st.success(
                    "Enkrypt security check passed."
                )

            else:

                st.error(
                    "Enkrypt security guardrail "
                    "blocked the response."
                )

        else:

            st.info(
                "Enkrypt is not configured."
            )


        st.json(
            result["enkrypt"]
        )


# ============================================================
# ARCHITECTURE
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🏗️ AquaSentinel AI Architecture
    </div>

    <div class="section-caption">
        End-to-end intelligent incident processing pipeline
    </div>
    """,
    unsafe_allow_html=True
)


architecture = [
    ("🌊", "Sensors", "Flow + Pressure"),
    ("🧠", "ML + Rules", "Anomaly Detection"),
    ("🗄️", "Qdrant", "Historical Memory"),
    ("🤖", "Lyzr", "AI Decision"),
    ("🛡️", "Enkrypt", "Security Guardrail")
]


architecture_cols = st.columns(5)


for col, item in zip(
    architecture_cols,
    architecture
):

    with col:

        st.markdown(
            f"""
            <div class="dashboard-card"
                 style="text-align:center;">

                <div style="
                    font-size:30px;
                ">
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
                    font-size:11px;
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
    <div class="dashboard-card"
         style="text-align:center;">

        <div style="
            font-size:14px;
            color:#70dcff;
            font-weight:800;
        ">

            SENSOR DATA
            &nbsp; → &nbsp;

            ML + RULES
            &nbsp; → &nbsp;

            QDRANT MEMORY
            &nbsp; → &nbsp;

            LYZR DECISION
            &nbsp; → &nbsp;

            ENKRYPT
            &nbsp; → &nbsp;

            ACTION

        </div>

        <div style="
            color:#7eaabd;
            font-size:11px;
            margin-top:9px;
        ">

            Confirmed incidents are written back
            into Qdrant for future contextual retrieval.

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ABOUT
# ============================================================

with st.expander(
    "ℹ️ About AquaSentinel AI"
):

    st.write(
        """
        **AquaSentinel AI** is an intelligent water
        infrastructure monitoring solution designed to detect
        potential pipeline leaks by analyzing water-flow and
        pressure patterns.

        The system combines anomaly analysis, deterministic
        rule-based detection, historical incident memory
        through Qdrant, AI-assisted decision making through
        Lyzr, and security validation through Enkrypt AI.

        The current prototype uses simulated sensor data and
        is designed to support real flow and pressure sensors
        in a future deployment.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#537f91;
        font-size:10px;
        padding:28px 0 12px 0;
    ">

        💧 AquaSentinel AI
        • Intelligent Water Infrastructure Monitoring
        • Zone A

    </div>
    """,
    unsafe_allow_html=True
)
