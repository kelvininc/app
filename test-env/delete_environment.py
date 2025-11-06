from kelvin.api.client import Client
import json
import os
import sys


# -----------------------------
# Delete Workloads (Connections)
# -----------------------------
def delete_workloads(client, assets):
    workload_names = [a["workload"]["name"] for a in assets if "workload" in a and a["workload"].get("name")]
    if not workload_names:
        print("No workloads found to delete.")
        return
    print("\nDeleting workloads...")
    try:
        client.app_workloads.delete_workloads(data={"workload_names": workload_names})
        print(f"Deleted workloads: {workload_names}")
    except Exception as e:
        print(f"Error deleting workloads: {e}")


# -----------------------------
# Delete Uploaded Files
# -----------------------------
def delete_files(client, assets):
    print("\nDeleting uploaded CSV files...")
    for a in assets:
        uploaded = a.get("uploaded_file")
        if not uploaded or not uploaded.get("file_id"):
            print(f"No file_id found for asset {a['name']}, skipping.")
            continue
        fid = uploaded["file_id"]
        try:
            client.filestorage.delete_file(file_id=fid)
            print(f"Deleted file: {fid}")
        except Exception as e:
            print(f"Error deleting file {fid}: {e}")


# -----------------------------
# Delete Data Streams
# -----------------------------
def delete_data_streams(client, streams):
    stream_names = [s["name"] for s in streams if "name" in s]
    if not stream_names:
        print("No data streams found to delete.")
        return
    print("\nDeleting data streams...")
    try:
        client.datastreams.delete_bulk_data_stream(data={"datastream_names": stream_names})
        print(f"Deleted data streams: {stream_names}")
    except Exception as e:
        print(f"Error deleting data streams: {e}")


# -----------------------------
# Delete Assets
# -----------------------------
def delete_assets(client, assets):
    asset_names = [a["name"] for a in assets if "name" in a]
    if not asset_names:
        print("No assets found to delete.")
        return
    print("\nDeleting assets...")
    try:
        client.asset.delete_asset_bulk(data={"names": asset_names})
        print(f"Deleted assets: {asset_names}")
    except Exception as e:
        print(f"Error deleting assets: {e}")


# -----------------------------
# Delete Asset Type
# -----------------------------
def delete_asset_type(client, asset_type_name):
    if not asset_type_name:
        print("No asset type name found to delete.")
        return
    print("\nDeleting asset type...")
    try:
        client.asset.delete_asset_type(asset_type_name=asset_type_name)
        print(f"Deleted asset type: {asset_type_name}")
    except Exception as e:
        print(f"Error deleting asset type {asset_type_name}: {e}")


# -----------------------------
# Rename JSON file after cleanup
# -----------------------------
def mark_file_deleted(filepath):
    base = filepath
    suffix = ".deleted"
    new_name = base + suffix

    # Handle duplicate deleted files
    counter = 1
    while os.path.exists(new_name):
        new_name = f"{base}{suffix}{counter:03d}"
        counter += 1

    os.rename(filepath, new_name)
    print(f"\nRenamed JSON file to '{new_name}'")


# -----------------------------
# Orchestrator: main()
# -----------------------------
def main():
    # List all JSON files
    json_files = [f for f in os.listdir(".") if f.endswith(".json")]
    print("Available JSON files:")
    for i, f in enumerate(json_files, start=1):
        print(f"  {i}. {f}")
    print()

    default_file = "created_resources.json"
    json_file = input(f"Enter the JSON file to use [default '{default_file}']: ").strip() or default_file

    if not os.path.exists(json_file):
        print(f"File '{json_file}' not found. Run the creation script first.")
        sys.exit(1)

    with open(json_file, "r") as f:
        data = json.load(f)

    API_URL = data.get("api_url")
    ASSET_TYPE = data.get("asset_type")
    ASSETS = data.get("assets", [])
    STREAMS = data.get("data_streams", [])

    USERNAME = "demo@kelvin.ai"
    PASSWORD = os.getenv("USERPASS")
    if not PASSWORD:
        raise ValueError("Environment variable USERPASS not set. Please export USERPASS before running.")

    print("\nLogging into Kelvin API...")
    client = Client(url=API_URL, username=USERNAME)
    client.login(password=PASSWORD)
    print("Logged into Kelvin API.\n")

    # DELETE IN REVERSE ORDER
    delete_workloads(client, ASSETS)
    delete_files(client, ASSETS)
    delete_data_streams(client, STREAMS)
    delete_assets(client, ASSETS)
    delete_asset_type(client, ASSET_TYPE)

    print("\nCleanup complete. All created resources have been deleted (where applicable).")

    # Rename JSON file after success
    mark_file_deleted(json_file)


if __name__ == "__main__":
    main()
