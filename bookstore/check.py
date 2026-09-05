import json
from collections import Counter

books = json.load(open("books.json", encoding="utf-8"))

assert len(books) == 1000, f"expected 1000 books, got {len(books)}"
assert len({b["upc"] for b in books}) == 1000, "duplicate UPCs"
assert len({b["category"] for b in books}) == 50, "missing categories"
assert all(isinstance(b["price"], (int, float)) for b in books), "price not numeric"
assert all(1 <= b["rating"] <= 5 for b in books), "bad rating"
assert all(b["product_url"].startswith("http") for b in books), "relative URL"
assert "Â" not in json.dumps(books), "encoding artifact"

print("OK —", len(books), "books")
print("Cheapest:", min(books, key=lambda b: b["price"])["title"])
print("Top categories:", Counter(b["category"] for b in books).most_common(5))

# --- Level 5 ---
expected = {
    "travel": ("Travel", 11),
    "poetry": ("Poetry", 19),
    "historical-fiction": ("Historical Fiction", 26),
    "mystery": ("Mystery", 32),
}
all_upcs = {b["upc"] for b in books}

for filename, (label, count) in expected.items():
    rows = json.load(open(f"{filename}.json", encoding="utf-8"))
    assert len(rows) == count, f"{label}: expected {count}, got {len(rows)}"
    assert all(r["category"] == label for r in rows), f"{label}: wrong category"
    assert all(r["upc"] in all_upcs for r in rows), f"{label}: book not in books.json"
    print(f"OK — {label}: {count}")