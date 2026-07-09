import platform


def _patch_python_version_for_mavsdk():
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

    def _compat_python_version():
        return ".".join(_compat_python_version_tuple()[:3])

    platform.python_version_tuple = _compat_python_version_tuple
    platform.python_version = _compat_python_version


_patch_python_version_for_mavsdk()
