Title: Produce Data Tags — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/data-tag-messages/
Fetched: 2025-10-27

Detailed Summary :
Data Tags provide a way for SmartApps to label points or ranges in asset time series with semantic tags. Tags are useful for ML training datasets, operational annotations, and historical event tracking. Data Tags appear in the Kelvin UI Data Explorer and can be created programmatically by publishing a `DataTag` message. A DataTag carries a time range (`start_date`, optional `end_date`), a `tag_name`, the target `resource` (KRN asset), an optional human `description`, and optional `contexts` (other KRN resources such as datastreams or apps).

Key examples :

1) Create and publish a DataTag (Python)
```python
from datetime import datetime, timedelta
from kelvin.application import KelvinApp
from kelvin.message import DataTag
from kelvin.krn import KRNAsset, KRNDatastream, KRNApp

app = KelvinApp()

now = datetime.now()
datatag_duration_secs = 60

await app.publish(
    DataTag(
        start_date=now - timedelta(seconds=datatag_duration_secs),
        end_date=now,
        tag_name="My Tag",
        resource=KRNAsset("my_asset"),
        contexts=[KRNApp("app_name"), KRNDatastream("my_datastream")],
    )
)
```

Notes:
- `start_date` is required and must be RFC3339/UTC-formatted (use timezone-aware datetimes). `end_date` is optional for point tags.
- `tag_name` serves as the categorical label — choose stable names and consider namespacing to avoid collisions.
- `resource` must be a valid KRN (e.g., `krn:asset:my_asset`) and the asset should be associated with the SmartApp workload; writes to unrelated assets may be dropped or logged as errors.
- `contexts` is optional and can include other KRN references (e.g., `KRNDatastream`) to provide richer linkage for the tag.
- Use tags for ML training, auditing, and operational annotations — ensure producers and consumers agree on tag semantics and naming.
- Add tests that publish DataTag objects (or use the Kelvin test generator) and assert that they appear in the Data Explorer or downstream consumers as expected.
- Mirror any UI-exposed configuration (if you add tag-related parameters) in `ui_schemas/*` and `defaults` per repo contract.

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/data-tag-messages/

---

Depth‑0 extract intended for offline use by repository contributors and reviewers.
