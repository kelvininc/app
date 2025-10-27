Title: Asset Properties
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/asset-properties/
Fetched: 2025-10-27

Detailed Summary :
Asset Properties are metadata values attached to Assets and are created dynamically when a Platform Administrator creates Assets. These properties are exposed to Kelvin SmartApps through the `KelvinApp` runtime and can be accessed from the `assets` dictionary that lives on the running application instance. The documentation's core guidance shows how to read a specific property for a known asset name and property key.

Access pattern summary:
- `app.assets` is a mapping (dictionary-like) keyed by asset name.
- Each asset object exposes a `properties` mapping (dictionary-like) containing the asset properties by key.
- Accessing properties requires the app to be connected (for example by calling `await app.connect()`), and you should guard against missing assets or missing property keys in production code.

The page points to the broader Asset Properties/Concepts overview for additional conceptual material but the concrete usage is the simple retrieval pattern shown below.

Key examples :
The page contains a small Python example demonstrating how to instantiate `KelvinApp`, connect, and read a property value from an asset's `properties` mapping.

```python
import asyncio
from kelvin.application import KelvinApp

async def main() -> None:
    app = KelvinApp()
    await app.connect()

    # Get a single asset property
    manufacturer = app.assets["my-motor-asset"].properties["brand"]
    print("manufacturer:", manufacturer)

if __name__ == '__main__':
    asyncio.run(main())
```

Notes:
- Asset Properties are created/managed by the Platform Administrator when Assets are provisioned; they are not declared in a SmartApp's `app.yaml` parameters section (those are App Parameters). Use the Kelvin UI or Asset provisioning APIs to define properties.
- Always check that the asset key exists in `app.assets` (KeyError) and that the desired property key exists in the asset's `properties` mapping before using the value; properties may be absent for some assets.
- Access `app.assets[...]` only after the app has been connected; otherwise the mapping may be empty or uninitialized.
- Asset properties are useful for static metadata (brand, model, serial number, location identifiers) which SmartApps can use to route logic, display friendly names, or apply asset-specific business rules.
