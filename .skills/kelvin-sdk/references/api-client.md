# Kelvin API Client Reference

## When to Use

Use this file to implement reads/writes through `app.api` (apps, workloads, control changes, custom actions, recommendations, data tags, and timeseries queries).

## Table of Contents
- [When to Use](#when-to-use)
- [Client Setup](#client-setup)
- [Pagination](#pagination)
- [Apps](#apps)
- [App Parameters](#app-parameters)
- [App Workloads](#app-workloads)
- [Control Changes](#control-changes)
- [Custom Actions](#custom-actions)
- [Data Tags](#data-tags)
- [Recommendations](#recommendations)
- [Timeseries](#timeseries)

## Client Setup

Use `app.api` inside a SmartApp.

```python
client = app.api
```

Use these KRN examples in filters:
- Asset: `krn:asset:bp_16`
- Asset/DataStream: `krn:ad:bp_02/motor_speed`
- User: `krn:user:person@kelvin.ai`
- App: `krn:app:motor_speed_control`
- Workload app version: `krn:wlappv:cluster1/workload1:app1/1.2.0`

For KRN construction/parsing, use [krn.md](krn.md).

## Pagination

Use these pagination arguments on most list methods:
- `pagination_type`: `"limits" | "cursor" | "stream"` (`"stream"` returns all results)
- `page_size`: `int` (1-10000, default 10000)
- `page`: `int` for `"limits"`
- `next` / `previous`: `str` for `"cursor"`
- `direction`: `"asc" | "desc"`
- `sort_by`: `list[str]`

Use `pagination_type="stream"` unless you need paged UI behavior.

## Apps

Use these methods:
- `app.api.apps.list_apps(...)`
- `app.api.apps.get_app(app_name=...)`
- `app.api.apps.get_app_version(app_name=..., app_version=...)`
- `app.api.apps.list_apps_context(data=...)`

```python
apps = await app.api.apps.list_apps(
    app_names=["my-app"],
    app_types=["smartapp"],
    resources=["krn:asset:bp_16"],
    search=["motor"],
    pagination_type="stream",
)

app_details = await app.api.apps.get_app(app_name="my-app")
app_version = await app.api.apps.get_app_version(app_name="my-app", app_version="1.0.0")
```

Response fields (`AppShort`):
- `name`: str
- `title`: str
- `description`: str
- `category`: str | None
- `type`: AppType
- `dashboard_uid`: str | None
- `latest_version`: str | None
- `status`: `running` | `stopped` | `updating` | `requires_attention` | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

Response fields (`App`):
- `name`: str
- `title`: str
- `description`: str
- `category`: str | None
- `type`: AppType
- `dashboard_uid`: str | None
- `latest_version`: str | None
- `versions`: list[AppVersionOnly] | None
- `deployment`: Deployment | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

Response fields (`AppVersion`):
- `name`: str
- `title`: str
- `description`: str
- `category`: str | None
- `type`: AppType
- `version`: str
- `flags`: Flags | None
- `io`: list[AppIO] | None
- `dynamic_io`: list[DynamicAppIO] | None
- `parameters`: list[Parameter] | None
- `custom_actions`: list[CustomAction] | None
- `data_quality`: list[CustomDataQuality] | None
- `schemas`: Schemas | None
- `defaults`: Defaults | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

Response fields (`AppsResourceContext`):
- `resource`: str | None
- `source`: str | None

## App Parameters

Use this method:
- `app.api.app_parameters.list_app_parameters(data=...)`

```python
params = await app.api.app_parameters.list_app_parameters(
    data={
        "app_names": ["my-app"],
        "names": ["max_casing_pressure"],
        "data_types": ["number"],
        "search": ["pressure"],
    },
    pagination_type="stream",
)
```

Response fields (`AppParameter`):
- `app_name`: str | None
- `title`: str | None
- `name`: str | None
- `data_type`: `number` | `string` | `boolean` | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

## App Workloads

Use these methods:
- `app.api.app_workloads.list_workloads(...)`
- `app.api.app_workloads.get_workload(workload_name=...)`

```python
workloads = await app.api.app_workloads.list_workloads(
    app_names=["my-app"],
    statuses=["running"],
    resources="krn:asset:bp_16",
    pagination_type="stream",
)

workload = await app.api.app_workloads.get_workload(workload_name="my-workload")
```

Workload status enums:
- `status`: `pending_deploy` | `running` | `stopped` | `failed` | ...
- `download_status`: `pending` | `scheduled` | `processing` | `downloading` | `ready` | `failed`

Response fields (`WorkloadSummary`):
- `name`: str | None
- `title`: str | None
- `app_name`: str | None
- `app_version`: str | None
- `app_type`: AppType | None
- `cluster_name`: str | None
- `node_name`: str | None
- `download_status`: `pending` | `scheduled` | `processing` | `downloading` | `ready` | `failed` | None
- `download_error`: str | None
- `status`: WorkloadStatus | None
- `staged`: WorkloadStagedSummary | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

Response fields (`Workload`):
- `name`: str | None
- `title`: str | None
- `app_name`: str | None
- `app_version`: str | None
- `app_type`: AppType | None
- `cluster_name`: str | None
- `node_name`: str | None
- `download_status`: WorkloadDownloadStatus | None
- `download_error`: str | None
- `status`: WorkloadStatus | None
- `runtime`: WorkloadRuntime | None
- `system`: System | None
- `staged`: WorkloadStaged | None
- `created_at`: datetime | None
- `created_by`: str | None
- `updated_at`: datetime | None
- `updated_by`: str | None

## Control Changes

Use these methods:
- `app.api.control_change.get_control_change_last(data=...)`
- `app.api.control_change.get_control_change_range(data=...)`
- `app.api.control_change.list_control_changes(data=...)`
- `app.api.control_change.get_control_change(control_change_id=...)`

```python
last_cc = await app.api.control_change.get_control_change_last(
    data={
        "resources": ["krn:ad:bp_02/motor_speed_set_point"],
        "sources": ["krn:app:motor_speed_control"],
        "states": ["applied", "sent"],
    },
    pagination_type="stream",
)

cc_range = await app.api.control_change.get_control_change_range(
    data={
        "start_date": "2024-01-01T00:00:00Z",
        "end_date": "2024-12-31T00:00:00Z",
        "resources": ["krn:ad:bp_02/motor_speed_set_point"],
    },
    pagination_type="stream",
)
```

Control change states:
- `pending` | `ready` | `sent` | `processed` | `applied` | `failed` | `rejected`

Response fields (`ControlChangeGet`):
- `id`: UUID
- `resource`: str
- `payload`: int | float | str | bool | dict[str, Any] | None
- `created`: datetime | None
- `created_by`: str | None
- `created_type`: str | None
- `trace_id`: str | None
- `last_message`: str | None
- `last_state`: `pending` | `ready` | `sent` | `processed` | `applied` | `failed` | `rejected` | None
- `retries`: int | None
- `timeout`: int | None
- `expiration_date`: datetime | None
- `from`: ControlChangeFrom | None
- `reported`: ControlChangeReported | None
- `status_log`: list[ControlChangeGetStatus] | None
- `timestamp`: datetime | None
- `updated`: datetime | None

## Custom Actions

Use these methods:
- `app.api.custom_actions.list_custom_actions(data=...)`
- `app.api.custom_actions.get_custom_action(action_id=...)`

```python
actions = await app.api.custom_actions.list_custom_actions(
    data={
        "resources": ["krn:asset:bp_16"],
        "states": ["pending", "completed"],
        "types": ["email"],
    },
    pagination_type="stream",
)

action = await app.api.custom_actions.get_custom_action(
    action_id="0002bc79-b42f-461b-95d6-cf0a28ba87aa"
)
```

Custom action states:
- `pending` | `ready` | `in_progress` | `completed` | `cancelled` | `failed`

Response fields (`CustomAction`):
- `id`: UUID
- `type`: str
- `type_title`: str | None
- `resource`: str
- `title`: str
- `description`: str | None
- `expiration_date`: datetime
- `payload`: dict[str, Any] | None
- `trace_id`: str | None
- `state`: `pending` | `ready` | `in_progress` | `completed` | `cancelled` | `failed`
- `failure_reason`: str | None
- `message`: str | None
- `status_logs`: list[StatusLog] | None
- `timestamp`: datetime | None
- `created`: datetime
- `created_by`: str
- `updated`: datetime
- `updated_by`: str

## Data Tags

Use these methods:
- `app.api.data_tag.list_data_tag(data=...)`
- `app.api.data_tag.get_data_tag(datatag_id=...)`

```python
tags = await app.api.data_tag.list_data_tag(
    data={
        "tag_names": ["Breakdown", "Valve Change"],
        "resources": ["krn:asset:bp_16"],
        "start_date": "2024-01-01T00:00:00Z",
        "end_date": "2024-12-31T00:00:00Z",
    },
    pagination_type="stream",
)

tag = await app.api.data_tag.get_data_tag(
    datatag_id="0002bc79-b42f-461b-95d6-cf0a28ba87aa"
)
```

Response fields (`DataTag`):
- `id`: UUID | None
- `start_date`: datetime | None
- `end_date`: datetime | None
- `tag_name`: str | None
- `resource`: str | None
- `source`: str | None
- `description`: str | None
- `contexts`: list[str] | None
- `created`: datetime | None
- `updated`: datetime | None

## Recommendations

Use these methods:
- `app.api.recommendation.get_recommendation_last(data=...)`
- `app.api.recommendation.get_recommendation_range(data=...)`
- `app.api.recommendation.list_recommendations(data=...)`
- `app.api.recommendation.get_recommendation(recommendation_id=...)`

```python
last_recs = await app.api.recommendation.get_recommendation_last(
    data={
        "resources": ["krn:asset:bp_16"],
        "states": ["pending", "accepted"],
        "types": ["decrease_speed"],
    },
    pagination_type="stream",
)

recs = await app.api.recommendation.list_recommendations(
    data={
        "resources": ["krn:asset:bp_16"],
        "states": ["pending", "accepted"],
    },
    pagination_type="stream",
)
```

Recommendation states:
- `pending` | `accepted` | `auto_accepted` | `rejected` | `expired`

Response fields (`Recommendation`):
- `id`: UUID | None
- `type`: str
- `type_title`: str | None
- `resource`: str
- `description`: str | None
- `confidence`: int | None
- `custom_identifier`: str | None
- `expiration_date`: datetime | None
- `metadata`: dict[str, Any] | None
- `resource_parameters`: dict[str, Any] | None
- `trace_id`: str | None
- `evidences`: list[RecommendationEvidence] | None
- `actions`: RecommendationActions | None
- `message`: str | None
- `state`: `pending` | `accepted` | `auto_accepted` | `rejected` | `expired` | None
- `created`: datetime | None
- `source`: str | None
- `updated`: datetime | None
- `updated_by`: str | None

## Timeseries

Use Timeseries API for historical data queries.

Apply these rules:
- Do not declare Timeseries-only streams in `data_streams.inputs`.
- Keep real-time logic in stream handlers/windows.
- Use `get_timeseries_last` for current snapshot and `get_timeseries_range` for time intervals.

```python
last = await app.api.timeseries.get_timeseries_last(
    data={
        "selectors": [
            {"resource": "krn:ad:bp_02/motor_speed", "fields": ["value", "quality"]}
        ]
    }
)

series = await app.api.timeseries.get_timeseries_range(
    data={
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-12-31T00:00:00Z",
        "selectors": [{"resource": "krn:ad:bp_02/motor_speed", "fields": ["value"]}],
        "agg": "mean",
        "time_bucket": "1h",
        "fill": "none",
        "order": "ASC",
        "group_by_selector": True,
    }
)
```

Response fields (`TimeseriesLastGet`):
- `resource`: str | None
- `source`: str | None
- `data_type`: str | None
- `fields`: list[str] | None
- `last_value`: int | float | str | bool | dict[str, Any] | None
- `last_timestamp`: datetime | None
- `created`: datetime | None
- `updated`: datetime | None

Response fields (`TimeseriesRangeGet`):
- `resource`: str | None
- `timestamp`: datetime | None
- `payload`: int | float | str | bool | dict[str, Any] | None

DataFrame conversion pattern:

```python
from datetime import datetime, timedelta

result = await app.api.timeseries.get_timeseries_range(
    data={
        "start_time": datetime.now().astimezone() - timedelta(days=7),
        "end_time": datetime.now().astimezone(),
        "agg": "mean",
        "time_bucket": "30s",
        "selectors": [
            {"resource": f"krn:ad:{asset_name}/gas_rate"},
            {"resource": f"krn:ad:{asset_name}/casing_pressure"},
        ],
        "order": "ASC",
        "fill": "none",
    }
)

df = result.to_df(datastreams_as_column=True)
```

For window-first real-time patterns, use [data-processing.md](data-processing.md).
