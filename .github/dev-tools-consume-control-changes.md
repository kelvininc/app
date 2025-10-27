Title: Consume Control Changes — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/control-changes-messages/
Fetched: 2025-10-26

Summary
This short, offline reference explains how to produce and consume Control Change objects between Kelvin SmartApps (app-to-app) and connectors. It includes minimal, copyable examples for declaring control changes in `app.yaml`, producing ControlChange messages, consuming them via callbacks, and inspecting control change status events. Use this document when implementing app-to-app actuations or connector-driven control flows.

Key examples

1) app.yaml: declare Control Change outputs (producer)
```yaml
control_changes:
  outputs:
    - name: motor_speed_set_point
      data_type: number
```

2) app.yaml: declare Control Change inputs (consumer)
```yaml
control_changes:
  inputs:
    - name: motor_speed_set_point
      data_type: number
```

3) Produce a Control Change (Python) — create & publish
```python
from datetime import timedelta
from kelvin.application import KelvinApp
from kelvin.message import ControlChange
from kelvin.krn import KRNAssetDataStream

app = KelvinApp()

# resource: KRN reference to asset + data stream (must match consumer app.yaml)
resource = KRNAssetDataStream("my-motor-asset", "motor_speed_set_point")

async def produce_control_change():
    await app.connect()
    ctrl = ControlChange(
        resource=resource,
        payload=1000,                      # must match declared data_type (number)
        expiration_date=timedelta(minutes=5)  # optional TTL
    )
    await app.publish(ctrl)
    # app.publish returns once the local platform accepts the message
```

4) Consume a Control Change (callback-style) — Python
```python
from kelvin.application import KelvinApp
from kelvin.message.primitives import AssetDataMessage

app = KelvinApp()

async def on_control_change(msg: AssetDataMessage) -> None:
    # msg.resource is a KRNAssetDataStream-like object
    asset = msg.resource.asset
    value = msg.payload
    print(f"Received Control Change from asset {asset}: {value}")
    # validate type and quick-processing only; offload heavy work
    # e.g., asyncio.create_task(handle_heavy_processing(msg))

# register the event callback
app.on_control_change = on_control_change

import asyncio
async def main():
    await app.connect()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

5) Control Change Status events — check delivery / state (Python)
```python
from kelvin.message import ControlChangeStatus

async def on_control_status(status: ControlChangeStatus) -> None:
    print("Control change status:", status)
    # status may include fields like id, timestamp, state, reason

app.on_control_status = on_control_status
```

Notes about resources & KRN
- Use `KRNAssetDataStream(asset, data_stream)` on the producer side to reference the exact asset and data stream the consumer has declared in `app.yaml`.
- Ensure `data_type` in `app.yaml` matches the Python payload type (number -> int/float, boolean -> bool, string -> str).

Notes for repo authors / reviewers
- Ensure the producing SmartApp declares the control change under `control_changes.outputs` and the consuming SmartApp declares the same name under `control_changes.inputs` in their respective `app.yaml`.
- App-to-app control changes require apps to be on the same Kelvin Cluster (can work offline/local between apps on same cluster).
- For connectors: control change inputs are often auto-declared by connector setup — confirm connector config when applicable.
- Keep handler functions non-blocking: do minimal work in the callback and offload long-running tasks with `asyncio.create_task`.
- Validate payload types and consider guardrails around acceptance: confirm ranges and units where applicable; control changes may drive actuators and require review.
- Include small unit/integration tests that simulate a ControlChange publish and assert the consumer callback received the message (see Kelvin test generator / generator tool).
- When editing `app.yaml`, mirror changes in `ui_schemas/*` and `defaults` per the repository contract.

Authoritative link
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/control-changes-messages/

---

File generated as a standalone depth-0 extract for offline review. If you want the full page prose included, re-run with INCLUDE_FULL_PAGE=true.
