
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "dataset" / "PhishingData.csv"
CLEAN_DATASET_PATH = PROJECT_ROOT / "dataset" / "phishingdata_clean.csv"

# Load original dataset
df = pd.read_csv(DATASET_PATH)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Remove only the unnecessary index column
if "index" in df.columns:
    df = df.drop(columns=["index"])

# Do not remove any rows
df.to_csv(CLEAN_DATASET_PATH, index=False)

print("Dataset preparation completed!")
print("Original rows:", len(pd.read_csv(DATASET_PATH)))
print("Cleaned dataset shape:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Target counts:")
print(df["Result"].value_counts())
print("Saved to:", CLEAN_DATASET_PATH)