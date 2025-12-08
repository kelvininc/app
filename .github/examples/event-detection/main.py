from datetime import timedelta

from kelvin.application import KelvinApp
from kelvin.message import ControlChange, Recommendation
from kelvin.krn import KRNAssetDataStream, KRNAsset

app = KelvinApp()

# Wait for Data Stream Messages
@app.stream(inputs=["motor_temperature"])
async def handle_specific_inputs(msg) -> None:
    asset = msg.resource.asset
    value = msg.payload

    print(f"\nReceived Motor Temperature | Asset: {asset} | Value: {value}")

    # Check if the Temperature is above the Max Threshold
    if value > app.assets[asset].parameters["temperature_max_threshold"]:

        # Build Control Change Object
        control_change = ControlChange(
            resource=KRNAssetDataStream(asset, "motor_speed_set_point"),
            payload=app.assets[asset].parameters["speed_decrease_set_point"],
            expiration_date=timedelta(minutes=10)
        )

        if app.assets[asset].parameters["closed_loop"]:
            # Publish Control Change
            await app.publish(control_change)

            print(f"\nPublished Motor Speed SetPoint Control Change: {control_change.payload}")            
        else:
            # Build and Publish Recommendation
            await app.publish(
                Recommendation(
                    resource=KRNAsset(asset),
                    type="decrease_speed",
                    control_changes=[control_change]
                )
            )

            print(f"\nPublished Motor Speed SetPoint (Control Change) Recommendation: {control_change.payload}") 

app.run()