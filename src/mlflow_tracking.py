import joblib
import mlflow
import mlflow.xgboost


MODEL_PATH = "artifacts/models/xgboost_final_model.joblib"

EXPERIMENT_NAME = "olist-late-delivery"



mlflow.set_experiment(EXPERIMENT_NAME)


model = joblib.load(MODEL_PATH)

print("Model loaded:", model.__class__.__name__)
# Start an MLflow run and log the selected model configuration and evaluation metrics
with mlflow.start_run() as run:
    mlflow.log_params({
        "model": "XGBClassifier",
        "n_estimators": 300,
        "learning_rate": 0.05,
        "max_depth": 5,
        "colsample_bytree": 0.8,
        "scale_pos_weight": 20.0,
        "random_state": 42,
        "eval_metric": "logloss",
        "n_jobs": -1
    })

    mlflow.log_metrics({
        "validation_f1_late": 0.12621194080625958,
        "test_precision_late": 0.06641123882503193,
        "test_recall_late": 0.6466321243523316,
        "test_f1_late": 0.12045169385194479
    })
    # Log the trained XGBoost model to the MLflow run
    mlflow.xgboost.log_model(
        model,
        name="model"
    )
    # Register the logged model in the MLflow Model Registry
    model_uri = f"runs:/{run.info.run_id}/model"

    registered_model = mlflow.register_model(
        model_uri=model_uri,
        name="olist-late-delivery-xgb"
    )

    print("Registered model:", registered_model.name)
    print("Model version:", registered_model.version)
    print("Run ID:", run.info.run_id)