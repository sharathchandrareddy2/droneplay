import unittest

from mavsdk_runtime import get_mavsdk_server_asset_name


class MavsdkRuntimeTest(unittest.TestCase):
    def test_x86_64_asset_name(self):
        self.assertEqual(get_mavsdk_server_asset_name("x86_64"), "mavsdk_server_musl_x86_64")

    def test_arm64_asset_name(self):
        self.assertEqual(get_mavsdk_server_asset_name("aarch64"), "mavsdk_server_linux-arm64-musl")


if __name__ == "__main__":
    unittest.main()
