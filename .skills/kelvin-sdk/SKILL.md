---
name: kelvin-sdk
description: Use when implementing, reviewing, debugging, refactoring, or migrating Kelvin SmartApps with the Kelvin Python SDK, including app.yaml schema/configuration, stream and window handlers, recommendations/control changes/custom actions, Kelvin API client usage, and KRN construction/parsing.
---

# Kelvin SDK Developer

Build and modify Kelvin SmartApps with the Kelvin Python SDK. Start with a minimal working implementation, then expand only for explicit requirements.

## Execution Workflow

1. Clarify only missing requirements.
2. Identify app shape (stream-only, windows, recommendations/actions, API client usage).
3. Choose the first reference file with deterministic decision rules.
4. Load only additional references required by the task.
5. Implement with decorator-based handlers by default.
6. Validate against the rule checklist before finalizing.

## Clarify Missing Requirements

Ask at most 2-3 high-impact questions at a time, and only when missing information blocks correct implementation.

Prioritize questions in this order:
- Inputs: stream names, data types, and target assets.
- Outputs: data streams and/or recommendation/control/custom-action outputs.
- Behavior: thresholds, logic, cadence, and expiration/timeout requirements.
- Configuration: app-level configuration vs per-asset parameters.
- Delivery constraints: standalone outputs vs outputs embedded in recommendations.

If the request is already explicit enough, proceed without extra questions.

When details are missing but non-blocking, proceed with explicit assumptions and mark them clearly:
- Use placeholder names like `input_stream`, `output_stream`, and `threshold` only when concrete names are unknown.
- Prefer configurable values (parameters/app configuration) over hardcoded constants.
- Do not invent credentials, KRN identifiers, or environment-specific secrets.
- Summarize all assumptions in the final response so they can be confirmed quickly.

## First-File Decision Rules

Pick exactly one first reference file from the list below, then expand only if needed:
- `app.yaml` declarations, defaults, UI schema wiring, or naming mismatches: [references/app-yaml.md](references/app-yaml.md)
- Lifecycle/decorators/runtime callback behavior: [references/sdk-patterns.md](references/sdk-patterns.md)
- Windowing, DataFrame aggregation, or shared state races: [references/data-processing.md](references/data-processing.md)
- Output message classes, recommendations, control changes, custom actions, or evidences: [references/messages-outputs.md](references/messages-outputs.md)
- Kelvin API reads/writes (`app.api`) or timeseries queries: [references/api-client.md](references/api-client.md)
- KRN construction/parsing: [references/krn.md](references/krn.md)
- Ambiguous runtime failures or mixed-category bugs: [references/best-practices.md](references/best-practices.md)

Do not load all references by default. Load only what the current task needs.

## Implementation Defaults

- Use decorator-based API (`@app.stream()`, `@app.timer()`, `@app.task`) unless explicitly asked for function-based patterns.
- Prefer small explicit handlers with clear stream and asset names.
- Keep business validation in app logic. Rely on framework guarantees for SDK-managed fields.
- Use per-asset parameters for asset-specific behavior and `app.app_configuration` for global behavior.
- Use windows only when aggregation is required. Process streams directly otherwise.
- Keep recommendations and actions minimal and explicit. Add evidences only when requested or clearly useful.

## Validation Checklist

### `app.yaml` and schema alignment

- Declare all published outputs in `app.yaml` before publishing.
- Do not introduce a `configuration:` declaration. Use `defaults.configuration` for global values.
- Keep parameter names identical between `app.yaml` and `ui_schemas`.
- Follow naming conventions: app names with hyphens, stream/parameter names with underscores (or dots when required).

### Messages and actions

- Embed control changes and custom actions inside `Recommendation` unless explicitly asked to publish them standalone.
- Add and use `kelvin_closed_loop` when recommendations carry actions that may auto-accept.
- Set explicit expiration/timeouts for control changes and action-like recommendations.

### Window and data handling

- Always provide `inputs=[...]` for windows.
- Read DataFrame columns by input stream names.
- Guard with `df.empty` and handle NaN values explicitly.
- Use Timeseries API for historical data (typically older than 12 hours), not as `data_streams.inputs`.

### Reliability and safety

- Treat `@app.task` exceptions as fatal unless caught. Add error handling in long-running tasks.
- Log decisions and threshold crossings with asset and stream context.
- Keep secrets and credentials out of source files.

## Framework Guarantees

Assume these SDK guarantees and avoid redundant checks:
- `msg.resource.asset` is a non-null `str` present in `app.assets`.
- `msg.resource.data_stream` is a non-null `str`.
- `msg.payload` matches the type declared in `app.yaml`.

Validate domain and business rules (thresholds, ranges, state transitions), not framework invariants.
