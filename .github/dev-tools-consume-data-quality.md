Title: Consume Data Quality Messages — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/data-quality-messages/
Fetched: 2025-10-27

Detailed Summary :
Data Quality messages are produced by the Kelvin Data Quality Application when validations run against asset data streams. To receive Data Quality messages in your SmartApp you must enable Data Quality monitoring for the target data streams (usually in the Kelvin UI or via the Kelvin API). Data Quality outputs are declared in `app.yaml` under the `data_quality` key; the SmartApp then listens for messages emitted by the Data Quality app and can react in real time.

This extract covers:
- How to declare `data_quality` inputs in `app.yaml`.
- How to fetch Data Quality values and aggregations via the Kelvin Python API client (`kelvin.api.client.Client`).
- How to consume Data Quality messages at runtime using the Kelvin Python SDK (async streaming with `app.stream_filter(filters.is_data_quality_message)`).
- Important operational notes: enabling monitoring, non-blocking handlers, payload shapes and resource KRN types.

Key examples :

1) app.yaml: declare Data Quality inputs
```yaml
data_quality:
  inputs:
    - name: kelvin_data_availability
      data_type: number
      data_streams:
        - speed
        - temperature
        - tubing_pressure
    - name: kelvin_outlier_detection
      data_type: number
      data_streams:
        - speed
        - temperature
```

2) Get latest Data Quality score (Python) — Kelvin API Client
```python
from kelvin.api.client import Client

client = Client(config={"url": "https://<url.kelvin.ai>", "username": "<your_username>"})
client.login(password="<your_password>")

response = client.asset_insights.get_asset_insights(data={
    "asset_names": ["pcp_03"],
    "extra_fields": {
        "data_qualities": [
            {"data_quality_name": "kelvin_data_quality_score", "name": "quality_score"}
        ]
    }
})

print(f"The Data Quality Score is {response[0].extra_fields['quality_score']} and was last recorded on {response[0].last_seen.strftime('%d %b %Y %H:%M:%S')}")
```

3) Get aggregated Data Quality over a time range (Python)
```python
from kelvin.api.client import Client

client = Client(config={"url": "https://<url.kelvin.ai>", "username": "<your_username>"})
client.login(password="<your_password>")

response = client.asset_insights.get_asset_insights(data={
    "asset_names": ["pcp_03"],
    "extra_fields": {
        "data_qualities": [
            {
                "computation": {"agg": "mean", "start_time": "2025-10-12T12:00:00Z", "end_time": "2025-10-16T12:00:00Z"},
                "data_quality_name": "kelvin_data_quality_score",
                "name": "quality_score_mean"
            }
        ]
    }
})

print(f"The average Data Quality Score over the last four days is {response[0].extra_fields['quality_score_mean']}%")
```

4) Runtime consumption — async stream filter for Data Quality messages (Python)
```python
import asyncio
from typing import AsyncGenerator
from kelvin.application import KelvinApp, filters
from kelvin.message import Number

async def main() -> None:
    app = KelvinApp()
    await app.connect()

    data_quality_stream: AsyncGenerator[Number, None] = app.stream_filter(filters.is_data_quality_message)

    async for data_quality_msg in data_quality_stream:
        # data_quality_msg.resource will be a KRNAssetDataStreamDataQuality-like object
        print(f"Received Data Quality Message: {data_quality_msg}")

if __name__ == '__main__':
    asyncio.run(main())
```

Example runtime output (shortened)
```
Received PCP02 | Asset: resource=KRNAssetDataStreamDataQuality(asset='pcp_02', data_stream='speed', data_quality='kelvin_data_availability') payload=20
Received PCP02 | Asset: resource=KRNAssetDataStreamDataQuality(asset='pcp_02', data_stream='gas_flow_rate', data_quality='kelvin_data_availability') payload=66
```

Notes:
- Enable Data Quality monitoring for the desired data streams in the Kelvin UI (or via the Kelvin API). If monitoring is not enabled, no Data Quality outputs will be produced.
- Declare Data Quality inputs in `app.yaml` under the `data_quality` key; list the `data_streams` that the validator monitors.
- Use the Kelvin API Client (`kelvin.api.client.Client`) for one-off queries or aggregated views when you don't need real-time streaming.
- For realtime processing prefer `app.stream_filter(filters.is_data_quality_message)` and non-blocking processing (offload heavy work to background tasks).
- The data quality message `resource` is a KRN-style object including `asset`, `data_stream`, and the `data_quality` name — use these fields to correlate messages to assets and streams.
- Validate numeric payloads and consider guardrails/thresholds before triggering recommendations or control changes based on data quality scores.
- Mirror `data_quality` declarations in `ui_schemas/*` and `defaults` when changing `app.yaml` to keep repository consistency.
- Add unit/integration tests that either mock `KelvinApp` message delivery or use the Kelvin test generator to verify handlers react to Data Quality messages.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/data-quality-messages/

---

This file is a depth-0 offline extract intended for repository reviewers and contributors who do not have internet access.
