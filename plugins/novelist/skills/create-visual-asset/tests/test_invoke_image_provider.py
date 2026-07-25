from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "invoke_image_provider.py"
FAKE_PNG = b"\x89PNG\r\n\x1a\nmock-image"
SUCCESS_PROVIDER = (
    "import json, pathlib, sys; "
    "request=json.load(sys.stdin); "
    f"pathlib.Path(request['output']).write_bytes({FAKE_PNG!r})"
)
INVALID_PROVIDER = (
    "import json, pathlib, sys; "
    "request=json.load(sys.stdin); "
    "pathlib.Path(request['output']).write_text('not an image')"
)


class InvokeImageProviderTests(unittest.TestCase):
    def run_script(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_installs_a_valid_provider_raster(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "assets" / "cover.png"
            result = self.run_script(
                "--prompt",
                "A style-locked cover",
                "--output",
                str(output),
                "--",
                sys.executable,
                "-c",
                SUCCESS_PROVIDER,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(output.read_bytes(), FAKE_PNG)
            self.assertIn(str(output), result.stdout)

    def test_rejects_an_invalid_raster(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "cover.png"
            result = self.run_script(
                "--prompt",
                "A cover",
                "--output",
                str(output),
                "--",
                sys.executable,
                "-c",
                INVALID_PROVIDER,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("valid png raster", result.stdout)
            self.assertFalse(output.exists())

    def test_existing_output_is_protected_before_provider_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "cover.png"
            output.write_bytes(b"keep")
            result = self.run_script(
                "--prompt",
                "A cover",
                "--output",
                str(output),
                "--",
                sys.executable,
                "-c",
                "raise SystemExit('must not run')",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to overwrite", result.stdout)
            self.assertEqual(output.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
