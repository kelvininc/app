## Quick context for code agents

This repo is a Kelvin SmartApp that streams asset data, computes simple data-quality and safety checks, and issues Recommendations/ControlChanges via the Kelvin Python SDK.

Key files to read first:
- `app.yaml` — canonical app configuration: spec_version, data_streams (inputs/outputs), parameters and ui_schemas.
- `main.py` — entrypoint and primary application logic; shows streaming patterns using `KelvinApp`, `app.connect()`, and `app.stream_filter(...)`.
- `ui_schemas/parameters.json` — parameter shapes and validation used per-asset.
- `requirements.txt` — external dependency: `kelvin-python-sdk[ai]`.
- `Dockerfile` — how the image is built and that the container runs `python main.py`.

Primary patterns and conventions
- The app uses KelvinApp from `kelvin.application`. Connect with `await app.connect()` and then use `async for message in app.stream_filter(filters.is_asset_data_message)` to consume messages.
- Resource identifiers use KRN helpers (e.g. `KRNAsset`, `KRNAssetDataStream`) — prefer these to hand-built strings.
- Publish Recommendations and ControlChanges via `app.publish(...)`. See `main.py` for a Recommendation example with evidences (Markdown, Image).
- Configuration is driven by `app.yaml` and per-asset parameters; UI schema files in `ui_schemas/` describe validation/fields.

How to run and common developer commands
- Run locally: `python main.py` (entrypoint defined in `main.py`).
- Build image: `docker build -t kelvin-app .` then `docker run --rm kelvin-app`.
- Upload to Kelvin from your environment: `kelvin auth login <instance>.kelvin.ai` then `kelvin app upload` (see README for context).

What to look for when changing code
- If you change data streams or outputs, also update `app.yaml` and the `ui_schemas`/parameters if needed.
- When adding new message handling, add a focused `stream_filter(...)` and keep handlers small and testable.
- Avoid blocking the async stream loop; use `asyncio.create_task()` for background work and keep the stream consumer responsive.

Integration points and external dependencies
- Kelvin platform SDK: `kelvin-python-sdk[ai]` (installed via `requirements.txt`). Side effects and publishing are performed through SDK objects.
- The runtime expects network access to Kelvin; local runs require valid Kelvin credentials for upload/publish tests.

Examples from this repo
- Data streams: `app.yaml` declares `data_streams.inputs` like `speed` and `casing_pressure` and an output `motor_speed_set_point`.
- Message handling: `main.py` demonstrates `filters.is_asset_data_message` and builds a `Recommendation` with `ControlChange` and evidences.

If something is unclear or you need a different scope (unit tests, CI hooks, or endpoint mocks), tell me which area to expand and I will update this guidance.
