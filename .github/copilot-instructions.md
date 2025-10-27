# Copilot instructions (core structure) — use this as authoritative guidance

Short purpose
This file defines the core SmartApp structure and the rules an AI coding agent should follow when editing this repository. All edit requests must be interpreted against this guidance first. For the detailed Kelvin docs extract, see `.github/dev-tools-create-smartapp.md` (it contains the depth-0 summary and copyable snippets).

Core structure to maintain
## Copilot instructions — Core SmartApp contract (starter)

Purpose
This file defines the minimal, repository-level contract for Kelvin SmartApps in this repo. It focuses on the immutable core aspects that must be preserved across edits: the canonical app definition (`app.yaml`), UI schemas, the runtime entrypoint and packaging. It does *not* attempt to cover every SDK API — the offline detailed extract of the Kelvin "create" docs (v6.3) lives in `.github/dev-tools-create-smartapp.md` and is the authoritative reference for examples and copyable snippets.

What this file covers (core only)
- Mapping user prompts to files to edit
- Required consistency rules (app.yaml ↔ ui_schemas ↔ defaults)
- Non-blocking streaming handler expectation for `main.py`
- Quick verification steps (local run / docker smoke)

Core files (read these first)
- `app.yaml` — authoritative definition of data streams, data-quality validators, control_changes, parameters, ui_schemas, and defaults (system, datastream_mapping, configuration, parameters).
- `ui_schemas/parameters.json` and `ui_schemas/configuration.json` — JSON schemas used by the Kelvin UI; keep these synchronized with `app.yaml`.
- `main.py` — streaming handlers and business logic (use `KelvinApp`, `app.stream_filter`, and SDK message objects).
- `requirements.txt`, `Dockerfile`, `.dockerignore` — runtime packaging and build.

Mandatory rules (apply to all edits)
1. Single source of truth: `app.yaml` drives platform-facing behaviour. Any structural changes to streams/parameters/outputs must be mirrored in `ui_schemas/*` and `defaults` when appropriate.
2. Minimal, focused changes: one logical change per PR; provide a short rationale and a test plan in the PR description.
3. Non-blocking handlers: `main.py` stream consumers must not block the event loop. Offload long work to `asyncio.create_task()` or background tasks.
4. Use SDK types: prefer `KRNAsset`, `KRNAssetDataStream`, `Recommendation`, `ControlChange` and other SDK types for correctness.
5. Declarative outputs: declare any control change outputs in `app.yaml.control_changes.outputs`.

Examples — mapping prompts to edits
- "Add data stream `temperature_c`": `app.yaml.data_streams.inputs` + `ui_schemas/*` + optional `defaults.datastream_mapping`.
- "Add parameter `safety_margin`": `app.yaml.parameters` + `ui_schemas/parameters.json` + `defaults.parameters`.
- "Auto-accept recommendations": update `Recommendation` creation in `main.py` to read `kelvin_closed_loop` parameter or set `auto_accepted=True`; ensure parameter exists in `app.yaml` and ui_schemas.
 - "Consume timeseries / asset data": consult `.github/dev-tools-consume-timeseries-data.md` and implement handlers in `main.py` using `app.stream_filter(...)`, `app.filter(...)` (queue), or `app.on_asset_input` as appropriate; ensure corresponding inputs are declared in `app.yaml.data_streams.inputs` and use `filters` to limit scope (e.g., `input_equals`, `resource_equals`, `asset_equals`).
"Consume timeseries / asset data": consult `.github/dev-tools-consume-timeseries-data.md` and implement handlers in `main.py` using `app.stream_filter(...)`, `app.filter(...)` (queue), or `app.on_asset_input` as appropriate; ensure corresponding inputs are declared in `app.yaml.data_streams.inputs` and use `filters` to limit scope (e.g., `input_equals`, `resource_equals`, `asset_equals`).
 - "Consume Control Changes / App-to-App messages": consult `.github/dev-tools-consume-control-changes.md` and implement callbacks or handlers using `app.on_control_change` and `app.on_control_status`; ensure `control_changes.inputs` / `control_changes.outputs` are declared and KRN resources match between producer and consumer.

Quick verification steps
- Local: run `python main.py` to check imports and basic runtime (requires internet/Kelvin creds for publishing).
- Docker: `docker build -t kelvin-app . && docker run --rm kelvin-app` (validates Dockerfile/entrypoint).

Offline reference
- The full, self-contained extract of the Kelvin "create" docs (v6.3) is in `.github/dev-tools-create-smartapp.md`. Use it for copyable YAML/JSON examples and authoritative explanations when internet access is unavailable.
- KRN reference: `.github/dev-tools-krn.md` — offline KRN registry (patterns, examples and regex) for stable resource naming and references.
 - Timeseries consumption patterns: `.github/dev-tools-consume-timeseries-data.md` — offline extract with copyable examples (async generator, queue, callback) and filter usage. Use this when implementing or reviewing message-handling code.
Timeseries consumption patterns: `.github/dev-tools-consume-timeseries-data.md` — offline extract with copyable examples (async generator, queue, callback) and filter usage. Use this when implementing or reviewing message-handling code.
Control Changes (produce & consume): `.github/dev-tools-consume-control-changes.md` — offline reference with app.yaml declarations, producer/consumer Python examples, and control-change status handling.

When you are uncertain
- Ask a single clarifying question that maps a requested change to file(s) above. Do not make large edits based on assumptions.

This file is intentionally limited to core repository-level rules. Additions (testing patterns, SDK idioms, code cookbook) should be appended in separate sections or files after review.
