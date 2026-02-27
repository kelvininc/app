# Best Practices and Common Pitfalls

## When to Use

Use this file as a final implementation/review checklist and to debug common SmartApp failures.

## Table of Contents
- [When to Use](#when-to-use)
- [Pre-Flight Checklist](#pre-flight-checklist)
- [App.yaml and UI Schemas](#appyaml-and-ui-schemas)
- [Streams and Windows](#streams-and-windows)
- [Messages, Recommendations, and Actions](#messages-recommendations-and-actions)
- [API and Timeseries](#api-and-timeseries)
- [State and Concurrency](#state-and-concurrency)
- [Error Handling](#error-handling)
- [Logging and Security](#logging-and-security)

## Pre-Flight Checklist

- Confirm every published output is declared in `app.yaml` before publishing.
- Confirm parameter names match exactly between `app.yaml` and `ui_schemas/*`.
- Confirm stream names used in code match declarations and naming rules.
- Confirm long-running logic runs in `@app.task` or timers (not blocking stream handlers).
- Confirm recommendations/actions include explicit expiration/timeout behavior.

For canonical templates and examples, use:
- [app-yaml.md](app-yaml.md)
- [sdk-patterns.md](sdk-patterns.md)
- [messages-outputs.md](messages-outputs.md)
- [data-processing.md](data-processing.md)

## App.yaml and UI Schemas

- Do not create a `configuration:` declaration section in `app.yaml`.
- Put global values under `defaults.configuration` and per-asset values under `parameters`.
- Use app names with hyphens; use snake_case for stream/parameter names (dots only when needed).
- Keep UI schemas aligned with declared parameter/configuration keys.

Reference: [app-yaml.md](app-yaml.md)

## Streams and Windows

- Use decorator-based handlers (`@app.stream`, `@app.timer`, `@app.task`) unless explicitly asked for function-based patterns.
- For windows, always set `inputs=[...]` explicitly.
- Read DataFrame columns by stream names, not generic `payload`/`value` keys.
- Always guard with `df.empty` and NaN checks before numeric calculations.

References:
- [sdk-patterns.md](sdk-patterns.md)
- [data-processing.md](data-processing.md)

## Messages, Recommendations, and Actions

- Use the correct message class for each output type.
- Embed control changes and custom actions inside `Recommendation` unless explicitly asked to publish standalone.
- Add `kelvin_closed_loop` when recommendations include control changes or custom actions.
- Send `ControlAck` only when handling incoming control changes (`control_changes.inputs`).

Reference: [messages-outputs.md](messages-outputs.md)

## API and Timeseries

- Use real-time streams/windows for recent data and Timeseries API for historical queries.
- Do not declare streams in `data_streams.inputs` when they are used only through Timeseries API.
- Include required client environment vars (`KELVIN_CLIENT__URL`, `KELVIN_CLIENT__CLIENT_ID`, `KELVIN_CLIENT__CLIENT_SECRET`).

Reference: [api-client.md](api-client.md)

## State and Concurrency

- Protect shared mutable state in concurrent handlers (`asyncio.Lock` when needed).
- Handle asset add/remove events (`on_asset_change`) to keep per-asset state consistent.
- Clean up removed asset state to prevent stale memory growth.

Reference: [data-processing.md](data-processing.md)

## Error Handling

- `@app.stream` and `@app.timer` continue after exceptions; `@app.task` does not.
- Wrap long-running task loops in `try/except` and log exceptions with context.
- Validate business/domain rules only; rely on framework guarantees for typed payload/resource fields.

Reference: [sdk-patterns.md](sdk-patterns.md)

## Logging and Security

- Log asset, stream, and decision context for operational debugging.
- Keep secrets out of source; load them via `defaults.system.environment_vars`.
- Avoid logging secret values or full sensitive payloads.
