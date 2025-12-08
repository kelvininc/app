# Control Changes

## Control Change Data Messages

When control changes are initiated by any Application on the Kelvin Platform, they can be processed by any Application.

## Stream Decorators (Preferred)

The preferred and simplest method for consuming incoming control change messages is to create a Stream Decorator function and add a filter for Control Changes.

!!! Note

    You can filter by assets or datastreams to react only to specific incoming messages.

```py title="Stream Decorators for Control Changes" linenums="1"
from kelvin.application import KelvinApp
from kelvin.message.typing import AssetDataMessage

app = KelvinApp()

@app.stream()
async def handle(msg: AssetDataMessage):
    if app.msg_is_control_change(msg):
        print(f"Control change: {msg.payload}")

app.run()
```

## Callbacks

**Event Callbacks** are functions that are triggered when a control change is initiated.

![](../../../../assets/event-callbacks-overview.jpg)

### Video Tutorial

You can watch this **Event Callback** video tutorial which will show you how to program and test it on you local machine with the Kelvin test data generator Python script.

!!! success "Copy the code in the Video Tutorial"

    In the following chapters after the video tutorial you can see and copy all the scripts shown in the video tutorial.

<iframe width="800" height="450" src="https://www.youtube.com/embed/L_ZWngLzd0M?si=eXnTI9GHnRj1TKt_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### Control Change Data Event

When any new control change is initiated, a callback event is created.

??? note "Detailed Explanation of Parameters"

    **Response Parameters**

    - **id**: UUID('db18aaaf-9a70-4c3e-babb-b7571867871f')  
        - **Description**: A unique random generated UUID as the key `id` for the control change object.

    - **type**: KMessageTypeData('data', 'pt=number')  
        - **Options**: `number`, `boolean`, `string`  
        - **Description**: The format of the data to expect.

    - **trace_id**: UUID('db18aaaf-9a70-4c3e-babb-b7571867871f')

    - **timestamp**: datetime.datetime(2024, 10, 28, 11, 51, 44, 601689, tzinfo=datetime.timezone(datetime.timedelta(seconds=25200), '+07'))  
        - **Description**: The time of recording of the time series data in the local computer's timezone.

    - **resource**: KRNAssetDataStream(asset='test-asset-1', data_stream='sa-rw-number')  
        - **Description**: The Asset and Data Stream names associated with the control change.

    - **payload**: The actual value in the declared `type` key format.


The full code is given here for the `main.py` script.

!!! success "Detailed Code Explanations"

    Click on the :fontawesome-solid-circle-plus:{ .code-descriptions } for details about the code

```py title="main.py" linenums="1"
from kelvin.application import KelvinApp # (1)!
from kelvin.message.typing import AssetDataMessage # (2)!

async def on_control_change(msg: AssetDataMessage): # (3)!
    # Get Asset and Value
    asset = msg.resource.asset
    value = msg.payload

    print("Received Control Message: ", msg)
    print(f"Asset: {asset}, Value: {value}")

app.run()
```

1. The `KelvinApp` class is used to initlize and connect the Kelvin SmartApp™ to the Kelvin Platform.
2. The `AssetDataMessage` is a class representing the structure and properties of the asset data messages which will be held in an instance called `msg`.
3. The `on_control_change` callback function is triggered automatically whenever a new control change object is initiated to an Asset associated with the Kelvin SmartApp™. It serves as an event handler to process incoming control change data in real time, ensuring that relevant review, actions or data updates occur immediately upon receipt.

When you run this Python script, the following output will be view in the terminal or logs;

```bash title="Output from Program" linenums="1"
Received Control Message:  id=UUID('44ba34f7-6689-464f-9804-7bcc0e347f68') type=KMessageTypeData('data', 'pt=number') trace_id=None source=None timestamp=datetime.datetime(2024, 10, 28, 14, 29, 41, 553346, tzinfo=datetime.timezone(datetime.timedelta(seconds=25200), '+07')) resource=KRNAssetDataStream(asset='test-asset-1', data_stream='sa-cc-number') payload=20.0

Asset: test-asset-1, Value: 20.0
```

## App to App

Control Changes can be sent from one Kelvin SmartApp to another.

!!! success ""

    This can also operate even if the edge device does not have any Internet connection.

    The only stipulation is that the Kelvin SmartApp™ that produces the control change object and the Kelvin SmartApp™ or Connector that consumes the control change object are hosted on the same Cluster and have local communications if they are hosted on different Nodes.

![](../../../../assets/produce-control-change-messages-offline.jpg)

### Producing App

To set this up, the `app.yaml` file of the Kelvin SmartApp™ that produces the control change object must be defined under the `control_change` key.

```yaml title="app.yaml Example" linenums="1"
control_changes:
  outputs:
    - name: motor_speed_set_point
      data_type: number
```

Then you can produce a Control Change to be sent to another Kelvin SmartApp™.

!!! note ""

    This is a simple Control Change example.

    Read the [Control Change Produce](../produce/control-change-messages.md#examples) page to see all the types of Control Changes you are produce.

```python title="Simple Control Change Python Example" linenums="1"
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.message import ControlChange
from kelvin.krn import KRNAssetDataStream

(...)

# Create and Publish a Control Change
await app.publish(
    ControlChange(
        resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
        payload=1000,
        expiration_date=timedelta(minutes=5)
    )
)
```

### Consuming App

and the Kelvin SmartApp™ that consumes the control change object must define the input Data Stream with the `control_change` key.

```yaml title="app.yaml Example" linenums="1"
control_changes:
  inputs:
    - name: motor_speed_set_point
      data_type: number
```

Then you can consume a Control Change that has been sent by another Kelvin SmartApp™.

```python title="Consume Control Change Python Example" linenums="1"

async def on_control_change(cc: AssetDataMessage) -> None:
    
    """Callback when a Control Change is received."""
    print("Received Control Change: ", cc)

```

You can also see the control change status with this code;

```python title="Control Change Event Python Example" linenums="1"
from kelvin.message import ControlChangeStatus

(...)

async def on_control_status(cc_status: ControlChangeStatus) -> None:
    """Callback when a Control Status is received."""
    print("Received Control Status: ", cc_status)
```

!!! note ""

    If the consumer is a Connector, then this key is automatically set using the Kelvin Connector setup process. It will automatically receive the control change object directly from the Kelvin SmartApp™ without requiring any connection to the Kelvin Cloud.


## Data Generator for Local SmartApp Testing

Easily test your SmartApp locally on your computer.

Comprehensive documentation is available for the **Generator Tool**. [Click here](../test/generator.md) to learn how to use this event callback script with the Test Generator on the "Test a SmartApp" ⟹ "Generator" page.