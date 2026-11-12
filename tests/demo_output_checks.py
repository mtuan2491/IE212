import csv
import unittest
from pathlib import Path


class DemoOutputTests(unittest.TestCase):
    def test_complete_pair_counts(self):
        output = Path(__file__).resolve().parents[1] / "artifacts/demo/pair_counts.csv"
        with output.open(encoding="utf-8", newline="") as source:
            self.assertEqual(list(csv.reader(source)), [
                ["product_a", "product_b", "count"],
                ["3", "7", "2"],
                ["3", "9", "1"],
            ])
