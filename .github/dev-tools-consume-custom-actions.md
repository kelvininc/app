# Custom Actions

## Custom Action Data Messages

You can use Custom Actions to enable communication between two Applications on either the same cluster or across different clusters.

!!! note

    To understand the purpose of Custom Actions or view the overall structure of how they work, check out the [documentation in the overview page here](../../../../overview/concepts/custom-action.md).

<iframe width="800" height="450" src="https://www.youtube.com/embed/jMD7oIb6Vf4?si=OWBkhHJAC6yfMnSz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

As a consumer of Custom Action Messages, this Application is defined as Consumer (Executor) Application.

!!! note

    The Publisher Application which outputs Custom Actions to a Consumer (Executor) Application, is discussed in detail in the [Produce Custom Action section here](../produce/custom-actions.md).

To ensure the Custom Action Messages are handled properly, the `app.yaml` inputs needs to be declared:

!!! warning

    Only **ONE** Consumer (Executor) Application can be deployed on the Kelvin Platform to receive each Type name.

    Multiple Consumer (Executor) Applications with the same TYPE name is not supported.

```yaml title="app.yaml Example" linenums="1"
custom_actions:
  inputs:
    - type: custom-action-name
```

The Custom Action Object in the `main.py` script supports the following attributes :

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

## Consumer App Example

In this example we will create a Consumer (Executor) Application that will;

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

**Consumer (Executor) Application**

```python title="main.py Example" linenums="1"
from kelvin.application import KelvinApp
from kelvin.message import CustomAction, CustomActionResult

app = KelvinApp()

async def send_mail(recipient, subject, body):
    print(f"Sending email to {recipient}")

async def on_custom_action(action: CustomAction):
    if action.type == "email":
        try:
            await send_mail(
                action.payload.get("recipient"),
                action.payload.get("subject"),
                action.payload.get("body")
            )

            await app.publish(CustomActionResult(
                success=True,
                action_id=action._msg.id,
                resource=action.resource,
                metadata={}
            ))

        except Exception as e:
            await app.publish(action.result(success=False, message=str(e)))

app.on_custom_action = on_custom_action

app.run()
```