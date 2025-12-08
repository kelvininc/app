# Kelvin SmartApps™ Configuration

You can learn more about [App Configurations in the Overview ⟶ Concepts page](../../../overview/concepts/variables/app-configurations.md).

## Creating App Configurations

The configuration variable names and values are defined in the Kelvin SmartApp™'s `app.yaml` file as `configuration`.

Configurations can also be optionally defined in the `ui_schemas` that provides a link to a JSON file containing all the information about how to display Configurations in the Kelvin UI.

!!! note

    Operations will have the option to change these at runtime from the Kelvin UI.

!!! note

    If you use the Data Types, then a full list of Data Types is available at [overview concepts page here](../../../overview/concepts/variables/app-configurations.md#data-type).

```yaml title="app.yaml Example" linenums="1"
ui_schemas:
  configuration: "ui_schemas/configuration.json"

defaults:
  configuration:
    broker-ip: edge-mqtt-broker
    broker-port: 1883
    nest-example:
      nest1: 25
      next2: 30
```

For the `configuration.json` file you can define all the information for the Kelvin UI. This can be the title, type of input required and limitations of the values allowed.

It will look something like this.

```json title="sample ui_schema/configuration.json" linenums="1"
{
  "type": "object",
  "properties": {
    "broker-ip": {
      "type": "string",
      "title": "Broker IP Address"
    },
      "broker-port": {
      "type": "number",
      "title": "Broker Port Number",
      "minimum": 0,
      "maximum": 65535
    }
  },
  "required": ["broker-ip", "broker-port"]
}
```
## Get Configuration Values

This is how to access the global configuration variables in a Kelvin SmartApp™:

```python title="Get Configuration Values Python Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    (...)

    # Get IP
    ip = app.app_configuration["broker-ip"]
```
!!! info

    `app.app_configuration` will only be available after `app.connect()`

You can also get nested App Configuration values;

```python title="Get Nested Configuration Values Python Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp


async def main() -> None:
    app = KelvinApp()
    await app.connect()

    (...)

    # Get IP
    ip = app.app_configuration["nest-example"]["nest1"]
```

## Updating Configuration Values

Developers and Administrators can update these values through the Kelvin API without needing to re-upload the complete Kelvin SmartApp™ or Kelvin UI.

![](../../../assets/produce-configuration-messages-upgrade-smartapp.jpg)

To update the configuration values dynamically, you use the Kelvin API endpoint `/workloads/{workload_name}/configurations/update`.

!!! note

    The configurations values are applied directly to a workload. This will not affect the values in the App Registry.

    If you have a Kelvin SmartApp™ deployed as many workloads, the updates will only affect the workload you target.

```bash title="API cURL Example" linenums="1"
    curl -X 'POST' \
  "https://<url.kelvin.ai>/api/v4{workloads/<workload_name}/configurations/update" \
  -H "Authorization: Bearer <Your Current Token>" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "configuration": {
    "recommendations": [
      {
        "description": "Water level increasing, higher pump speed will lead water level to return to optimal.",
        "setpoint": {
          "name": "speed_sp",
          "variation_factor": 0.1
        },
        "type": "increase_speed"
      },
      {
        "description": "Production gain possible after step test, with higher pump speed",
        "setpoint": {
          "name": "speed_sp",
          "variation_factor": 0.1
        },
        "type": "increase_speed"
      },
      {
        "description": "Erratic Torque detected at this speed previously, lower pump speed will reduce vibrations",
        "setpoint": {
          "name": "speed_sp",
          "variation_factor": -0.1
        },
        "type": "decrease_speed"
      },
      {
        "description": "Reducing Speed will save energy and keep production levels constant",
        "setpoint": {
          "name": "speed_sp",
          "variation_factor": -0.1
        },
        "type": "decrease_speed"
      },
      {
        "description": "Above max Drawdown, parameters stable",
        "setpoint": null,
        "type": "no_action"
      },
      {
        "description": "Casing Pressure Event Detected, no changes allowed",
        "setpoint": null,
        "type": "no_action"
      },
      {
        "description": "No action - monitoring",
        "setpoint": null,
        "type": "no_action"
      }
    ]
  }
}'
```

## Upgrading Kelvin SmartApps™

When a Kelvin SmartApp™ is upgraded, Kelvin automatically propagates all matching App Configuration values from the previous version to the new version.

For any new App Configurations introduced in the upgraded Kelvin SmartApp™ version, the default values will initially applied to the Workload.


