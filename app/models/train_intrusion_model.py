import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Example dataset structure
# attack_type,packet_rate,failed_logins,label

data = pd.read_csv("intrusion_dataset.csv")

X = data[["packet_rate", "failed_logins"]]
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "intrusion_model.pkl")

print("Model trained and saved!")
