# Create a Kelvin SmartApp™

!!! success ""

    You can build for both x86\_64 and arm64 devices.

```bash title="create default application" linenums="1"
$ kelvin app create <SMARTAPP_NAME>
```

This will give a response similar to this;

```bash title="command output" linenums="1"
[kelvin.sdk][2025-03-19 18:39:54][I] Refreshing metadata..
Please provide a name for the application: event-detection
```

After providing Kelvin SmartApps™ name (i.e.: **event-detection**):

```bash title="command output" linenums="1"
[kelvin.sdk][2025-03-19 18:43:36][I] Creating new application "event-detection"
[kelvin.sdk][2025-03-19 18:43:36][I] Retrieving the latest schema version
[kelvin.sdk][2025-03-19 18:43:39][R] Successfully created new application: "event-detection".
```

This will automatically create a Kelvin SmartApp™ bootstrap within a directory named as `event-detection` populated with some default files and configurations.

## Folder Structure

You can now open the folder in your favorite IDE or editor and start to modify the files to create your Kelvin SmartApp™.

```bash title="default folder structure" linenums="1"
$ cd event-detection
$ tree ./
├── Dockerfile
├── app.yaml
├── main.py
├── requirements.txt
└── schemas
    ├── configuration.json
    └── parameters.json
```

Below is a brief description of each file.

### app.yaml

The `app.yaml` is the main configuration file that holds both Application definitions as well as the deployment/runtime configuration.

!!! info ""

    This file is used for Kelvin SmartApps™, Docker Apps, Imports (Connectors) and Exports.

    On this page we are only focused on the Kelvin SmartApps™ options. 

It is composed of the following sections:

#### spec_version key

The `spec_version` key is automatically injected and specifies Kelvin SmartApps™ [JSON Schema](https://apps.kelvininc.com/schemas/kelvin/5.0.0/app.json) (_latest_) version which both defines and validates the `app.yaml` structure.

```yaml title="spec_version" linenums="1"
spec_version: 5.0.0
```

#### type

This defines the type for the application.

* `app`: A Smart App that allows mapping inputs and outputs to data streams, sending control changes, recommendations, and data tags.
* `docker`: An docker application that does not connect to the platform's data streams.
* `importer`: Connects to an external system to import data into the platform as well as receive control changes to act on the external system.
* `exporter`: Connects to the platform to export data to an external system.

```yaml title="application type" linenums="1"
type: app
```

#### info

The root section holds Kelvin SmartApp™ basic information required to make itself uploadable to _Kelvin's App Registry_.

```yaml title="application info" linenums="1"
name: event-detection
title: Event Detection
description: Monitors if a motor is overheating. If so, it will send a Control Change to reduce the Motor Speed.
version: 1.0.0
category: smartapp    # Optional
```

The `name` is Kelvin SmartApp™ unique identifier.

The `title` and `description` will appear on the Kelvin UI once Kelvin SmartApps™ is uploaded.

![](../../../assets/kelvin-sdk-kelvin-app-yaml-info.png)

The `version` defines the version of this Kelvin SmartApp™ and is used in the Kelvin UI.

!!! info

    The `version` should be bumped every time Kelvin SmartApps™ gets an update, and before it gets uploaded to the _App Registry_.

The `category` will decide which group in the Applications dashboard of the Kelvin UI the Kelvin SmartApp™ will be placed by default.

!!! info

    This is an optional key.

    Operations will still be able to change the group the Kelvin SmartApp™ is associated with through the Kelvin UI.

![](../../../assets/applications_dashboard_groups.png)

#### flags

This is where you are able to set some of the Application's capabilities.

```yaml title="application flags" linenums="1"
flags:
  enable_runtime_update:

    # Reload Application Configuration in runtime
    configuration: false

    # Enables the deployment of assets in runtime
    resources: false

    # Reload Asset Parameters in runtime
    parameters: true

    # Reload Asset Properties in runtime
    resource_properties: true
```

#### data_streams

This defines the inputs and outputs for the Kelvin SmartApp™

!!! warning

    If you are generating Control Changes to an Asset through a Connector, then you will need to declare these outputs in the `control_changes` section which is documented in the next tab.

```yaml title="application data streams" linenums="1"
data_streams:
  inputs:
    - name: temp_f
      data_type: number
    - name: speed_sp_out
      data_type: number
        
  outputs:
    - name: temp_c
      data_type: number
```

#### data_quality

This defines the Data Streams that will have data quality validation monitoring. These validations help detect issues ensuring the integrity and reliability of the data within the Kelvin Platform.

| Stream | Quality Parameters | Description |
| --- | --- | -- |
| `inputs` |  | Applications can connect to and receive the results in real time of a Data Quality validation calculations |
|  | `name` | The name of the Data Quality validation. Below is a list of the inbuilt Kelvin Data Quality validations. Custom validations can also be developed by users |
|  | `data_type` | The Data Type expected. Full documentation on the data types is found in [the overview here](../../../overview/concepts/data-stream.md#data-type) |
|  | `data_streams` | A list of Data Streams to subscribe to. This must also be declared under the `data_streams` key mentioned above. |
| `outputs` |  | Defined for the application that will act as a Data Quality Validator and perform validation calculation for Data Quality outputs |
|  | `name` | The name of the Data Quality validation. Other Applications can then subscribe to this Data Quality Application using this name as an `input` |
|  | `data_type` | The Data Type expected. Full documentation on the data types is found in [the overview here](../../../overview/concepts/data-stream.md#data-type) |
|  | `data_streams` | A list of Data Streams that will be monitored and validated. This must also be declared under the `data_streams` key mentioned above. |

```yaml title="application data quality" linenums="1"
data_quality:
  inputs:
    - name: kelvin_duplicate_detection # !! ALLOWED: kelvin_ or others
      data_type: number
      data_streams:
        - temperature
        - gas_flow

  outputs:
    - name: custom_score # !! NOT ALLOWED: kelvin_
      data_type: number
      data_streams:
        - temperature
        - gas_flow
```

There are a number of inbuilt Data Quality validation options available. Use the appropriate validation as the `name` key value.

| Validation | Description | Configurable Parameters |
| --- | --- | --- |
| kelvin_timestamp_anomaly | Detects anomalies or irregularities in the timestamp sequence | None |
| kelvin_duplicate_detection | Detects duplicate values within a defined window size | window_size (default: 5) |
| kelvin_out_of_range_detection | Validates whether values fall within an expected range | min_threshold, max_threshold |
| kelvin_outlier_detection | Uses statistical methods to detect outliers over a moving window | model, threshold (default: 3), window_size (default: 10) |
| kelvin_data_availability | Ensures expected number of messages are received in a given time window | window_expected_number_msgs, window_time_interval_unit (second, minute, hour, day) |

If you want to reference these inputs and outputs using KRN, they are defined differently from the standard Asset and Data Stream KRN. See the [KRN definitions](./krn.md#data-quality-asset-data-stream) for more details.

#### control_changes

This defines the data streams that are allowed to handle control changes.

!!! note ""

    You do not need to declare the Data Stream in the `data_streams` and `control_changes` sections. Either depending on its role in the Kelvin SmartApp™ is sufficient.

```yaml title="application data streams with control change flag" linenums="1"
control_changes:
  inputs:
    - name: inter_app_value
      data_type: number

  outputs:
    - name: speed_sp_out
      data_type: number
    - name: control_mode
      data_type: number
    - name: scada_mode
      data_type: number
```    

#### parameters

Kelvin SmartApp™ App Parameters are defined in three sections in the `app.yaml` file;

* `parameters` defines the name and type of the App Parameter.
* `ui_schemas` (this section) is a link to a JSON file containing all the information about how to display App Parameters in the Kelvin UI.
* `defaults` / `parameters` [define the default values](#defaults) assigned to each Asset when it is first created or when a Kelvin SmartApp™ update introduces a new App Parameter to existing Assets.

Each parameter can be defined by four different `data_types`. Full documentation on the different `data_types` is in the [concept overview page](../../../overview/concepts/data-stream.md#data-type).

In the `app.yaml` file it will look like this;

!!! note

  Defaults section is explained in detail in the `defaults` tab.

```yaml title="app parameters" linenums="1"
parameters:
  - name: closed_loop
    data_type: boolean
  - name: speed_decrease_set_point
    data_type: number
  - name: temperature_max_threshold
    data_type: number

ui_schemas:
  parameters: "schemas/parameters.json"

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

#### ui_schemas

This is where the Kelvin SmartApp™ configuration and Kelvin SmartApp™ Parameters are defined for the Kelvin UI.

The actual information is kept in a `json` file in the schemas folder of the project. The file location is defined in the `app.yaml` file like this;

```yaml title="application ui schemas" linenums="1"
ui_schemas:
  # Application Configuration Schema
  configuration: "ui_schemas/configuration.json"

  # Asset Parameters Schema
  parameters: "ui_schemas/parameters.json"
```

The json files will come with default blank schemas when first created.

!!! note

    `configuration.json` information is optional, and if not provided, the Kelvin UI will display the configuration settings in a raw JSON or YAML file format without verifying the structure or content before applying them to the Kelvin SmartApp™.


```json title="default ui_schemas/configuration.json" linenums="1"
{
    "type": "object",
    "properties": {},
    "required": []
}
```

!!! note

    `ui_schemas/parameters.json` information is optional, and if not provided, the Kelvin UI will display a simple UI interface with the keys as the titles and no restrictions beyond the type of input.

```json title="default ui_schemas/parameters.json" linenums="1"
{
    "type": "object",
    "properties": {},
    "required": []
}
```

An example of a App Parameters JSON file filled in would look something like this;

```json title="sample ui_schemas/parameters.json" linenums="1"
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

Which will be displayed on the Kelvin UI like this:

![App Parameters](../../../assets/qs-create-app-asset-parameters.jpg)

#### defaults

This section hold four main sections;

!!! note

    All items in the defaults section are optional.

* `system` : Is used to set different system requirements/constraints within Kelvin SmartApps™ running environment. i.e. Resources, Environment Variables, Volumes, Ports, etc.
* `datastream_mapping` : Here you can map specific app inputs/outputs declared earlier in the `app.yaml` file to existing Data Streams on the Kelvin Platform.
* `configuration` : These are global variables that apply to the SmartApp as a whole, regardless of which asset is being managed.
* `parameters` : Default app parameter values used in a Kelvin SmartApp. These are applied: When an asset is first added to the Kelvin SmartApp or During upgrades, when new app parameters become available for existing assets.

```yaml title="application defaults" linenums="1"
defaults:
  system: {}
  datastream_mapping: []
  configuration: {}
  parameters: {}
```

**defaults/system section**

The `system` section is **[optional]**.

This is where developers can set the system settings that the Kelvin SmartApp™ needs to be able to function as intended.

This includes opening ports, setting environment variables, limited resource usage, attaching volumes and setting the privileged tag which gives extended privileges on the host system.

```yaml title="application system defaults" linenums="1"
defaults:
  system:
    resources: {}
    environment_vars: []
    volumes: []
    ports: []
    privileged: Boolean
```

???+ note "System Section Options"

    === "resources"

        **resources section**

        The `resources` defines the reserved (`requests`) and `limits` the resources allocated to Kelvin SmartApps™:

        * **Limits**: This is a maximum resource limit enforced by the cluster. Kelvin SmartApps™ will not be allowed to use more than the limit set.

        * **Requests**: This is the minimum resources that is allocated to Kelvin SmartApps™. This is reserved for Kelvin SmartApps™ and can not be used by other Kelvin SmartApps™. If there are extra resources available, Kelvin SmartApps™ can use more than the requested resources as long as it does not exceed the Limits.

        You can read the full [documentation about CPU and Memory](../advanced/set-cpu-and-memory-limits.md) resources in the Advanced section.

        ```yaml title="application resource defaults" linenums="1"
        defaults:
          system:
            resources:
              requests:   # Reserved
                cpu: 100m
                memory: 256Mi
            limits:     # Limits
                cpu: 200m
                memory: 512Mi
        ```

    === "environment_vars"

        **environment_vars section**

        The `environment_vars` is used to define Environment Variables available within Kelvin SmartApps™ container. i.e.:
            
        ```yaml title="application environmental variable defaults" linenums="1"
        defaults:
          system:
            environment_vars:
              - name: AZURE_ACCOUNT_NAME
                value: <% secrets.azure-account-name %>
              - name: AZURE_ACCOUNT_KEY
                value: <% secrets.azure-account-key %>
              - name: AZURE_STORAGE_CONTAINER
                value: <% secrets.azure-storage-container %>
        ```

    === "volumes"

        **volumes section**

        Mounted `volumes` are **[optional]** and their main purpose is to share and persist data generated by Kelvin SmartApps™ or used by it in a specific place. They act like a shared folder between Kelvin SmartApps™ and the host. Kelvin supports directory volumes, such as folders or serial ports, persistent, and file/test volumes:

        ```yaml title="application attached volume defaults" linenums="1"
        defaults:
          system:
            volumes:
              # Folder Volume
              - name: serial-rs232
                target: /dev/rs232 # Container path
                type: host
                host:
                source: /dev/ttyS0 # Host path

              # Persistent Volume
              - name: extremedb
                target: /extremedb/data
                type: persistent

              # File/Text Volume
              - name: model-parameters
                target: /opt/kelvin/data/parameters.bin
                type: text # Renders data into a file
                text:
                base64: true
                encoding: utf-8
                data: |-
                      SGVsbG8gUHJvZHVjdCBHdWlsZCwgZnJvbSB0aGUgRW5naW5lZXJpbmcgR3VpbGQhCg==
        ```

    === "ports"

        **ports section**

        The `ports` is **[optional]** and used to define network port mappings. i.e.:

        ```yaml title="application open ports defaults" linenums="1"
        defaults:
          system:
            ports:
              - name: http
                type: host # Exposed on the host
                host:
                port: 80

              - name: opcua
                type: service # Exposed as a service for other containers
                service:
                port: 48010
                exposed_port: 30120
                exposed: true
        ```

    === "privileged"

        **privileged key**

        The `privileged` key is **[optional]** and used to grant extended privileges to Kelvin SmartApps™, allowing it to access any devices on the host, such as a Serial device:

        ```yaml title="application privileged defaults" linenums="1"
        defaults:
          system:
            privileged: true
        ```

**defaults/datastream_mapping**

Here you can map specific Kelvin SmartApp™ inputs/outputs declared earlier in the `app.yaml` file to existing Data Streams on the Kelvin Platform.

```yaml title="application data stream mapping defaults" linenums="1"
defaults:
  datastream_mapping:
    - app: temp_f
      datastream: temperature_fahrenheit
    - app: temp_c
      datastream: temperature_celsius
```

**defaults/configuration**

These are the default global Kelvin SmartApp™ configuration values.

Configurations can also be optionally defined in the `ui_schemas` that provides a link to a JSON file containing all the information about how to display Configurations in the Kelvin UI.

!!! note

    Operations will have the option to change these at runtime from the Kelvin UI.

```yaml title="application app configuration defaults" linenums="1"
defaults:
  configuration:
    broker-ip: edge-mqtt-broker
    broker-port: 1883
```

**defaults/parameters**

Kelvin SmartApp™ App Parameters are defined in three sections in the `app.yaml` file;

* `parameters` defines the name and type of the App Parameter.
* `ui_schemas` (this section) is a link to a JSON file containing all the information about how to display App Parameters in the Kelvin UI.
* `defaults` / `parameters` [define the default values](#defaults) assigned to each Asset when it is first created or when a Kelvin SmartApp™ update introduces a new App Parameter to existing Assets.

!!! note

    Operations will have the option to change these at runtime from the Kelvin UI.

```yaml title="application app parameter defaults" linenums="1"
defaults:
  parameters:
    closed_loop: false
    speed_decrease_set_point: 1000
    temperature_max_threshold: 59
```

### Python

The `main.py` is used as the entry point of Kelvin SmartApps™.

When it runs, `main.py` is typically the first script that gets executed, and it usually contains the main logic or orchestrates the flow of Kelvin SmartApps™.

!!! note

    However, naming a file "main.py" is just a convention, and it's not mandatory.
    
    The name helps developers quickly identify where the primary logic of Kelvin SmartApps™ begins.

The following code example will be generated upon `kelvin app create`:

```python title="default main.py with stream decorators" linenums="1"
import asyncio

from kelvin.application import KelvinApp
from kelvin.logs import logger

app = KelvinApp()

@app.task
async def continuous_task():
    """Runs continuously in the background"""
    while True:
        logger.debug("My APP is running!")
        await asyncio.sleep(10)

app.run()
```

On older versions you may see the original format.

```python title="default original main.py" linenums="1"
import asyncio

from kelvin.application import KelvinApp
from kelvin.logs import logger


async def main() -> None:
    app = KelvinApp()

    await app.connect()

    while True:
        # Custom Loop
        logger.debug("My APP is running!")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
```

### Supporting Files

<div class="result" markdown>

=== "requirements.txt"

    The `requirements.txt` file is used to list all the dependencies a _Python_ Kelvin SmartApps™ needs.

    It includes the default Kelvin SmartApp™ libraries.
    
    Add here any additional packages your application needs.

=== "Dockerfile"
  
    The `Dockerfile` is a script used to define the instructions and configuration for building a Docker image. It specifies the base image, installation of software, file copying, and other setup tasks needed to create a reproducible and isolated environment for running Kelvin SmartApps™ in Docker containers.

    ```Dockerfile title="default Dockerfile" linenums="1"
    FROM --platform=${TARGETPLATFORM:-linux/amd64} python:3.12-slim

    ENV PYTHONUNBUFFERED=1
    WORKDIR /opt/kelvin/app

    # Install dependencies
    COPY requirements.txt ./
    RUN pip install --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt

    # Copy the remaining project files
    COPY . /opt/kelvin/app

    ENTRYPOINT ["python", "main.py"]
    ```
    
    !!! info
        If `main.py` is not the intended entry point, it also needs to be replaced on the `Dockerfile`.

=== ".dockerignore"

    Specifies which files and directories should be excluded when building Kelvin SmartApps™ Docker image.
    
    It includes the default folders that should not be compiled into the Kelvin SmartApp™ container.
    
    Add here any other folders or files that should not be compiled into the container.

</div>
