# Callback Functions

## Overview

Callbacks (event hooks) allow you to respond to important lifecycle and data events in your Kelvin SmartApp.

There are a number of callback functions available.

This allows your Kelvin SmartApp™ application to response instantly to certain events happening on the Kelvin Platform.

!!! note

    For advanced scenarios you can use these callbacks for specific lifecycle events.
    
    However, stream decorators are generally preferred for message processing.

## Options

### on_connect

Use this event callback to monitor when the app connects to Kelvin.

```python title="Callback on_connect Python Example" linenums="1"
from kelvin.application import KelvinApp, AssetInfo

app = KelvinApp()

async def on_connect():
    """Called when the app connects to Kelvin"""
    print("Connected to Kelvin platform")
    print(f"Configuration: {app.app_configuration}")
    print(f"Assets: {app.assets}")

# Assign callback
app.on_connect = on_connect

app.run()
```

### on_asset_input

Triggered for incoming data messages from asset inputs.

```python title="Callback on_asset_input Python Example" linenums="1"
from kelvin.application import KelvinApp
from kelvin.message.typing import AssetDataMessage

app = KelvinApp()

async def on_asset_input(msg: AssetDataMessage):
    """Called for data messages from asset inputs"""
    print(f"Data from {msg.resource}: {msg.payload}")

# Assign callback
app.on_asset_input = on_asset_input

app.run()
```

### on_control_change

Triggered when control change messages are received.

```python title="Callback on_control_change Python Example" linenums="1"
from kelvin.application import KelvinApp
from kelvin.message.typing import AssetDataMessage

app = KelvinApp()

async def on_control_change(msg: AssetDataMessage):
    """Called when control changes are received"""
    print(f"Control change for {msg.resource}: {msg.payload}")

# Assign callback
app.on_control_change = on_control_change

app.run()
```

### on_asset_change

Use this event to detect when Assets are added, removed, or modified.

```python title="Callback on_asset_change Python Example" linenums="1"
from kelvin.application import KelvinApp, AssetInfo
from typing import Optional

app = KelvinApp()

async def on_asset_change(new_asset: Optional[AssetInfo], old_asset: Optional[AssetInfo]):
    """Called when assets are added, removed, or modified"""
    if new_asset is None:
        print(f"Asset removed: {old_asset.name}")
    else:
        print(f"Asset changed: {new_asset.name}")

# Assign callback
app.on_asset_change = on_asset_change

app.run()
```

### on_app_configuration

Triggered when the app configuration is updated.

```python title="Callback on_app_configuration Python Example" linenums="1"
from kelvin.application import KelvinApp

app = KelvinApp()

async def on_app_configuration(config: dict):
    """Called when app configuration changes"""
    print(f"New configuration: {config}")

# Assign callback
app.on_app_configuration = on_app_configuration

app.run()
```