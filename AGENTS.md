# AGENTS.md

## Project Scope
This repository is a Kelvin SmartApp template (`app.yaml` + Python runtime code).

## Project Tree Structure
```text
.
├── .devcontainer/
│   ├── Dockerfile
│   └── devcontainer.json
├── .skills/
│   └── kelvin-sdk/
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── Dockerfile
├── README.md
├── app.yaml
├── logo.png
├── main.py
├── requirements.txt
└── ui_schemas/
    ├── configuration.json
    └── parameters.json
```

## Skill Requirement
- Use the `kelvin-sdk` skill for any task that implements, reviews, debugs, refactors, or migrates SmartApp behavior.
- Use the `kelvin-sdk` skill for changes involving:
  - `app.yaml` schema/configuration
  - data streams, windows, recommendations, control changes, or custom actions
  - Kelvin API client usage
  - KRN construction/parsing

Reference skill file:
- `.skills/kelvin-sdk/SKILL.md`

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
