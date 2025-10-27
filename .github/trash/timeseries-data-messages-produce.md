## Timeseries Data

You can update Asset / Data Stream data values on the Kelvin Cloud from the Kelvin SmartApp™.

![](../../../../assets/produce-timeseries-messages-overview.png)

## Structure

### Define Data Stream Names

In order to publish an `output` Data Message, the first requirement is to add the intended Data Stream names to the outputs to the `app.yaml` as follows:

```yaml title="app.yaml Example" linenums="1"
data_streams:
  outputs:
    - name: motor_temperature_fahrenheit
      data_type: number

    - name: motor_error
      data_type: number

    - name: motor_error_description
      data_type: number

    - name: gps_data
      data_type: number
```

### Define Asset Names

The Asset name can only be related to any Assets associated with the Kelvin SmartApp™ workload.

!!! note

    Any attempt to write to Assets not associated with the Kelvin SmartApp™ workload will be dropped and an error recorded in the logs.  

## Timeseries Data Messages

Output (Number/Boolean/String/Object) Objects support the following attribute:

| Attribute | Required     | Description                                                                                 |
|-----------|--------------|---------------------------------------------------------------------------------------------|
| `payload` | **required** | Number, Boolean, String or object value, depending on the `data_type`                               |


You need to create and publish each `output` Data Message according to the Asset / Data Stream's `data_type`.

<div class="result" markdown>

=== "Number"

    ```python title="Create and Publish Number Python Example" linenums="1"
    from kelvin.message import Number
    from kelvin.krn import KRNAssetDataStream
    
    (...)

    # Create and Publish a Number
    await app.publish(
        Number(resource=KRNAssetDataStream(asset, "motor_temperature_fahrenheit"), payload=97.3)
    )
    ```

=== "Boolean"

    ```python title="Create and Publish Boolean Python Example" linenums="1"
    from kelvin.message import Boolean
    from kelvin.krn import KRNAssetDataStream
    
    (...)

    # Create and Publish a Boolean
    await app.publish(
        Boolean(resource=KRNAssetDataStream(asset, "motor_error"), payload=True)
    )
    ```

=== "String"

    ```python title="Create and Publish String Python Example" linenums="1"
    from kelvin.message import String
    from kelvin.krn import KRNAssetDataStream
    
    (...)

    # Create and Publish a String
    await app.publish(
        String(resource=KRNAssetDataStream(asset, "motor_error_description"), payload="Temperature is too high")
    )
    ```

=== "Object"

    For objects, the payload is an arbitrary dict with any given dict structure.

    ```python title="Create and Publish Object Python Example" linenums="1"
    from kelvin.message import String
    from kelvin.krn import KRNAssetDataStream
    
    (...)

    # Create and Publish an Object
    gpsd_dict = {
        "latitude": 90,
        "longitude": 100
    }

    await app.publish(
        Message(
            type=KMessageTypeData(primitive="object", icd="gps"),
            resource=KRNAssetDataStream(asset, datastream),
            payload=gps_dict,
        )
    )
    ```
</div>