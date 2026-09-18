# Test the FastAPI health-check endpoint
from fastapi.testclient import TestClient
from app.main import app
import numpy as np
import pytest
from src import predictor


class MockModel:
    def predict(self, X):
        return np.array([1] * len(X))

    def predict_proba(self, X):
        return np.array([[0.4, 0.6]] * len(X))


@pytest.fixture(autouse=True)
def mock_mlflow_model(monkeypatch):
    monkeypatch.setattr(predictor, "load_model", lambda: MockModel())

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# Test that the prediction endpoint accepts valid input and returns a prediction
def test_predict_valid_input():
    payload = {
        "number_of_items": 2,
        "total_price": 100.0,
        "total_freight": 20.0,
        "number_of_payments": 1,
        "total_payment_value": 120.0,
        "purchase_hour": 14,
        "purchase_weekday": "2",
        "purchase_month": "3",
        "estimated_delivery_days": 10,
        "customer_state": "SP",
        "distance_km": 350.0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "late_probability" in response.json()

# Test that the prediction endpoint rejects an invalid purchase hour
def test_predict_invalid_input():
    payload = {
        "number_of_items": 2,
        "total_price": 100.0,
        "total_freight": 20.0,
        "number_of_payments": 1,
        "total_payment_value": 120.0,
        "purchase_hour": 25,
        "purchase_weekday": "2",
        "purchase_month": "3",
        "estimated_delivery_days": 10,
        "customer_state": "SP",
        "distance_km": 350.0,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422

    
# Test that the batch prediction endpoint accepts multiple valid orders
def test_predict_batch_valid_input():
    payload = {
        "orders": [
            {
                "number_of_items": 2,
                "total_price": 100.0,
                "total_freight": 20.0,
                "number_of_payments": 1,
                "total_payment_value": 120.0,
                "purchase_hour": 14,
                "purchase_weekday": "2",
                "purchase_month": "3",
                "estimated_delivery_days": 10,
                "customer_state": "SP",
                "distance_km": 350.0,
            },
            {
                "number_of_items": 1,
                "total_price": 200.0,
                "total_freight": 30.0,
                "number_of_payments": 2,
                "total_payment_value": 230.0,
                "purchase_hour": 18,
                "purchase_weekday": "5",
                "purchase_month": "4",
                "estimated_delivery_days": 15,
                "customer_state": "RJ",
                "distance_km": 800.0,
            },
        ]
    }

    response = client.post("/predict-batch", json=payload)

    assert response.status_code == 200
    assert len(response.json()["predictions"]) == 2

# Test that the batch prediction endpoint rejects invalid input
def test_predict_batch_invalid_input():
    payload = {
        "orders": [
            {
                "number_of_items": 2,
                "total_price": 100.0,
                "total_freight": 20.0,
                "number_of_payments": 1,
                "total_payment_value": 120.0,
                "purchase_hour": 14,
                "purchase_weekday": "2",
                "purchase_month": "3",
                "estimated_delivery_days": 10,
                "customer_state": "SP",
                "distance_km": 350.0,
            },
            {
                "number_of_items": 1,
                "total_price": 200.0,
                "total_freight": 30.0,
                "number_of_payments": 2,
                "total_payment_value": 230.0,
                "purchase_hour": 25,
                "purchase_weekday": "5",
                "purchase_month": "4",
                "estimated_delivery_days": 15,
                "customer_state": "RJ",
                "distance_km": 800.0,
            },
        ]
    }

    response = client.post("/predict-batch", json=payload)
    assert response.status_code == 422
    