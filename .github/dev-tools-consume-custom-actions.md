Title: Consume Custom Actions — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/custom-actions/
Fetched: 2025-10-27

Detailed Summary:
Custom Actions let one Kelvin SmartApp (the Publisher) ask another SmartApp (the Executor / Consumer) to perform arbitrary application-level work. Custom Actions are routed by a string "type" declared by the publisher and a matching input declared by the consumer. Important platform rules:

- The consumer must declare the Custom Action `type` it will accept in its `app.yaml` under `custom_actions.inputs`.
- For each Custom Action `type`, only one Consumer Application (Executor) may be deployed to receive that type on a given Kelvin platform — multiple consumers with identical type are not supported.
- Custom Actions carry a `resource` (KRNAsset), a `payload` object with arbitrary custom data required by the consumer, and metadata such as `expiration_date` and optional `trace_id` for tracking.

This document provides the essential examples (app.yaml and Python) and notes so the repo maintainer can implement or review Custom Action handlers offline.

Key examples:

1) app.yaml: declare a Custom Action input (consumer / executor)
```yaml
custom_actions:
  inputs:
    - type: email
```

2) Attributes of the CustomAction object (summary)
- resource (required): The `KRNAsset` that this Custom Action is meant for.
- type (required): Name of the Custom Action (string).
- title (required): Human-friendly title.
- description (required): Description of what the action does.
- expiration_date (required): Absolute datetime or timedelta when the action expires.
- payload (required): Arbitrary JSON/object containing action parameters.
- trace_id (optional): Custom id for tracking the action status.

3) Attributes of the CustomActionResult (summary)
- success (required): Boolean indicating success or failure.
- message (optional): Optional human-readable message.
- metadata (optional): Additional metadata to return to the publisher.
- action_id (optional): ID of the Custom Action object being reported on.
- resource (optional): KRNAsset associated with the result.

4) Consumer (Executor) `main.py` example — receive, act, respond
```python
import asyncio
from kelvin.application import KelvinApp
from kelvin.message import CustomAction, CustomActionResult

app = None

async def send_mail(recipient, subject, body):
    # Placeholder for real SMTP/email sending logic
    print(f"Sending email to {recipient}")
    # e.g., use aiosmtplib or another async email client here

async def on_custom_action(action: CustomAction) -> None:
    # Only react to types this consumer handles
    if action.type == "email":
        try:
            await send_mail(
                action.payload.get("recipient"),
                action.payload.get("subject"),
                action.payload.get("body"),
            )
            # Publish a CustomActionResult back to the platform to inform the publisher
            await app.publish(
                CustomActionResult(
                    success=True,
                    action_id=action._msg.id,
                    resource=action.resource,
                    metadata={},
                )
            )
        except Exception as e:
            # If the action fails, publish a failed result
            await app.publish(
                CustomActionResult(
                    success=False,
                    action_id=action._msg.id,
                    message=str(e),
                    resource=action.resource,
                )
            )

async def main() -> None:
    global app
    app = KelvinApp()
    app.on_custom_action = on_custom_action
    await app.connect()
    # Keep the app running; the platform will call on_custom_action
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

Notes:
- Declare the `custom_actions.inputs` types in `app.yaml` for any consumer application.
- Ensure the action `type` is globally unique per cluster — only one executor per type is allowed; choose type names carefully (prefix with your org or app name to avoid collisions).
- Keep handlers non-blocking: do minimal work in the callback and offload heavier tasks via `asyncio.create_task` or background workers.
- Validate `payload` contents strictly; the publisher and consumer must agree on the payload schema and units.
- Publish `CustomActionResult` objects to report success/failure back to the producer; include `action_id` to correlate results.
- Consider security and safety: Custom Actions may trigger side effects (emails, actuations). Add guardrails, permission checks, and review processes before enabling production publishers that trigger actions.
- Add unit/integration tests: simulate publishing a CustomAction and assert the executor publishes the correct `CustomActionResult`.
- When editing `app.yaml`, update `ui_schemas/*` and `defaults` to keep the repository consistent.

Authoritative link
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/custom-actions/

---

This file is a depth-0 offline extract intended for repository reviewers and contributors who do not have internet access.
