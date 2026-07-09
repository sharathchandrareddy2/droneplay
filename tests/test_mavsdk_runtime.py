import asyncio
import unittest

from mavsdk_runtime import get_mavsdk_server_asset_name
from telemetry_listener import _wait_for_connection


class MavsdkRuntimeTest(unittest.TestCase):
    def test_x86_64_asset_name(self):
        self.assertEqual(get_mavsdk_server_asset_name("x86_64"), "mavsdk_server_musl_x86_64")

    def test_arm64_asset_name(self):
        self.assertEqual(get_mavsdk_server_asset_name("aarch64"), "mavsdk_server_linux-arm64-musl")

    def test_wait_for_connection_timeout(self):
        drone = type("Drone", (), {})()
        drone.core = type("Core", (), {})()
        drone.core.connection_state = lambda: _never_connecting_stream()

        result = asyncio.run(_wait_for_connection(drone, timeout=0.01))

        self.assertFalse(result)


async def _never_connecting_stream():
    while True:
        await asyncio.sleep(0.1)
        yield type("State", (), {"is_connected": False})()


if __name__ == "__main__":
    unittest.main()
