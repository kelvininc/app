## Data Tag Messages

Data Tags are used to label Asset time series data. This has many applications such as;

* For data scientists to use for machine learning training
* For developers to have additional information beyond the raw data to review and improve Kelvin SmartApps™
* For Operations to tag events linked to the time series data for historical records

![](../../../../assets/produce-data-tags-messages-overview.jpg)

On the Kelvin UI, the data tags will show in the Data Explorer.

![](../../../../assets/data_explorer_tags_lanes.png)

Kelvin SmartApps™ can publish a `DataTag` Message in order to label important events on a certain point in time (or time range) for a certain Asset.

!!! note

    Operations can also their own add Data Tags manually through the Kelvin UI

The DataTag Object supports the following attributes:

| Data Tag Attribute       | Required     | Description                                                                                 |
|-----------------|--------------|---------------------------------------------------------------------------------------------|
| `start_date`    | **required** | Start date for the Data Tag. Time is based on UTC timezone, formatted in RFC 3339.          |
| `end_date`      | **optional** | End date for the Data Tag. Time is based on UTC timezone, formatted in RFC 3339.            |
| `tag_name`      | **required** | Tag name to categorize the Data Tag.                                                        |
| `resource`      | **required** | The Asset that this Data Tag is related to. This is in KRN format (e.g. `krn:asset:bp_01`). |
| `description`   | **optional** | Detailed description of the Data Tag.                                                       |
| `contexts`      | **optional** | A list of associated Kelvin resources with this Data Tag. (e.g. KRNDatastream, KRNApp, etc).|

This is how they can be created and published:

```python title="Create and Publish Data Tag Python Example" linenums="1"
from datetime import timedelta, datetime

from kelvin.application import KelvinApp
from kelvin.message import DataTag
from kelvin.krn import KRNAsset, KRNDatastream

app = KelvinApp()

@app.timer(interval=10)
async def publish_data():

    now = datetime.now()

    # Create and Publish DataTag
    await app.publish(
        DataTag(
            start_date=now - timedelta(seconds=datatag_duration_secs),
            end_date=now,
            tag_name="My Tag",
            resource=KRNAsset("my_asset"),
            contexts=[KRNApp("app_name"), KRNDatastream("my_datastream")]
        )
    )

app.run()
```