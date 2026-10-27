"""Generate Juniper Lane Goods' nightly CSV drop: six files in data/raw/.

Juniper Lane Goods is a fictional 12-store outdoor-gear retailer. Every night
its store system drops six CSV files: customers, products, stores, dates,
sales and returns. This script writes that drop for twelve weeks of trading,
Monday 2026-07-06 to Sunday 2026-09-27.

The output is deterministic. A fixed seed, and every random draw goes through
Random.random(), the one method Python promises to repeat across versions, so
every reader gets byte-identical files and the same numbers as the book.

The drop carries four defects on purpose, as real drops do:
  - customers with no email address
  - a store's batch of sales sent twice (duplicate order ids)
  - sales keyed in with a negative quantity
  - returns logged after the 30-day return window

Standard library only, so it runs anywhere Python 3 runs:

    python make_data.py                          # writes data/raw/ beside this file
    python make_data.py --out some/folder
    python make_data.py --through 2026-09-20     # the drop as it stood on that date
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20261016
START = date(2026, 7, 6)            # a Monday
WEEKS = 12
END = START + timedelta(days=7 * WEEKS - 1)   # Sunday 2026-09-27
RETURN_WINDOW_DAYS = 30             # store policy: returns accepted up to 30 days after the sale

CUSTOMERS = 900
NULL_EMAILS = 27
RESENT_BATCHES = 2                  # store-days whose sales batch arrived twice
NEGATIVE_QUANTITIES = 11
LATE_RETURNS = 9

# store_id, city, state, region, opened_on, square_feet, traffic (orders per day, before day effects)
STORES = [
    ("S01", "Boulder", "CO", "Mountain", "2012-04-14", 11800, 9.5),
    ("S02", "Bend", "OR", "Pacific", "2014-05-03", 9600, 7.5),
    ("S03", "Bozeman", "MT", "Mountain", "2015-08-22", 8400, 6.0),
    ("S04", "Flagstaff", "AZ", "Southwest", "2016-03-19", 7900, 5.5),
    ("S05", "Asheville", "NC", "Southeast", "2017-06-10", 9100, 7.0),
    ("S06", "Burlington", "VT", "Northeast", "2018-04-28", 7200, 5.0),
    ("S07", "Missoula", "MT", "Mountain", "2019-05-18", 6800, 4.5),
    ("S08", "Moab", "UT", "Southwest", "2019-09-07", 6100, 5.5),
    ("S09", "Duluth", "MN", "Midwest", "2020-07-11", 6500, 4.0),
    ("S10", "Truckee", "CA", "Pacific", "2021-05-01", 8800, 8.0),
    ("S11", "Hood River", "OR", "Pacific", "2022-06-04", 5900, 4.5),
    ("S12", "Durango", "CO", "Mountain", "2023-04-15", 7400, 6.0),
]

# product_name, category, list_price, unit_cost
PRODUCTS = [
    ("Ridgeline 2-Person Tent", "Tents", 249.00, 112.00),
    ("Ridgeline 4-Person Tent", "Tents", 399.00, 181.00),
    ("Summit Ultralight 1-Person Tent", "Tents", 329.00, 151.00),
    ("Basecamp 6-Person Cabin Tent", "Tents", 529.00, 244.00),
    ("Trail Bivy Shelter", "Tents", 159.00, 70.00),
    ("Tent Footprint 2-Person", "Tents", 39.00, 14.00),
    ("Alpine 20F Down Sleeping Bag", "Sleeping", 289.00, 128.00),
    ("Meadow 40F Synthetic Sleeping Bag", "Sleeping", 119.00, 49.00),
    ("Self-Inflating Sleeping Pad", "Sleeping", 89.00, 37.00),
    ("Insulated Air Pad", "Sleeping", 149.00, 63.00),
    ("Camp Pillow", "Sleeping", 29.00, 10.00),
    ("Sleeping Bag Liner", "Sleeping", 45.00, 17.00),
    ("Switchback 28L Daypack", "Packs", 99.00, 41.00),
    ("Switchback 45L Backpack", "Packs", 189.00, 82.00),
    ("Expedition 65L Backpack", "Packs", 279.00, 124.00),
    ("Hydration Reservoir 2L", "Packs", 39.00, 14.00),
    ("Hip Pack 5L", "Packs", 45.00, 17.00),
    ("Pack Rain Cover", "Packs", 25.00, 8.00),
    ("Trailhead Hiking Boot Men's", "Footwear", 169.00, 74.00),
    ("Trailhead Hiking Boot Women's", "Footwear", 169.00, 74.00),
    ("Scree Trail Runner Men's", "Footwear", 139.00, 60.00),
    ("Scree Trail Runner Women's", "Footwear", 139.00, 60.00),
    ("Camp Sandal", "Footwear", 59.00, 22.00),
    ("Merino Hiking Socks 2-Pack", "Footwear", 32.00, 11.00),
    ("Storm Shell Rain Jacket", "Apparel", 199.00, 84.00),
    ("Ridge Fleece Jacket", "Apparel", 89.00, 35.00),
    ("Down Puffy Jacket", "Apparel", 229.00, 98.00),
    ("Quick-Dry Hiking Pants", "Apparel", 79.00, 30.00),
    ("Merino Base Layer Top", "Apparel", 85.00, 33.00),
    ("Sun Hoodie", "Apparel", 55.00, 20.00),
    ("Compact Canister Stove", "Cooking", 59.00, 23.00),
    ("Fuel Canister 230g", "Cooking", 9.00, 4.00),
    ("Titanium Cook Pot 1L", "Cooking", 69.00, 28.00),
    ("Camp Utensil Set", "Cooking", 25.00, 8.00),
    ("Insulated Camp Mug", "Cooking", 22.00, 7.00),
    ("Squeeze Water Filter", "Cooking", 45.00, 18.00),
    ("Climbing Harness", "Climbing", 79.00, 32.00),
    ("Belay Device", "Climbing", 32.00, 12.00),
    ("Locking Carabiner", "Climbing", 15.00, 5.00),
    ("Chalk Bag", "Climbing", 24.00, 8.00),
    ("Climbing Helmet", "Climbing", 75.00, 31.00),
    ("Dynamic Rope 60m", "Climbing", 239.00, 109.00),
    ("LED Headlamp 350 Lumen", "Accessories", 49.00, 18.00),
    ("Trekking Poles Pair", "Accessories", 119.00, 48.00),
    ("First-Aid Kit", "Accessories", 35.00, 13.00),
    ("Insulated Water Bottle 1L", "Accessories", 34.00, 12.00),
    ("Dry Bag 20L", "Accessories", 29.00, 10.00),
    ("Pocket Multi-Tool", "Accessories", 59.00, 24.00),
]

# Small items people buy several of at once.
MULTI_BUY = {"Merino Hiking Socks 2-Pack", "Fuel Canister 230g", "Locking Carabiner",
             "Insulated Camp Mug", "Camp Utensil Set", "Chalk Bag"}

RETURN_RATE = {"Footwear": 0.10, "Apparel": 0.09, "Packs": 0.06, "Tents": 0.05,
               "Sleeping": 0.05, "Accessories": 0.04, "Cooking": 0.03, "Climbing": 0.03}
REASONS = {
    "Footwear": ["Wrong size", "Wrong size", "Wrong size", "Uncomfortable", "Changed mind"],
    "Apparel": ["Wrong size", "Wrong size", "Changed mind", "Not as described"],
    "default": ["Defective", "Changed mind", "Not as described", "Gift return"],
}

# Labor Day week: 20% off apparel and footwear.
SALE_WEEK = (date(2026, 9, 7), date(2026, 9, 13))
SALE_CATEGORIES = {"Apparel", "Footwear"}

FIRST_NAMES = [
    "Avery", "Mateo", "Priya", "Owen", "Hana", "Caleb", "Sofia", "Elijah", "Mei", "Jonah",
    "Ruth", "Tariq", "Lena", "Marcus", "Ines", "Felix", "Grace", "Rafael", "Nora", "Theo",
    "Amara", "Wyatt", "Leila", "Silas", "Yuki", "Hugo", "Clara", "Desmond", "Ingrid", "Kofi",
    "Maya", "Ezra", "Talia", "Rowan", "Anya", "Bennett", "Zara", "Gideon", "Lucia", "Arjun",
]
LAST_NAMES = [
    "Alvarez", "Brennan", "Chen", "Dubois", "Eriksen", "Fischer", "Gallagher", "Haddad",
    "Ivanova", "Jensen", "Kowalski", "Lindqvist", "Moreau", "Nakamura", "Okafor", "Petrov",
    "Quinn", "Rossi", "Sato", "Thornton", "Underwood", "Varga", "Whitaker", "Xu", "Yamada",
    "Zielinski", "Abernathy", "Bianchi", "Castellanos", "Delacroix",
]
EMAIL_DOMAINS = ["example.com", "example.net", "example.org"]   # reserved for examples: never real inboxes
TIERS = ["basic"] * 6 + ["silver"] * 3 + ["gold"]


class Rng:
    """Every draw comes from Random.random(), which repeats across Python versions."""

    def __init__(self, seed: int) -> None:
        self._random = random.Random(seed).random

    def unit(self) -> float:
        return self._random()

    def chance(self, p: float) -> bool:
        return self._random() < p

    def between(self, lo: int, hi: int) -> int:
        """An integer from lo to hi, both included."""
        return lo + int(self._random() * (hi - lo + 1))

    def pick(self, items: list):
        return items[int(self._random() * len(items))]

    def weighted(self, items: list, weights: list[float]):
        target = self._random() * sum(weights)
        for item, weight in zip(items, weights, strict=True):
            target -= weight
            if target < 0:
                return item
        return items[-1]

    def sample(self, items: list, k: int) -> list:
        """k distinct items, in the order drawn."""
        pool = list(items)
        for i in range(k):
            j = i + int(self._random() * (len(pool) - i))
            pool[i], pool[j] = pool[j], pool[i]
        return pool[:k]


def money(value: float) -> str:
    return f"{value:.2f}"


def build(rng: Rng) -> dict[str, list[dict]]:
    stores = [
        {"store_id": sid, "store_name": f"Juniper Lane {city}", "city": city, "state": state,
         "region": region, "opened_on": opened, "square_feet": sqft}
        for sid, city, state, region, opened, sqft, _ in STORES
    ]
    traffic = {sid: t for sid, *_, t in STORES}

    products = [
        {"product_id": f"P{n:03d}", "product_name": name, "category": cat,
         "list_price": money(price), "unit_cost": money(cost)}
        for n, (name, cat, price, cost) in enumerate(PRODUCTS, start=1)
    ]
    by_id = {p["product_id"]: p for p in products}
    product_ids = list(by_id)
    # Cheaper items sell more often; a random factor keeps every product different.
    popularity = [(1.0 + rng.unit()) / (float(p["list_price"]) ** 0.5) for p in products]

    customers = []
    seen_emails: set[str] = set()
    span = (START - date(2019, 3, 1)).days
    for n in range(1, CUSTOMERS + 1):
        first, last = rng.pick(FIRST_NAMES), rng.pick(LAST_NAMES)
        email = f"{first}.{last}@{rng.pick(EMAIL_DOMAINS)}".lower()
        suffix = 2
        while email in seen_emails:
            local, domain = email.split("@")
            email = f"{local.rstrip('0123456789')}{suffix}@{domain}"
            suffix += 1
        seen_emails.add(email)
        customers.append({
            "customer_id": f"C{n:04d}", "first_name": first, "last_name": last, "email": email,
            "home_store_id": rng.pick([s["store_id"] for s in stores]),
            "joined_on": (date(2019, 3, 1) + timedelta(days=rng.between(0, span - 1))).isoformat(),
            "loyalty_tier": rng.pick(TIERS),
        })
    for customer in rng.sample(customers, NULL_EMAILS):           # defect 1
        customer["email"] = ""
    regulars: dict[str, list[str]] = {}
    for c in customers:
        regulars.setdefault(c["home_store_id"], []).append(c["customer_id"])
    all_ids = [c["customer_id"] for c in customers]

    dates = []
    day = START
    while day <= END:
        week_start = day - timedelta(days=day.weekday())
        dates.append({
            "date_key": day.strftime("%Y%m%d"), "date": day.isoformat(),
            "day_name": day.strftime("%A"), "week_start": week_start.isoformat(),
            "iso_week": day.isocalendar().week, "month": day.month,
            "month_name": day.strftime("%B"), "quarter": (day.month - 1) // 3 + 1,
            "is_weekend": "true" if day.weekday() >= 5 else "false",
        })
        day += timedelta(days=1)

    # Sales: one row per order, one product per order in this extract.
    batches: list[list[dict]] = []
    order_no = 100000
    for d in dates:
        day = date.fromisoformat(d["date"])
        weekday_factor = [0.8, 0.75, 0.8, 0.9, 1.15, 1.7, 1.5][day.weekday()]
        season = 1.0 - 0.15 * (day - START).days / (END - START).days   # summer fades into September
        holiday = 1.6 if day == date(2026, 9, 7) else 1.0               # Labor Day
        for s in stores:
            sid = s["store_id"]
            mean = traffic[sid] * weekday_factor * season * holiday
            count = max(0, round(mean * (0.7 + 0.6 * rng.unit())))
            batch = []
            for _ in range(count):
                order_no += 1
                pid = rng.weighted(product_ids, popularity)
                product = by_id[pid]
                if product["product_name"] in MULTI_BUY:
                    qty = rng.between(1, 4)
                else:
                    qty = 2 if rng.chance(0.08) else 1
                price = float(product["list_price"])
                if SALE_WEEK[0] <= day <= SALE_WEEK[1] and product["category"] in SALE_CATEGORIES:
                    price *= 0.80
                elif rng.chance(0.05):
                    price *= 0.85                                       # clearance or price match
                customer = rng.pick(regulars[sid]) if rng.chance(0.8) else rng.pick(all_ids)
                batch.append({
                    "order_id": f"JL-{order_no}", "order_date": d["date"], "store_id": sid,
                    "customer_id": customer, "product_id": pid, "quantity": qty,
                    "unit_price": money(round(price + 1e-9, 2)),
                })
            batches.append(batch)

    sales = [row for batch in batches for row in batch]
    category = {p["product_id"]: p["category"] for p in products}

    # Returns inside the window.
    returns = []
    for row in sales:
        cat = category[row["product_id"]]
        if not rng.chance(RETURN_RATE[cat]):
            continue
        lag = int(rng.unit() ** 1.5 * (RETURN_WINDOW_DAYS + 1))          # 0..30 days
        returned = date.fromisoformat(row["order_date"]) + timedelta(days=lag)
        qty = 1 if row["quantity"] > 1 and rng.chance(0.5) else row["quantity"]
        reasons = REASONS.get(cat, REASONS["default"])
        if returned <= END:                                             # not yet happened otherwise
            returns.append({"order_id": row["order_id"], "return_date": returned.isoformat(),
                            "quantity": qty, "reason": rng.pick(reasons)})

    returned_orders = {r["order_id"] for r in returns}
    latest_ok = END - timedelta(days=RETURN_WINDOW_DAYS + 10)
    candidates = [r for r in sales if r["order_id"] not in returned_orders
                  and date.fromisoformat(r["order_date"]) <= latest_ok]
    for row in rng.sample(candidates, LATE_RETURNS):                    # defect 4
        ordered = date.fromisoformat(row["order_date"])
        longest = min(70, (END - ordered).days)
        lag = rng.between(RETURN_WINDOW_DAYS + 4, longest)
        cat = category[row["product_id"]]
        returns.append({"order_id": row["order_id"],
                        "return_date": (ordered + timedelta(days=lag)).isoformat(),
                        "quantity": row["quantity"],
                        "reason": rng.pick(REASONS.get(cat, REASONS["default"]))})
        returned_orders.add(row["order_id"])

    returns.sort(key=lambda r: (r["return_date"], r["order_id"]))
    for n, r in enumerate(returns, start=1):
        r["return_id"] = f"R{n:05d}"

    # Defect 3: quantities keyed in as negatives (never on an order that was returned).
    keyed = [r for r in sales if r["order_id"] not in returned_orders]
    negated = set()
    for row in rng.sample(keyed, NEGATIVE_QUANTITIES):
        row["quantity"] = -row["quantity"]
        negated.add(row["order_id"])

    # Defect 2: two store-days whose whole batch the till sent twice, back to back.
    busy = [i for i, b in enumerate(batches)
            if len(b) >= 6 and not any(r["order_id"] in negated for r in b)]
    resent = set(rng.sample(busy, RESENT_BATCHES))
    sales = []
    for i, batch in enumerate(batches):
        sales.extend(batch)
        if i in resent:
            sales.extend(dict(row) for row in batch)

    return {"customers": customers, "products": products, "stores": stores,
            "dates": dates, "sales": sales, "returns": returns}


COLUMNS = {
    "customers": ["customer_id", "first_name", "last_name", "email", "home_store_id",
                  "joined_on", "loyalty_tier"],
    "products": ["product_id", "product_name", "category", "list_price", "unit_cost"],
    "stores": ["store_id", "store_name", "city", "state", "region", "opened_on", "square_feet"],
    "dates": ["date_key", "date", "day_name", "week_start", "iso_week", "month", "month_name",
              "quarter", "is_weekend"],
    "sales": ["order_id", "order_date", "store_id", "customer_id", "product_id", "quantity",
              "unit_price"],
    "returns": ["return_id", "order_id", "return_date", "quantity", "reason"],
}


def cut_off(tables: dict[str, list[dict]], through: date) -> None:
    """Keep only what the drop held on `through`: later sales, returns and dates go."""
    stamp = through.isoformat()
    tables["dates"] = [d for d in tables["dates"] if d["date"] <= stamp]
    tables["sales"] = [s for s in tables["sales"] if s["order_date"] <= stamp]
    tables["returns"] = [r for r in tables["returns"] if r["return_date"] <= stamp]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "data" / "raw",
                        help="folder to write the six CSV files into (default: data/raw beside this script)")
    parser.add_argument("--through", type=date.fromisoformat, default=END,
                        help=f"last day of trading to include, {START} to {END} (default: {END})")
    args = parser.parse_args()
    if not START <= args.through <= END:
        parser.error(f"--through must fall between {START} and {END}")

    tables = build(Rng(SEED))
    cut_off(tables, args.through)

    args.out.mkdir(parents=True, exist_ok=True)
    for name, columns in COLUMNS.items():
        path = args.out / f"{name}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows({c: row[c] for c in columns} for row in tables[name])
        print(f"{path.name:<14}{len(tables[name]):>6} rows")
    print(f"Wrote the drop for {START} to {args.through} into {args.out}")


if __name__ == "__main__":
    main()
