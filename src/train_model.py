
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "phishingdata_clean.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "random_forest_model.joblib"

# Load the cleaned dataset
df = pd.read_csv(DATASET_PATH)
df.columns = df.columns.str.strip()

# Separate features and target
X = df.drop(columns=["Result"])
y = df["Result"]

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# Create and train one model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1,
)

print("Training Random Forest model...")
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)

print("\n--- MODEL EVALUATION ---")
print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
print(f"Precision: {precision_score(y_test, predictions, pos_label=1):.4f}")
print(f"Recall   : {recall_score(y_test, predictions, pos_label=1):.4f}")
print(f"F1-score : {f1_score(y_test, predictions, pos_label=1):.4f}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save the trained model
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully at: {MODEL_PATH}")
