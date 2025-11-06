# Purpose

This file defines the core SmartApp structure and the rules an AI coding agent should follow when editing this repository. All edit requests must be interpreted against this guidance first. For the detailed Kelvin docs extract, see `.github/dev-tools-create-smartapp.md` (it contains the depth-0 summary and copyable snippets).

# Copilot instructions

The instructions below define the core structure and rules for Kelvin SmartApps in this repository. They serve as the authoritative guidance for any edits or additions to the SmartApp codebase.

# User Prompt

On initial user prompt, you must:

1. Collect detailed clarification from user on the requirements and ensure you are fully clear on what they want before starting any coding changes.
2. Summarize the full understanding in a structured format.
3. Upon confirmation, generate the files in strict order: requirements.txt, app.yaml, main.py, parameters.json, .dockerignore, Dockerfile, README.md and any other requested files.
4. If user rejects summary, repeat clarification and revise until confirmed.

On subsequent user prompts, you must:

1. Ask a single clarifying question that maps a requested change to file(s) above. NEVER make large edits based on assumptions.

# Minimal SmartApp Structure

The minimal file, file contents and folder structure for Kelvin SmartApps is in the `.github/core/` folder. The final structure of this repository should mirror that minimal structure and follow this format. Files that are mandatory are noted below.

```
project-name/
  ├── main.py                     (mandatory)
  ├── app.yaml                    (mandatory)
  ├── requirements.txt            (mandatory)
  ├── Dockerfile                  (mandatory)
  ├── .dockerignore               (mandatory)
  ├── README.md
  └── ui_schemas/
      └── parameters.json         (mandatory)
      └── configurations.json
```

# Core files (read these first)

- `app.yaml` — authoritative definition of data streams, data-quality validators, control_changes, parameters, ui_schemas, and defaults (system, datastream_mapping, configuration, parameters) and more. Detailed information in `.github/dev-tools-create-smartapp.md`
- `main.py` — streaming handlers and business logic (use `KelvinApp`, `app.stream_filter`, and SDK message objects).
- `requirements.txt`, `Dockerfile`, `.dockerignore` — runtime packaging and build.
- Example apps: `.github/examples/event-detection` and `.github/examples/casting-defect-detection` — example `main.py` and `app.yaml` files that demonstrate meaningful handler structures, app.yaml layout (data_streams, control_changes, parameters), and programming patterns to reference when implementing new SmartApps.
- `ui_schemas/parameters.json` and `ui_schemas/configuration.json` — JSON schemas used by the Kelvin UI; keep these synchronized with `app.yaml`.

# Mandatory rules (apply to all edits)

1. Single source of truth: `app.yaml` drives platform-facing behaviour. Detailed information about the keys and structure are in the file `.github/dev-tools-create-smartapp.md`. Any structural changes to streams/parameters/outputs must be mirrored in `ui_schemas/*` and `defaults` when appropriate.
2. Minimal, focused changes: one logical change per PR; provide a short rationale and a test plan in the PR description.
3. Non-blocking handlers: `main.py` stream consumers must not block the event loop. Offload long work to `asyncio.create_task()` or background tasks.
4. Use SDK types: prefer `KRNAsset`, `KRNAssetDataStream`, `Recommendation`, `ControlChange` and other SDK types for correctness.
5. Declarative outputs: declare any control change outputs in `app.yaml.control_changes.outputs`.
6. All programming changes must try to follow the Best Practices reference from `.github/dev-tools-best-practices.md`. This is not mandatory but strongly advised and can be ignored when the circumstances warrant it.
7. Only key names defined in documentation or examples may be used in app.yaml and parameters.json.
8. Must check the `app.yaml` `name` key and update the appropriate fields.
    a. If it is `application-name`, then also update the `name`, `title` and `description` fields to appropriate values.
    b. If it is NOT `application-name`, then increment the third digit of the version number.

## Kelvin SDK enforcement (MANDATORY)

- Do NOT invent, guess, abbreviate, alias, or fabricate any Kelvin SDK module, class, function, constant, or import path. Use only symbols and import lines that appear verbatim in this repository's authoritative docs and examples (for example: `.github/dev-tools-create-smartapp.md`, `.github/copilot-instructions.md`, and any file under `.github/examples/`).
- Every Kelvin SDK import used in generated code must be verifiable against an example in the repo. If the exact import line or symbol cannot be found, STOP and ask a single clarifying question — do not guess.
- When you produce code that references a Kelvin SDK symbol, include a one-line reference comment pointing to the example or doc file that demonstrates that exact symbol or import (file path and example section or line if possible).
- Do NOT change canonical import lines. Example (forbidden):
  - `from kelvin.message.msg_builders import ControlChange, Recommendation`  # <-- FORBIDDEN unless that exact path exists in repo examples
  - Use the exact import shown in the docs, e.g. `from kelvin.message import ControlChange, Recommendation` if that is what the repo shows.
- Prefer examples in `.github/dev-tools-create-smartapp.md`, `.github/examples/*`, or other `.github/*.md` examples.
- If a user's instruction conflicts with these rules, follow these rules and ask the user to resolve the conflict.

## app.yaml and JSON schema enforcement (MANDATORY)

- Do NOT invent or introduce new top-level keys, parameter names, schema shapes, or configuration fields in `app.yaml` or any JSON UI schema (`ui_schemas/*.json`) that are not present in this repository's authoritative docs or examples. Use only keys and structures that appear verbatim in `.github/dev-tools-create-smartapp.md`, `.github/examples/*`, or other `.github/*.md` examples.
- Every `app.yaml` or `ui_schemas/*.json` change must be verifiable against an example in the repo. If you cannot find an exact example demonstrating the structure or key, STOP and ask a single clarifying question — do not guess or invent a shape.
- When generating or editing `app.yaml` or `ui_schemas/parameters.json`, include a one-line reference comment in the PR or the file (if supported) that points to the example/doc demonstrating the required key or block. Example: `# example: .github/examples/event-detection/app.yaml (input stream declaration)`.
- JSON schema keys and property names must match the `parameters` declared in `app.yaml` exactly (case and spelling). Do not create `min_`/`max_` helper parameters; use the property's `minimum`/`maximum` attributes as shown in examples.
- Do NOT create new helper methods, utility functions, or SDK wrappers that change the public behaviour or message contract expected by `app.yaml` or by the platform. Only implement functions and handlers that match the patterns in `.github/examples/*` and the docs (for example: `async def main()`, per-stream handlers, `app.stream_filter(...)`).


Below sub chapters give detailed rules for each core file.

## main.py Rules (Strict)

1. Must use async structure: `async def main()` and launched by `asyncio.run(main())`.
2. Must use consistent imports and structure as demonstrated in the provided examples.
3. Each input stream must be handled in an individual async function `async def FUNCTION_NAME()`.
4. Each input stream must use: `VARIABLE = app.stream_filter(filters.input_equals("STREAM_NAME"))`.
5. All input-handling functions must be awaited concurrently via `await asyncio.gather(...)` in `main()`.
6. Only valid Kelvin SDK components and documented patterns may be used.
7. Logic must pass Python concurrency and linting standards.
8. Use correct message types (`Number`, `String`, etc.) and validate payloads.
9. Control logic must conform to app parameter usage (`closed_loop`, thresholds, etc.).
10. Code must be reviewed after generation to validate behavior matches spec. If not, regenerate.
11. No global blocking code or infinite loops outside of designated input handling.
12. Evidence, control changes, or custom actions must follow documentation exactly.
13. Do not include any unused imports or code.
14. Only import Kelvin SDK modules or methods from approved files and examples.
15. All variable names used must follow the regex format ^[a-z0-9]([-_.a-z0-9]*[a-z0-9])?$
16. Always use asyncio.gather when running multiple async functions.

These rules will be updated as needed. Every generated `main.py` must strictly follow all rules.

## Recommendations

- If `closed_loop` is true, set `auto_accepted=True`.
- All recommendations must include an alert message. Control changes are optional.
- Multiple control changes **and** actions can be included in the same Recommendation.
- Evidence can be added to Recommendations and should be asked during clarification.

## If Custom Actions are requested
- Make sure to get one or more action `type` values from the user.
- Confirm if it's a Producer or Consumer App (Executor). If needed, explain the difference.
- For Consumer App, create a separate function for each custom action `type`.
- Ensure `app.yaml` is declared correctly with inputs or outputs under `custom_actions`.

## app.yaml Rules (Strict)
1. Must contain: `spec_version: 5.0.0`, `type: app`, `name`, `title`, `description`, and `version` fields.
2. `name` must follow this regex: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$` (only lowercase letters, digits, and hyphens, must start and end with alphanumeric).
3. Control changes only go under `control_changes:` block (never repeated under `data_streams`,`outputs` key).
4. Default parameters must be specified under the `defaults:` section.
5. Only declared data streams, parameters, or custom actions may be used. No invented keys.
6. `ui_schemas` must reference an actual `parameters.json` file located in `ui_schemas/` folder.

## parameters.json
- Must be placed in ui_schemas folder and linked in app.yaml.
- Property keys must match `parameters` in app.yaml.
- Each property requires type and title; min/max are optional.
- When app parameters are involved, you must ask for:
  - Name
  - Data type
  - min/max (if numeric)
  - Default value
  - Display title
- Constraints must be attributes of parameters, not separate ones.
- You must never invent parameter names like min_* or max_*.

## Dockerfile
- Always copied byte-for-byte from default-Dockerfile sample. Never regenerated or altered.

## .dockerignore
- Always copied byte-for-byte from default-.dockerignore sample. Never regenerated or altered.

## README.md
- Describes the project.
- Last line: `Upload the application to a Kelvin Instance with this CLI command `kelvin app upload`.

# Examples — mapping prompts to edits

- "Add data stream `temperature_c`": `app.yaml.data_streams.inputs` + `ui_schemas/*` + optional `defaults.datastream_mapping`.
- "Add parameter `safety_margin`": `app.yaml.parameters` + `ui_schemas/parameters.json` + `defaults.parameters`.
- "Auto-accept recommendations": update `Recommendation` creation in `main.py` to read `kelvin_closed_loop` parameter or set `auto_accepted=True`; ensure parameter exists in `app.yaml` and ui_schemas.
 - "Consume timeseries / asset data": consult `.github/dev-tools-consume-timeseries-data.md` and implement handlers in `main.py` using `app.stream_filter(...)`, `app.filter(...)` (queue), or `app.on_asset_input` as appropriate; ensure corresponding inputs are declared in `app.yaml.data_streams.inputs` and use `filters` to limit scope (e.g., `input_equals`, `resource_equals`, `asset_equals`).
 - "Consume Control Changes / App-to-App messages": consult `.github/dev-tools-consume-control-changes.md` and implement callbacks or handlers using `app.on_control_change` and `app.on_control_status`; ensure `control_changes.inputs` / `control_changes.outputs` are declared and KRN resources match between producer and consumer.

# Quick verification steps

 - Local: run `python main.py` to check imports and basic runtime.

## Linting & validation (MANDATORY)

- Before finalizing any new or modified code, run the repository-configured linters and static checks and resolve any errors reported. The repository's linting configuration and commands are available in `pyproject.toml`, `.devcontainer/devcontainer.json`, and the `Dockerfile` — use those to discover the exact tools/commands (for example: `ruff`, `flake8`, `mypy`, `black --check`, or other configured tools).
- At minimum, ensure there are no Python syntax errors (e.g., `python -m py_compile`) and that the project's linter(s) exit with success. If the exact project commands are not obvious, ask a single clarifying question before proceeding.
- If lint or test failures are non-trivial to fix, report the failures and either (a) implement minimal, well-scoped fixes or (b) ask the user for guidance. Do not ship code that introduces new linter errors.


# Offline reference

 - The full, self-contained extract of the Kelvin "create" docs (v6.3) is in `.github/dev-tools-create-smartapp.md`. Use it for copyable `app.yaml` and JSON examples and authoritative explanations when internet access is unavailable.
 - KRN reference: `.github/dev-tools-krn.md` — offline KRN registry (patterns, examples and regex) for stable resource naming and references.
 - Timeseries consumption patterns: `.github/dev-tools-consume-timeseries-data.md` — offline extract with copyable examples (async generator, queue, callback) and filter usage. Use this when implementing or reviewing message-handling code.
 - Control Changes (produce & consume): `.github/dev-tools-consume-control-changes.md` — offline reference with app.yaml declarations, producer/consumer Python examples, and control-change status handling.
 - Custom Actions (consume): `.github/dev-tools-consume-custom-actions.md` — offline extract with app.yaml declarations, consumer (executor) Python example and guidance on publishing `CustomActionResult`.
 - Data Quality messages: `.github/dev-tools-consume-data-quality.md` — offline extract with app.yaml data_quality examples, API client queries, and runtime stream-filter examples for realtime processing.
 - Windowing (tumbling/hopping/rolling): `.github/dev-tools-consume-windowing.md` — offline extract with examples for `tumbling_window`, `hopping_window`, and `rolling_window` usage and notes on alignment and lateness.
 - Produce Timeseries Data (publish): `.github/dev-tools-produce-timeseries-data.md` — offline extract describing `data_streams.outputs` declarations, primitive message types (`Number`, `Boolean`, `String`, objects), and sample `app.publish(...)` usage.
 - Produce Control Changes (publish): `.github/dev-tools-produce-control-changes.md` — offline extract describing `control_changes.outputs`, ControlChange message attributes (payload, expiration_date, retries, timeout, from_value) and example `app.publish(ControlChange(...))` usage.
 - Produce Custom Actions (publish): `.github/dev-tools-produce-custom-actions.md` — offline extract describing `custom_actions.outputs`, CustomAction attributes (resource, type, title, description, payload, expiration_date) and example `app.publish(CustomAction(...))` usage (direct publish or embedded in a Recommendation).
 - Produce Recommendations (publish): `.github/dev-tools-produce-recommendations.md` — offline extract covering Recommendation message structure, embedding `control_changes`, `evidences` (charts/images/markdown/iframes), `metadata`, and sample `app.publish(Recommendation(...))` usage.
 - Produce Data Tags (publish): `.github/dev-tools-produce-data-tags.md` — offline extract describing the `DataTag` message (start_date, end_date, tag_name, resource, contexts) and a sample `app.publish(DataTag(...))` usage.
 - Produce Asset Parameters (publish): `.github/dev-tools-produce-asset-parameters.md` — offline extract describing `AssetParameter` and `AssetParameters` messages, attributes (`resource`, `value`, `comment`), App-to-App usage, and Python examples for publishing single or multiple asset parameter updates.
 - Asset Properties (reference): `.github/dev-tools-asset-properties.md` — offline extract explaining how Asset Properties are exposed to `KelvinApp` via `app.assets[<asset_name>].properties` and a Python example showing how to read a single property.
 - App Parameters (reference): `.github/dev-tools-app-parameters.md` — offline extract explaining App Parameters declared in `app.yaml` (schema example: `closed_loop`, `speed_decrease_set_point`, `temperature_max_threshold`), how resolved values are exposed at runtime via `app.assets[<asset_name>].parameters[...]`, and Python examples for reading and App-to-App updates.
 - App Configuration (reference): `.github/dev-tools-app-configuration.md` — offline extract describing the `app.app_configuration` mapping exposed on `KelvinApp`, examples for reading simple and nested configuration keys, and a platform API example demonstrating how to post configuration updates to workloads.
 - Best Practices (reference): `.github/dev-tools-best-practices.md` — offline extract with guidance on asynchronous coding (`asyncio`), subscription vs polling, event-driven design, logging and runtime knobs, workload resources (Requests/Limits), asset-to-workload assignment, and secret management.

# When you are uncertain

- Ask a single clarifying question that maps a requested change to file(s) above. NEVER make large edits based on assumptions.

This file is intentionally limited to core repository-level rules. Additions (testing patterns, SDK idioms, code cookbook) should be appended in separate sections or files after review.
