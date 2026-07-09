import os
import platform
import shutil
import subprocess
import sys
import urllib.request


def get_mavsdk_server_asset_name(machine):
    normalized = (machine or "").lower()
    if "x86_64" in normalized or "amd64" in normalized:
        return "mavsdk_server_musl_x86_64"
    if "aarch64" in normalized or "arm64" in normalized:
        return "mavsdk_server_linux-arm64-musl"
    return "mavsdk_server_musl_x86_64"


def ensure_mavsdk_server(binary_path="/tmp/mavsdk/mavsdk_server", port=50051):
    if os.path.exists(binary_path):
        return binary_path

    os.makedirs(os.path.dirname(binary_path), exist_ok=True)
    asset_name = get_mavsdk_server_asset_name(platform.machine())
    download_url = (
        f"https://github.com/mavlink/MAVSDK/releases/download/v3.17.1/{asset_name}"
    )

    with urllib.request.urlopen(download_url, timeout=60) as response, open(binary_path, "wb") as handle:
        handle.write(response.read())

    os.chmod(binary_path, 0o755)
    return binary_path


def start_mavsdk_server(binary_path="/tmp/mavsdk/mavsdk_server", port=50051):
    if shutil.which("mavsdk_server"):
        binary_path = shutil.which("mavsdk_server")

    if not os.path.exists(binary_path):
        binary_path = ensure_mavsdk_server(binary_path, port)

    subprocess.Popen([binary_path, "-p", str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return binary_path


if __name__ == "__main__":
    start_mavsdk_server()
