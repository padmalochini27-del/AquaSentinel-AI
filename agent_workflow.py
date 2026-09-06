import os
import json
import numpy as np
def get_secret(name):
    value = os.getenv(name)

    if value:
        return value

    try:
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None

# -----------------------------
# OPTIONAL AI SERVICE IMPORTS
# -----------------------------

try:
    from lyzr import Studio
    LYZR_AVAILABLE = True
except Exception:
    LYZR_AVAILABLE = False

try:
    from qdrant_client import QdrantClient, models
    QDRANT_AVAILABLE = True
except Exception:
    QDRANT_AVAILABLE = False

try:
    from enkryptai_sdk import GuardrailsClient
    ENKRYPT_AVAILABLE = True
except Exception:
    ENKRYPT_AVAILABLE = False

# -----------------------------
# RULE-BASED DETECTION
# -----------------------------

def rule_based_detection(flow, pressure):
    """
    Critical rule-based checks for pipeline conditions.
    """

    alerts = []

    if pressure < 2.0 and flow > 70:
        alerts.append("Critical pressure drop with unusually high flow")

    if flow > 80:
        alerts.append("High flow condition detected")

    if pressure < 2.2:
        alerts.append("Low pressure condition detected")

    if alerts:
        return {
            "status": "ALERT",
            "alerts": alerts
        }

    return {
        "status": "NORMAL",
        "alerts": []
    }


# -----------------------------
# ML DETECTION
# -----------------------------

def ml_detection(flow, pressure):
    """
    Lightweight anomaly score based on the existing
    sensor operating range.
    """

    normal_flow = 43.0
    normal_pressure = 3.4

    flow_deviation = abs(flow - normal_flow) / normal_flow
    pressure_deviation = abs(pressure - normal_pressure) / normal_pressure

    score = (flow_deviation * 0.5 + pressure_deviation * 0.5) * 100

    score = float(np.clip(score, 0, 100))

    return {
        "anomaly_score": round(score, 2),
        "anomaly": score >= 35
    }


# -----------------------------
# QDRANT MEMORY
# -----------------------------

def get_qdrant_client():
    if not QDRANT_AVAILABLE:
        return None

    url = get_secret("QDRANT_URL")
    api_key = get_secret("QDRANT_API_KEY")

    if not url:
        return None

    return QdrantClient(
        url=url,
        api_key=api_key
    )


def create_sensor_vector(flow, pressure):
    """
    Small deterministic vector representing the
    current sensor pattern.
    """

    vector = [
        flow / 100.0,
        pressure / 5.0,
        abs(flow - 43.0) / 100.0,
        abs(pressure - 3.4) / 5.0
    ]

    return vector
def seed_historical_incidents():
    client = get_qdrant_client()

    if client is None:
        return {
            "available": False,
            "message": "Qdrant is not configured."
        }

    collection_name = "aquasentinel_incidents"

    incidents = [
        {
            "flow": 88,
            "pressure": 1.7,
            "type": "Pipeline Leak",
            "severity": "CRITICAL",
            "zone": "Zone A"
        },
        {
            "flow": 82,
            "pressure": 1.9,
            "type": "Pressure Drop",
            "severity": "HIGH",
            "zone": "Zone A"
        },
        {
            "flow": 76,
            "pressure": 2.1,
            "type": "High Flow Event",
            "severity": "MEDIUM",
            "zone": "Zone B"
        },
        {
            "flow": 43,
            "pressure": 3.4,
            "type": "Normal Operation",
            "severity": "LOW",
            "zone": "Zone A"
        }
    ]

    points = []

    for i, incident in enumerate(incidents):

        vector = create_sensor_vector(
            incident["flow"],
            incident["pressure"]
        )

        points.append(
            models.PointStruct(
                id=i + 1,
                vector={
                    "sensor_vector": vector
                },
                payload={
                    "flow_lpm": incident["flow"],
                    "pressure_bar": incident["pressure"],
                    "incident_type": incident["type"],
                    "severity": incident["severity"],
                    "zone": incident["zone"]
                }
            )
        )

    try:
        client.upsert(
            collection_name=collection_name,
            points=points
        )

        return {
            "available": True,
            "message": f"{len(points)} historical incidents stored in Qdrant."
        }

    except Exception as e:
        return {
            "available": False,
            "message": f"Qdrant seed error: {str(e)}"
        }


def retrieve_historical_context(flow, pressure):
    """
    Retrieve similar historical incidents from Qdrant.
    """

    client = get_qdrant_client()

    if client is None:
        return {
            "available": False,
            "matches": []
        }

    collection_name = "aquasentinel_incidents"
    vector = create_sensor_vector(flow, pressure)

    try:
        results = client.query_points(
            collection_name=collection_name,
            query=vector,
            using="sensor_vector",
            limit=5
        ).points

        matches = []

        for result in results:
            matches.append({
                "score": round(float(result.score), 3),
                "incident": result.payload
            })

        return {
            "available": True,
            "matches": matches
        }

    except Exception as e:
        return {
            "available": False,
            "matches": [],
            "error": str(e)
        }


# -----------------------------
# LYZR AGENT
# -----------------------------

def run_lyzr_agent(sensor_data, ml_result, rule_result, memory):
    """
    Lyzr harmonizes ML detection, rule detection,
    and historical context into one assessment.
    """

    if not LYZR_AVAILABLE:
        return {
            "available": False,
            "assessment": "Lyzr is not configured yet."
        }

    api_key = get_secret("LYZR_API_KEY")

    if not api_key:
        return {
            "available": False,
            "assessment": "LYZR_API_KEY is not configured."
        }

    try:
        studio = Studio(api_key=api_key)

        agent = studio.create_agent(
            name="AquaSentinel Decision Agent",
            provider="gpt-4o",
            role="Water infrastructure incident decision agent",
            goal="Analyze sensor anomalies and produce safe actionable incident assessments",
            instructions=(
                "You analyze water pipeline sensor conditions. "
                "Combine ML anomaly results, rule-based alerts, and historical "
                "incident context. Do not invent sensor evidence. "
                "If ML and rules conflict, recommend human review. "
                "Return a concise assessment containing severity, likely cause, "
                "recommended action, and confidence."
            ),
            temperature=0.2
        )

        prompt = f"""
AquaSentinel AI incident:

Sensor data:
{json.dumps(sensor_data)}

ML detection:
{json.dumps(ml_result)}

Rule detection:
{json.dumps(rule_result)}

Historical Qdrant context:
{json.dumps(memory)}

Produce a unified incident assessment.
"""

        response = agent.run(prompt)

        return {
            "available": True,
            "assessment": response.response
        }

    except Exception as e:
        return {
            "available": False,
            "assessment": f"Lyzr error: {str(e)}"
        }


# -----------------------------
# ENKRYPT GUARDRAIL
# -----------------------------

def enkrypt_check(text):
    if not ENKRYPT_AVAILABLE:
        return {
            "available": False,
            "safe": True,
            "message": "Enkrypt SDK is not installed or could not be imported."
        }

    api_key = get_secret("ENKRYPTAI_API_KEY")

    if not api_key:
        return {
            "available": False,
            "safe": True,
            "message": "ENKRYPTAI_API_KEY is not configured."
        }

    try:
        client = GuardrailsClient(
            api_key=api_key,
            base_url="https://api.enkryptai.com"
        )

        result = client.detect(text=text)

        # Support SDK response formats
        if hasattr(result, "is_safe"):
            safe_value = result.is_safe
            if callable(safe_value):
                safe_value = safe_value()

        else:
            safe_value = True

        violations = []

        if hasattr(result, "get_violations"):
            violations = result.get_violations()

        return {
            "available": True,
            "safe": bool(safe_value),
            "violations": violations
        }

    except Exception as e:
        return {
            "available": False,
            "safe": True,
            "message": f"Enkrypt error: {str(e)}"
        }
        


# -----------------------------
# COMPLETE WORKFLOW
# -----------------------------

def run_aquasentinel_workflow(flow, pressure):

    sensor_data = {
        "flow_lpm": flow,
        "pressure_bar": pressure,
        "zone": "Zone A"
    }

    ml_result = ml_detection(flow, pressure)

    rule_result = rule_based_detection(flow, pressure)

    conflict = (
        ml_result["anomaly"] != (rule_result["status"] == "ALERT")
    )

    memory = retrieve_historical_context(
        flow,
        pressure
    )

    lyzr_result = run_lyzr_agent(
        sensor_data,
        ml_result,
        rule_result,
        memory
    )

    enkrypt_result = enkrypt_check(
        lyzr_result["assessment"]
    )

    if conflict:
        final_status = "HUMAN REVIEW REQUIRED"
    elif not enkrypt_result["safe"]:
        final_status = "BLOCKED BY SECURITY GUARDRAIL"
    elif ml_result["anomaly"] or rule_result["status"] == "ALERT":
        final_status = "LEAK / ANOMALY DETECTED"
    else:
        final_status = "NORMAL"

    return {
        "sensor_data": sensor_data,
        "ml_result": ml_result,
        "rule_result": rule_result,
        "conflict": conflict,
        "qdrant_memory": memory,
        "lyzr": lyzr_result,
        "enkrypt": enkrypt_result,
        "final_status": final_status
    }
