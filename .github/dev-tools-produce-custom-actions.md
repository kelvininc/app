# Custom Actions

## Produce Custom Action Messages

You can use Custom Actions to enable communication between two Applications on either the same cluster or across different clusters.

!!! note

    To understand the purpose of Custom Actions or view the overall structure of how they work, check out the [documentation in the overview page here](../../../../overview/concepts/custom-action.md).

<iframe width="800" height="450" src="https://www.youtube.com/embed/jMD7oIb6Vf4?si=OWBkhHJAC6yfMnSz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

To ensure the Custom Action being sent is handled properly, the `app.yaml` outputs needs to be declared:

!!! note

    You can choose any name for the `type`.

    This is how the Custom Action Manager chooses which Consumer Application (Executor) will receive the Custom Action object.

```yaml title="app.yaml Example" linenums="1"
custom_actions:
  outputs:
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
import asyncio
from datetime import timedelta, datetime

from kelvin.application import KelvinApp
from kelvin.krn import KRNAsset
from kelvin.message import Recommendation, CustomAction

app = KelvinApp()

@app.timer(interval=10)
async def publish_data():

    asset = KRNAsset("air-conditioner-1")
    
    # Direct Custom Action
    action = CustomAction(resource=asset,
    type="email",
    title="Recommendation to reduce speed",
    description="It is recommended that the speed is reduced",
    expiration_date=datetime.now() + timedelta(hours=1),
    payload={
        "recipient": "operations@example.com",
        "subject": "Recommendation to reduce speed",
        "body": "This is the email body",
    })
    await app.publish(action)


    # Or embedded the Custom Action into a Recommendation   
    rec = Recommendation(resource=asset,
    type="Reduce speed",
    actions=[action],
    )
    await app.publish(rec)

app.run()
```