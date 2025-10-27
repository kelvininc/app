import asyncio
from datetime import timedelta

from kelvin.application import KelvinApp

async def main() -> None:
    """
    Start streaming asset data, monitor motor temperature vs. thresholds,
    and issue speed-reduction recommendations when necessary.
    """
    app = KelvinApp()
    await app.connect()



if __name__ == "__main__":
    asyncio.run(main())
