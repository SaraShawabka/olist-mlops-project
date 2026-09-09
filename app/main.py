from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from src.preprocessing import transform_features
from src.predictor import predict
import pandas as pd
from pathlib import Path
import logging
import time
import yaml
from src.validation import validate_input_data
# Set up logging to track API requests and errors
# Configure logging to write messages to both the terminal and a log file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

LOGS_DIR = PROJECT_ROOT / config["logs_dir"]
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "app.log"

logger = logging.getLogger("olist_api")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

class OrderInput(BaseModel):
    number_of_items: int
    total_price: float
    total_freight: float
    number_of_payments: int
    total_payment_value: float
    purchase_hour: float
    purchase_weekday: str
    purchase_month: str
    estimated_delivery_days: float
    customer_state: str
    distance_km: float
from typing import List
class BatchOrderInput(BaseModel):
    orders: List[OrderInput]
# Read the model version from the central configuration file
MODEL_VERSION = config["model"]["version"]
app = FastAPI()
@app.get("/health")
def health():
    return{"status":"ok"}
@app.get("/model-info")
def model_info():
    return{
        "model" :"XGBoost",
        "version" : MODEL_VERSION
    }
@app.post("/predict")
def make_prediction(order: OrderInput):
    # Start the timer so we can measure how long the prediction takes
    start_time = time.perf_counter()
    # Log when a prediction request is received
    logger.info("Prediction request received")
    # Handle errors during preprocessing and prediction without crashing the API
    try:
        input_data = pd.DataFrame([order.model_dump()])
        validation_result = validate_input_data(input_data)
        if not validation_result.success:
            raise HTTPException(
                status_code = 422,
                detail = str(validation_result)
            )

        logger.info(
            f"Prediction input: {order.model_dump()}"
        )

        X = transform_features(input_data)

        prediction, probability = predict(X)

        latency = time.perf_counter() - start_time

        logger.info(
            f"Prediction latency: {latency:.4f} seconds"
        )

        logger.info(
            f"Prediction result: prediction={int(prediction[0])}, "
            f"late_probability={float(probability[0])}"
        )

        logger.info(
            f"Model version: {MODEL_VERSION}"
        )

        return {
            "prediction": int(prediction[0]),
            "late_probability": float(probability[0])
        }
    except HTTPException :
        raise

    except Exception:
        # Record the full error details in the log for debugging
        logger.exception("Prediction failed")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again later."
        )

# Validate the entire batch before preprocessing and model prediction
@app.post("/predict-batch")
def perdict_batch(batch: BatchOrderInput):
    # Handle errors during batch validation, preprocessing, and prediction
    try:
        # Start the timer to measure the total batch prediction latency
        start_time = time.perf_counter()

        # Convert the batch orders into a pandas DataFrame
        input_data = pd.DataFrame(
            [order.model_dump() for order in batch.orders]
        )

        # Validate all batch input rows using Great Expectations
        validation_result = validate_input_data(input_data)

        # Reject the entire batch if any validation check fails
        if not validation_result.success:
            raise HTTPException(
                status_code=422,
                detail="Input data failed validation checks."
            )

        # Log the input features for all orders in the batch request
        logger.info(
            f"Batch prediction input: "
            f"{input_data.to_dict(orient='records')}"
        )

        # Transform the validated input features for the model
        X = transform_features(input_data)

        # Make predictions for all orders in the batch
        predictions, probabilities = predict(X)

        # Calculate and log the total time taken for the batch prediction
        latency = time.perf_counter() - start_time

        logger.info(
            f"Batch prediction latency: {latency:.4f} seconds"
        )

        # Log the predictions and probabilities returned for the batch
        logger.info(
            f"Batch prediction results: "
            f"predictions={predictions.tolist()}, "
            f"late_probabilities={probabilities.tolist()}"
        )

        # Log the model version used for the batch prediction
        logger.info(
            f"Batch model version: {MODEL_VERSION}"
        )

        # Return one prediction result for each order
        return {
            "predictions": [
                {
                    "prediction": int(prediction),
                    "late_probability": float(probability)
                }
                for prediction, probability in zip(
                    predictions,
                    probabilities
                )
            ]
        }

    except HTTPException:
        # Re-raise validation errors so they remain 422 responses
        raise

    except Exception:
        # Record the full batch prediction error in the log for debugging
        logger.exception("Batch prediction failed")

        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed. Please try again later."
        )
