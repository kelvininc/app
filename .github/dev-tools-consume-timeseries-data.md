```markdown
# dev-tools-consume-timeseries-data — depth-0 extract (Kelvin docs: Timeseries Data Messages)

Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/timeseries-data-messages/
Fetched: 2025-10-26 (offline extract stored in this repo)

Overview
This document is a self-contained depth-0 extract of the Kelvin docs covering how Kelvin SmartApps consume timeseries/asset data messages. It is intended to be an offline reference you can include in PRs or consult when editing `main.py` and `app.yaml`.

Key points
- Define the inputs your SmartApp will consume in `app.yaml.data_streams.inputs`. Kelvin will only deliver inputs listed there.
- Two primary consumption styles: asynchronous streams (async generators / queues) and callbacks.
- Use `filters` (e.g., `input_equals`, `resource_equals`, `asset_equals`) to limit which messages your handlers receive.
- Example consumption patterns: AsyncGenerator stream, asyncio Queue, and on_asset_input callback. All are shown below with copyable examples.

1) app.yaml: declare inputs
The `inputs` array is required for any timeseries data your app will receive. Each input has a unique name (lowercase, alphanumeric with .,_,- allowed inside) and a data_type (number, boolean, string).

Example `app.yaml` inputs snippet

```yaml
data_streams:
  inputs:
    - name: motor_temperature
      data_type: number
    - name: motor_state
      data_type: string
```

2) Filters
Use the `filters` helpers in the SDK to restrict which messages are delivered to a stream/queue/callback. Common filters:
- `filters.input_equals(input: str)` — match a named input
- `filters.resource_equals(resource: KRN)` — match a specific resource KRN
- `filters.asset_equals(asset: str)` — match messages from a specific asset

3) Consumption patterns — examples

a) Streams (AsyncGenerator) — filtered async generator

This pattern uses `app.stream_filter(...)` to create an async generator that yields messages only matching the filter. It is convenient when you want to `async for` over messages.

Python example (AsyncGenerator)

```python
import asyncio
from typing import AsyncGenerator
from kelvin.application import KelvinApp, filters
from kelvin.message import Number

async def main() -> None:
    app = KelvinApp()

    # Create a filtered async generator for the 'motor_temperature' Number input
    motor_temperature_msg_stream: AsyncGenerator[Number, None] = (
        app.stream_filter(filters.input_equals("motor_temperature"))
    )

    await app.connect()

    # Consume messages as they arrive
    async for motor_temperature_msg in motor_temperature_msg_stream:
        print("Received Motor Temperature:", motor_temperature_msg)

if __name__ == "__main__":
    asyncio.run(main())
```

b) Streams (asyncio.Queue) — filter -> queue pattern

This pattern uses `app.filter(...)` which returns an asyncio.Queue you can `await` on. Useful when you want explicit control over message retrieval.

Python example (Queue)

```python
import asyncio
from asyncio import Queue
from kelvin.application import KelvinApp, filters
from kelvin.message import Number

async def main() -> None:
    app = KelvinApp()

    # Create a filtered Queue for motor_temperature Number messages
    motor_temperature_msg_queue: Queue[Number] = app.filter(filters.input_equals("motor_temperature"))

    await app.connect()

    while True:
        # Wait for the next message from the queue
        motor_temperature_msg = await motor_temperature_msg_queue.get()
        print("Received Motor Temperature:", motor_temperature_msg)

if __name__ == "__main__":
    asyncio.run(main())
```

c) Callback handler — `on_asset_input`

The `on_asset_input` callback is invoked for every incoming asset data message. Set `app.on_asset_input` to your async callback function. This is useful for a central event-style handler.

Python example (Callback)

```python
import asyncio
from kelvin.application import KelvinApp
from kelvin.message.primitives import AssetDataMessage

async def on_asset_input(msg: AssetDataMessage):
    print("Received Data Message:", msg)
    # Example: extract asset and payload
    asset = msg.resource.asset
    value = msg.payload
    # process value

async def main() -> None:
    app = KelvinApp()
    app.on_asset_input = on_asset_input
    await app.connect()

    # Keep the app running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

4) Message types and payloads
- Messages delivered to SmartApps are typed. For numeric inputs use `Number` from `kelvin.message` (or the appropriate primitive). Callback handlers typically receive `AssetDataMessage` objects with `resource` and `payload` properties.

5) Filtering by resource or asset
You can filter streams by KRN resource (use `filters.resource_equals(KRN)`) or by asset name (use `filters.asset_equals(asset_name)`). This is useful when you want a handler to only process messages for a specific asset or datastream.

6) Notes and best practices
- Only inputs declared in `app.yaml` will be delivered — make sure all needed inputs are declared.
- Prefer non-blocking handlers; heavy computation should be offloaded to background tasks via `asyncio.create_task()`.
- Use filters to reduce unnecessary message handling and improve efficiency.
- Include small example test cases or unit tests for message handling logic where feasible (mock `KelvinApp` or wrap handlers in test harnesses).

Authoritative link
- Live docs: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/timeseries-data-messages/

Keep this file synchronized with any local code examples and `app.yaml` changes so reviewers can validate consumption logic offline.

```
