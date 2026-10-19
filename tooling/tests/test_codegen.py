"""Compatibility coverage for the scoped datamodel-code-generator override."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class CodegenCompatibilityTest(unittest.TestCase):
    def test_protocol_output_matches_pre_override_generator(self):
        """Preserve all nine files produced with fastapi-codegen 0.8.1/DCG 0.65.1."""
        expected = {
            "models.py": "2feb62565765e1c9161534fa7f9763ac62f944d40a1b8138bf64bd229b765caa",
            "main.py": "24323a8f910d192c2310cd4eb99e7312389ffe7ce0eeeb81fb8e11ceeb21f7ba",
            "dependencies.py": "e86760276f16d1b02ed8d3f13fefeaa959b2af109b844c481a1fe8073a0db2f4",
            "routers/runs.py": "17268a86604a5690bb92199c7a91ff2d80a27720e38a99b8e4b9eb897b979b15",
            "routers/streaming.py": "85be0791445663d23e542d7ec31485043aa069ba3ab192e3a5076a5dafba4ac5",
            "routers/threads.py": "85cd528da9ced024e3f658c79c7ae709c41d5f17ed2241f8e2793f63493022c5",
            "routers/store.py": "7519ff141498712f8eb7d31ef282ba7ed056810cbe88fb23733c489f287f4d41",
            "routers/background_runs.py": "a8e245b48732a3df1fb436196b7ac2cfc5e4a3a3075c5a4308c9fcf2bc1f2e87",
            "routers/agents.py": "bca683e2030764be8aa1383fa2c9dbf1b6e88bd02e4034e1fc179ec0d62cbfc4",
        }
        spec = Path(__file__).resolve().parents[2] / "openapi.json"
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "fastapi_code_generator",
                    "--input",
                    str(spec),
                    "--output-model-type",
                    "pydantic_v2.BaseModel",
                    "--output",
                    directory,
                    "--generate-routers",
                    "--disable-timestamp",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            actual = {
                str(path.relative_to(directory)): hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
                for path in Path(directory).rglob("*.py")
            }
        self.assertEqual(actual, expected)
