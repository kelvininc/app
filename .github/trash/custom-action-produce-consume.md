# Custom Action

## Overview

Custom Actions are used to enable communication between two Kelvin SmartApps™, whether on the same cluster or across different clusters.

They allow developers to create a dedicated Kelvin SmartApp™ to perform specific tasks that are commonly needed by other Kelvin SmartApps™.

!!! example

    For example, you can create a Kelvin SmartApp™ to send emails or perform specific conversion calculations before saving data to the Kelvin Platform.

    The tasks that can be performed are flexible and depend on the developer’s objectives.

Other Kelvin SmartApps™ can then send data to this Kelvin SmartApp™ for processing.

This approach allows you to centralize common tasks or isolate sensitive information, such as email login credentials, within a single Kelvin SmartApp™.

## Structure

Custom Actions require two different types of Applications (Kelvin SmartApps™) to be properly setup;

* **Publisher Application**: Any Kelvin SmartApp™ that packages and sends the custom action either directly or via a Recommendation
* **Consumer Application (Executor)**: A specific Kelvin SmartApp™ that will receive the custom action and performs predefined actions on the payload data

!!! warning

    For each Type declared in any Publisher App, only **ONE** Consumer App (Executor) can be deployed on the Kelvin Platform to receive that Type.

Custom Actions are sent from a Publisher to a Consumer Application.

It can also be packaged into a Recommendation for approval by Operations before the Custom Action is sent to the Consumer App (Executor).

!!! note

    This functionality will work even when there is no internet connectivity as long as the two Applications are on the same Cluster network.

![](../../../../assets/develop-custom-actions.jpg)

Custom Actions has a robust fault tolerant protocol to ensure all custom actions are traceable and will report failures back to the sending Application.

# Produce Custom Actions

## Produce Custom Action Messages

You can use Custom Actions to enable communication between two Applications on either the same cluster or across different clusters.

!!! note

    To understand the purpose of Custom Actions or view the overall structure of how they work, check out the [documentation in the overview page here](../../../../overview/concepts/custom-action.md).

To ensure the Custom Action being sent is handled properly, the `app.yaml` outputs needs to be declared:

!!! note

    You can choose any name for the `type`.

    This is how the Custom Action Manager chooses which Consumer Application (Executor) will receive the Custom Action object.

```yaml title="app.yaml Example" linenums="1"
custom_actions:
  outputs:
    - type: custom-action-name
```

The Custom Action Object supports the following attributes :

| Attribute           | Required     | Default Value | Description                                                                          |
|---------------------|--------------|---------------| -------------------------------------------------------------------------------------|
| `resource`          | **required** |      N/A      | The KRNAsset that this Custom Action is meant for.                                   |
| `type`              | **required** |      N/A      | The name of Custom Action.                                   |
| `title`             | **required** |      N/A      | Title of the Custom Action                                      |
| `description`      | **required** |      N/A      | Description details of the Custom Action                                     |
| `expiration_date`   | **required** |      N/A      | Absolute datetime or a timedelta (from now) when the Control Change will expire.     |
| `payload`           | **required** |      N/A      | The custom information of the Custom Action that will be required by the Consumer Application |
| `trace_id`           | **optional** |      N/A      | A custom id for tracking the Custom Action status |

## Example

In this example we will create a Producer Application that will;

1. Package the email details into a Custom Action Object
1. Send the Custom Action object directly to the Consumer Application (Executor) for processing.
1. Package the Custom Action object in a Recommendation and publish the "Recommendation with Custom Action" to the Kelvin UI for approval. (Typically, you would choose either direct sending or publishing with a Recommendation—not both.)

Check out the [Consume Custom Actions documentation here](../consume/custom-actions.md) to see how to receive this Custom Action in a Consumer Application (Executor).

**app.yaml**

```yaml title="app.yaml Example" linenums="1"
spec_version: 5.0.0
type: app            # Any app type can handle and/or publish custom actions.

name: hello-app
title: Hello App
description: Lorem ipsum dolor sit amet, consectetur adipiscing elit
version: 1.0.0

custom_actions:
  outputs:
    - type: email

  ...
```

**Publisher Application**

```python title="main.py Example" linenums="1"
from kelvin.message import Recommendation, CustomAction

asset = KRNAsset("air-conditioner-1")

###
# Directly
#
action = CustomAction(resource=asset,
  type="email",
  title="Recommendation to reduce speed",
  description="It is recommended that the speed is reduced",
  expiration_date=datetime.now() + timedelta(hours=1),
  payload={
    "to": "operations@example.com",
    "subject": "Recommendation to reduce speed",
    "body": "This is the email body",
  },
  trace_id="my-trace-id")
app.publish(action)

###
# Or embedded in a recommendation   
#
rec = Recommendation(resource=asset,
  type="Reduce speed",
  actions=[action],
)
app.publish(rec)
```


# Consume Custom Actions

## Consume Custom Action Messages

You can use Custom Actions to enable communication between two Applications on either the same cluster or across different clusters.

!!! note

    To understand the purpose of Custom Actions or view the overall structure of how they work, check out the [documentation in the overview page here](../../../../overview/concepts/custom-action.md).

To ensure the Custom Action being sent is handled properly, the `app.yaml` outputs needs to be declared:

!!! note

    You can choose any name for the `type`.

    This is how the Custom Action Manager chooses which Consumer Application (Executor) will receive the Custom Action object.

!!! warning

    For each Type declared in any Publisher App, only **ONE** Consumer Application (Executor) can be deployed on the Kelvin Platform to receive that Type.

    Multiple Consumer Application (Executor) with the same TYPE is not supported.

```yaml title="app.yaml Example" linenums="1"
custom_actions:
  inputs:
    - type: custom-action-name
```

The Custom Action Object supports the following attributes :

| Attribute           | Required     | Default Value | Description                                                                          |
|---------------------|--------------|---------------| -------------------------------------------------------------------------------------|
| `resource`          | **required** |      N/A      | The KRNAsset that this Custom Action is meant for.                                   |
| `type`              | **required** |      N/A      | The name of Custom Action.                                   |
| `title`             | **required** |      N/A      | Title of the Custom Action                                      |
| `description`      | **required** |      N/A      | Description details of the Custom Action                                     |
| `expiration_date`   | **required** |      N/A      | Absolute datetime or a timedelta (from now) when the Control Change will expire.     |
| `payload`           | **required** |      N/A      | The custom information of the Custom Action that will be required by the Consumer Application |
| `trace_id`           | **optional** |      N/A      | A custom id for tracking the Custom Action status |

The Custom Action Result Object supports the following attributes :

| Attribute           | Required     | Default Value | Description                                                                          |
|---------------------|--------------|---------------| -------------------------------------------------------------------------------------|
| `success`          | **required** |      N/A      | Whether the Custom Actions were completed successfully. Boolean `True` or `False`.         |
| `message`              | **optional** |      N/A      | Any message to return to the Publishing Application.                                   |
| `metadata`             | **optional** |      N/A      | Any additional metadata that needs to be returned to the Publishing Application  |
| `action_id`             | **optional** |      N/A      | The `id` of the Custom Action Object  |
| `resource`             | **optional** |      N/A      | The KRNAsset that this Custom Action is meant for. |

## Example

In this example we will create a Consumer Application (Executor) that will;

1. Listen and receive any new Custom Action objects with the type `email`.
1. Extract the relevant email information from the `payload`
1. Connect to an SMTP and send the email (This function is defined but not fully coded)
1. Return the status of the Custom Action (`True` or `False`)

Check out the [Produce Custom Actions documentation here](../produce/custom-actions.md) to see how to send this Custom Action from the Publisher Application.

**app.yaml**

```yaml title="app.yaml Example" linenums="1"
spec_version: 5.0.0
type: app            # Any app type can handle and/or publish custom actions.

name: hello-app
title: Hello App
description: Lorem ipsum dolor sit amet, consectetur adipiscing elit
version: 1.0.0

custom_actions:
  inputs:
    - type: email

  ...
```

**Publisher Application**

```python title="main.py Example" linenums="1"
import asyncio

from kelvin.application import KelvinApp
from kelvin.message import CustomAction, CustomActionResult

async def send_mail(recipient, subject, body):
    
    # Specific code for sending an email.

async def on_custom_action(action: CustomAction):
		if action.type == "email":
		    try:
				###
				# Receive the expected Custom Action
				#
		    
				# action.{action-specific-fields} are accessible
		        send_mail(action.payload.get("recipient"),
		                  action.payload.get("subject"),
		                  action.payload.get("body")

				###
				# Send the result of the action execution
				#
		        result = action.result(success=True,
		                               message="",
		                               metadata={}))
		        self.app.publish(result)
			    #
		        # or
		        #
		        self.app.publish(CustomActionResult(success=True,
		                                            action_id=action._msg.id,
										            resource=action.resource,
										            metadata={}))
		    except Exception as e:
		        self.app.publish(action.result(success=False, message=":(")

async def main() -> None:
    app = KelvinApp()
    app.on_custom_action = on_custom_action

    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
```


