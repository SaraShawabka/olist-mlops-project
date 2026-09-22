# Olist MLOps Project

An end-to-end MLOps project built using the **Brazilian E-Commerce Public Dataset by Olist**.

The project predicts whether an e-commerce order is likely to be delivered **late or on time**, and demonstrates the transition from exploratory notebooks to a reproducible production inference service.

---

## Project Overview

The project covers the main stages of an ML production workflow:

* Data ingestion and exploration
* Data validation
* Feature engineering
* Model training and evaluation
* Reusable inference pipeline
* MLflow experiment and model tracking
* DVC data and artifact versioning
* FastAPI prediction service
* Docker containerization
* Automated testing
* CI/CD with GitHub Actions
* Prediction monitoring and data drift detection

---

## Business Problem

Late deliveries can negatively affect customer satisfaction and the overall e-commerce experience.

The goal is to predict the likelihood that an order will be delivered late using information available at prediction time.

The model produces:

* A predicted class
* The probability of late delivery
* The model version used for the prediction

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

* Orders
* Customers
* Sellers
* Products
* Payments
* Reviews
* Order items
* Geolocation
* Product categories

The original raw dataset is not stored in Git because of its size.

Data and selected production artifacts are versioned using **DVC**.

---

## Machine Learning Model

The final model is an **XGBoost classifier**.

The inference pipeline uses previously fitted preprocessing artifacts and does **not** fit transformers during prediction.

The production service loads:

* Numeric imputer
* Categorical encoder
* Feature scaler
* XGBoost model
* Feature list

This keeps the production inference process consistent with the trained model.

---

## Production Features

The model uses the following input features:

### Numeric features

* `number_of_items`
* `total_price`
* `total_freight`
* `number_of_payments`
* `total_payment_value`
* `purchase_hour`
* `estimated_delivery_days`
* `distance_km`

### Categorical features

* `purchase_weekday`
* `purchase_month`
* `customer_state`

---

## Technologies

### Data & Machine Learning

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Joblib

### API & Validation

* FastAPI
* Pydantic
* Great Expectations
* PyYAML

### MLOps

* MLflow
* DVC
* MinIO
* Prometheus
* Docker
* Docker Compose

### Development & CI/CD

* Git
* GitHub
* GitHub Actions
* Ruff
* Pytest
* Pre-commit

---

## Project Structure

```text
olist-mlops-project/
│
├── app/
│   └── main.py
│
├── artifacts/
│   ├── models/
│   ├── feature_list.json
│   └── drift_baseline.csv
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── great_expectations/
│   ├── expectations/
│   ├── validation_definitions/
│   └── great_expectations.yml
│
├── notebooks/
│   └── ...
│
├── sql/
│   ├── schema.sql
│   └── validation.sql
│
├── src/
│   ├── features.py
│   ├── predictor.py
│   ├── preprocessing.py
│   ├── validation.py
│   └── drift_monitor.py
│
├── tests/
│   └── ...
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── Dockerfile
├── Dockerfile.mlflow
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .pre-commit-config.yaml
├── .gitignore
└── README.md
```

---

## Project Workflow

```text
Olist Dataset
      │
      ▼
Data Ingestion
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
Model Training
      │
      ▼
MLflow Tracking
      │
      ▼
Saved Model & Preprocessing Artifacts
      │
      ▼
FastAPI Inference Service
      │
      ├── Input Validation
      ├── Prediction
      ├── Prediction Logging
      └── Monitoring
      │
      ▼
Docker / Docker Compose
      │
      ▼
GitHub Actions CI/CD
```

---

## Setup

### Clone the repository

```bash
git clone https://github.com/SaraShawabka/olist-mlops-project.git
cd olist-mlops-project
```

### DVC

The project uses DVC to version selected data and artifacts.

Configure the DVC remote according to your environment, then retrieve the required artifacts:

```bash
dvc pull
```

The production drift baseline is also available in the repository so that the Docker image can be built directly by CI/CD.

---

## Run with Docker Compose

The project uses Docker Compose to run the main production services and supporting infrastructure.

Start the services with:

```bash
docker compose up -d --build
```

The main services are:

| Service       | Purpose                    | Port |
| ------------- | -------------------------- | ---: |
| API           | FastAPI prediction service | 8000 |
| MLflow        | Experiment/model tracking  | 5000 |
| MinIO         | Artifact storage           | 9000 |
| MinIO Console | MinIO management UI        | 9001 |
| PostgreSQL    | MLflow backend store       | 5433 |

Check the running containers:

```bash
docker compose ps
```

---

## API

The FastAPI service is available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Model information

```http
GET /model-info
```

Returns information about the model currently used by the service.

### Single prediction

```http
POST /predict
```

Example request:

```json
{
  "number_of_items": 1,
  "total_price": 100.0,
  "total_freight": 20.0,
  "number_of_payments": 1,
  "total_payment_value": 120.0,
  "purchase_hour": 14,
  "purchase_weekday": "2",
  "purchase_month": "8",
  "estimated_delivery_days": 25.0,
  "customer_state": "SP",
  "distance_km": 500.0
}
```

Example response:

```json
{
  "prediction": 1,
  "late_probability": 0.5994933247566223,
  "model_version": "1"
}
```

A prediction of `1` represents a predicted late delivery, while `0` represents a predicted on-time delivery.

### Batch prediction

```http
POST /predict-batch
```

Accepts multiple orders in a single request.

---

## Input Validation

Prediction inputs are validated before inference.

The project uses:

* Pydantic schemas for API-level validation
* Great Expectations for data validation
* Feature type and range checks
* Category validation
* Missing-value checks

Invalid input is rejected instead of being passed directly to the model.

The Great Expectations validation suite is stored under:

```text
great_expectations/expectations/
```

---

## Monitoring

The API exposes Prometheus-compatible metrics through:

```http
GET /metrics
```

The service tracks:

* Total prediction requests
* Prediction latency
* Prediction errors
* Prediction distribution

Prediction requests are also stored as JSON Lines under:

```text
logs/predictions.jsonl
```

Each prediction log contains information such as:

* Timestamp
* Input features
* Prediction
* Late-delivery probability
* Latency
* Model version

Prediction logs are stored in a Docker volume so they can persist across API container restarts.

---

## Data Drift Monitoring

The service provides:

```http
GET /monitoring/drift
```

The endpoint compares current prediction inputs against a stored baseline dataset.

The current drift threshold is:

```text
0.20
```

For numeric features, the monitoring compares the relative change in feature means.

For categorical features, it compares changes in category distributions.

The response includes:

* Sample count
* Overall drift status
* Numeric drift results
* Categorical drift results
* Features triggering alerts

The baseline is stored at:

```text
artifacts/drift_baseline.csv
```

The drift monitoring utility is implemented in:

```text
src/drift_monitor.py
```

---

## MLflow

MLflow is used for experiment and model tracking.

The project tracks model-related information and stores the production model in the MLflow model registry.

The production service uses the configured MLflow model/version rather than relying on a notebook-only model path.

MLflow is available at:

```text
http://localhost:5000
```

---

## DVC

DVC is used to version selected data and production artifacts.

The configured remote is MinIO:

```text
s3://olist-dvc
```

The DVC configuration should contain environment-specific credentials locally and should not expose credentials in Git.

DVC files such as:

```text
*.dvc
```

are committed to Git, while the corresponding artifacts are stored in the configured DVC remote.

---

## Testing

Tests are written using **pytest**.

Run the complete test suite with:

```bash
pytest -v
```

The tests cover areas including:

* Preprocessing
* Feature engineering
* Input validation
* Data leakage checks
* Model loading
* Prediction behavior
* API endpoints
* Drift monitoring

---

## Code Quality

The project uses Ruff for linting and formatting.

Run:

```bash
ruff check .
ruff format --check .
```

Pre-commit hooks run the configured code-quality checks before commits.

---

## CI/CD

GitHub Actions provides automated CI/CD.

### CI

The CI workflow runs on pushes and pull requests and performs:

* Dependency installation
* Ruff checks
* Ruff formatting checks
* Automated tests

A failing test or code-quality check stops the workflow.

### CD

The CD workflow builds the Docker image after changes are pushed to `master`.

The image is then pushed to **GitHub Container Registry (GHCR)**.

This ensures that the production image is rebuilt automatically after successful changes.

---

## Current Status

The main production workflow is currently implemented, including:

* Data ingestion and analysis
* Feature engineering
* XGBoost model development
* Reusable inference pipeline
* Great Expectations validation
* MLflow tracking and model registry
* DVC artifact versioning
* FastAPI prediction service
* Single and batch prediction endpoints
* Docker and Docker Compose
* Prediction logging
* Prometheus metrics
* Data drift monitoring
* Automated tests
* Ruff and pre-commit checks
* GitHub Actions CI/CD
* Docker image publishing to GHCR

---

## Future Improvements

Possible future improvements include:

* More robust drift detection using statistical tests
* Minimum sample-size requirements before triggering drift alerts
* Automated model retraining workflows
* More advanced production monitoring dashboards
* Cloud deployment
* Additional API authentication and security controls