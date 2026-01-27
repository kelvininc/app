# Purpose and Audience

This guide helps coding agents build Kelvin SmartApps using the Kelvin Python SDK. It assumes no prior knowledge of Kelvin or industrial IoT. All platform concepts and SDK patterns you need are defined here.

# Kelvin Concepts (Glossary + Mental Model)

A Kelvin SmartApp runs on the Kelvin platform. It subscribes to asset data streams and publishes outputs (data, control changes, recommendations, custom actions). The `app.yaml` file is the contract with the platform; `main.py` implements behavior.

**Glossary**
- **Asset**: A physical or logical entity (pump, well, compressor, chiller).
- **Data stream**: Named time-series signal for an asset (e.g., `temperature`).
- **KRN**: Kelvin Resource Name; addresses assets and streams.
- **Parameters**: Per-asset configuration values (can differ per asset).
- **Configuration**: Global app-level settings (same for all assets).
- **Recommendation**: Operator-facing recommendation, optionally containing evidences.
- **Control change**: Command/setpoint update to equipment; supports acks/timeouts.
- **Custom action**: Action to external systems (email, work order, etc.).
- **Evidence**: Contextual content attached to recommendations.
- **Data quality**: Quality metrics about data streams or assets.

# Clarification Checklist

Ask for clarification if you do not know any of the following:
- Input data streams (names, types, assets, sources)
- Output data streams (names, types, destinations)
- Recommendations (types, conditions, evidences)
- Parameters (per-asset configuration values)
- Configuration (global app-level settings)
- Control changes (control outputs, acknowledgments)
- Custom actions (types, payloads, external destinations)
- Whether control changes or custom actions should be sent outside recommendations

Example questions:
- "What are the exact names and data types of the input streams?"
- "Should recommendations be open-loop or closed-loop?"

# Project Structure and app.yaml

The Kelvin SDK provides the following file structure out of the box:

```
my-app-name/
├── main.py                        # Application logic with KelvinApp instance
├── app.yaml                       # Platform configuration
├── requirements.txt               # Python dependencies (always use kelvin-python-sdk[ai])
├── Dockerfile                     # Container build configuration
├── .dockerignore                  # Build exclusions
└── ui_schemas/                    # UI configuration schemas (optional but recommended)
    ├── parameters.json            # UI schema for asset-level parameters
    └── configuration.json         # UI schema for app-level configuration
```

**Full app.yaml example (canonical template):**

```yaml
spec_version: 5.0.0
type: app

name: well-production-monitor
title: Well Production Monitoring
description: Monitors well production metrics and generates optimization recommendations
version: 1.0.0
category: smartapp

flags:
  enable_runtime_update:
    configuration: false   # Can update config at runtime (default: false)
    resources: false       # Can add/remove assets at runtime (default: false)
    parameters: true       # Can update parameters at runtime (default: true)
    resource_properties: true  # Can update asset properties at runtime (default: true)

data_streams:
  inputs:
    - name: casing_pressure
      data_type: number
    - name: tubing_pressure
      data_type: number
    - name: temperature
      data_type: number
    - name: oil_rate
      data_type: number
    - name: gas_rate
      data_type: number
    - name: choke_setpoint
      data_type: number
  outputs:
    - name: production_index
      data_type: number
    - name: optimization_status
      data_type: string

control_changes:
  inputs:
    - name: external_setpoint
      data_type: number
  outputs:
    - name: choke_setpoint
      data_type: number
    - name: speed_sp
      data_type: number

data_quality:
  inputs:
    - name: kelvin_timestamp_anomaly
      data_type: number
      data_streams: [casing_pressure, tubing_pressure, oil_rate, gas_rate]
    - name: kelvin_stale_detection
      data_type: number
      data_streams: [temperature]
    - name: kelvin_out_of_range_detection
      data_type: number
      data_streams: [casing_pressure]
    - name: kelvin_outlier_detection
      data_type: number
      data_streams: [oil_rate]
    - name: kelvin_data_availability
      data_type: number
      data_streams: [gas_rate]
    - name: kelvin_score
      data_type: number

parameters:  # Per-asset, can differ between assets
  - name: max_casing_pressure
    data_type: number
  - name: min_oil_rate
    data_type: number
  - name: max_water_cut
    data_type: number
  - name: kelvin_closed_loop
    data_type: boolean

custom_actions:
  inputs:
    - type: slack
  outputs:
    - type: email
    - type: work_order

ui_schemas:
  parameters: ui_schemas/parameters.json
  configuration: ui_schemas/configuration.json

defaults:
  parameters:
    max_casing_pressure: 1500.0
    min_oil_rate: 100.0
    max_water_cut: 0.80
    kelvin_closed_loop: false
  configuration:  # Global app-level, same for all assets (no declaration needed)
    analysis_window_minutes: 15
    optimization_interval_seconds: 300
  system:
    environment_vars:
      - name: KELVIN_CLIENT__URL
        value: https://example.kelvin.ai
      - name: KELVIN_CLIENT__CLIENT_ID
        value: <% secrets.applications-client-id %>
      - name: KELVIN_CLIENT__CLIENT_SECRET
        value: <% secrets.applications-client-secret %>
```

**Data types**
- `number` - Numeric values (int, float)
- `string` - Text values
- `boolean` - True/False values
- `object` - JSON objects

**Naming conventions**
- App names: lowercase with hyphens (e.g., `motor-monitor`)
- Variable names: lowercase with underscores (e.g., `motor_speed_set_point`)
- Regex: `^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$`

**Configuration vs parameters**
- Use `defaults.configuration` for global app settings (same for all assets).
- Use `parameters` for per-asset settings (can differ per asset).

```python
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

async def on_connect():
    # Global app-level configuration
    window_minutes = int(app.app_configuration.get("analysis_window_minutes", 15))
    optimization_interval = int(app.app_configuration.get("optimization_interval_seconds", 300))
    logger.info("App configuration", window_minutes=window_minutes, optimization_interval=optimization_interval)

    # Per-asset parameters
    for asset_name, asset in app.assets.items():
        max_casing_pressure = float(asset.parameters.get("max_casing_pressure", 1500.0))
        min_oil_rate = float(asset.parameters.get("min_oil_rate", 100.0))
        max_water_cut = float(asset.parameters.get("max_water_cut", 0.80))
        logger.info("Asset configured", asset=asset_name, max_pressure=max_casing_pressure)

app.on_connect = on_connect
app.run()
```

**UI schemas**

JSON schemas configure the Kelvin UI for parameters and configuration. Always create these when your app has parameters or configuration.

**parameters.json** (asset-level parameters):
```json
{
  "type": "object",
  "properties": {
    "max_casing_pressure": {
      "type": "number",
      "title": "Max Casing Pressure (psi)",
      "description": "Alert when casing pressure exceeds this value",
      "minimum": 0,
      "maximum": 3000,
      "default": 1500.0
    },
    "min_oil_rate": {
      "type": "number",
      "title": "Minimum Oil Rate (bbl/day)",
      "description": "Alert when oil production falls below this rate",
      "minimum": 0,
      "maximum": 5000,
      "default": 100.0
    },
    "max_water_cut": {
      "type": "number",
      "title": "Maximum Water Cut",
      "description": "Alert when water cut exceeds this fraction",
      "minimum": 0,
      "maximum": 1,
      "default": 0.80
    },
    "kelvin_closed_loop": {
      "type": "boolean",
      "title": "Closed Loop Recommendations",
      "description": "Auto-accept recommendations that include actions",
      "default": false
    }
  },
  "required": ["max_casing_pressure", "min_oil_rate", "max_water_cut", "kelvin_closed_loop"]
}
```

**configuration.json** (app-level configuration):
```json
{
  "type": "object",
  "properties": {
    "analysis_window_minutes": {
      "type": "number",
      "title": "Analysis Window (minutes)",
      "description": "Time window for production data analysis",
      "minimum": 1,
      "maximum": 60,
      "default": 15
    },
    "optimization_interval_seconds": {
      "type": "number",
      "title": "Optimization Interval (seconds)",
      "description": "How often to run optimization calculations",
      "minimum": 60,
      "maximum": 3600,
      "default": 300
    }
  }
}
```

# SDK Core Components + Imports

**Core imports**
```python
from api.src.kelvin.api.client import AsyncClient
from kelvin.application import KelvinApp, filters
from kelvin.krn import KRNAsset
from kelvin.krn import KRNAssetDataStream
from kelvin.krn import KRNAssetDataQuality, KRNAssetDataStreamDataQuality
from kelvin.krn import KRNAssetParameter
from kelvin.message import Number, String, Boolean
from kelvin.message import ControlChange, ControlAck
from kelvin.message import AppParameter, AppParameters
from kelvin.message import DataTag, CustomAction, Recommendation
from kelvin.message.evidences import BarChart, LineChart
from kelvin.message.evidences import DataExplorer, DataExplorerSelector, AggregationTypes
from kelvin.message.evidences import IFrame, Image, Markdown

app = KelvinApp()

# filters.input_equals(["temperature", "oil_rate"]) - Filter by data stream name
# filters.asset_equals(["asset_1", "asset_2"]) - Filter by asset name
# filters.is_data_quality_message - Filter for data quality messages

client: AsyncClient = app.api
# client.timeseries.get_timeseries_last(...)
# client.timeseries.get_timeseries_range(...)
# client.asset.create_asset(...)
# client.filestorage.upload_file(...)
```

# Lifecycle and Callbacks

`app.run()` connects to the platform and blocks the current thread. Use `await app.connect()` for manual event-loop control.

**Startup sequence**
1. Platform connection established
2. Assets and parameters loaded (`app.assets` populated)
3. `on_connect()` invoked (if defined)
4. Stream subscriptions activated
5. Background tasks started
6. Timers scheduled
7. Stream handlers receive messages

```python
from typing import Optional
from kelvin.application import AssetInfo, KelvinApp
from kelvin.logs import logger
from kelvin.message import AssetDataMessage, ControlAck, ControlChangeStatus, CustomAction, StateEnum

app = KelvinApp()

async def on_asset_input(msg: AssetDataMessage):
    """Called for all incoming data messages"""
    logger.info("Data received", resource=str(msg.resource), payload=msg.payload)


async def on_asset_change(newAssetInfo: Optional[AssetInfo], oldAssetInfo: Optional[AssetInfo]):
    """Called when there are changes on asset parameters and/or properties"""
    if newAssetInfo is not None:
        logger.info("Asset changed", asset=newAssetInfo.name, parameters=newAssetInfo.parameters)
    elif oldAssetInfo is not None:
        logger.info("Asset removed", asset=oldAssetInfo.name)


async def on_control_change(msg: AssetDataMessage):
    """Called for incoming control changes"""
    logger.info("Control change received", resource=str(msg.resource), payload=msg.payload)

    # Acknowledge the control change
    ack = ControlAck(resource=msg.resource, state=StateEnum.applied, message="Control change successfully applied")
    await app.publish(ack)


async def on_control_status(cc_status: ControlChangeStatus) -> None:
    """Called for incoming Control Change Status"""
    logger.info("Received Control Change Status", status=cc_status)


async def on_custom_action(action: CustomAction):
    """Called for incoming Custom Action messages"""
    logger.info("Received Custom Action", action=action)


async def on_app_configuration(conf: dict):
    """Called when there are changes on app configuration"""
    logger.info("App configuration change", config=conf)


app.on_asset_input = on_asset_input
app.on_asset_change = on_asset_change
app.on_control_change = on_control_change
app.on_control_status = on_control_status
app.on_custom_action = on_custom_action
app.on_app_configuration = on_app_configuration

app.run()
```

# Recommended Code Patterns

Use the decorator-based API by default.

**Decorator-based streams with filtering**
```python
from kelvin.application import KelvinApp
from kelvin.logs import logger
from kelvin.message import AssetDataMessage

app = KelvinApp()

@app.stream(assets=["asset-1"], inputs=["casing_pressure", "tubing_pressure", "oil_rate"])
async def monitor_production(msg: AssetDataMessage):
    asset = msg.resource.asset
    data_stream = msg.resource.data_stream
    value = msg.payload

    logger.info("Production data", asset=asset, data_stream=data_stream, value=value)

    if data_stream == "casing_pressure":
        max_pressure = float(app.assets[asset].parameters.get("max_casing_pressure", 1500.0))
        if value < 0 or value > max_pressure:
            logger.warning("Invalid casing pressure", asset=asset, pressure=value, limit=max_pressure)
            return
    elif data_stream == "tubing_pressure":
        if value < 0 or value > 2500:
            logger.warning("Invalid tubing pressure", asset=asset, pressure=value)
            return

app.run()
```

**Tasks and timers**
Synchronous `@app.task` runs in a worker thread; keep it short and bounded.
```python
import asyncio
import time
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

@app.task
async def background_task():
    logger.info("Initialized")

@app.task
async def continuous():
    try:
        while True:
            await asyncio.sleep(10)
            logger.info("Working")
    except Exception as e:
        logger.error("Task failed", error=str(e), exc_info=True)

@app.timer(interval=30)
async def periodic():
    logger.info("Periodic check")

@app.task
def calculate_metrics():
    time.sleep(1)

app.run()
```

**Function-based pattern** (use only if explicitly requested)
```python
from kelvin.application import KelvinApp, filters
from kelvin.logs import logger
from kelvin.message import Number
from kelvin.krn import KRNAssetDataStream
import asyncio

async def process_stream(app: KelvinApp):
    stream = app.stream_filter(filters.input_equals(["temperature"]))
    async for msg in stream:
        asset = msg.resource.asset
        data_stream = msg.resource.data_stream
        value = msg.payload

        logger.info("Received message", asset=asset, data_stream=data_stream, value=value)

        await app.publish(
            Number(
                resource=KRNAssetDataStream(asset, "production_index"),
                payload=value * 2
            )
        )

async def main():
    app = KelvinApp()
    await app.connect()
    await process_stream(app)

if __name__ == "__main__":
    asyncio.run(main())
```

**Error handling by decorator**
- `@app.stream()` and `@app.timer()` catch exceptions; handlers continue with next message/tick.
- `@app.task` does not catch exceptions; use `try/except` in long-running tasks.

**Framework guarantees**

The framework enforces schema and resource validity at the boundary. Assume the following are always valid:
- `msg.resource.asset` is a non-null `str` and exists in `app.assets`
- `msg.resource.data_stream` is a non-null `str`
- `msg.payload` matches the type declared in `app.yaml`

```python
from kelvin.application import AssetInfo

@app.stream(inputs=["casing_pressure"])
async def handle(msg: AssetDataMessage) -> None:
    value: float = msg.payload
    asset: AssetInfo = app.assets[msg.resource.asset]
    max_pressure = float(asset.parameters.get("max_casing_pressure", 1500.0))
```

Validate only business rules (ranges, thresholds), external inputs, and derived computations.

**Error handling details**

| Decorator | Exceptions Handled? | Behavior |
|-----------|---------------------|----------|
| `@app.stream()` | YES | Next message still calls handler |
| `@app.timer()` | YES | Timer continues firing |
| `@app.task` | NO | Task dies if exception escapes |


# Messages and Outputs

**IMPORTANT**: Declare any published `data_streams.outputs`, `control_changes.outputs`, and `custom_actions.outputs` in `app.yaml` before publishing.

## Data messages
```python
from kelvin.application import KelvinApp
from kelvin.krn import KRNAssetDataStream
from kelvin.message import Number, String

app = KelvinApp()

@app.task
async def publish_data():
    await app.publish(Number(resource=KRNAssetDataStream("asset-1", "production_index"), payload=0.82))
    await app.publish(String(resource=KRNAssetDataStream("asset-1", "optimization_status"), payload="stable"))

app.run()
```

## Control changes and acks
```python
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.krn import KRNAssetDataStream
from kelvin.logs import logger
from kelvin.message import AssetDataMessage, ControlAck, ControlChange, StateEnum

app = KelvinApp()

@app.timer(interval=10)
async def publish_control_change():
    control_change = ControlChange(
        resource=KRNAssetDataStream("asset-1", "choke_setpoint"),
        payload=75.0,
        expiration_date=timedelta(minutes=10),
        timeout=60,
        retries=3,
    )
    await app.publish(control_change)

async def on_control_change(msg: AssetDataMessage):
    logger.info("Control change received", resource=str(msg.resource), payload=msg.payload)

    ack = ControlAck(
        resource=msg.resource,
        state=StateEnum.applied,
        message="Control change successfully applied",
    )
    await app.publish(ack)

app.on_control_change = on_control_change
app.run()
```

**IMPORTANT**: Use control changes for set points or commands. This ensures tracking, acknowledgement, and timeout handling.


## Custom actions
Publish custom actions inside recommendations unless explicitly asked to send standalone actions.
```python
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset
from kelvin.message import CustomAction, Recommendation

app = KelvinApp()

@app.timer(interval=10)
async def publish_data():
    asset = KRNAsset("asset-1")

    # Direct Custom Action
    action = CustomAction(
        resource=asset,
        type="email",
        title="Recommendation to reduce speed",
        description="It is recommended that the speed is reduced",
        expiration_date=datetime.now() + timedelta(hours=1),
        payload={
            "recipient": "operations@example.com",
            "subject": "Recommendation to reduce speed",
            "body": "This is the email body",
        },
    )
    await app.publish(action)

app.run()
```

## Recommendations

- If the user does not specify otherwise, send control changes and custom actions inside `Recommendation` messages (not standalone).
- Always add `kelvin_closed_loop` as a boolean parameter (default `false`) when the app makes control changes or custom actions through recommendations.

```python
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import ControlChange, Recommendation

app = KelvinApp()

@app.task
async def publish_recommendation():
    recommendation = Recommendation(
        resource=KRNAsset("asset-1"),
        type="pressure_optimization",
        control_changes=[
            ControlChange(
                resource=KRNAssetDataStream("asset-1", "choke_setpoint"),
                payload=70.0,
                expiration_date=timedelta(minutes=10),
            )
        ],
        actions=[
            CustomAction(
                resource=asset,
                type="work_order",
                title="Work Order Maintenance Required",
                description="Casing pressure exceeds threshold, maintenance needed",
                expiration_date=datetime.now() + timedelta(days=1),
                payload={
                    "priority": "high",
                    "equipment_id": "asset-1",
                    "issue_type": "pressure",
                    "requested_by": "monitoring-app",
                },
            )
        ]
        expiration_date=timedelta(hours=1),
        auto_accepted=bool(app.assets["asset-1"].parameters.get("kelvin_closed_loop", False)),
    )
    await app.publish(recommendation)

app.run()
```

## Recommendation Evidences

- You should always aim to include a `DataExplorer` and `Markdown` evidence inside a `Recommendation`. 

**Available Evidence Types:**
- `Markdown` - Formatted text explanations
- `DataExplorer` - Time-series chart visualization
- `LineChart` - Custom line charts
- `BarChart` - Custom bar charts
- `Image` - Static images
- `IFrame` - Embedded web content

```python
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import Recommendation
from kelvin.message.evidences import AggregationTypes, DataExplorer, DataExplorerSelector, LineChart, Markdown

app = KelvinApp()

@app.task
async def publish_recommendation():
    markdown = Markdown(
        title="Pressure Optimization Summary",
        markdown="""
## Pressure Optimization Triggered

The system detected unusually high casing pressure:
- Average: 1800 psi
- Normal range: 1200-1600 psi
- Duration: 2 hours

**Recommended action**: Reduce choke setpoint to stabilize pressure.
""",
    )

    now = datetime.now()
    data_explorer = DataExplorer(
        title="Pressure Optimization Trend",
        start_time=now - timedelta(hours=6),
        end_time=now,
        selectors=[
            DataExplorerSelector(resource=KRNAssetDataStream("asset-1", "casing_pressure")),
            DataExplorerSelector(
                resource=KRNAssetDataStream("asset-1", "tubing_pressure"),
                agg=AggregationTypes.mean,
                time_bucket="5m",
            ),
        ],
    )

    line_chart = LineChart(
        title="Casing Pressure (Optimization Window)",
        x_axis={"type": "datetime", "title": {"text": "Time"}},
        y_axis={"title": {"text": "Pressure (psi)"}},
        series=[
            {
                "name": "Casing Pressure",
                "type": "line",
                "data": [[0, 0]],
            }
        ],
    )

    recommendation = Recommendation(
        resource=KRNAsset("asset-1"),
        type="pressure_optimization",
        evidences=[markdown, data_explorer, line_chart],
        auto_accepted=False,
    )
    await app.publish(recommendation)

app.run()
```

## Data Tags
**Required fields:**
- `resource`: KRNAsset
- `start_date`: datetime (start of tagged period)
- `end_date`: datetime (end of tagged period)
- `tag_name`: str (name/type of the tag)

**Optional fields:**
- `description`: str (detailed description)
- `contexts`: list[KRNAssetDataStream] (related data streams)

```python
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import DataTag

app = KelvinApp()

@app.task
async def publish_data_tag():
    tag = DataTag(
        resource=KRNAsset("asset-1"),
        start_date=datetime.now() - timedelta(hours=2),
        end_date=datetime.now(),
        tag_name="cycle",
        description="Detected a well cycle.",
        contexts=[
            KRNAssetDataStream("asset-1", "temperature"),
            KRNAssetDataStream("asset-1", "tubing_pressure"),
        ],
    )
    await app.publish(tag)

app.run()
```

## Asset Parameters
```python
from kelvin.application import KelvinApp
from kelvin.krn import KRNAssetParameter
from kelvin.message import AppParameter, AppParameters

app = KelvinApp()

@app.task
async def publish_parameter_change():
    param = AppParameter(
        resource=KRNAssetParameter("asset-1", "max_casing_pressure"),
        value=1600.0,
        comment="Updated based on analysis",
    )
    await app.publish(AppParameters(parameters=[param]))

    params = [
        AppParameter(resource=KRNAssetParameter("asset-1", "min_oil_rate"), value=120.0),
        AppParameter(resource=KRNAssetParameter("asset-1", "max_water_cut"), value=0.75),
        AppParameter(resource=KRNAssetParameter("asset-1", "kelvin_closed_loop"), value=True),
    ]
    await app.publish(AppParameters(parameters=params))

app.run()
```

## Data Quality Messages

Consume data quality metrics via the data quality stream filter.

```python
from kelvin.application import KelvinApp, filters
from kelvin.logs import logger
from kelvin.message import AssetDataQualityMessage, AssetDataStreamDataQualityMessage

app = KelvinApp()

@app.task
async def handle_data_quality_messages():
    async for msg in app.stream_filter(filters.is_data_quality_message):
        asset = msg.resource.asset
        data_quality = msg.resource.data_quality
        value = msg.payload

        logger.info("Received Data Quality message", asset=asset, data_quality=data_quality, value=value)

        if isinstance(msg.resource, AssetDataStreamDataQualityMessage):
            data_stream = msg.resource.data_stream

            if data_quality == "kelvin_stale_detection" and data_stream == "temperature":
                pass
            elif data_quality == "kelvin_out_of_range_detection" and data_stream == "casing_pressure":
                pass
            elif data_quality == "kelvin_outlier_detection" and data_stream == "oil_rate":
                pass
            elif data_quality == "kelvin_data_availability" and data_stream == "gas_rate":
                pass

        elif isinstance(msg.resource, AssetDataQualityMessage):
            if data_quality == "kelvin_score":
                pass

app.run()
```

# Data Processing

## Data windows

Windows aggregate data over time or count and return `(asset_name: str, df: pandas.DataFrame)`.

**Key rules**
- DataFrame columns match `inputs=[...]` names exactly
- `df.index` is tz-aware datetime
- Always check `df.empty` before processing
- Values may be NaN; handle explicitly
- Declare inputs explicitly; no implicit columns

**Window best practices**
- Choose appropriate window type for the analysis
- Use `@app.task` for window processing
- Consider memory usage for large window sizes
- Use `window_start` for predictable alignment

**Window types**
1. Tumbling: time-based, non-overlapping
2. Hopping: time-based, overlapping
3. Rolling: count-based

**window_start** aligns boundaries for tumbling/hopping. Use it when alignment matters.

```python
from datetime import datetime, timedelta
import pandas as pd
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

@app.task
async def process_data() -> None:
    window_start = datetime.now().astimezone()

    async for asset, df in app.tumbling_window(
        window_size=timedelta(minutes=15),
        inputs=["casing_pressure", "tubing_pressure", "oil_rate", "gas_rate"],
    ).stream(window_start=window_start):
        try:
            if df.empty:
                continue

            avg_casing_pressure = float(df["casing_pressure"].mean())
            avg_tubing_pressure = float(df["tubing_pressure"].mean())
            avg_oil_rate = float(df["oil_rate"].mean())
            avg_gas_rate = float(df["gas_rate"].mean())

            if pd.isna(avg_casing_pressure) or pd.isna(avg_tubing_pressure):
                logger.warning("Insufficient pressure data", asset=asset)
                continue

            if pd.isna(avg_oil_rate) or pd.isna(avg_gas_rate):
                logger.warning("Insufficient production data", asset=asset)
                continue

            gor = avg_gas_rate / avg_oil_rate if avg_oil_rate > 0 else 0

            logger.info(
                "Production performance",
                asset=asset,
                avg_pressure=avg_casing_pressure,
                avg_oil_rate=avg_oil_rate,
                gas_oil_ratio=gor,
            )
        except Exception as e:
            logger.error("Window error", asset=asset, error=str(e))
            continue

app.run()
```

**Hopping window example**
```python
from datetime import datetime, timedelta
import pandas as pd
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

@app.task
async def process_data() -> None:
    window_start = datetime.now().astimezone()

    async for asset, df in app.hopping_window(
        window_size=timedelta(minutes=30),
        hop_size=timedelta(minutes=10),
        inputs=["casing_pressure", "tubing_pressure", "temperature"],
    ).stream(window_start=window_start):
        if df.empty:
            continue

        avg_diff_pressure = (df["casing_pressure"] - df["tubing_pressure"]).mean()
        max_temperature = df["temperature"].max()

        if pd.isna(avg_diff_pressure):
            logger.warning("Insufficient pressure data", asset=asset)
            continue

        if pd.isna(max_temperature):
            logger.warning("Insufficient temperature data", asset=asset)
            continue

        logger.info(
            "Wellhead health",
            asset=asset,
            differential_pressure=avg_diff_pressure,
            max_temperature=max_temperature,
        )

app.run()
```

**Rolling window example**
```python
import pandas as pd
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

@app.task
async def process_data() -> None:
    async for asset, df in app.rolling_window(
        count_size=20,
        slide=5,
        inputs=["oil_rate", "gas_rate"],
    ).stream():
        if df.empty:
            continue

        current_oil_rate = float(df["oil_rate"].iloc[-1])
        current_gas_rate = float(df["gas_rate"].iloc[-1])

        if pd.isna(current_oil_rate) or pd.isna(current_gas_rate):
            logger.warning("Insufficient production data", asset=asset)
            continue

        gor = current_gas_rate / current_oil_rate if current_oil_rate > 0 else 0

        avg_gor = (df["gas_rate"] / df["oil_rate"]).mean()
        std_gor = (df["gas_rate"] / df["oil_rate"]).std()

        if pd.isna(avg_gor) or pd.isna(std_gor):
            logger.warning("Insufficient data for GOR analysis", asset=asset)
            continue

        if std_gor > 0 and abs(gor - avg_gor) > 2 * std_gor:
            logger.warning("GOR anomaly", asset=asset, gor=gor)

app.run()
```


## Timeseries API

Use the Timeseries API for historical data older than 12 hours. Recent data should use real-time streaming windows or handlers.

**IMPORTANT**: Streams accessed via the Timeseries API do not need to be declared in `data_streams.inputs`. Declare inputs only for real-time streaming.

**Required environment variables**
```yaml
defaults:
  system:
    environment_vars:
    - name: KELVIN_CLIENT__URL
      value: https://example.kelvin.ai
    - name: KELVIN_CLIENT__CLIENT_ID
      value: <% secrets.applications-client-id %>
    - name: KELVIN_CLIENT__CLIENT_SECRET
      value: <% secrets.applications-client-secret %>
```

**Usage example**
```python
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

async def fetch_timeseries(asset_name: str, datastream_names: list[str]) -> None:
    request = {
        "start_time": datetime.now() - timedelta(days=7),
        "end_time": datetime.now(),
        "agg": "mean", # max, min, mean, sum, count, distinct, integral, stddev, spread, median, mode, first, last
        "time_bucket": "30s", # 10m, 30m, 1h, 6h, 1d, 7d, 30d
        "selectors": [
            {
                "resource": f"krn:ad:{asset_name}/{datastream_name}",
            } for datastream_name in datastream_names
        ],
        "order": "ASC", # ASC, DESC
        "fill": "none", # none, null, linear, previous, <value>
    }

    result = await app.api.timeseries.get_timeseries_range(data=request)

    df = result.to_df(datastreams_as_column=True)

    # df.head(5)
    #
    #     timestamp                         asset_name   gas_rate     casing_pressure
    # 0   2025-12-02 12:04:43.811316+00:00  asset-1     424.623553   NaN
    # 1   2025-12-02 12:04:58.839218+00:00  asset-1     NaN          28.282359
    # 2   2025-12-02 12:04:58.843605+00:00  asset-1     NaN          NaN
    # 3   2025-12-02 12:04:58.859270+00:00  asset-1     329.235913   NaN
    # 4   2025-12-02 12:04:58.883542+00:00  asset-1     NaN          NaN
```

# Operational Guidance

## State management and concurrency
- In-memory state is lost on restart; use external storage for persistence.
- Stream handlers run concurrently; use `asyncio.Lock` for shared mutable state.

```python
import asyncio

state_lock = asyncio.Lock()
count = 0

@app.stream(inputs=["oil_rate"])
async def count_events(msg: AssetDataMessage):
    global count
    async with state_lock:
        count += 1
```

**State initialization**

- Always handle asset changes (removal/addition) on global states to keep data consistent.

```python
asset_state = {}

# Option 1: Lazy (create on first message)
@app.stream(inputs=["oil_rate"])
async def handler(msg: AssetDataMessage):
    if msg.resource.asset not in asset_state:
        asset_state[msg.resource.asset] = {"count": 0}

# Option 2: Via on_asset_change (for dynamic assets)
async def on_asset_change(new_asset: Optional[AssetInfo], old_asset: Optional[AssetInfo]):
    if new_asset:
        asset_state[new_asset.name] = {"count": 0}
    elif old_asset and old_asset.name in asset_state:
        del asset_state[old_asset.name]
```

**State persistence**
- Use external storage (database, file) for persistence.
- Use Timeseries API to seed state on startup if needed.


## Logging
```python
from kelvin.logs import logger

@app.stream(inputs=["temperature"])
async def process_temperature(msg: AssetDataMessage):
    logger.info(
        "Processing Temperature",
        asset=msg.resource.asset,
        data_stream=msg.resource.data_stream,
        value=msg.payload,
        timestamp=msg.timestamp,
    )

logger.debug("Detailed debugging info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical failure")
```

## Security and secrets
- Do not hardcode credentials.
- Use secrets in `defaults.system.environment_vars`.
- Avoid logging secret values.
- Validate external inputs and third-party responses.

## Best practices and common pitfalls

### General Code Patterns
- Use decorator-based API (`@app.stream()`, `@app.timer()`, `@app.task`) by default unless explicitly requested to use function-based patterns.

### App.yaml Configuration
- Never create a `configuration:` declaration section in app.yaml. Only use `parameters:` for per-asset declarations and put values directly in `defaults.configuration` for global settings.
- Match parameter names exactly between app.yaml and ui_schemas files. Mismatched names will cause runtime errors when the UI tries to update parameters.
- Follow naming conventions strictly: lowercase-with-hyphens for app names, lowercase-with-underscores for stream/parameter names matching regex `^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$`.

### Data Window Processing
- Always specify the `inputs` parameter when using windows (tumbling, hopping, rolling). Without it, the DataFrame will contain unpredictable mixed data.
- Use input stream names as DataFrame column names, not 'payload' or 'value'. If your input is "temperature", access `df['temperature']`.
- Check `df.empty` before any DataFrame operations. Windows may be empty if no data arrived during the window period.
- Handle NaN values explicitly using `pd.isna()` or `pd.notna()` before calculations. DataFrame operations may return NaN even with non-empty DataFrames.
- Run window processing in `@app.task`, not in the main event loop. Window processing can block other handlers if not properly backgrounded.

### Message and Resource Handling
- Declare outputs in `app.yaml` before publishing.
- Use appropriate message types (do not send everything as Number).
- If a handler receives no messages, verify the input is declared in `app.yaml`.
- Access `msg.timestamp` directly as a datetime object, never parse it. The timestamp is already a timezone-aware datetime, not a string.
- Construct KRN resources correctly for each message type: `KRNAssetDataStream(asset, stream)` for data, `KRNAsset(asset)` for recommendations, `KRNAssetParameter(asset, param)` for parameters.
- Set appropriate expiration dates for all temporal messages. Use `timedelta` for relative times from publish, `datetime` for absolute times.
- Validate business logic only, not framework-provided values. The SDK guarantees `msg.resource.asset`, `msg.resource.data_stream`, and type-correct `msg.payload`.

### State Management and Concurrency
- Use `asyncio.Lock` when modifying shared state from stream handlers. Stream handlers run concurrently and can cause race conditions.
- Handle asset additions and removals in `on_asset_change` to maintain consistent state. Clean up state for removed assets to prevent memory leaks.
- Initialize asset-specific state lazily in handlers or explicitly in `on_asset_change`. Never assume assets exist before the first message arrives.

### Timeseries API Usage
- Do NOT declare streams in `data_streams.inputs` if only accessing via Timeseries API. Only declare inputs for real-time streaming subscriptions.
- Include required environment variables for Timeseries API access: `KELVIN_CLIENT__URL`, `KELVIN_CLIENT__CLIENT_ID`, and `KELVIN_CLIENT__CLIENT_SECRET` in `defaults.system.environment_vars`.
- Use Timeseries API only for historical data older than 12 hours. Use real-time windows for recent data.

### Error Handling and Async Patterns
- Remember `@app.task` does NOT catch exceptions by default, unlike `@app.stream()` and `@app.timer()`. Always wrap long-running task loops in try/except to prevent silent failures.

### Recommendations and Control Changes
- Use meaningful recommendation types for categorization.
- Include evidences in recommendations where possible. Prefer `DataExplorer` and `Markdown` evidences.
- Embed control changes and custom actions inside Recommendation messages unless explicitly requested otherwise. Standalone control changes bypass recommendation workflow.
- Always add `kelvin_closed_loop` boolean parameter (default false) when recommendations include actions. Use this to control `auto_accepted` field dynamically per asset.
- Provide `timeout` and `retries` for critical control changes. Default timeout is 60 seconds; use retries for unreliable connections.
- Only send ControlAck if your app declares `control_changes.inputs`. Apps that only publish control changes should not acknowledge them.
