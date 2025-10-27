Title: Produce Timeseries Data — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/timeseries-data-messages/
Fetched: 2025-10-27

Detailed Summary :
This document explains how a Kelvin SmartApp publishes timeseries (asset / data stream) values to the Kelvin platform. To publish timeseries messages you must declare the output data streams in `app.yaml` under `data_streams.outputs`. The SDK exposes primitive message types (Number, Boolean, String, Object) and a general Message/primitive mechanism for complex payloads. Each published message includes a `resource` (typically a `KRNAssetDataStream`) and a `payload` matching the declared `data_type`.

Key concepts covered:
- Declare outputs in `app.yaml` (data stream names and types).
- Use `KRNAssetDataStream(asset, datastream)` as the `resource` to target an asset and data stream.
- Use typed message classes (`Number`, `Boolean`, `String`, or `Message`/object) and `app.publish(...)` to send values.
- For objects use Message with `KMessageTypeData(primitive='object', icd=<icd>)` and pass a dict payload.

Key examples :

1) app.yaml: declare output data streams
```yaml
data_streams:
  outputs:
    - name: motor_temperature_fahrenheit
      data_type: number
    - name: motor_error
      data_type: number
    - name: motor_error_description
      data_type: number
    - name: gps_data
      data_type: number
```

2) Create and publish a Number (Python)
```python
from kelvin.message import Number
from kelvin.krn import KRNAssetDataStream

# assume `app` is a connected KelvinApp and `asset` is set
await app.publish(
    Number(
        resource=KRNAssetDataStream(asset, "motor_temperature_fahrenheit"),
        payload=97.3,
    )
)
```

3) Create and publish a Boolean (Python)
```python
from kelvin.message import Boolean
from kelvin.krn import KRNAssetDataStream

await app.publish(
    Boolean(
        resource=KRNAssetDataStream(asset, "motor_error"),
        payload=True,
    )
)
```

4) Create and publish a String (Python)
```python
from kelvin.message import String
from kelvin.krn import KRNAssetDataStream

await app.publish(
    String(
        resource=KRNAssetDataStream(asset, "motor_error_description"),
        payload="Temperature is too high",
    )
)
```

5) Create and publish an Object (Python) — arbitrary dict payload
```python
from kelvin.message import Message, KMessageTypeData
from kelvin.krn import KRNAssetDataStream

gps_dict = {"latitude": 90, "longitude": 100}

await app.publish(
    Message(
        type=KMessageTypeData(primitive="object", icd="gps"),
        resource=KRNAssetDataStream(asset, datastream),
        payload=gps_dict,
    )
)
```

Notes:
- The Asset name must be associated with the SmartApp workload; writes to assets not associated with the workload will be dropped and an error recorded.
- Ensure `data_type` in `app.yaml` matches the Python payload types (number -> int/float, boolean -> bool, string -> str, object -> dict).
- The `resource` must be a valid KRN reference (use `KRNAssetDataStream` for asset+datastream targeting).
- Use `await app.publish(...)` in async code; `publish` returns when the local platform accepts the message.
- For object payloads include an `icd` if you want to indicate a schema/ICD for downstream consumers.
- Monitor logs for dropped writes or type mismatches; the platform will record errors for invalid targets or types.
- Add unit/integration tests that simulate publishing messages to ensure types and KRN resources match `app.yaml` declarations.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/timeseries-data-messages/

---

Depth‑0 extract intended for offline use by repository contributors and reviewers.
