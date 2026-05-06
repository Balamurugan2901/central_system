import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model():
    df = pd.read_csv("models/synthetic_intrusion_dataset.csv")

    X = df[["packet_rate", "failed_logins"]]
    y_raw = df["action_label"]

    # Encode string actions to integers
    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save both model and encoder
    joblib.dump(model, "models/intrusion_model.pkl")
    joblib.dump(encoder, "models/action_label_encoder.pkl")

    print(f"✅ Model trained on {len(df)} samples and saved.")
    print("Classes mapped:", list(encoder.classes_))

if __name__ == "__main__":
    train_model()
