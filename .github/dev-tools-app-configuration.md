Title: App Configuration
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/app-configuration/
Fetched: 2025-10-27

Detailed Summary :
App Configuration exposes runtime configuration data for a SmartApp. The page documents how configuration is surfaced to a running `KelvinApp` instance via the `app.app_configuration` mapping and shows examples for nested configuration access and usage. The App Configuration is distinct from App Parameters and Asset Properties — it typically contains runtime configuration settings for the SmartApp itself (for example broker settings, nested configuration objects, or recommendation templates) which are provided via the platform configuration APIs or the Kelvin UI.

Key points from the page:
- `app.app_configuration` is a mapping-like object available on the `KelvinApp` instance after connection; use `await app.connect()` before accessing it.
- You can read simple configuration keys with `app.app_configuration["key"]`.
- Nested configuration objects can be accessed with chained indexing, e.g. `app.app_configuration["nest-example"]["nest1"]`.
- The page includes an example showing how to read a broker IP from `app.app_configuration["broker-ip"]`.
- The docs also illustrate platform-side configuration updates via an HTTP API example (curl) that posts a configuration payload to update workload configurations (this is for platform operators or automation and shows a JSON body structure containing `configuration.recommendations` with multiple recommendation templates and setpoint definitions).

Key examples :
Python — connect and get simple App Configuration keys:

```python
import asyncio
from kelvin.application import KelvinApp

async def main() -> None:
    app = KelvinApp()
    await app.connect()

    # Get IP from app configuration
    ip = app.app_configuration["broker-ip"]
    print("broker ip:", ip)

    # Get nested configuration value
    nested_value = app.app_configuration["nest-example"]["nest1"]
    print("nested value:", nested_value)

if __name__ == '__main__':
    asyncio.run(main())
```

Platform API example (curl):

The page includes a curl sample showing how an operator can POST a JSON configuration update to the Kelvin API workloads configurations endpoint. The body demonstrates a `configuration.recommendations` array with recommendation templates (description, setpoint with name and variation_factor, and type). This payload shows the structure expected by the platform when creating or updating app configuration entries.

Notes:
- Access `app.app_configuration` only after the app has connected — otherwise the mapping may be empty.
- Treat configuration values as potentially nested dicts/objects; perform existence checks before dereferencing nested keys to avoid KeyError.
- Use the platform workloads configuration API shown by the curl example when automating configuration updates from CI/CD or operator scripts. Ensure requests are authenticated with a valid Bearer token.
- App Configuration is intended for app-level runtime configuration; prefer App Parameters for user-editable per-asset parameterization and Asset Properties for asset metadata.
