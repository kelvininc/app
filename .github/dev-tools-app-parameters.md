Title: App Parameters
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/app-parameters/
Fetched: 2025-10-27

Detailed Summary :
App Parameters are configuration values exposed by a Kelvin SmartApp that can be used to control app behaviour per-asset or globally. They are declared in the SmartApp's `app.yaml` under a `parameters` section using a JSON Schema-like structure (type, title, minimum, maximum, required, etc.). The platform exposes resolved App Parameter values to a running SmartApp through the `app.assets[<asset_name>].parameters` mapping (i.e., per-asset parameters). The docs show both the parameter schema example and how to access the resolved parameter value at runtime from within `KelvinApp`.

Schema example (from page): the sample parameters schema includes three example parameters:

- `closed_loop` (boolean) — a toggle labelled "Closed Loop" (required).
- `speed_decrease_set_point` (number) — labelled "Speed Decrease SetPoint", with minimum 1000 and maximum 3000 (required).
- `temperature_max_threshold` (number) — labelled "Temperature Max Threshold", with minimum 50 and maximum 100 (required).

The schema also contains a `required` list referencing these three parameter keys. App authors should declare parameter types, titles and constraints in `app.yaml` so the Kelvin UI and runtime can validate and present configuration controls correctly.

Access patterns and runtime notes:
- `app.assets` is a dictionary keyed by asset name. Each asset object exposes a `parameters` mapping for the resolved App Parameter values for that asset.
- Accessing parameter values should be done after `await app.connect()` so the runtime has loaded configuration and asset mappings.
- Parameter values must be treated as typed primitives (boolean, number, string) according to the declared schema; perform defensive checks for missing values or mismatched types.

Key examples :
Python — connect and read a single App Parameter value for an asset:

```python
import asyncio
from kelvin.application import KelvinApp

async def main() -> None:
    app = KelvinApp()
    await app.connect()

    # Read a per-asset App Parameter
    temperature_max_threshold = app.assets["my-motor-asset"].parameters["temperature_max_threshold"]
    print("temperature_max_threshold:", temperature_max_threshold)

if __name__ == '__main__':
    asyncio.run(main())
```

Python — (the page also shows how App Parameters can be updated via AssetParameters messages; example producing AssetParameters is included here since the page demonstrates App-to-App parameter update patterns):

```python
from kelvin.message import AssetParameters, AssetParameter
from kelvin.krn import KRNAssetParameter, KRNAppVersion

# publish multiple AssetParameters to update App Parameters for an asset
await app.publish(
    AssetParameters(
        parameters=[
            AssetParameter(
                resource=KRNAssetParameter(asset, "min_treshold"),
                value=0,
            ),
            AssetParameter(
                resource=KRNAssetParameter(asset, "max_treshold"),
                value=50,
            ),
        ],
        resource=KRNAppVersion(target_app_name, "1.0.0"),
    )
)
```

Notes:
- App Parameters (declared in `app.yaml`) are distinct from Asset Properties (metadata created when assets are provisioned). App Parameters appear under `app.assets[<asset_name>].parameters` at runtime; Asset Properties appear under `app.assets[<asset_name>].properties`.
- Ensure parameter names and types exactly match those declared in `app.yaml` and any `ui_schemas`—typos will cause runtime lookup failures.
- Use the `required` property in the parameter schema to force presence and help the UI validate configuration.
- When reading parameters, guard against missing asset keys or missing parameter keys (KeyError) and consider sensible defaults where appropriate.
- When publishing App Parameter updates programmatically (App-to-App), remember updates must reach the Kelvin Cloud to persist and propagate — local-only changes won't be visible to other apps.
