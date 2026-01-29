from kelvin.application import KelvinApp
from kelvin.logs import logger
from kelvin.message import AssetDataMessage

app = KelvinApp()


async def on_connect():
    logger.info("App connected", assets=list(app.assets.keys()))


@app.stream()
async def on_asset_input(msg: AssetDataMessage):
    logger.info(
        "Data received",
        asset=msg.resource.asset,
        data_stream=msg.resource.data_stream,
        value=msg.payload,
    )


app.on_connect = on_connect
app.run()
