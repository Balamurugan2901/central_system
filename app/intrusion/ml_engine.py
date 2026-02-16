import joblib
from pathlib import Path

MODEL_PATH = Path("models/intrusion_model.pkl")
model = None


def load_model():
    global model
    if model is None:
        model = joblib.load(MODEL_PATH)
    return model


def predict_risk(packet_rate: float, failed_logins: int) -> float:
    mdl = load_model()

    # prediction class
    pred_class = int(mdl.predict([[packet_rate, failed_logins]])[0])

    # map class → score
    mapping = {
        0: 2.0,   # low
        1: 5.0,   # medium
        2: 9.0    # high
    }

    return mapping.get(pred_class, 1.0)
