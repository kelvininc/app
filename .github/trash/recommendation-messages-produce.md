
## Recommendation Messages

**Recommendations** in Kelvin are a method to package one or more actions into a single Recommendation, which is then displayed in the Kelvin UI for Operations to review and approve.

![](../../../../assets/produce-recommendation-messages-overview.jpg)

The recommendation allows Operations to see and decide on the actions before they are implemented.

!!! note

    In short this puts the Operations as the man-in-the-middle between the automation programs and the Assets.

![](../../../../assets/asset_dashboard_recommendation_popup.png)

In this brief demo you can see the different parts of a Recommendation;

<iframe
src="https://demo.arcade.software/GEzpc9obq6XjFlNkIj1o?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
title="Kelvin Core | Operations"
frameborder="0"
loading="lazy"
webkitallowfullscreen
mozallowfullscreen
allowfullscreen
allow="clipboard-write"
style="width: 100%; height: 400px; border: none;">
</iframe>

The technical workflow of Recommendations from creation to approval/rejection can be found in the detailed [concept overview page here](../../../../overview/concepts/recommendation.md).

!!! note

    Currently the only action available is **Control Changes**.

The Recommendation Object supports the following attributes :

| Recommendation Attribute         | Required     | Description                                                                      |
|-------------------|--------------|----------------------------------------------------------------------------------|
| `resource`        | **required** | The KRNAsset that this Recommendation is meant for.                              |
| `type`            | **required** | The Recommendation type (String). (e.g. speed_increase, speed_decrease, etc)     |
| `expiration_date` | **optional** | Absolute datetime or a time delta (from now) when the Control Change will expire. |
| `description`     | **optional** | Detailed description for the Recommendation.                                     |
| `confidence`      | **optional** | Confidence of the recommendation (from 1 to 4).                                  |
| `control_changes` | **required** | List of ControlChange Objects associated with the recommendation.                |
| `metadata`        | **optional** | Metadata for the recommendation.                                                 |
| `auto_accepted`| **optional** | Sets the Recommendation as auto accepted (Default is False). |

## Open / Closed Loop Control

Kelvin supports both open-loop and closed-loop control approaches in its application logic, providing flexibility in how automation decisions are executed.

!!! info

    This is programming advice to optionally include a human-in-the-loop by using App Parameters and conditional logic to decide whether to create a recommendation or execute actions directly.

This concept enables you to insert human oversight between your algorithms or ML models and the final actions applied to your assets.

To implement this, define a boolean App Parameter called `closed_loop`:

- If `true`, actions are executed automatically without human intervention.
- If `false`, a recommendation is created instead, allowing operators to review and decide whether to proceed.

There are two implementation strategies:

1. **(Recommended)** Always package the control change or action inside a recommendation object. Use the `auto_accept` field to control behavior:  
   - `true` for automatic execution  
   - `false` for manual review  
   This ensures consistent history logging and easier auditing or debugging during future upgrades.

2. Use conditional logic (`if/else`) in your app:
   - If `closed_loop` is true, apply the action directly.
   - If false, wrap it in a recommendation with `auto_accept: false`.

This approach gives full control over automation level per deployment while retaining traceability and operational flexibility.

## Evidences

When creating Recommendations, it is useful to embed the data used in the calculations for creating the new value in the recommendation.

This data is intended for;

* Operations : They can view the data when deciding whether to accept or reject the recommendation.
* Data Scientists : They can use the data to correlate with the confidence level reported by Operations to improve their machine learning models.

!!! info

    Evidence can only be embedded into Recommendation if used in a Kelvin SmartApp™.

    You can not create Recommendations with evidences using the Kelvin API or the Kelvin API Client (Python)

There are a number of different types of evidences that can be embedded with the Recommendation;

??? example "Data Explorer"

    This evidence is for linking to specific time and Assets in the Data Explorer.

    <center>![](../../../../assets/recommendations-evidences-data-explorer.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Bar Chart Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import DataExplorer, DataExplorerSelector
    from kelvin.krn import KRNAsset, KRNAssetDataStream
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidence = DataExplorer(
            title="Data Explorer Title",
            start_time=datetime.now() - timedelta(hours=1),
            end_time=datetime.now(),
            selectors=[
            DataExplorerSelector(resource=KRNAssetDataStream("asset_01", "datastream1"))
            DataExplorerSelector(resource=KRNAssetDataStream("asset_02", "datastream2"), agg="mean", time_bucket="5m")
            ]
        )

        recommendation = Recommendation(
            resource=KRNAsset('asset_01'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

    Options;

    | Attribute           | Required     | Default Value | Description                                                                          |
    |---------------------|--------------|---------------| -------------------------------------------------------------------------------------|
    | `resource`          | **required** |      N/A      | This can be Asset Data Stream (ad), Data Quality - Asset (dqasset) or Data Quality - Asset Data Stream (dqad)                                 |
    | `agg`              | **optional** |      N/A      | Valid ag : none, count, distinct, integral, mean, median, mode, spread, stddev, sum, max, min, first, last                                   |
    | `time_bucket`             | **optional** |      N/A      | Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h"                                      |

??? example "Bar Chart"

    This evidence is for creating bar charts.

    <center>![](../../../../assets/recommendations-evidences-bar-chart.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Bar Chart Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import BarChart
    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            BarChart(
                title="Sample Bar Chart Title",
                timestamp=datetime.now(),
                x_axis={
                    "title": "X-Axis Title",
                    "categories": ["Category A", "Category B", "Category C", "Category D"]
                },
                y_axis={
                    "title": "Y-Axis Title",
                    "min": 0
                },
                series=[
                    {"name": "Series 1", "data": [5, 10, 15, 20]},
                    {"name": "Series 2", "data": [7, 14, 21, 28]}
                ]
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "Line Chart"

    This evidence example is for creating line charts.

    There are four types of line charts you can create;

    * Linear
    * Date Time
    * Category
    * Logarithmic

    <center>![](../../../../assets/recommendations-evidences-line-chart.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Line Chart Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import LineChart
    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            LineChart(
                title="Sample Chart Title",
                timestamp=datetime.now(),
                x_axis={
                    "type":"linear", # | 'linear' | 'datetime' | 'category' | 'logarithmic';
                    "categories": ["Category 1", "Category 2", "Category 3"],
                    "title": "X-Axis Title"
                },
                y_axis={"title": "Y-Axis Title"},
                series=[
                    {"name": "Series 1", "data": [1, 2, 3, 4, 5]},
                    {"name": "Series 2", "data": [[1, 2], [2, 3], [3, 5], [4, 7]]}
                ]
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "Dynacard"

    This evidence example is for creating line charts.

    There are four types of line charts you can create;

    * Linear
    * Date Time
    * Category
    * Logarithmic

    <center>![](../../../../assets/recommendations-evidences-dynacard.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Dynacard Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import Dynacard
    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            Dynacard(
                title="Sample Chart Title",
                timestamp=datetime.now(),
                xAxis={
                        "title": "X-Axis Title"
                },
                yAxis={
                    "title": "Y-Axis Title"
                },
                series=[
                    {"name": "Series 1", "data": [1, 2, 3, 4, 5]},
                    {"name": "Series 2", "data": [[1, 2], [2, 3], [3, 5], [4, 7]]}
                ]
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "HighCharts"

    This evidence is for creating any type of chart using the powerful [High Charts](https://www.highcharts.com/demo) format.

    <center>![](../../../../assets/recommendations-evidences-highcharts.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Add HighCharts Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import Chart
    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            Chart(
                title="Sample Chart Title",
                timestamp=datetime.now(),

                ... # Content here will depend on the type of High Chart you choose to display.

            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "Image"

    This evidence is for showing images. This is particular useful for computer vision related Recommendations.

    <center>![](../../../../assets/recommendations-evidences-images.png)</center>

    !!! note

        The image must be either from the Kelvin File Storage or a publicly available link.

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Picture (Image) Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import Image
    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            Image(
                title="My Image",
                description="This is the image or evidence description.",
                url="https://www.example.com/image.jpg",
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "Markdown"

    This evidence is for showing text in markdown format.

    <center>![](../../../../assets/recommendations-evidences-markdown.png)</center>

    !!! note

        The image must be either from the Kelvin File Storage or a publicly available link.

    This is how you can add this evidence into your Recommendation.

    ```python title="Add Markdown Text Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import Markdown

    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            Markdown(
                title="My Markdown",
                markdown="""
                    # Evidence 1
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                    
                    # Evidence 2
                    ...
                """ # (Multi line) String 
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? example "IFrame"

    This evidence is for showing any web content in an iFrame.

    <center>![](../../../../assets/recommendations-evidences-iframe.png)</center>

    This is how you can add this evidence into your Recommendation.

    ```python title="Embed IFrame Evidence to Recommendation Python Example" linenums="1"
    from kelvin.application import KelvinApp
    from kelvin.message.evidences import IFrame

    from kelvin.krn import KRNAsset
    from datetime import datetime

    async def main() -> None:
        app = KelvinApp()
        await app.connect()

        evidences = [
            IFrame(
                title="My IFrame",
                url="https://www.example.com/content/",
            )
        ]

        recommendation = Recommendation(
            resource=KRNAsset('pcp_51'),
            type="decrease_speed",
            control_changes=[],
            evidences=evidences,
        )

        await app.publish(recommendation)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

## Examples

### Basic Usage

Here is a minimal Recommendation.


```python title="Create Basic Recommendation Python Example" linenums="1"
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.message import ControlChange, Recommendation
from kelvin.krn import KRNAssetDataStream, KRNAsset

(...)

# Create a Control Change
control_change = ControlChange(
    resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5)
)

# Create and Publish a Recommendation with one Control Change package
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change]
    )
)
```

### Multiple Control Changes


```python title="Create Recommendation with Multiple Control Changes Python Example" linenums="1"
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.message import ControlChange, Recommendation
from kelvin.krn import KRNAssetDataStream, KRNAsset

(...)

# Create a Control Change
control_change_01 = ControlChange(
    resource=KRNAssetDataStream("my-motor-asset_01", "motor_speed_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5)
)

control_change_02 = ControlChange(
    resource=KRNAssetDataStream("my-motor-asset_02", "motor_speed_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5)
)

control_change_03 = ControlChange(
    resource=KRNAssetDataStream("valve_01", "position_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5)
)

# Create and Publish a Recommendation with one Control Change package
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change_01, control_change_02, control_change_03]
    )
)
```

### Typical ML Usage

When you have a machine learning model producing the recommended control changes, then you can store additional data produced by the ML output

```python title="Create Recommendation with Metadata Python Example" linenums="1"
from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.message import ControlChange, Recommendation
from kelvin.krn import KRNAssetDataStream, KRNAsset

# Normally your ML mode predictions go here
(...)

# Create a Control Change
control_change = ControlChange(
    resource=KRNAssetDataStream("my-motor-asset", "motor_speed_set_point"),
    payload=1000,
    expiration_date=timedelta(minutes=5)
)

# Create and Publish a Recommendation with one Control Change package
# Add also the ML-specific Data
await app.publish(
    Recommendation(
        resource=KRNAsset("my-motor-asset"),
        type="decrease_speed",
        control_changes=[control_change],
        metadata={
            "predicted_speed": 2.5,
            "confidence": 0.87,
            "input_features": {"current_speed": 5, "load": 4},
            "timestamp": "2024-11-18T12:00:00Z",
            "model_version": "1.2.0"
        }
    )
)
```

### Incorporating Evidences

There are a number of types of evidences you can embed into the Recommendation.

!!! note

    Each Recommendation can have an unlimited amount of evidence added.

* Bar Charts
* Line Charts
* Dynacards
* Any type of HighCharts
* Images
* Markdown
* IFrames

You can see [full examples here](#evidences).

