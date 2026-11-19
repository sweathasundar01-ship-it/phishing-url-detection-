
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

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "dataset" / "phishingdata_clean.csv"
MODEL_PATH = ROOT / "models" / "url_only_model.joblib"

# URL-related features available in the dataset
FEATURES = [
    "having_IPhaving_IP_Address",
    "URLURL_Length",
    "Shortining_Service",
    "having_At_Symbol",
    "double_slash_redirecting",
    "Prefix_Suffix",
    "having_Sub_Domain",
    "port",
    "HTTPS_token",
]

def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)
    df.columns = df.columns.str.strip()

    missing = [col for col in FEATURES + ["Result"] if col not in df.columns]
    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")

    X = df[FEATURES].copy()
    y = df["Result"]

    print("Dataset shape:", df.shape)
    print("Training features:", len(FEATURES))
    print("Preparing train and test data...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    print("Training URL-only Random Forest model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\n--- URL-ONLY MODEL EVALUATION ---")
    print(f"Accuracy : {accuracy_score(y_test, predictions):.4f}")
    print(
        f"Precision: "
        f"{precision_score(y_test, predictions, pos_label=1, zero_division=0):.4f}"
    )
    print(
        f"Recall   : "
        f"{recall_score(y_test, predictions, pos_label=1, zero_division=0):.4f}"
    )
    print(
        f"F1-score : "
        f"{f1_score(y_test, predictions, pos_label=1, zero_division=0):.4f}"
    )

    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\nModel saved to:", MODEL_PATH)
    print("Feature count:", len(model.feature_names_in_))
    print("\nNote: Dataset test scores do not guarantee real-world URL accuracy.")

if __name__ == "__main__":
    main()