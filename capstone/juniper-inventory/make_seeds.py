"""Regenerate the seed CSVs in seeds/ (they are committed; run this only to rebuild them).

Juniper Lane Goods' inventory feed for four weekly stock counts, Mondays
2026-09-07 to 2026-09-28: suppliers, products, stores, stock counts and
supplier deliveries. Deterministic: a fixed seed, and every draw goes through
Random.random(), so the files are byte-identical on every machine.

Two known problems are left in the feed, as the warehouse sends it:
  - three stock counts keyed in as negative numbers
  - two deliveries for product ids that are not in the product list

    python make_seeds.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20260928
COUNT_DAYS = [date(2026, 9, 7) + timedelta(weeks=w) for w in range(4)]   # Mondays
NEGATIVE_COUNTS = 3
UNKNOWN_PRODUCTS = ["P051", "P057"]

SUPPLIERS = [
    ("SUP1", "Timberline Camp Works", 12),       # supplier_id, supplier_name, lead_time_days
    ("SUP2", "Granite Peak Textiles", 10),
    ("SUP3", "Northfork Footwear Co.", 14),
    ("SUP4", "Redrock Climbing Supply", 7),
    ("SUP5", "Bluewater Gear Traders", 9),
]
CATEGORY_SUPPLIER = {"Tents": "SUP1", "Sleeping": "SUP1", "Cooking": "SUP1", "Apparel": "SUP2",
                     "Packs": "SUP2", "Footwear": "SUP3", "Climbing": "SUP4", "Accessories": "SUP5"}

STORES = [("S01", "Boulder"), ("S02", "Bend"), ("S03", "Bozeman"), ("S04", "Flagstaff"),
          ("S05", "Asheville"), ("S06", "Burlington"), ("S07", "Missoula"), ("S08", "Moab"),
          ("S09", "Duluth"), ("S10", "Truckee"), ("S11", "Hood River"), ("S12", "Durango")]

# The same 48 products as the sales repository: product_id P001..P048 in this order.
PRODUCTS = [
    ("Ridgeline 2-Person Tent", "Tents"), ("Ridgeline 4-Person Tent", "Tents"),
    ("Summit Ultralight 1-Person Tent", "Tents"), ("Basecamp 6-Person Cabin Tent", "Tents"),
    ("Trail Bivy Shelter", "Tents"), ("Tent Footprint 2-Person", "Tents"),
    ("Alpine 20F Down Sleeping Bag", "Sleeping"), ("Meadow 40F Synthetic Sleeping Bag", "Sleeping"),
    ("Self-Inflating Sleeping Pad", "Sleeping"), ("Insulated Air Pad", "Sleeping"),
    ("Camp Pillow", "Sleeping"), ("Sleeping Bag Liner", "Sleeping"),
    ("Switchback 28L Daypack", "Packs"), ("Switchback 45L Backpack", "Packs"),
    ("Expedition 65L Backpack", "Packs"), ("Hydration Reservoir 2L", "Packs"),
    ("Hip Pack 5L", "Packs"), ("Pack Rain Cover", "Packs"),
    ("Trailhead Hiking Boot Men's", "Footwear"), ("Trailhead Hiking Boot Women's", "Footwear"),
    ("Scree Trail Runner Men's", "Footwear"), ("Scree Trail Runner Women's", "Footwear"),
    ("Camp Sandal", "Footwear"), ("Merino Hiking Socks 2-Pack", "Footwear"),
    ("Storm Shell Rain Jacket", "Apparel"), ("Ridge Fleece Jacket", "Apparel"),
    ("Down Puffy Jacket", "Apparel"), ("Quick-Dry Hiking Pants", "Apparel"),
    ("Merino Base Layer Top", "Apparel"), ("Sun Hoodie", "Apparel"),
    ("Compact Canister Stove", "Cooking"), ("Fuel Canister 230g", "Cooking"),
    ("Titanium Cook Pot 1L", "Cooking"), ("Camp Utensil Set", "Cooking"),
    ("Insulated Camp Mug", "Cooking"), ("Squeeze Water Filter", "Cooking"),
    ("Climbing Harness", "Climbing"), ("Belay Device", "Climbing"),
    ("Locking Carabiner", "Climbing"), ("Chalk Bag", "Climbing"),
    ("Climbing Helmet", "Climbing"), ("Dynamic Rope 60m", "Climbing"),
    ("LED Headlamp 350 Lumen", "Accessories"), ("Trekking Poles Pair", "Accessories"),
    ("First-Aid Kit", "Accessories"), ("Insulated Water Bottle 1L", "Accessories"),
    ("Dry Bag 20L", "Accessories"), ("Pocket Multi-Tool", "Accessories"),
]


class Rng:
    def __init__(self, seed: int) -> None:
        self._random = random.Random(seed).random

    def between(self, lo: int, hi: int) -> int:
        return lo + int(self._random() * (hi - lo + 1))

    def chance(self, p: float) -> bool:
        return self._random() < p

    def sample(self, items: list, k: int) -> list:
        pool = list(items)
        for i in range(k):
            j = i + int(self._random() * (len(pool) - i))
            pool[i], pool[j] = pool[j], pool[i]
        return pool[:k]


def write(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{path.name:<18}{len(rows):>6} rows")


def main() -> None:
    rng = Rng(SEED)
    out = Path(__file__).resolve().parent / "seeds"
    out.mkdir(exist_ok=True)
    lead = {sid: days for sid, _, days in SUPPLIERS}

    products = []
    for n, (name, category) in enumerate(PRODUCTS, start=1):
        small = category in {"Cooking", "Climbing", "Accessories"}
        products.append({
            "product_id": f"P{n:03d}", "product_name": name, "category": category,
            "supplier_id": CATEGORY_SUPPLIER[category],
            "reorder_point": rng.between(6, 12) if small else rng.between(3, 6),
            "case_pack": 12 if small else rng.between(2, 4),
        })

    counts, receipts = [], []
    for store_id, _ in STORES:
        for p in products:
            on_hand = rng.between(p["reorder_point"], p["reorder_point"] * 3)
            arriving: list[tuple[date, int]] = []
            for monday in COUNT_DAYS:
                on_hand += sum(q for when, q in arriving if when <= monday)
                arriving = [(when, q) for when, q in arriving if when > monday]
                counts.append({"count_date": monday.isoformat(), "store_id": store_id,
                               "product_id": p["product_id"], "on_hand": on_hand})
                on_hand = max(0, on_hand - rng.between(0, p["reorder_point"]))
                if on_hand <= p["reorder_point"] and not arriving and monday < COUNT_DAYS[-1]:
                    ordered = monday + timedelta(days=1)
                    late = rng.chance(0.2)
                    days = lead[p["supplier_id"]] + (rng.between(2, 6) if late else -rng.between(0, 3))
                    quantity = p["case_pack"] * rng.between(1, 3)
                    receipts.append({"store_id": store_id, "product_id": p["product_id"],
                                     "supplier_id": p["supplier_id"], "ordered_on": ordered,
                                     "received_on": ordered + timedelta(days=days),
                                     "quantity": quantity})
                    arriving.append((ordered + timedelta(days=days), quantity))

    for row in rng.sample(counts, NEGATIVE_COUNTS):
        row["on_hand"] = -max(1, row["on_hand"])
    for pid, row in zip(UNKNOWN_PRODUCTS, rng.sample(receipts, len(UNKNOWN_PRODUCTS)), strict=True):
        receipts.append({**row, "product_id": pid})

    # The feed is dated on the last count: deliveries still on the road are not in it.
    receipts = [r for r in receipts if r["received_on"] <= COUNT_DAYS[-1]]
    receipts.sort(key=lambda r: (r["received_on"], r["store_id"], r["product_id"]))
    for n, r in enumerate(receipts, start=1):
        r.update(receipt_id=f"RC{n:04d}", ordered_on=r["ordered_on"].isoformat(),
                 received_on=r["received_on"].isoformat())
    receipts = [{k: r[k] for k in ("receipt_id", "supplier_id", "store_id", "product_id",
                                   "ordered_on", "received_on", "quantity")} for r in receipts]

    write(out / "suppliers.csv", [{"supplier_id": s, "supplier_name": n, "lead_time_days": d}
                                  for s, n, d in SUPPLIERS])
    write(out / "products.csv", products)
    write(out / "stores.csv", [{"store_id": s, "city": c} for s, c in STORES])
    write(out / "stock_counts.csv", counts)
    write(out / "receipts.csv", receipts)


if __name__ == "__main__":
    main()
