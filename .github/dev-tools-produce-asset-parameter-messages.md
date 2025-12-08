## App Parameter Messages

Kelvin SmartApps™ can publish an `App Parameter` Message in order to (asynchronously) update a given App Parameter for a given Asset.

The App Parameter update will persist as soon as this message is synced with the Kelvin Cloud.

!!! note

    A user can also change the App Parameter value through the Kelvin UI.

    Any changes done automatically by an application will be updated on the Kelvin UI screen.

![](../../../../assets/asset-parameters-overview.jpg)

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

app = KelvinApp()

@app.timer(interval=10)
async def publish_data():

    # Create and Publish App Parameter
    await app.publish(
      AssetParameters(
        parameters=[
          AssetParameter(resource=KRNAssetParameter(asset, "min_treshold"), value=0)
        ],
        resource=KRNAppVersion(target_app_name, "1.0.0")
      )
    )

app.run()
```

### App to App Usage

App Parameters can also be automatically updated from one Kelvin SmartApp™ to another Kelvin SmartApp™.

!!! note ""

    There needs to be an Internet connection to the Kelvin Cloud even if both Kelvin SmartApps™ are deployed to the same Cluster.

![](../../../../assets/produce-asset-parameters-messages-app-to-app.jpg)

In the Kelvin SmartApp™ program, it can produce an update App Parameter value(s) to another Kelvin SmartApp™ like this;

```python title="Create and Publish Multiple App Parameters Python Example" linenums="1"
from kelvin.message import AssetParameters, AssetParameter
from kelvin.krn import KRNAppVersion

app = KelvinApp()

@app.timer(interval=10)
async def publish_data():

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

app.run()
```