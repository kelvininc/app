Title: Produce Custom Actions — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/custom-actions/
Fetched: 2025-10-27

Detailed Summary :
Custom Actions allow a Publisher SmartApp to request arbitrary work from a Consumer (Executor) SmartApp. Publishers declare the Custom Action "type" in `app.yaml` under `custom_actions.outputs`. Custom Actions carry attributes such as `resource` (a `KRNAsset`), `type` (string key), `title`, `description`, `expiration_date`, `payload` (arbitrary JSON/dict), and optional `trace_id` for tracking. A Custom Action can be sent directly to an Executor or embedded inside a Recommendation for review/approval via the Kelvin UI.

Key examples :

1) app.yaml: declare Custom Action output (publisher)
```yaml
custom_actions:
  outputs:
    - type: email
```

2) Publisher `main.py` — create and publish a CustomAction directly or inside a Recommendation
```python
import asyncio
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset
from kelvin.message import Recommendation, CustomAction

asset = KRNAsset("air-conditioner-1")
app = KelvinApp()

async def main() -> None:
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

    # Send directly to the Executor
    await app.publish(action)

    # Or embed into a Recommendation for review/approval in the UI
    rec = Recommendation(resource=asset, type="Reduce speed", actions=[action])
    await app.publish(rec)

if __name__ == "__main__":
    asyncio.run(main())
```

Notes:
- Declare publisher-side Custom Action `type`s in `app.yaml.custom_actions.outputs`. Consumer (executor) apps declare `custom_actions.inputs` for types they accept.
- The `type` string is how the platform routes Custom Actions to the correct Executor; choose names to avoid collisions (consider namespacing).
- Only one Consumer Executor per `type` is supported on a given platform — do not deploy multiple consumers for the same `type`.
- Use `payload` as an arbitrary dict agreed between publisher and consumer; validate payload shape before acting on it.
- `expiration_date` controls action validity. Track and handle expired actions appropriately on the Executor side.
- Consider putting Custom Actions into Recommendations when human review or approval is required rather than sending them directly.
- Use `trace_id` to correlate requests and results when needed.
- Add unit/integration tests: simulate publishing a CustomAction and validate the Executor receives and responds (use the Kelvin test generator for local testing).
- When editing `app.yaml`, mirror updates in `ui_schemas/*` and `defaults` to keep repository consistency.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/custom-actions/

---

Depth‑0 extract intended for offline use by repository contributors and reviewers.
