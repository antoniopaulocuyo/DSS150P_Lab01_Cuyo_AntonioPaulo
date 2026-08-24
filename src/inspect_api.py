import json
from datetime import datetime, timezone
from pathlib import Path
import requests

snap_shot_filename = "api_snapshot.json"
source_inventory_filename = "source_inventory.md"

API_URL = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(API_URL, timeout=20)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    raise SystemExit(1)

print("Status code:", response.status_code)

print("Content-Type:", response.headers.get("Content-Type"))

payload = response.json()

if isinstance(payload, list):
    structure = "list"
elif isinstance(payload, dict):
    structure = "object/dictionary"
else:
    structure = "unknown"
print("Top-level structure:", structure)

if isinstance(payload, list):
    print("Number of records:", len(payload))
elif isinstance(payload, dict):
    print("Top-level keys:", list(payload.keys()))
else:
    print("Number of records: N/A")

if isinstance(payload, list) and len(payload) > 0:
    print("Sample record:", payload[0])
elif isinstance(payload, dict):
    print("Sample record (top-level dict):", payload)

proj_dir = Path(__file__).resolve().parent.parent
output_path = proj_dir / "data" / "raw" / snap_shot_filename

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(payload, file, indent=2, ensure_ascii=False)

retrieved_at_utc = datetime.now(timezone.utc).isoformat()

inventory_path = proj_dir / "docs" / source_inventory_filename
with open(inventory_path, "a", encoding="utf-8") as source_file:
    source_file.write(f"\nRetrieved API at UTC: {retrieved_at_utc}")

print("retrieved_at_utc:", retrieved_at_utc)