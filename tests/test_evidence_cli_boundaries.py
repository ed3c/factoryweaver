"""Offline CLI inputs retain main's duplicate-key refusal."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class EvidenceCLIBoundaries(unittest.TestCase):
    def test_duplicate_json_keys_refused_before_claim_evaluation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "ambiguous.json"
            data.write_text('{"protocol":"invalid","protocol":"also-invalid"}')
            raw = root / "raw.txt"
            raw.write_text("Synthetic source data only.")
            seed = root / "seed.bin"
            seed.write_bytes(b"x" * 32)
            commands = (("source_lock.py", str(data), str(raw)),
                        ("semantic_golden.py", str(data)),
                        ("blind_review.py", "packet", str(data), "--seed-file", str(seed)))
            for script, *args in commands:
                with self.subTest(script=script):
                    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2)
                    self.assertIn("duplicate_json_key:protocol", json.loads(result.stderr)["error"])
