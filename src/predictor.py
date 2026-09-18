# Load the registered MLflow model only when a prediction is requested
import os
from pathlib import Path

import mlflow
import yaml

# Load the central project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Configure MLflow using the environment variable when available
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    config["mlflow"]["tracking_uri"],
)

MODEL_NAME = config["mlflow"]["model_name"]
MODEL_ALIAS = config["mlflow"]["model_alias"]

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Keep the model unloaded until it is needed
model = None


def load_model():
    # Load the registered production model from MLflow
    global model

    if model is None:
        model = mlflow.xgboost.load_model(
            f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
        )

    return model


def predict(X):
    # Generate predictions and late-delivery probabilities
    production_model = load_model()

    prediction = production_model.predict(X)
    probability = production_model.predict_proba(X)[:, 1]

    return prediction, probability