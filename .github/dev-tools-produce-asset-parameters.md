Title: App Parameter Messages
Source: https://docs.kelvin.ai/6.3/developer-tools/how-to/develop/produce/asset-parameter-messages/
Fetched: 2025-10-27

Detailed Summary :
Kelvin SmartApps can publish an App Parameter Message to update an App Parameter for a specific Asset. These messages update the target App Parameter value and persist the change when the message is synced with the Kelvin Cloud. Users may also change App Parameter values through the Kelvin UI; automated changes performed by SmartApps will be reflected on the Kelvin UI.

The main message types shown on the page are `AssetParameter` (single parameter) and `AssetParameters` (a collection). The AssetParameter object supports the following attributes:

- resource (required): a `KRNAssetParameter` reference identifying the App Parameter (asset + parameter name).
- value (required): the App Parameter value (Boolean, Integer, Float or String).
- comment (optional): a description or comment describing the update.

When publishing `AssetParameters`, you can also include a `resource` that is an application version reference (`KRNAppVersion`) to indicate which target app/version the parameter update is intended for (for example when sending App-to-App updates).

The page includes an App-to-App workflow note: App Parameters can be updated from one Kelvin SmartApp to another. Even if both SmartApps are deployed on the same cluster, the platform requires an Internet connection to sync with the Kelvin Cloud for App-to-App parameter updates.

Key examples :
Below are the Python examples and snippets reconstructed from the page. They show the imports required and two example usage patterns: publish a single App Parameter, and publish multiple App Parameters in a single message.

Python - imports (required symbols shown):

```python
from kelvin.application import KelvinApp
from kelvin.message import AssetParameter, AssetParameters
from kelvin.krn import KRNAssetParameter, KRNAppVersion
```

Python - Create and publish a single App Parameter

```python
# single AssetParameter example
await app.publish(
    AssetParameters(
        parameters=[
            AssetParameter(
                resource=KRNAssetParameter(asset, "min_treshold"),
                value=0,
            )
        ],
        resource=KRNAppVersion(target_app_name, "1.0.0"),
    )
)
```

Python - Create and publish multiple App Parameters

```python
# multiple AssetParameter example
await app.publish(
    AssetParameters(
        parameters=[
            AssetParameter(
                resource=KRNAssetParameter(asset, "min_treshold"),
                value=0,
            ),
            AssetParameter(
                resource=KRNAssetParameter(asset, "max_treshold"),
                value=50,
            ),
        ],
        resource=KRNAppVersion(target_app_name, "1.0.0"),
    )
)
```

Notes:
- The `resource` for each `AssetParameter` must be a `KRNAssetParameter`, which encodes the asset and parameter name. Use the repository's KRN helpers to generate these resources consistently.
- `value` accepts primitive types: boolean, integer, float, or string. Ensure the value type matches the App Parameter's defined schema in the target SmartApp.
- `comment` may be included on `AssetParameter` for human-readable context (optional).
- App-to-App updates require the message to reach the Kelvin Cloud; a local-only update (no cloud sync) will not persist across SmartApps.
- Images on the source page illustrate the UI and App-to-App flow; assets captured on the source include `asset-parameters-overview.jpg` and `produce-asset-parameters-messages-app-to-app.jpg`.

Additional implementation notes:
- Validate that the parameter names (e.g. "min_treshold", "max_treshold") exactly match the parameter keys declared in the target SmartApp's `app.yaml` (`parameters` section) and `ui_schemas`.
- When automating App Parameter changes, consider permission and guardrail checks. If your app exposes controls that affect physical equipment, ensure safety and authorization concerns are handled before publishing parameter updates.
- Use `KRNAppVersion` with a `target_app_name` and semantic version when you need to target a specific consumer SmartApp version for the parameter update.