import joblib
from pathlib import Path
import json
import pandas as pd
import yaml
# Load the central project configuration so file paths are not hardcoded
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

ARTIFACTS_DIR = PROJECT_ROOT / config["artifacts_dir"]
numeric_imputer = joblib.load(
    ARTIFACTS_DIR / "models" / "numeric_imputer.joblib"
)
categorical_encoder = joblib.load(
    ARTIFACTS_DIR / "models" / "categorical_encoder.joblib"
)
scaler = joblib.load(
    ARTIFACTS_DIR / "models" / "scaler.joblib"
)
with open(ARTIFACTS_DIR / "feature_list.json", "r") as f:
    feature_list = json.load(f)
numeric_features = [
    "number_of_items",
    "total_price",
    "total_freight",
    "number_of_payments",
    "total_payment_value",
    "purchase_hour",
    "estimated_delivery_days",
    "distance_km"
]
categorical_features = [
    "purchase_weekday",
    "purchase_month",
    "customer_state"
]
def transform_features(df):
    required_featurse = numeric_features + categorical_features
    missing_features =[col for col in required_featurse if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    X_numeric = df[numeric_features]
    X_numeric = pd.DataFrame(
    numeric_imputer.transform(X_numeric),
    columns=numeric_features
)
    X_numeric = scaler.transform(X_numeric)
    X_categorical = df[categorical_features]
    X_categorical = categorical_encoder.transform(X_categorical)
    X_numeric = pd.DataFrame(
        X_numeric,
        columns=numeric_features
    )
    X_categorical = pd.DataFrame(
        X_categorical,
        columns=categorical_encoder.get_feature_names_out(categorical_features)
    )
    X_transformed = pd.concat(
        [X_numeric,X_categorical],
        axis=1
    )
    X_transformed = X_transformed[feature_list]
    return X_transformed
