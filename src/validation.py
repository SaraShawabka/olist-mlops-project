from pathlib import Path
import yaml
import great_expectations as gx
import pandas as pd
import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnToExist,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToBeInSet,
)
# Load the project root and create a persistent Great Expectations context
PROJECT_ROOT = Path(__file__).resolve().parents[1]

context = gx.get_context(
    context_root_dir=PROJECT_ROOT / "great_expectations"
)

# Define the feature columns that must be present in every prediction request
required_features = [
    "number_of_items",
    "total_price",
    "total_freight",
    "number_of_payments",
    "total_payment_value",
    "purchase_hour",
    "purchase_weekday",
    "purchase_month",
    "estimated_delivery_days",
    "customer_state",
    "distance_km",
]


# Load the existing Suite and remove old expectations
# so that outdated validation rules do not remain persisted
suite = context.suites.get("olist_prediction_input")
suite.expectations.clear()


# Check that all required feature columns exist
for column in required_features:
    suite.add_expectation(
        ExpectColumnToExist(column=column)
    )


# Validate that purchase_hour is between 0 and 23
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="purchase_hour",
        min_value=0,
        max_value=23,
    )
)


# Validate that purchase_weekday contains only valid weekday values
suite.add_expectation(
    ExpectColumnValuesToBeInSet(
        column="purchase_weekday",
        value_set=["0", "1", "2", "3", "4", "5", "6"],
    )
)


# Validate that purchase_month contains only valid month values
suite.add_expectation(
    ExpectColumnValuesToBeInSet(
        column="purchase_month",
        value_set=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ],
    )
)


# Ensure every order contains at least one item
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="number_of_items",
        min_value=1,
    )
)


# Ensure the number of payments is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="number_of_payments",
        min_value=0,
    )
)


# Ensure total_price is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="total_price",
        min_value=0,
    )
)


# Ensure total_freight is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="total_freight",
        min_value=0,
    )
)


# Ensure total_payment_value is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="total_payment_value",
        min_value=0,
    )
)


# Ensure estimated_delivery_days is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="estimated_delivery_days",
        min_value=0,
    )
)


# Ensure distance_km is not negative
suite.add_expectation(
    ExpectColumnValuesToBeBetween(
        column="distance_km",
        min_value=0,
    )
)


# Save the cleaned and updated Suite
context.suites.add_or_update(suite)


# Define the pandas Data Source and Data Asset used for runtime validation
data_source_name = "olist_pandas_source"
data_asset_name = "olist_prediction_data"
batch_definition_name = "whole_dataframe"


# Get the existing Data Source or create it if it does not exist
try:
    data_source = context.data_sources.get(data_source_name)
except Exception:
    data_source = context.data_sources.add_pandas(
        name=data_source_name
    )


# Get the existing Data Asset or create it if it does not exist
try:
    data_asset = data_source.get_asset(data_asset_name)
except Exception:
    data_asset = data_source.add_dataframe_asset(
        name=data_asset_name
    )


# Get the existing Batch Definition or create it if it does not exist
try:
    batch_definition = data_asset.get_batch_definition(
        batch_definition_name
    )
except Exception:
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        batch_definition_name
    )


# Retrieve the existing Validation Definition or create it if it does not exist
try:
    validation_definition = context.validation_definitions.get(
        "olist_prediction_validation"
    )
except Exception:
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            data=batch_definition,
            suite=suite,
            name="olist_prediction_validation",
        )
    )


# Validate a pandas DataFrame using the Great Expectations Validation Definition
def validate_input_data(df):
    validation_result = validation_definition.run(
        batch_parameters={"dataframe": df}
    )

    return validation_result
