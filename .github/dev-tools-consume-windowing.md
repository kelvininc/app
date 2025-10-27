Title: Consume Windowing — Kelvin SDK (v6.3) — Depth-0 extract
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/windowing/
Fetched: 2025-10-27

Detailed Summary :
The Kelvin SDK includes built-in windowing primitives to process timeseries data in grouped frames. Windowing supports three primary patterns: Tumbling (fixed, non-overlapping time windows), Hopping (fixed-size, overlapping time windows with a hop interval), and Rolling (count-based windows moving by one observation). Windows are ordered by timestamp; the SDK handles out-of-order and late-arriving data according to window semantics. Windows produce pandas DataFrames keyed by timestamp and can be filtered by data streams and assets. The SDK provides helpers such as `tumbling_window`, `hopping_window`, and `rolling_window` that yield (asset_name, DataFrame) pairs for each window.

Key examples :

1) Basic tumbling window (5-minute windows)
```python
from datetime import timedelta
from kelvin.application import KelvinApp

app = KelvinApp()
await app.connect()

# Streaming data in 5-minute tumbling windows for all datastreams and assets
async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5)).stream():
    print(asset_name, df)
```

2) Filtered tumbling window (specific datastreams)
```python
async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5), datastreams=['temperature','pressure']).stream():
    print(asset_name, df)
```

3) Time-aligned tumbling window (round_to alignment)
```python
async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5), round_to=timedelta(minutes=1)).stream():
    print(asset_name, df)
```

4) Hopping window (5-minute windows with 2-minute hop)
```python
async for asset_name, df in app.hopping_window(window_size=timedelta(minutes=5), hop_size=timedelta(minutes=2)).stream():
    print(asset_name, df)
```

5) Rolling window (count-based)
```python
async for asset_name, df in app.rolling_window(count_size=5).stream():
    print(asset_name, df)
```

Notes:
- Windows are ordered by timestamp; ensure timestamps are present and consistent in incoming messages.
- Time windows include the start and exclude the end (e.g., [start, end)). This prevents duplication of messages across adjacent windows.
- Lateness and out-of-order events: Kelvin will place events into windows by timestamp. Late events may be included in open windows per platform policy or ignored if outside allowed lateness.
- Use `round_to` to align timestamps to a consistent grid (seconds/minutes/hours) which helps ensure DataFrame rows align across assets and streams.
- Specify `datastreams` and/or `assets` to narrow processing scope and control DataFrame column ordering.
- Rolling windows use a fixed number of messages (count_size) instead of time; useful for smoothing and moving-average calculations.
- DataFrames returned by window streams are timestamp-indexed and contain monotonic increasing timestamps in the index.
- Offload heavy post-processing (model inference, network calls) from the window loop using `asyncio.create_task` to avoid blocking the streaming loop.
- Add unit tests that simulate windowed messages or use the Kelvin test generator to validate window behavior (alignment, late data handling, and correct grouping).

Authoritative link:
https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/consume/windowing/

---

Depth‑0 extract intended for offline use by repository contributors and code reviewers.
