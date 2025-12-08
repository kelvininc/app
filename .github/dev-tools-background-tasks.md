# Background Tasks

Background and scheduled tasks run independently from the main execution path.

They execute in separate threads or event loop slots, preventing them from blocking the main workflow.

This keeps the application responsive while background operations run safely.

## Tasks

Tasks are functions executed in the background when the application connects.

!!! note

    If you create an infinite loop, then you can keep the background task running indefinitely.

```python title="Background Tasks Python Example" linenums="1"
from kelvin.application import KelvinApp
import asyncio

app = KelvinApp()

@app.task
async def background_task():
    """Runs once when the app starts"""
    print("Task started")
    # Perform initialization or one-time operations

@app.task
async def continuous_task():
    """Runs continuously in the background"""
    while True:
        print("Processing...")
        await asyncio.sleep(10)

# Can also register functions directly
async def another_task():
    print("Another task")

app.task(another_task, name="my_task")

app.run()
```

## Timers

Timers run functions at fixed intervals.

```python title="Background Timers Python Example" linenums="1"
from kelvin.application import KelvinApp

app = KelvinApp()

@app.timer(interval=30)  # seconds
async def periodic_check():
    """Runs every 30 seconds"""
    print("Periodic check executed")

@app.timer(interval=60)
async def publish_metrics():
    """Runs every 60 seconds"""
    # Publish periodic metrics
    await app.publish(...)

# Register timers directly
def sync_timer():
    print("Sync timer")

app.timer(sync_timer, interval=10, name="sync_timer")

app.run()
```