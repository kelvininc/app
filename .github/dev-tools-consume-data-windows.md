# Data Windows

Data windows aggregate incoming data over time or count, returning pandas DataFrames for analysis.

!!! note

    You must have installed the `kelvin-python-sdk[ai]` library for this feature to work.

## Introduction

The Kelvin SDK facilitates three primary windowing methods:

1. **Tumbling Window:** This method uses fixed-size, non-overlapping windows that reset after each window period, making it suitable for isolated data analysis in each segment.
2. **Hopping Window:** These windows are also fixed-size but can overlap based on a specified hop size, allowing for more frequent data analysis intervals.
3. **Rolling Window:** Unlike the other types, this method creates fixed-size windows based on the count of messages, not on time intervals.

!!! info

    It is important to note that windows are always ordered by timestamp, ensuring that temporal sequencing is maintained across the data processed.

![](../../../../assets/windowing-overview.jpg)

### Irregular Data Scenarios

* **Lateness in Data:** Lateness occurs when data arrives after its processing window. Kelvin incorporates late data into open windows; otherwise, it is ignored.

* **Out-of-Order Events:** Out-of-order events arrive in a sequence different from their timestamps. Window methods correctly place them in their respective windows by timestamp, preserving temporal order.

### Time Windows

Time-based windows include the start of the interval but exclude the end, preventing data duplication across windows.

## Tumbling Window

Example of temperature readings with a tumbling window of 10 seconds.

``` title="Tumbling Window Example" linenums="1"
Original Data:
Time: [00:00]   25°C
Time: [00:04]   26°C
Time: [00:07]   27°C
Time: [00:12]   28°C
Time: [00:18]   26°C
Time: [00:22]   29°C
Time: [00:27]   30°C
Time: [00:31]   27°C
Time: [00:35]   25°C

Tumbling Windows:
Time: [00:00, 00:10):   [25°C (00:00), 26°C (00:04), 27°C (00:07)]
Time: [00:10, 00:20):   [28°C (00:12), 26°C (00:18)]
Time: [00:20, 00:30):   [29°C (00:22), 30°C (00:27)]
Time: [00:30, 00:40):   [27°C (00:31), 25°C (00:35)]
```

Each window (W1, W2, etc.) processes data that falls within its respective 10-second time frame. No data overlaps between the windows.

### Examples

<div class="result" markdown>

=== "Basic"

    ```python title="Basic Tumbling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Streaming data in 5-minute tumbling windows
    window_start = datetime.now()
    async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5)).stream(window_start):
        print(asset_name, df)
    ```

    This will automatically process data in 5-minute intervals for all data streams defined in your `app.yaml` and for all assets your app is running on. Each iteration of the loop will return:

    * `asset_name`: the unique identifier of the asset
    * `df`: a Pandas DataFrame containing the data for that asset within the 5-minute window. This DataFrame’s index is timestamp-based, with the values in monotonic increasing order.

=== "Filter Data Streams"

    To narrow down the processing to specific data streams within a window, you can specify which streams to include:

    !!! info
        The order of data streams in the list specifies the order of the columns within the DataFrame produced by the window. 

    ```python title="Filtered Data Streams Tumbling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    window_start = datetime.now()
    async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5), 
                                            datastreams=['temperature', 'pressure']).stream(window_start):
        print(asset_name, df)
    ```

=== "Filter Assets"

    To narrow down the processing to specific Assets within a window, you can specify which Asset to include:

    ```python title="Filtered Asset Tumbling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    window_start = datetime.now()
    async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5), 
                                            assets=['asset1', 'asset2']).stream(window_start):
        print(asset_name, df)
    ```

=== "Aligned Data"

    The `round_to` parameter is designed to align message timestamps to the nearest specified time unit, such as a second, minute, or hour. This functionality is particularly beneficial for ensuring that rows within a DataFrame are synchronized, which is crucial for consistent data analysis and reporting.

    ```python title="Time Aligned Tumbling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Aligning windows to the nearest minute
    window_start = datetime.now()
    async for asset_name, df in app.tumbling_window(window_size=timedelta(minutes=5), 
                                            round_to=timedelta(minutes=1)).stream(window_start):
        print(asset_name, df)
    ```

</div>

## Hopping Window
A hopping window, also known as a sliding window, is a series of fixed-sized, overlapping intervals where each window “hops” forward by a specified time interval (hop size). It is suitable for applications where data points may need to be included in multiple intervals for continuous calculations.

Example of temperature readings with a hopping window size of 10 seconds and a hop size of 5 seconds:

``` title="Hopping Window Example" linenums="1"
Original Data:
Time: [00:00]   25°C
Time: [00:04]   26°C
Time: [00:07]   27°C
Time: [00:12]   28°C
Time: [00:18]   26°C
Time: [00:22]   29°C
Time: [00:27]   30°C
Time: [00:31]   27°C
Time: [00:35]   25°C

Windows:
Time: [00:00, 00:10):   [25°C (00:00), 26°C (00:04), 27°C (00:07)]
Time: [00:05, 00:15):   [26°C (00:04), 27°C (00:07), 28°C (00:12)]
Time: [00:10, 00:20):   [28°C (00:12), 26°C (00:18)]
Time: [00:15, 00:25):   [26°C (00:18), 29°C (00:22)]
Time: [00:20, 00:30):   [29°C (00:22), 30°C (00:27)]
Time: [00:25, 00:35):   [30°C (00:27), 27°C (00:31)]
Time: [00:30, 00:40):   [27°C (00:31), 25°C (00:35)]
```

Here, each new window starts every 5 seconds, causing overlapping between windows (e.g., 26°C and 29°C appear in multiple windows).

### Examples

<div class="result" markdown>

=== "Basic"

    ```python title="Basic Hopping Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Processing data using a 5-minute hopping window with a 2-minute hop size
    window_start = datetime.now()
    for asset_name, df in app.hopping_window(window_size=timedelta(minutes=5), 
                                            hop_size=timedelta(minutes=2)).stream(window_start=window_start):
        print(asset_name, df)
    ```

    This code snippet will stream data from all configured data streams and assets, processing it in 5-minute windows that move forward by 2 minutes after each iteration. 


=== "Filter Data Streams"

    To narrow down the processing to specific data streams within a window, you can specify which streams to include:

    !!! info
        The order of data streams in the list specifies the order of the columns within the DataFrame produced by the window. 

    ```python title="Filtered Data Streams Hopping Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Processing data using a 5-minute hopping window with a 2-minute hop size
    window_start = datetime.now()
    async for asset_name, df in app.hopping_window(window_size=timedelta(minutes=5), 
                                            hop_size=timedelta(minutes=2), 
                                            datastreams=['temperature', 'pressure']).stream(window_start=window_start):
        print(asset_name, df)
    ```

=== "Filter Assets"

    To narrow down the processing to specific Assets within a window, you can specify which Asset to include:

    ```python title="Filtered Asset Hopping Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Processing data using a 5-minute hopping window with a 2-minute hop size
    window_start = datetime.now()
    async for asset_name, df in app.hopping_window(window_size=timedelta(minutes=5), 
                                            hop_size=timedelta(minutes=2), 
                                            assets=['asset1', 'asset2']).stream(window_start=window_start):
        print(asset_name, df)
    ```

=== "Aligned Data"

    The `round_to` parameter is designed to align message timestamps to the nearest specified time unit, such as a second, minute, or hour. This functionality is particularly beneficial for ensuring that rows within a DataFrame are synchronized, which is crucial for consistent data analysis and reporting.

    ```python title="Time Aligned Hopping Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    # Processing data using a 5-minute hopping window with a 2-minute hop size
    window_start = datetime.now()
    async for asset_name, df in app.hopping_window(window_size=timedelta(minutes=5), 
                                            hop_size=timedelta(minutes=2), 
                                            round_to=timedelta(minutes=1)).stream(window_start=window_start):
        print(asset_name, df)
    ```

</div>

## Rolling Window
A rolling window, also known as a moving window, calculates over a window of a specified number of data points (count size). Unlike time-based windows, it moves one observation at a time. This method is ideal for smoothing or averaging data points directly.

Example of temperature readings with a rolling window of 3 elements:

``` title="Rolling Window Example" linenums="1"
Original Data:
Time: [00:00]   25°C
Time: [00:04]   26°C
Time: [00:07]   27°C
Time: [00:12]   28°C
Time: [00:18]   26°C
Time: [00:22]   29°C
Time: [00:27]   30°C
Time: [00:31]   27°C
Time: [00:35]   25°C

Windows:
Window 1:   [25°C (00:00), 26°C (00:04), 27°C (00:07)]
Window 2:   [26°C (00:04), 27°C (00:07), 28°C (00:12)]
Window 3:   [27°C (00:07), 28°C (00:12), 26°C (00:18)]
Window 4:   [28°C (00:12), 26°C (00:18), 29°C (00:22)]
Window 5:   [26°C (00:18), 29°C (00:22), 30°C (00:27)]
Window 6:   [29°C (00:22), 30°C (00:27), 27°C (00:31)]
Window 7:   [30°C (00:27), 27°C (00:31), 25°C (00:35)]
```

Each window contains 3 events, and as new data arrives, the window shifts forward, always keeping the latest 3 events in focus.

### Examples

<div class="result" markdown>

=== "Basic"

    ```python title="Basic Rolling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    async for asset_name, df in app.rolling_window(count_size=5).stream():
        print(asset_name, df)
    ```

=== "Filter Data Streams"

    To narrow down the processing to specific data streams within a window, you can specify which streams to include:

    !!! info
        The order of data streams in the list specifies the order of the columns within the DataFrame produced by the window. 

    ```python title="Filtered Data Streams Rolling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    async for asset_name, df in app.rolling_window(count_size=5, 
                                            datastreams=['temperature', 'pressure']).stream():
        print(asset_name, df)
    ```

=== "Filter Assets"

    To narrow down the processing to specific Assets within a window, you can specify which Asset to include:

    ```python title="Filtered Asset Rolling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    async for asset_name, df in app.rolling_window(count_size=5, a
                                            assets=['asset1', 'asset2']).stream():
        print(asset_name, df)
    ```

=== "Aligned Data"

    The `round_to` parameter is designed to align message timestamps to the nearest specified time unit, such as a second, minute, or hour. This functionality is particularly beneficial for ensuring that rows within a DataFrame are synchronized, which is crucial for consistent data analysis and reporting.

    ```python title="Time Aligned Rolling Window Python Example" linenums="1"
    app = KelvinApp()
    await app.connect()

    async for asset_name, df in app.rolling_window(count_size=5, 
                                            round_to=timedelta(minutes=1)).stream():
        print(asset_name, df)
    ```

</div>