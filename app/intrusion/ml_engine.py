import joblib
from pathlib import Path

MODEL_PATH = Path("models/intrusion_model.pkl")
ENCODER_PATH = Path("models/action_label_encoder.pkl")
model = None
encoder = None

def load_model():
    global model, encoder
    if model is None:
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
    return model, encoder

def predict_action(packet_rate: float, failed_logins: int) -> str:
    mdl, enc = load_model()

    # Predict the numeric class
    pred_class_idx = mdl.predict([[packet_rate, failed_logins]])[0]

    # Decode action string
    predicted_action = enc.inverse_transform([pred_class_idx])[0]
    
    return predicted_action
