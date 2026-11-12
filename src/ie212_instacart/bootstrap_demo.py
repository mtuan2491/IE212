"""Exercise bootstrap gates on a tiny fixture. Production pair counting starts at T20/T21."""
import csv
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests/fixtures/baskets.csv"
OUTPUT = ROOT / "artifacts/demo/pair_counts.csv"


def count_pairs(source):
    baskets = defaultdict(set)
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["order_id", "product_id"]:
            raise ValueError("Invalid basket fixture header")
        for row in reader:
            order, product = int(row["order_id"]), int(row["product_id"])
            if order <= 0 or product <= 0:
                raise ValueError("Order and product IDs must be positive")
            baskets[order].add(product)
    return Counter(pair for basket in baskets.values() for pair in combinations(sorted(basket), 2))


def write_counts(source=FIXTURE, destination=OUTPUT):
    counts = count_pairs(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("product_a", "product_b", "count"))
        writer.writerows((first, second, counts[first, second]) for first, second in sorted(counts))


if __name__ == "__main__":
    write_counts()
