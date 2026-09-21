import pandas as pd

from src.drift_monitor import detect_drift

BASELINE_PATH = "artifacts/drift_baseline.csv"


def test_no_drift_when_current_data_matches_baseline():
    baseline = pd.read_csv(BASELINE_PATH)

    result = detect_drift(
        baseline=baseline,
        current=baseline,
    )

    assert result["drift_detected"] is False
    assert result["alerts"]["numeric_features"] == []
    assert result["alerts"]["categorical_features"] == []


def test_detects_numeric_drift():
    baseline = pd.read_csv(BASELINE_PATH)

    current = baseline.copy()
    current["total_price"] = current["total_price"] * 1.5

    result = detect_drift(
        baseline=baseline,
        current=current,
    )

    assert result["drift_detected"] is True
    assert "total_price" in result["alerts"]["numeric_features"]
