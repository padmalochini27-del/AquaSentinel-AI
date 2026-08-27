import numpy as np
from sklearn.ensemble import IsolationForest

# Normal operating sensor data
normal_data = np.array([
    [40, 3.4],
    [42, 3.2],
    [45, 3.5],
    [43, 3.3],
    [41, 3.6],
    [44, 3.4],
    [46, 3.2],
    [42, 3.5],
    [40, 3.3],
    [45, 3.4]
])

# Train anomaly detection model
model = IsolationForest(
    contamination=0.1,
    random_state=42
)

model.fit(normal_data)


def detect_anomaly(flow, pressure):
    """
    Returns:
        1  = normal
       -1  = anomaly
    """
    sensor_data = np.array([[flow, pressure]])
    return model.predict(sensor_data)[0]


def get_anomaly_score(flow, pressure):
    """
    Converts model decision score into a simple
    0-100 anomaly score.
    """
    sensor_data = np.array([[flow, pressure]])

    score = model.decision_function(sensor_data)[0]

    anomaly_score = int(
        np.clip((0.5 - score) * 100, 0, 100)
    )

    return anomaly_score
