# SDK Patterns Reference

## When to Use

Use this file to build app structure and runtime behavior: imports, lifecycle callbacks, stream decorators, timers, tasks, and error-handling patterns.

## Table of Contents
- [When to Use](#when-to-use)
- [Core Imports](#core-imports)
- [Lifecycle and Callbacks](#lifecycle-and-callbacks)
- [Extended Callbacks](#extended-callbacks)
- [Decorator-Based Streams](#decorator-based-streams)
- [Tasks and Timers](#tasks-and-timers)
- [Function-Based Pattern](#function-based-pattern)
- [Error Handling](#error-handling)
- [Framework Guarantees](#framework-guarantees)

## Core Imports

Use minimal imports per task. Add message/resource types only when needed.

```python
from kelvin.application import KelvinApp, filters
from kelvin.logs import logger
from kelvin.message import AssetDataMessage
from kelvin.krn import KRNAssetDataStream

app = KelvinApp()
client = app.api
```

For detailed message classes and payload examples, use [messages-outputs.md](messages-outputs.md).
For KRN constructors and parsing, use [krn.md](krn.md).

## Lifecycle and Callbacks

`app.run()` connects and blocks the current thread.
Use `await app.connect()` only when managing the event loop manually.

Startup order:
1. Connect to platform.
2. Load assets/parameters into `app.assets`.
3. Call `on_connect`.
4. Activate streams/timers/tasks.

```python
from typing import Optional
from kelvin.application import AssetInfo

async def on_connect() -> None:
    logger.info("Connected", assets=list(app.assets.keys()))

async def on_asset_change(new_asset: Optional[AssetInfo], old_asset: Optional[AssetInfo]) -> None:
    if new_asset is not None:
        logger.info("Asset added/updated", asset=new_asset.name)
    elif old_asset is not None:
        logger.info("Asset removed", asset=old_asset.name)

app.on_connect = on_connect
app.on_asset_change = on_asset_change
```

## Extended Callbacks

Use these callbacks when your app handles control workflows, custom actions, or runtime configuration updates.

```python
from kelvin.message import AssetDataMessage, ControlAck, ControlChangeStatus, CustomAction, StateEnum

async def on_asset_input(msg: AssetDataMessage) -> None:
    logger.info("Asset input", resource=str(msg.resource), payload=msg.payload)

async def on_control_change(msg: AssetDataMessage) -> None:
    logger.info("Control change received", resource=str(msg.resource), payload=msg.payload)
    ack = ControlAck(resource=msg.resource, state=StateEnum.applied, message="Applied successfully")
    await app.publish(ack)

async def on_control_status(status: ControlChangeStatus) -> None:
    logger.info("Control change status", status=status)

async def on_custom_action(action: CustomAction) -> None:
    logger.info("Custom action received", action=action)

async def on_app_configuration(conf: dict) -> None:
    logger.info("App configuration changed", config=conf)

app.on_asset_input = on_asset_input
app.on_control_change = on_control_change
app.on_control_status = on_control_status
app.on_custom_action = on_custom_action
app.on_app_configuration = on_app_configuration
```

## Decorator-Based Streams

Use decorators by default.

```python
@app.stream(assets=["asset-1"], inputs=["casing_pressure", "oil_rate"])
async def monitor(msg: AssetDataMessage) -> None:
    asset = msg.resource.asset
    stream = msg.resource.data_stream
    value = msg.payload

    logger.info("Stream message", asset=asset, stream=stream, value=value)

    if stream == "casing_pressure":
        max_pressure = float(app.assets[asset].parameters.get("max_casing_pressure", 1500.0))
        if value > max_pressure:
            logger.warning("Pressure limit exceeded", asset=asset, value=value, limit=max_pressure)
```

## Tasks and Timers

Use `@app.task` for background processing and window loops.
Use `@app.timer` for periodic checks.

```python
import asyncio

@app.task
async def continuous_check() -> None:
    try:
        while True:
            await asyncio.sleep(10)
            logger.info("Background check")
    except Exception as exc:
        logger.error("Task failed", error=str(exc), exc_info=True)

@app.timer(interval=30)
async def periodic_check() -> None:
    logger.info("Timer tick")
```

## Function-Based Pattern

Use only when explicitly requested.

```python
from kelvin.message import Number

async def process_stream(app: KelvinApp) -> None:
    stream = app.stream_filter(filters.input_equals(["temperature"]))
    async for msg in stream:
        await app.publish(
            Number(
                resource=KRNAssetDataStream(msg.resource.asset, "production_index"),
                payload=msg.payload * 2,
            )
        )
```

## Error Handling

| Decorator | Exceptions Handled? | Behavior |
|-----------|---------------------|----------|
| `@app.stream()` | YES | Next message still calls handler |
| `@app.timer()` | YES | Timer continues firing |
| `@app.task` | NO | Task stops if exception escapes |

Wrap long-running `@app.task` loops in `try/except`.

## Framework Guarantees

Assume:
- `msg.resource.asset` is non-null and present in `app.assets`.
- `msg.resource.data_stream` is non-null.
- `msg.payload` type matches `app.yaml` declarations.

Validate business logic (thresholds, ranges, state transitions), not framework invariants.
