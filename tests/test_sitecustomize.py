import importlib
import os
import sys
import unittest


class SiteCustomizeCompatibilityTest(unittest.TestCase):
    def test_mavsdk_imports_after_sitecustomize_patch(self):
        repo_root = os.path.dirname(os.path.dirname(__file__))
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)

        sys.modules.pop("mavsdk", None)

        module = importlib.import_module("mavsdk")

        self.assertTrue(hasattr(module, "System"))


if __name__ == "__main__":
    unittest.main()
