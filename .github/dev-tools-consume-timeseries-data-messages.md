## Timeseries Data Messages

!!! note

    Visit the [concept overview for Data Streams](../../../../overview/concepts/data-stream.md) to understand how time series data references are constructed using one Asset name and one Data Stream name as a pair.

Timeseries data from Assets can be served to the Kelvin SmartApp™ in multiple ways, depending on the preferred data consumption method.

![Overview](../../../../assets/develop-consume-produce-overview.jpg)

### `app.yaml` setup

To consume streaming data, you must define the `inputs` section in the `app.yaml` file.

!!! note

    That means that Kelvin SmartApps™ is only going to be able to consume the specified inputs. i.e.:

```yaml title="app.yaml Example" linenums="1"
data_streams:
  inputs:
    - name: motor_temperature
      data_type: number
    - name: motor_state
      data_type: string
```

`inputs` is an array (list) composed by two fields:

* A **unique name** to identify the input. This will be used in the Python code to reference the input. It must contain only lowercase alphanumeric characters. The characters `.`, `_` and `-` are allowed to separate words instead of a space BUT can not be at the beginning or end of the name.
* An **expected data type**, which can be: `number`, `boolean` or `string`.

Now that the Kelvin SmartApps™ inputs are defined, use one of the following methods to monitor and react to new incoming messages.

### Stream Decorators (Preferred)

The preferred and simplest method for consuming incoming timeseries data is to create a **Stream Decorator** function.

You use the Data Stream filter to process only the relevant data.

!!! note

    You can use filtering to only react and process specific incoming messages.

!!! note

    You can see a full list of stream decorators available in the [SDK documentation section here](../../../sdk/app/sdk-python-messages.md#message-handling).

```python title="Stream Decorators Method (preferred)" linenums="1"
from kelvin.application import KelvinApp
from kelvin.message.typing import AssetDataMessage

app = KelvinApp()

# Filter by input data stream example 1
@app.stream(inputs=["temperature", "pressure"])
async def handle_specific_inputs(msg: AssetDataMessage) -> None:
    print(f"From specific inputs: {msg.payload}")

# Filter by input data stream example 2
async def handle_inputs(msg: AssetDataMessage) -> None:
    print(f"From specific inputs: {msg.payload}")

app.stream(handle_inputs, inputs=["humidity"])

app.run()
```

### Callbacks (Advanced)

For advanced scenarios, you can define callbacks for specific lifecycle events.

Callbacks work on a "per asset" message, so you will need to manually program filters for individual data stream processing.

The callback `on_asset_input` can be used to read every input flowing into Kelvin SmartApps™:

```python title="Timeseries Data Callback Python Example" linenums="1"
from kelvin.application import KelvinApp, AssetInfo
from kelvin.message.typing import AssetDataMessage

app = KelvinApp()

async def on_asset_input(msg: AssetDataMessage):
    """Called for data messages from asset inputs"""
    print(f"Data from {msg.resource}: {msg.payload}")

# Assign callbacks
app.on_asset_input = on_asset_input

app.run()
```

### Asynchronous Consumption

This approach pauses program execution until new data arrives, resuming only when data is available. To enhance efficiency and reduce unnecessary executions, filters can also be applied to limit the types of data that trigger events.

<div class="result" markdown>

=== "AsynGenerator"

    Streams are a different way of filtering inputs as a **Python Async Generator**, also based upon a filter function.

    !!! info

        Different Data _filters_ are available within the `filters` class, such as `input_equals(input: str)`, `resource_equals(resource: KRN)` and `asset_equals(asset: str)`. On the following example we're gonna use the most common and expected use case (`input_equals(input: str)`).

    Filters to limit which inputs are monitored can be expressed as `filters.input_equals(input: str)`.

    ```python title="Streams (with AsynGenerator) Python Example" linenums="1"
    import asyncio
    from typing import AsyncGenerator # AsyncGenerator import

    from kelvin.application import KelvinApp, filters # filters import
    from kelvin.message import Number # Number (Input Type) import


    async def main() -> None:
        app = KelvinApp()

        # Create a Filtered Stream with Temperature (Number) Input Messages
        motor_temperature_msg_stream: AsyncGenerator[Number, None] = app.stream_filter(filters.input_equals("motor_temperature"))

        await app.connect()

        # Wait & Read new Temperature Inputs
        async for motor_temperature_msg in motor_temperature_msg_stream:
            print("Received Motor Temperature: ", motor_temperature_msg)


    if __name__ == "__main__":
        asyncio.run(main())
    ```

=== "Queue"

    Filters can be used to filter a specific subset of the Kelvin Inputs as a **Python Message Queue** based upon a filter function.

    !!! info

        Different Data _filters_ are available within the `filters` class, such as `input_equals(input: str)`, `resource_equals(resource: KRN)` and `asset_equals(asset: str)`. On the following example we're gonna use the most common and expected use case (`input_equals(input: str)`).

    Filters to limit which inputs are monitored can be expressed as `filters.input_equals(input: str)`.

    ```python title="Streams (with Queue) Python Example" linenums="1"
    import asyncio
    from asyncio import Queue # Queue import

    from kelvin.application import KelvinApp, filters # filters import
    from kelvin.message import Number # Number (Input Type) import


    async def main() -> None:
        app = KelvinApp()

        # Create a Filtered Queue with Temperature (Number) Input Messages
        motor_temperature_msg_queue: Queue[Number] = app.filter(filters.input_equals("motor_temperature"))

        await app.connect()

        while True:
            # Wait & Read new Temperature Inputs
            motor_temperature_msg = await motor_temperature_msg_queue.get()

            print("Received Motor Temperature: ", motor_temperature_msg)


    if __name__ == "__main__":
        asyncio.run(main())
    ```

</div>

## Filters

When working with queues or async streams, you can apply filters to receive only the timeseries data that matches your criteria.

!!! note

    In our earlier examples above you will see how we use filters.

### Built-in Filters

There are a number of built-in filters available.

#### By Data Stream Name

You can receive Messages that only have certain Data Stream names.

```python title="Filter by input data stream name(s)" linenums="1"
filters.input_equals("temperature")
filters.input_equals(["temperature", "pressure"])
```

#### By Asset Name

You can receive Messages that only have certain Asset names.

```python title="Filter by asset name(s)" linenums="1"
filters.asset_equals("my-asset")
filters.asset_equals(["asset-1", "asset-2"])
```

#### By KRN Resource

You can receive Messages that only have certain Resources by Kelvin Resource Name (KRN).

!!! note

    You can see a full list of KRN names in [Developer Tools KRN page here](../krn.md).

```python title="Filter by resource KRN" linenums="1"
filters.resource_equals(krn_instance)
filters.resource_equals([krn1, krn2])
```

#### By Message Type

You can receive certain types of Messages only.

```python title="Filter by message type" linenums="1"
filters.is_data_message(msg)
filters.is_asset_data_message(msg)
filters.is_control_status_message(msg)
filters.is_custom_action(msg)
filters.is_data_quality_message(msg)
```

### Custom Filters

You can also create your own custom filters.

For example, you only want to receive Messages where the value is greater than 100.

```python title="Custom Filter Example" linenums="1"
def custom_filter(msg: Message) -> bool:
    """Filter for high-value readings"""
    return msg.payload > 100

queue = app.filter(custom_filter)
```