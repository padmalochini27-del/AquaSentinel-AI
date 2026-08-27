# 💧 AquaSentinel AI

### AI-Powered Water Leak Detection & Monitoring System

AquaSentinel AI is an intelligent water monitoring platform designed to detect potential pipeline leaks by continuously analyzing **water flow and pipeline pressure**.

The system identifies abnormal combinations of sensor readings, estimates the probability of a leak, calculates an anomaly score, and provides alerts through an interactive monitoring dashboard.

---

## 🚨 Problem Statement

Water pipeline leaks can result in:

* 💧 Significant water wastage
* 💰 Increased operational costs
* 🏗️ Infrastructure damage
* 🌍 Unnecessary environmental impact
* ⏱️ Delayed detection and maintenance

Traditional leak detection methods often depend on manual inspection or periodic monitoring, which can delay the identification of small or developing leaks.

---

## 💡 Proposed Solution

**AquaSentinel AI** provides continuous monitoring of water-system conditions using sensor data.

The system analyzes:

* **Water Flow Rate**
* **Pipeline Pressure**
* **Sensor Trends**
* **Anomaly Scores**

When an abnormal pattern is detected, the system estimates the likelihood of a leak and generates an appropriate alert.

### Example

A combination of:

> **High water flow + Low pipeline pressure**

can indicate a potential pipeline leak.

---

## ✨ Key Features

### 🌊 Real-Time Water Monitoring

Displays important water-system parameters such as:

* Water flow in L/min
* Pipeline pressure in bar
* Current system status

### 🤖 AI-Based Anomaly Detection

The system evaluates sensor readings and generates an anomaly score to identify unusual operating conditions.

### 🚨 Leak Detection

The prototype identifies potential leaks based on abnormal flow and pressure combinations.

### 📊 Sensor Trend Visualization

Historical/simulated sensor readings are visualized through interactive charts to make abnormal patterns easier to identify.

### 🧪 Leak Simulation

A built-in simulation mode allows users to demonstrate different operating conditions:

* Normal Operation
* High Flow Warning
* Simulated Leak

This allows the system to be demonstrated without requiring physical sensors.

### 🔔 Alert Center

The system provides alerts based on the detected condition and recommends an appropriate action.

---

## 🏗️ System Architecture

```text
┌──────────────────────┐
│   Water Sensors      │
│                      │
│ Flow + Pressure      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Data Processing    │
│                      │
│ Cleaning & Analysis  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Anomaly Detection    │
│                      │
│ Flow/Pressure        │
│ Pattern Analysis     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Leak Probability     │
│ & Anomaly Score      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Alert Generation     │
│                      │
│ Normal / Warning /   │
│ Leak Detected        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Streamlit Dashboard  │
│                      │
│ Monitoring & Alerts  │
└──────────────────────┘
```

---

## 🧠 AI / ML Approach

The current prototype demonstrates the **AI-ready architecture** using simulated sensor data and anomaly scoring.

The anomaly detection layer evaluates deviations from expected operating conditions.

For example:

```text
Normal Flow + Normal Pressure
            ↓
       Low Anomaly
            ↓
     System Normal
```

```text
High Flow + Low Pressure
            ↓
      High Anomaly
            ↓
    Possible Leak
            ↓
      Alert Generated
```

### Future Machine Learning Integration

The system can be extended using machine-learning models trained on historical sensor data.

Potential approaches include:

* Isolation Forest
* Random Forest
* Logistic Regression
* One-Class SVM
* Autoencoders
* Time-Series Anomaly Detection

The ML model could learn normal pipeline behavior and identify deviations automatically.

### Machine Learning Prototype

AquaSentinel AI includes an Isolation Forest anomaly-detection model
trained on normal water-flow and pressure patterns.

The model identifies sensor combinations that differ significantly
from normal operating conditions and produces an anomaly score.

The architecture can later be extended using real historical
sensor datasets for improved leak detection accuracy.

---

## 📊 Monitoring Parameters

| Parameter         | Description                                               |
| ----------------- | --------------------------------------------------------- |
| Water Flow        | Measures the amount of water passing through the pipeline |
| Pipeline Pressure | Measures pressure inside the pipeline                     |
| Leak Probability  | Estimated likelihood of a potential leak                  |
| Anomaly Score     | Indicates how unusual the current readings are            |
| System Status     | Normal, Warning, or Leak Detected                         |

---

## 🧪 Simulation Modes

### 🟢 Normal Operation

Represents normal pipeline conditions.

Example:

```text
Flow: 42 L/min
Pressure: 3.2 bar
Leak Probability: 8%
Status: NORMAL
```

### 🟡 High Flow Warning

Represents unusually high water consumption or a possible developing problem.

Example:

```text
Flow: 68 L/min
Pressure: 3.0 bar
Status: WARNING
```

### 🔴 Simulated Leak

Represents a potential pipeline leak.

Example:

```text
Flow: 87 L/min
Pressure: 1.8 bar
Leak Probability: 94%
Status: LEAK DETECTED
```

---

## 🛠️ Technology Stack

### Frontend / Dashboard

* Streamlit

### Programming Language

* Python

### Data Processing

* Pandas
* NumPy

### AI / ML

* Anomaly Detection
* Machine Learning integration planned

### Data Source

* Simulated sensor data for the current prototype

---

## 📁 Project Structure

```text
AquaSentinel-AI/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Future Enhancements

The prototype can be extended with:

* 🔌 Real IoT water-flow sensors
* 📡 Real-time sensor data streaming
* 🤖 Trained machine-learning leak detection model
* 📍 Leak location estimation
* 🗺️ Pipeline monitoring map
* 📱 Mobile notifications
* ☁️ Cloud-based sensor data storage
* 📈 Historical analytics
* 🔐 Secure IoT communication
* ⚡ Automated emergency shut-off integration

---

## 🌍 Impact

AquaSentinel AI aims to support more efficient water management by enabling **early detection of abnormal pipeline conditions**.

Potential benefits include:

* Reduced water wastage
* Faster leak identification
* Lower maintenance costs
* Improved infrastructure monitoring
* More sustainable water usage

---

## ⚠️ Prototype Disclaimer

This project is currently a **proof-of-concept prototype** using simulated sensor data.

The simulation demonstrates how the proposed monitoring and anomaly-detection workflow would operate when connected to real water-flow and pressure sensors.

---

## 👩‍💻 Project

**AquaSentinel AI**

An AI-driven approach to intelligent water pipeline monitoring and early leak detection.

