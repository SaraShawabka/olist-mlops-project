import joblib
from pathlib import Path
import pandas as pd
import yaml
from src.preprocessing import transform_features
# Load the central project configuration so the model path is not hardcoded
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

ARTIFACTS_DIR = PROJECT_ROOT / config["artifacts_dir"]
model = joblib.load(
    ARTIFACTS_DIR / "models" / "xgboost_final_model.joblib"
)
def predict(X):
    prediction = model.predict(X)
    probability = model.predict_proba(X)[:,1]
    return prediction, probability
