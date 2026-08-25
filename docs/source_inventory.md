# Source Inventory

## CSV Source

- **Source name:** customers.csv
- **Source-system type:** Flat file
- **Data format:** CSV
- **Structured / semi-structured / unstructured:** Structured
- **Expected update pattern:** Unknown (likely batch export)
- **Likely acquisition method:** File drop / manual or scheduled export into `data/raw/`
- **Schema location or schema owner:** [GitHub Owner] jrnmapanao@yahoo.com
- **Possible primary/business key:** `customer_id`
- **Potential schema-evolution risk:** All columns are typed as plain strings on read. Potential for format change.
- **Potential data-quality risk:** Contains nulls in `email` (3) and `city` (2), and 2 duplicate rows. `customer_id` uniqueness is not guaranteed by the source.

## JSON Source

- **Source name:** orders.json
- **Source-system type:** Flat file
- **Data format:** JSON
- **Structured / semi-structured / unstructured:** Semi-structured
- **Expected update pattern:** Unknown (likely batch export)
- **Likely acquisition method:** File drop into `data/raw/`
- **Schema location or schema owner:** [GitHub Owner] jrnmapanao@yahoo.com
- **Possible primary/business key:** `order_id` (with `customer_id` as a likely foreign key linking to `customers.csv`)
- **Potential schema-evolution risk:** The nested `shipping` field is a dict/object, not a flat value. Any changes to its internal structure would not appear as a top-level schema change.
- **Potential data-quality risk:** `order_timestamp` is stored as a string rather than a native datetime type and required explicit coercion. The nested `shipping` field also made duplicate-row detection fail outright (unhashable type), so duplicate risk in this source is currently unverified.

## Parquet Source

- **Source name:** products.parquet
- **Source-system type:** Flat file
- **Data format:** Parquet
- **Structured / semi-structured / unstructured:** Structured
- **Expected update pattern:** Unknown (likely a periodic snapshot)
- **Likely acquisition method:** File drop into `data/raw/`
- **Schema location or schema owner:** [GitHub Owner] jrnmapanao@yahoo.com
- **Possible primary/business key:** `product_id`
- **Potential schema-evolution risk:** Lower risk than the CSV/JSON sources since Parquet embeds its schema (column names and types) directly in the file.
- **Potential data-quality risk:** No nulls or duplicates were found.

## REST API

- **Source name:** "https://jsonplaceholder.typicode.com/posts"
- **Source-system type:** API
- **Data format:** JSON (response payload)
- **Structured / semi-structured / unstructured:** Semi-structured
- **Expected update pattern:** Unknown (Likely real-time or on-demand)
- **Likely acquisition method:** HTTP GET request via `requests`
- **Schema location or schema owner:** [GitHub Owner] jrnmapanao@yahoo.com
- **Possible primary/business key:** row-id
- **Potential schema-evolution risk:** APIs can change response structure.
- **Potential data-quality risk:** Network/timeout failures, rate limiting, or partial responses could result in incomplete or missing data compared to a stable file-based source.

## PostgreSQL

- **Source name:** inventory_snapshot (table)
- **Source-system type:** Relational database (RDBMS)
- **Data format:** Relational table (SQL rows/columns)
- **Structured / semi-structured / unstructured:** Structured
- **Expected update pattern:** Unknown (Likely ongoing updates)
- **Likely acquisition method:** SQL query via `psycopg2`
- **Schema location or schema owner:** Defined in the database itself (`information_schema.columns`). Owned by [GitHub Owner] jrnmapanao@yahoo.com
- **Possible primary/business key:** row-id
- **Potential schema-evolution risk:** Lower risk day-to-day since the schema is explicitly defined in the database.
- **Potential data-quality risk:** Since data can be updated live (unlike a static file snapshot), values queried at different times may be inconsistent for comparison/testing.
