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
