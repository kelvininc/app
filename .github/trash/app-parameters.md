# App Parameters

You can learn more about [Asset Parameters in the Overview ⟶ Concepts page](../../../overview/concepts/variables/asset-parameters.md).

## Creating Parameters

They are initially declared with default values in the Kelvin SmartApp™ `app.yaml` file.

The variables can then be dynamically changed by Operations for each Asset deployed to the Kelvin SmartApp™. This allows customized values for each Asset.

![](../../../assets/produce-asset-parameters-messages-overview.jpg)

The keys used in the `app.yaml` file are;

* `parameters` defines the name and type of the App Parameter.
* `ui_schemas` is a link to a JSON file containing all the information about how to display App Parameters in the Kelvin UI.
* `defaults` / `parameters` define the default values assigned to each Asset when it is first created or when a Kelvin SmartApp™ update introduces a new App Parameter to existing Assets.

Each parameter can be defined by four different `data_types`. Full documentation on the different `data_types` is in the [concept overview page](../../../overview/concepts/data-stream.md#data-type).

In the `app.yaml` file it will look like this;

```yaml title="app.yaml Example" linenums="1"
parameters:
    - name: closed_loop
    data_type: boolean
    - name: speed_decrease_set_point
    data_type: number
    - name: temperature_max_threshold
    data_type: number

ui_schemas:
    parameters: "ui_schemas/parameters.json"

defaults:
    parameters:
    closed_loop: false
    speed_decrease_set_point: 1000
    temperature_max_threshold: 59
```

For the `parameters.json` file you can define all the information for the Kelvin UI. This can be the title, type of input required and limitations of the values allowed.

It will look something like this.

```json title="sample ui_schema/parameters.json" linenums="1"
{
    "type": "object",
    "properties": {
        "closed_loop": {
            "type": "boolean",
            "title": "Closed Loop"
        },
        "speed_decrease_set_point": {
            "type": "number",
            "title": "Speed Decrease SetPoint",
            "minimum": 1000,
            "maximum": 3000
        },
        "temperature_max_threshold": {
            "type": "number",
            "title": "Temperature Max Threshold",
            "minimum": 50,
            "maximum": 100
        }
    },
    "required": [
        "closed_loop",
        "speed_decrease_set_point",
        "temperature_max_threshold"
    ]
}
```

Which will be displayed on the Kelvin UI as:

![App Parameters](../../../assets/qs-create-app-asset-parameters.jpg)

## Get Parameter Values

Access a single `App Parameter` value directly from an `assets` Dictionary Object embedded within `KelvinApp`:

```python title="Get Parameter Values Python Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    (...)

    # Get App Parameter
    temperature_max_threshold = app.assets["my-motor-asset"].parameters["temperature_max_threshold"]
```

## Updating Parameter Values

Writing to a single `App Parameter` value directly from an `assets` Dictionary Object embedded within `KelvinApp`:

```python title="Updating Parameter Values Python Example" linenums="1"
from kelvin.message import AssetParameters, AssetParameter
from kelvin.krn import KRNAppVersion

(...)

await app.publish(
  AssetParameters(
    parameters=[
      AssetParameter(resource=KRNAssetParameter(asset, "min_treshold"), value=0), 
      AssetParameter(resource=KRNAssetParameter(asset, "max_treshold"), value=50)
    ],
    resource=KRNAppVersion(target_app_name, "1.0.0")
  )
)
```

## Upgrading Kelvin SmartApps™

When a Kelvin SmartApp™ is upgraded, Kelvin automatically propagates all matching App Parameter values from the previous version to the new version.

For any new App Parameters introduced in the upgraded Kelvin SmartApp™ version, the default values will initially apply to all Assets using the updated version.

![](../../../assets/produce-asset-parameters-messages-upgrade-smartapp.jpg)

## Other Examples

### Basic

In the `app.yaml` file, the minimum you can put is this

```yaml title="app.yaml Example" linenums="1"
parameters:
    - name: temperature_max_threshold
      data_type: number
```

In the Kelvin SmartApp™ program, it can access the App Parameter values for each Asset like this.

Access a single `App Parameter` value directly from an `assets` Dictionary Object embedded within `KelvinApp`:

```python title="Get Parameter Values Python Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    (...)

    # Get App Parameter
    temperature_max_threshold = app.assets["my-motor-asset"].parameters["temperature_max_threshold"]
```

!!! info

    `app.assets` will only be available after `app.connect()`

The App Parameter values can be updated by Operations in the Kelvin UI through the parameters section.

![](../../../assets/applications_configuration_overview.png)


### SmartLift

A practical example is in the Kelvin SmartApp™ called SmartLift where the Operations can change the values for different App Parameters for each Asset.

![](../../../assets/produce-asset-parameters-messages-example-smartlift.png)

In this example, Operations can set the following values for each Asset;

* Maximum Drawdown rate
* Minimum Drawdowm rate
* Maximum Power

They can also assign whether the gauge is faulty.

Finally, they can choose whether to run the Asset in Open or Closed control mode:

* **Open Control Mode**: Any data changes the Kelvin SmartApp intends to make to the Asset data values must first be approved by Operations before being applied to the Asset.
* **Closed Control Mode**: Any data changes the Kelvin SmartApp intends to make are automatically applied to the Asset without requiring prior approval.

## App Parameter Messages

Kelvin SmartApps™ can publish an `App Parameter` Message in order to (asynchronously) update a given App Parameter for a given Asset.

The App Parameter update will persist as soon as this message is synced with the Kelvin Cloud.

!!! note

    A user can also change the App Parameter value through the Kelvin UI.

    Any changes done automatically by an application will be updated on the Kelvin UI screen.

IMAGE DESCRIPTION HERE : The app's parameters are initially set with default values in the app.yaml file. These default settings can be easily modified by users through the Kelvin UI. Once updated, the new values are dynamically applied across the entire application, ensuring that they are accessible and used by any Python script or program that requires them. This allows for flexible configuration and seamless integration throughout the application. 

You can see the configuration options for a Kelvin SmartApp™ for an Asset in SmartApp section of the Kelvin UI.

![](../../../../assets/applications_schedule_new_configurations_change_parameters.png)

The AssetParameter Object supports the following attributes:

| Attribute       | Required     | Description                                                                                 |
|-----------------|--------------|---------------------------------------------------------------------------------------------|
| `resource`      | **required** | The **KRNAssetParameter** that this update is meant for.                                    |
| `value`         | **required** | App Parameter value (Boolean, Integer, Float or String).                                  |
| `comment`       | **optional** | Detailed description of the App Parameter update.                                         |

## Examples

### Basic Usage

This is how an App Parameter can be created and published in a Kelvin SmartApp™:

```python title="Create and Publish App Parameter Python Example" linenums="1"
from datetime import timedelta, datetime

from kelvin.application import KelvinApp
from kelvin.message import AssetParameter
from kelvin.krn import KRNAssetParameter

(...)

# Create and Publish App Parameter
await app.publish(
  AssetParameters(
    parameters=[
      AssetParameter(resource=KRNAssetParameter(asset, "min_treshold"), value=0)
    ],
    resource=KRNAppVersion(target_app_name, "1.0.0")
  )
)
```

### App to App Usage

App Parameters can also be automatically updated from one Kelvin SmartApp™ to another Kelvin SmartApp™.

!!! note ""

    There needs to be an Internet connection to the Kelvin Cloud even if both Kelvin SmartApps™ are deployed to the same Cluster.

IMAGE DESCRIPTION HERE : App parameters can be produced by one app and consumed by another app at the edge.

In the Kelvin SmartApp™ program, it can produce an update App Parameter value(s) to another Kelvin SmartApp™ like this;

```python title="Create and Publish Multiple App Parameters Python Example" linenums="1"
from kelvin.message import AssetParameters, AssetParameter
from kelvin.krn import KRNAppVersion

(...)

# Create and Publish Multiple App Parameters
await app.publish(
  AssetParameters(
    parameters=[
      AssetParameter(resource=KRNAssetParameter(asset, "min_treshold"), value=0), 
      AssetParameter(resource=KRNAssetParameter(asset, "max_treshold"), value=50)
    ],
    resource=KRNAppVersion(target_app_name, "1.0.0")
  )
)
```
