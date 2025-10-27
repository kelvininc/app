Title: Produce Control Changes — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/control-change-messages/
Fetched: 2025-10-27

Detailed Summary :
Control Changes are a special output message type used to write values to Assets in a fault-tolerant way. Unlike ordinary timeseries outputs, Control Changes include delivery guarantees, retries, timeouts, and expiration semantics. Producers must declare control change outputs in `app.yaml` under the `control_changes.outputs` key (do not declare them under `data_streams.outputs`). Each Control Change references a `resource` (a `KRNAssetDataStream`) and supports attributes such as `payload`, `expiration_date`, `retries`, `timeout`, `from_value`, and an optional `control_change_id`.

Key examples :

1) app.yaml: declare Control Change outputs
```yaml
control_changes:
  outputs:
    - name: motor_speed_set_point
      data_type: number
```

2) Basic publish Control Change (Python)
```python
import asyncio
from datetime import timedelta
from kelvin.application import KelvinApp
from kelvin.message import ControlChange
from kelvin.krn import KRNAssetDataStream

async def main() -> None:
    app = KelvinApp()
    await app.connect()

    await app.publish(
        ControlChange(
            resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
            payload=1000,
            expiration_date=timedelta(minutes=5),
        )
    )

if __name__ == "__main__":
    asyncio.run(main())
```

3) Publish Control Change including current (`from_value`) for context
```python
await app.publish(
    ControlChange(
        resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
        from_value={"value": last_value, "timestamp": datetime.now(timezone.utc)},
        payload=1000,
        expiration_date=timedelta(minutes=5),
    )
)
```

4) Publish Control Change with retries and timeout
```python
await app.publish(
    ControlChange(
        resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
        payload=1000,
        expiration_date=timedelta(minutes=10),
        retries=3,    # number of additional attempts
        timeout=60,   # seconds between retries
    )
)
```

Notes:
- Do NOT declare control change outputs under `data_streams.outputs`; use `control_changes.outputs` in `app.yaml`.
- Control Changes can operate in offline edge scenarios when both producer and consumer are on the same cluster; local delivery is supported.
- `expiration_date` defines when the Control Change will no longer be attempted; if not applied by then, it's marked failed.
- `retries` and `timeout` control retry behavior; set these thoughtfully for devices with intermittent connectivity.
- `from_value` is useful for UI/UX and auditing so reviewers can see the initial value before an attempted change.
- Validate that the `resource` KRN (asset + data stream) exists and is associated with your SmartApp workload — writes to unknown assets are dropped and logged as errors.
- Use unit/integration tests and the Kelvin test generator to simulate control change publish/consume workflows and edge-case failures.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/control-change-messages/

---

Depth‑0 extract intended for offline use by repository contributors and reviewers.
