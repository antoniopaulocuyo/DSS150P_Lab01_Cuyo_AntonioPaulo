# Source Profile: Interpretation

## customers.csv

- Nulls in `email` (3) and `city` (2) signal incomplete contact/location data.
- 2 duplicate rows indicate the source does not guarantee row-level uniqueness.

## products.parquet

- Zero nulls and zero duplicates make this the cleanest of the three sources

## orders.json

- `duplicated()` failed on this file because at least one column (`shipping`) contains nested dict/list values. This confirms `orders.json` is semi-structured, not flat/tabular like the CSV and Parquet sources.
- **`order_id` and `customer_id` both look like key candidates**

## Cross-source observations

- Three different serialization formats (CSV, Parquet, JSON) means three different parsing and validation paths** are required before data can be unified.
- **`customer_id` appears in both `customers.csv` and `orders.json`**, making it the most likely join key across sources.