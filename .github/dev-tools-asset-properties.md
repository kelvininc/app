You can learn more about [Asset Properties in the Overview ⟶ Concepts page](../../../overview/concepts/variables/asset-properties.md).

## Creating Asset Properties

Asset Properties are created dynamically when the Platform Administrator [creates the Assets](../../../platform-administration/how-to/asset/create-asset.md).

![](../../../assets/asset_admin_asset_add_new_step_2.png)

## Get Asset Property

To access a single `Asset Property` value directly from an `assets` Dictionary Object embedded within `KelvinApp`:

```python title="Get Asset Property Python Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    (...)

    # Get Asset Property
    manufacturer = app.assets["my-motor-asset"].properties["brand"]
```