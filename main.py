import pandas as pd
from src.preprocess import preprocess_data
from src.train import train_model
from src.evaluate import evaluate_model

# Load data
df = pd.read_csv("data/patient-vital-sign-time-series.csv")

# Preprocess
X, scaler = preprocess_data(df)

# Train
model = train_model(X, scaler)

# Evaluate
evaluate_model(model, X)

print("\nModel training complete.")