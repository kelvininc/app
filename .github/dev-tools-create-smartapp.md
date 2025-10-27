# dev-tools-create-smartapp — depth-0 extract (Kelvin docs: create)

Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/create/
Fetched: 2025-10-26 (offline extract stored in this repo)

Summary (depth-0)
This page documents the boilerplate and canonical layout produced by `kelvin app create` and explains the `app.yaml` structure used by Kelvin SmartApps (v6.3). It covers:

- The top-level `app.yaml` sections: `spec_version`, `type`, `name/title/description`, `version`, `flags`, `data_streams` (inputs/outputs), `data_quality` validators, `control_changes`, `parameters`, `ui_schemas`, and `defaults` (system, datastream_mapping, configuration, parameters).
- Built-in data-quality validators and configurable parameters (e.g. `kelvin_duplicate_detection`, `kelvin_outlier_detection`, `kelvin_data_availability`).
- How `ui_schemas` link to JSON files for parameter and configuration display and validation in the Kelvin UI.
- `defaults` usage for system resources, environment variables, volumes, ports, privileged access, datastream mappings, global configuration, and per-asset parameter defaults.
- The generated project files: `main.py` (sample async `KelvinApp` entrypoint), `requirements.txt`, `Dockerfile`, and `.dockerignore`.

Key actionable snippets (shortened)

app.yaml (essential parts)

```yaml
spec_version: 5.0.0
name: example-smartapp
data_streams:
  inputs:
    - name: motor_temperature
      data_type: number
  outputs: []
parameters:
  - name: kelvin_closed_loop
    data_type: boolean
ui_schemas:
  parameters: ui_schemas/parameters.json
defaults:
  parameters:
    kelvin_closed_loop: false
```

parameters UI schema (example)

```json
{
  "type": "object",
  "properties": {
    "kelvin_closed_loop": {"type":"boolean","title":"Kelvin Closed Loop"},
    "temperature_max_threshold": {"type":"number","minimum":50,"maximum":100}
  },
  "required": ["kelvin_closed_loop"]
}
```

Dockerfile excerpt

```dockerfile
FROM python:3.12-slim
WORKDIR /opt/kelvin/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /opt/kelvin/app
```markdown
# dev-tools-create-smartapp — depth-0 extract (Kelvin docs: create)

Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/create/
Fetched: 2025-10-26 (offline extract stored in this repo)

Overview
This document is a self-contained, depth-0 extract of the Kelvin developer "create" documentation (v6.3). It is intended to stand on its own when internet access is unavailable. It covers the `app.yaml` schema, the generated project layout, configuration and defaults, data-quality validators, and examples for quick copy/paste.

1) app.yaml — top-level structure and examples

The `app.yaml` file declares the SmartApp contract with the Kelvin platform. Typical top-level keys:
- `spec_version`: Kelvin spec version
- `type`: usually `app`
- `name`, `title`, `description`, `version`
- `flags`: runtime update flags
- `data_streams`: declares `inputs` and `outputs` the app consumes/produces
- `data_quality`: optional validators and mappings used by the platform
- `control_changes`: outputs intended as control change data streams
- `parameters`: app-level parameters (applied per-asset)
- `ui_schemas`: links to JSON schema files for parameter/config UI
- `defaults`: system, datastream_mapping, configuration, and parameter defaults

Minimal example (copyable)

```yaml
spec_version: 5.0.0
type: app
name: example-smartapp
title: Example SmartApp
description: Demonstration app
version: 1.0.0
data_streams:
  inputs:
    - name: motor_temperature
      data_type: number
    - name: motor_speed
      data_type: number
  outputs:
    - name: motor_speed_set_point
      data_type: number
data_quality:
  inputs:
    - name: kelvin_data_availability
      data_type: number
      data_streams:
        - motor_temperature
control_changes:
  outputs:
    - name: motor_speed_set_point
      data_type: number
parameters:
  - name: kelvin_closed_loop
    data_type: boolean
  - name: temperature_max_threshold
    data_type: number
ui_schemas:
  parameters: ui_schemas/parameters.json
defaults:
  configuration: {}
  parameters:
    kelvin_closed_loop: false
    temperature_max_threshold: 59
```

2) Data quality validators (built-ins)

Kelvin provides a set of inbuilt data-quality validators that you can reference by name in `app.yaml` under `data_quality`. Common validators and their configurable parameters:

- kelvin_timestamp_anomaly — Detects irregularities in timestamp sequences. (No params)
- kelvin_duplicate_detection — Detects duplicate values within a window. Config: `window_size` (default 5)
- kelvin_out_of_range_detection — Validates values against `min_threshold` and/or `max_threshold`.
- kelvin_outlier_detection — Uses statistical methods; Config: `model`, `threshold` (default 3), `window_size` (default 10)
- kelvin_data_availability — Ensures expected message counts within a window. Config: `window_expected_number_msgs`, `window_time_interval_unit` (second/minute/hour/day)

Use these validator names in `app.yaml.data_quality` entries. Each validator's parameters are validator-specific — include them under the validator entry.

3) control_changes

Declare control change outputs that the app may publish. You do not need to declare a data_stream under `data_streams` if it is only used for control changes; however declaring them in `data_streams` improves clarity.

Example

```yaml
control_changes:
  outputs:
    - name: speed_sp_out
      data_type: number
```

4) Parameters and UI schemas

App Parameters are defined in `app.yaml.parameters`. The `ui_schemas` section points to JSON schema files that control how parameters and configuration appear in the Kelvin UI. Keep these in sync.

Sample `ui_schemas/parameters.json`

```json
{
  "type": "object",
  "properties": {
    "kelvin_closed_loop": {"type":"boolean","title":"Closed Loop"},
    "speed_decrease_set_point": {"type":"number","title":"Speed Decrease SetPoint","minimum":1000,"maximum":3000},
    "temperature_max_threshold": {"type":"number","title":"Temperature Max Threshold","minimum":50,"maximum":100}
  },
  "required": ["kelvin_closed_loop","speed_decrease_set_point","temperature_max_threshold"]
}
```

Notes:
- If `ui_schemas/parameters.json` is missing or empty, Kelvin UI will render a simple form from keys and types only; adding the JSON schema enables validation and user-friendly labels.

5) defaults section — system / mappings / configuration / parameters

The `defaults` key contains optional subkeys used by the platform to populate initial values and runtime settings.

- `defaults.system` — container/system settings: `resources` (requests/limits), `environment_vars`, `volumes`, `ports`, `privileged`.
- `defaults.datastream_mapping` — maps app inputs/outputs to existing Kelvin Data Streams.
- `defaults.configuration` — global app configuration applied to the SmartApp as a whole.
- `defaults.parameters` — default per-asset parameter values applied when an asset is created or when new parameters are added during upgrades.

Example `defaults.system` (resources + env + volumes + ports)

```yaml
defaults:
  system:
    resources:
      requests:
        cpu: 100m
        memory: 256Mi
      limits:
        cpu: 200m
        memory: 512Mi
    environment_vars:
      - name: AZURE_ACCOUNT_NAME
        value: <% secrets.azure-account-name %>
    volumes:
      - name: serial-rs232
        target: /dev/rs232
        type: host
        host:
          source: /dev/ttyS0
    ports:
      - name: http
        type: host
        host:
          port: 80
    privileged: false
```

6) datastream_mapping example

```yaml
defaults:
  datastream_mapping:
    - app: temp_f
      datastream: temperature_fahrenheit
    - app: temp_c
      datastream: temperature_celsius
```

7) Generated files and runtime artifacts

When you run `kelvin app create`, a typical project is generated with:
- `main.py` — sample entrypoint that sets up `KelvinApp()` and runs a simple async loop or stream handlers.
- `requirements.txt` — dependencies; typically includes `kelvin-python-sdk[ai]`.
- `Dockerfile` — container recipe; base python image, installs requirements, copies app, and sets ENTRYPOINT.
- `.dockerignore` — to reduce build context.

Example `main.py` (more complete pattern)

```python
import asyncio
from datetime import timedelta

from kelvin.application import KelvinApp, filters
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import ControlChange, Recommendation
from kelvin.message.evidences import Image, Markdown

async def stream_asset_datastream_data_quality_messages(app: KelvinApp):
    async for message in app.stream_filter(filters.is_asset_data_stream_quality_message):
        asset_id = message.resource.asset
        datastream = message.resource.data_stream
        data_quality_metric = message.resource.data_quality
        dq_value = message.payload
        # handle data-quality

async def stream_asset_data_messages(app: KelvinApp):
    async for message in app.stream_filter(filters.is_asset_data_message):
        asset_id = message.resource.asset
        data_stream = message.resource.data_stream
        measurement = message.payload
        # process measurement

async def main() -> None:
    app = KelvinApp()
    await app.connect()
    await asyncio.gather(
        stream_asset_data_messages(app),
        stream_asset_datastream_data_quality_messages(app),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

8) requirements.txt example

```
kelvin-python-sdk[ai]
```

9) Dockerfile example

```dockerfile
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/kelvin/app
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . /opt/kelvin/app
ENTRYPOINT ["python","main.py"]
```

10) Notes for authors and reviewers

- Keep `app.yaml` and `ui_schemas` consistent. Changes here are platform-visible and must be reviewed carefully.
- Use `defaults.system` to request resources, environment variables, and volumes when your app needs host access or external services.
- When adding data-quality validators, include the validator name and any validator-specific parameters in `app.yaml` so the platform can perform checks.
- If a screenshot, image, or guidance is referenced in the app (evidences in Recommendations), include accessible alt text and a short caption.

Authoritative link
- Live docs: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/create/

This offline extract should be kept in sync with `app.yaml` changes. When you modify the app structure, update this file so reviewers can validate without internet access.

``` 
