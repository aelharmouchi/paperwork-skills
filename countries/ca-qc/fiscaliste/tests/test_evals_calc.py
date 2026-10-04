"""Vérifie que les valeurs attendues dans evals.json (champ "calc") correspondent
à la sortie réelle du calculateur. Empêche une dérive entre données, script et evals."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPT = SKILL / "scripts" / "calc_impot_qc.py"


def dig(obj, dotted):
    for part in dotted.split("."):
        obj = obj[part]
    return obj


class TestEvalsCalc(unittest.TestCase):
    def test_calc_expectations(self):
        evals = json.loads((SKILL / "evals" / "evals.json").read_text(encoding="utf-8"))["evals"]
        checked = 0
        for ev in evals:
            calc = ev.get("calc")
            if not calc:
                continue
            out = subprocess.run(
                [sys.executable, str(SCRIPT), *calc["args"], "--json"],
                capture_output=True, text=True, check=True,
            )
            result = json.loads(out.stdout)
            for path, expected in calc["expect"].items():
                self.assertAlmostEqual(dig(result, path), expected, places=2,
                                       msg=f"eval {ev['id']} {path}")
                checked += 1
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
