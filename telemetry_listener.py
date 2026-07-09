import asyncio
import importlib
import os
import sys

from mavsdk_runtime import start_mavsdk_server


async def _wait_for_connection(drone, timeout=15):
    async def _consume_connection_states():
        async for state in drone.core.connection_state():
            if state.is_connected:
                print("-- Connected to virtual drone!")
                return True
        return False

    try:
        return await asyncio.wait_for(_consume_connection_states(), timeout=timeout)
    except asyncio.TimeoutError:
        print("No drone connected within the timeout window.")
        return False


def _load_mavsdk_system():
    import platform

    original_version_tuple = platform.python_version_tuple

    def _compat_python_version_tuple():
        version = original_version_tuple()
        if len(version) >= 2:
            try:
                major = int(version[0])
                minor = int(version[1])
                if major == 3 and minor >= 6:
                    return ("3", "6", "0")
            except ValueError:
                pass
        return ("3", "6", "0")

    platform.python_version_tuple = _compat_python_version_tuple
    module = importlib.import_module("mavsdk")
    return module.System


System = _load_mavsdk_system()

async def run():
    start_mavsdk_server()
    drone = System(mavsdk_server_address="localhost", port=50051)
    # Connect to the local simulator broadcasting from Docker
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Waiting for drone to connect...")
    connected = await _wait_for_connection(drone, timeout=15)
    if not connected:
        return

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
