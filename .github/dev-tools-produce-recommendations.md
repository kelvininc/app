Title: Produce Recommendations — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/recommendation-messages/
Fetched: 2025-10-27

Detailed Summary :
Recommendations are higher-level messages that bundle suggested actions (for example ControlChanges), evidences (charts, images, markdown, iframes), and metadata for human review or automated workflows. A Recommendation targets a `resource` (usually a `KRNAsset`) and includes typed fields such as `type`, `control_changes` (list), `evidences` (list of evidence objects), `metadata` (free-form dict), and optional scheduling/expiration semantics. Recommendations may be published directly to the platform and displayed in the Kelvin UI where operators can review and action them.

Key examples :

1) Basic Recommendation with a single Control Change
```python
from datetime import timedelta
from kelvin.application import KelvinApp
from kelvin.message import ControlChange, Recommendation
from kelvin.krn import KRNAssetDataStream, KRNAsset

app = KelvinApp()

# Create a Control Change object
control_change = ControlChange(
    resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5),
)

# Create and publish a Recommendation that contains the control change
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change],
    )
)
```

2) Recommendation with multiple Control Changes
```python
# create multiple ControlChange objects (control_change_01, control_change_02, ...)
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change_01, control_change_02, control_change_03],
    )
)
```

3) Recommendation with ML metadata (model outputs, confidence, features)
```python
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change],
        metadata={
            "predicted_speed": 2.5,
            "confidence": 0.87,
            "input_features": {"current_speed": 5, "load": 4},
            "timestamp": "2024-11-18T12:00:00Z",
            "model_version": "1.2.0",
        },
    )
)
```

4) Recommendation with Evidences — Chart (HighCharts) example
```python
from kelvin.message.evidences import Chart
from kelvin.krn import KRNAsset
from datetime import datetime

evidences = [
    Chart(title="Sample Chart", timestamp=datetime.now(), /* chart payload here */)
]

await app.publish(
    Recommendation(
        resource=KRNAsset('pcp_51'),
        type='decrease_speed',
        control_changes=[control_change],
        evidences=evidences,
    )
)
```

5) Recommendation with Image evidence
```python
from kelvin.message.evidences import Image

evidences = [
    Image(title="My Image", description="desc", url="https://www.example.com/image.jpg")
]

await app.publish(Recommendation(resource=KRNAsset('pcp_51'), type='decrease_speed', evidences=evidences))
```

6) Recommendation with Markdown evidence
```python
from kelvin.message.evidences import Markdown

evidences = [
    Markdown(title="My Markdown", markdown="""
# Evidence 1
Lorem ipsum...
""")
]

await app.publish(Recommendation(resource=KRNAsset('pcp_51'), type='decrease_speed', evidences=evidences))
```

Notes:
- Recommendations can include unlimited evidence items; choose evidence types appropriate for the reviewer (charts, images, markdown, iframes).
- Images must be accessible (Kelvin file storage or public URL).
- Use `metadata` to include ML outputs, timestamps, model versions, and any data needed for auditing or automated scoring.
- Recommendations may encapsulate one or more ControlChange objects; consumers of Recommendations or UI workflows can present them for human approval or auto-action depending on app configuration.
- Test Recommendations locally using the Kelvin generator/test tools to validate UI display and action workflows.
- When adding Recommendation-related outputs or behaviors, ensure any `control_changes` referenced are declared in `app.yaml` and that `ui_schemas/*` and `defaults` are updated accordingly.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/recommendation-messages/

---

Depth‑0 extract intended for offline use by repository contributors and reviewers.
