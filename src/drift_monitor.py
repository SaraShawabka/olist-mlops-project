import pandas as pd

NUMERIC_FEATURES = [
    "number_of_items",
    "total_price",
    "total_freight",
    "number_of_payments",
    "total_payment_value",
    "purchase_hour",
    "estimated_delivery_days",
    "distance_km",
]

CATEGORICAL_FEATURES = [
    "purchase_weekday",
    "purchase_month",
    "customer_state",
]


def calculate_numeric_drift(
    baseline: pd.DataFrame,
    current: pd.DataFrame,
    threshold: float = 0.20,
) -> dict:
    results = {}

    for feature in NUMERIC_FEATURES:
        baseline_mean = baseline[feature].mean()
        current_mean = current[feature].mean()

        if baseline_mean == 0:
            drift_ratio = 0.0
        else:
            drift_ratio = abs(current_mean - baseline_mean) / abs(baseline_mean)

        results[feature] = {
            "baseline_mean": float(baseline_mean),
            "current_mean": float(current_mean),
            "drift_ratio": float(drift_ratio),
            "drift_detected": drift_ratio > threshold,
        }

    return results


def calculate_categorical_drift(
    baseline: pd.DataFrame,
    current: pd.DataFrame,
    threshold: float = 0.20,
) -> dict:
    results = {}

    for feature in CATEGORICAL_FEATURES:
        baseline_distribution = baseline[feature].value_counts(normalize=True)

        current_distribution = current[feature].value_counts(normalize=True)

        categories = set(baseline_distribution.index) | set(current_distribution.index)

        max_difference = 0.0

        for category in categories:
            baseline_value = baseline_distribution.get(
                category,
                0.0,
            )

            current_value = current_distribution.get(
                category,
                0.0,
            )

            difference = abs(current_value - baseline_value)

            max_difference = max(
                max_difference,
                difference,
            )

        results[feature] = {
            "max_distribution_change": float(max_difference),
            "drift_detected": max_difference > threshold,
        }

    return results


def detect_drift(
    baseline: pd.DataFrame,
    current: pd.DataFrame,
    threshold: float = 0.20,
) -> dict:
    numeric_drift = calculate_numeric_drift(
        baseline,
        current,
        threshold,
    )

    categorical_drift = calculate_categorical_drift(
        baseline,
        current,
        threshold,
    )

    numeric_alerts = [
        feature for feature, result in numeric_drift.items() if result["drift_detected"]
    ]

    categorical_alerts = [
        feature
        for feature, result in categorical_drift.items()
        if result["drift_detected"]
    ]

    return {
        "drift_detected": bool(numeric_alerts or categorical_alerts),
        "threshold": threshold,
        "numeric": numeric_drift,
        "categorical": categorical_drift,
        "alerts": {
            "numeric_features": numeric_alerts,
            "categorical_features": categorical_alerts,
        },
    }
