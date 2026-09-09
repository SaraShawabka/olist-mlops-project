from pathlib import Path
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "Artifacts"
RAW_DATA_DIR = PROJECT_ROOT / "Data" / "raw"
customers = pd.read_csv(
    RAW_DATA_DIR / "olist_customers_dataset.csv"
)
order_items = pd.read_csv(
    RAW_DATA_DIR / "olist_order_items_dataset.csv"
)
sellers = pd.read_csv(
    RAW_DATA_DIR / "olist_sellers_dataset.csv"
)
geolocation = pd.read_csv(
    RAW_DATA_DIR / "olist_geolocation_dataset.csv"
)
geo_by_zip = (
    geolocation
    .groupby("geolocation_zip_code_prefix")
    .agg(
        latitude=("geolocation_lat", "mean"),
        longitude=("geolocation_lng", "mean")
    )
    .reset_index()
)