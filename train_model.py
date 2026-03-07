import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Create dataset
data = {
    "sensor": [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95],
    "status": [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1]
}

df = pd.DataFrame(data)

X = df[["sensor"]]
y = df["status"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "downtime_model.pkl")

print("Model retrained successfully!")