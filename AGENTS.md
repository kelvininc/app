# AGENTS.md

## Project Scope
This repository is a Kelvin SmartApp template (`app.yaml` + Python runtime code).

## Project Tree Structure
This section shows the main files and folders only (not `.git` or tool internals).

```text
.
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── README.md
├── app.yaml
├── main.py
├── requirements.txt
├── ui_schemas/
    ├── configuration.json
    └── parameters.json
└── .skills/
    └── kelvin-sdk/
```

Tree maintenance note:
- Keep this tree concise and update it when project structure changes.
- Include only files/folders relevant to SmartApp development and agent guidance.

## Skill Requirement
- Use the `kelvin-sdk` skill for any task that implements, reviews, debugs, refactors, or migrates SmartApp behavior.
- Use the `kelvin-sdk` skill for changes involving:
  - `app.yaml` schema/configuration
  - data streams, windows, recommendations, control changes, or custom actions
  - Kelvin API client usage
  - KRN construction/parsing

Reference skill file:
- `.skills/kelvin-sdk/SKILL.md`

## Kelvin Authentication
Login to your Kelvin instance before upload:

```bash
kelvin auth login <instance>.kelvin.ai
```

## Kelvin SmartApp Build
Build the app package from the project root:

```bash
kelvin app build
```

## Kelvin SmartApp Upload
Upload the built app to your Kelvin instance:

```bash
kelvin app upload
```
