import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model():

    df = pd.read_csv("training_data.csv")

    X = df[["packet_rate", "failed_logins"]]
    y = df["label"]

    model = RandomForestClassifier()
    model.fit(X, y)

    joblib.dump(model, "models/intrusion_model.pkl")

    print("Model trained and saved")

if __name__ == "__main__":
    train_model()
