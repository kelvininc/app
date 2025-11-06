from kelvin.api.client import Client
import os
import tempfile
import json
import csv
import random
from datetime import datetime, timedelta


# -----------------------------
# Helper: Save Progress Incrementally
# -----------------------------
def save_progress(created: dict, output_file: str) -> None:
    """Write current progress to disk after each successful creation step."""
    with open(output_file, "w") as f:
        json.dump(created, f, indent=4)


# -----------------------------
# Step 1: Create Asset Type
# -----------------------------
def create_asset_type(client, created, asset_type_name: str, asset_type_title: str, output_file: str) -> None:
    print(f"Creating Asset Type '{asset_type_name}'...")
    try:
        client.asset.create_asset_type(
            data={
                "name": asset_type_name,
                "title": asset_type_title
            }
        )
        print(f"Asset Type created: {asset_type_name}")
        created["asset_type"] = asset_type_name
        save_progress(created, output_file)
    except Exception:
        print(f"Asset Type '{asset_type_name}' may already exist. Continuing...")


# -----------------------------
# Step 2: Create Assets
# -----------------------------
def create_assets(client, x: int, created, base_asset_name: str, base_asset_title: str, asset_type_name: str, output_file: str) -> list:
    print(f"\nCreating {x} assets...")
    assets = created.get("assets", [])
    for i in range(1, x + 1):
        asset_name = f"{base_asset_name}_{i}"
        asset_title = f"{base_asset_title} {i}"
        print(f"Creating asset: {asset_name}")

        try:
            resp_asset = client.asset.create_asset(
                data={
                    "name": asset_name,
                    "title": asset_title,
                    "asset_type_name": asset_type_name,
                    "properties": [
                        {"name": "plc_manufacturer", "title": "PLC Manufacturer", "value": "Siemens"},
                        {"name": "plc_model", "title": "PLC Model", "value": "S7-315"},
                        {"name": "plc_series", "title": "PLC Series", "value": "S7"},
                        {"name": "plc_cpu", "title": "PLC CPU", "value": "CPU-315-2 DP"},
                    ]
                }
            )
            asset_entry = {"name": resp_asset.get("name", asset_name), "title": asset_title}
            assets.append(asset_entry)
            print(f"Created asset: {asset_name}")
            created["assets"] = assets
            save_progress(created, output_file)
        except Exception as e:
            print(f"Error creating asset {asset_name}: {e}")
    return assets


# -----------------------------
# Step 3: Create Data Streams
# -----------------------------
def create_data_streams(client, y: int, created, base_stream_name: str, base_stream_title: str, output_file: str) -> list:
    print(f"\nCreating {y} independent data streams...")
    streams = created.get("data_streams", [])
    for i in range(1, y + 1):
        stream_name = f"{base_stream_name}_{i}"
        stream_title = f"{base_stream_title} {i}"
        print(f"Creating data stream: {stream_name}")

        try:
            resp_stream = client.datastreams.create_data_stream(
                data={
                    "description": f"Demo Data Stream {i} for temperature monitoring.",
                    "name": stream_name,
                    "data_type_name": "number",
                    "semantic_type_name": "temperature",
                    "title": stream_title,
                    "type": "measurement",
                    "unit_name": "degree_celsius"
                }
            )
            stream_entry = {"name": resp_stream.get("name", stream_name), "title": stream_title}
            streams.append(stream_entry)
            print(f"Created data stream: {stream_name}")
            created["data_streams"] = streams
            save_progress(created, output_file)
        except Exception as e:
            print(f"Error creating data stream {stream_name}: {e}")
    return streams


# -----------------------------------------
# Step 4: Generate Random CSV (Saved to Temp File)
# -----------------------------------------
def generate_random_csv(stream_names: list, num_rows: int, min_value: float, max_value: float, delta: float) -> str:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
    writer = csv.writer(tmp)

    headers = ["timestamp"] + stream_names
    writer.writerow(headers)

    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    previous_values = [random.uniform(min_value, max_value) for _ in stream_names]

    for i in range(num_rows):
        ts = (start_time + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        if i > 0:
            new_values = []
            for val in previous_values:
                delta_val = random.uniform(-delta, delta)
                new_val = max(min_value, min(max_value, val + delta_val))
                new_values.append(new_val)
            previous_values = new_values
        writer.writerow([ts] + [f"{v:.6f}" for v in previous_values])

    tmp.flush()
    tmp.close()
    print(f"Generated temporary CSV: {os.path.basename(tmp.name)} ({num_rows} rows)")
    return tmp.name


# -----------------------------------------
# Step 5: Upload CSV for a given Asset
# -----------------------------------------
def upload_csv_for_asset(client, csv_path: str, asset_name: str, asset_entry: dict, created: dict, output_file: str) -> dict:
    print(f"Uploading generated CSV for asset '{asset_name}' to Kelvin File Storage...")
    try:
        resp = client.filestorage.upload_file(
            file=csv_path,
            metadata={"description": f"Generated random data for simulator ({asset_name})"}
        )
        print("CSV file uploaded.")

        uploaded = {
            "file_id": getattr(resp, "file_id", None),
            "file_name": getattr(resp, "file_name", os.path.basename(csv_path)),
            "file_size": getattr(resp, "file_size", None),
            "checksum": getattr(resp, "checksum", None),
            "created": str(getattr(resp, "created", None)),
            "metadata": getattr(resp, "metadata", {"description": f"Generated random data for simulator ({asset_name})"})
        }

        asset_entry["uploaded_file"] = uploaded
        save_progress(created, output_file)
        return uploaded
    except Exception as e:
        print(f"Error uploading CSV for {asset_name}: {e}")
        return {}


# -----------------------------------------
# Step 6: Create Workload (Connection)
# -----------------------------------------
def create_workload(client, api_url: str, asset: dict, file_id: str, created: dict, output_file: str) -> dict:
    if not file_id:
        print(f"Skipping workload creation for {asset['name']} (no file_id).")
        return {}

    asset_name = asset["name"]
    asset_title = asset["title"]
    workload_name = f"{asset_name.replace('_', '-')}-simulator"
    workload_title = f"{asset_title} csv"
    csv_url = f"{api_url}/api/v4/filestorage/{file_id}/download"

    all_streams = [s["name"] for s in created["data_streams"]]
    runtime_datastreams = [{
        "name": sname,
        "data_type_name": "number",
        "semantic_type_name": "temperature",
        "unit_name": "degree_celsius"
    } for sname in all_streams]
    resource_datastream_map = {
        sname: {"way": "output", "storage": "node-and-cloud", "remote": False, "configuration": {"column": sname}}
        for sname in all_streams
    }

    data = {
        "name": workload_name,
        "title": workload_title,
        "app_name": "kelvin-csv-publisher-connector",
        "app_version": "1.0.9",
        "app_type": "importer",
        "cluster_name": "beta-cluster-01",
        "runtime": {
            "datastreams": runtime_datastreams,
            "resources": [{
                "resource": f"krn:asset:{asset_name}",
                "datastreams": resource_datastream_map,
                "asset": {
                    "name": asset_name,
                    "title": asset_title,
                    "type": {"name": created["asset_type"], "title": "Documentation Demo Asset Type"}
                }
            }],
            "configuration": {"csv_url": csv_url, "replay": False, "timestamp": {"type": "playback"}}
        },
        "system": None,
        "node_name": "beta-dev-01-cluster"
    }

    print(f"Creating workload (connection): {workload_name}")
    try:
        resp = client.app_workloads.create_workload(data=data)
        print(f"Workload created: {workload_name}")
        wl = {"name": resp.get("name", workload_name)}
        asset["workload"] = wl
        save_progress(created, output_file)
        return wl
    except Exception as e:
        print(f"Error creating workload for {asset_name}: {e}")
        return {}


# -----------------------------
# Orchestrator: main()
# -----------------------------
def main():
    x = int(input("How many assets do you want to create? "))
    y = int(input("How many data streams do you want to create? "))
    rows_input = input("How many rows of random data to generate? [default 100]: ")
    num_rows = int(rows_input) if rows_input.strip() else 100

    min_input = input("Minimum random value [default 0]: ").strip()
    max_input = input("Maximum random value [default 150]: ").strip()
    delta_input = input("Maximum delta change per new value [default 5]: ").strip()

    min_value = float(min_input) if min_input else 0
    max_value = float(max_input) if max_input else 150
    delta = float(delta_input) if delta_input else 5

    api_input = input("Kelvin API URL [default 'https://beta.kelvininc.com']: ").strip()
    API_URL = api_input or "https://beta.kelvininc.com"

    output_file = input("Output JSON filename [default 'created_resources.json']: ").strip() or "created_resources.json"

    asset_type_name = input("Asset type name [default 'doc_demo_asset_type']: ").strip() or "doc_demo_asset_type"
    asset_type_title = input("Asset type title [default 'Documentation Demo Asset Type']: ").strip() or "Documentation Demo Asset Type"

    base_asset_name = input("Base asset name [default 'docs_demo_asset']: ").strip() or "docs_demo_asset"
    base_asset_title = input("Base asset title [default 'Docs Demo Asset']: ").strip() or "Docs Demo Asset"

    base_stream_name = input("Base data stream name [default 'docs_demo_temperature']: ").strip() or "docs_demo_temperature"
    base_stream_title = input("Base data stream title [default 'Docs Demo Temperature']: ").strip() or "Docs Demo Temperature"

    USERNAME = os.getenv("KELVIN_USERNAME")
    PASSWORD = os.getenv("KELVIN_PASSWORD")

    if not USERNAME and not PASSWORD:
        raise ValueError("Environment variables KELVIN_USERNAME and KELVIN_PASSWORD are not set.")
    elif not USERNAME:
        raise ValueError("Environment variable KELVIN_USERNAME not set.")
    elif not PASSWORD:
        raise ValueError("Environment variable KELVIN_PASSWORD not set.")

    print("\nLogging into Kelvin API...")
    client = Client(url=API_URL, username=USERNAME)
    client.login(password=PASSWORD)
    print("Logged into Kelvin API.\n")

    created = {"api_url": API_URL, "asset_type": None, "assets": [], "data_streams": []}
    save_progress(created, output_file)

    create_asset_type(client, created, asset_type_name, asset_type_title, output_file)
    assets = create_assets(client, x, created, base_asset_name, base_asset_title, asset_type_name, output_file)
    streams = create_data_streams(client, y, created, base_stream_name, base_stream_title, output_file)

    stream_names = [s["name"] for s in streams]
    for idx, asset in enumerate(created["assets"], start=1):
        print(f"\nSimulator setup for asset {asset['name']} ({idx}/{len(created['assets'])})")
        csv_path = generate_random_csv(stream_names, num_rows, min_value, max_value, delta)
        try:
            uploaded = upload_csv_for_asset(client, csv_path, asset["name"], asset, created, output_file)
            create_workload(client, API_URL, asset, uploaded.get("file_id"), created, output_file)
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)

    print("\nSetup complete. The JSON file now reflects everything created on Kelvin.")


if __name__ == "__main__":
    main()
