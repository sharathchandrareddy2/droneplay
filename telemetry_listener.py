import asyncio
from mavsdk import System

async def run():
    drone = System()
    # Connect to the local simulator broadcasting from Docker
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to virtual drone!")
            break

    print("Starting interval telemetry stream (5 seconds)...")
    
    # Launch parallel tasks to pull data every 5 seconds
    asyncio.create_task(print_battery(drone))
    asyncio.create_task(print_altitude(drone))

    # Keep the main script running
    while True:
        await asyncio.sleep(1)

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent * 100:.1f}%")
        await asyncio.sleep(5)

async def print_altitude(drone):
    async for position in drone.telemetry.position():
        print(f"Altitude: {position.relative_altitude_m:.2f}m")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run())
