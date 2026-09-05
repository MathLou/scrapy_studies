# Scrapy Challenge: Books to Scrape

Your mission is to build a Scrapy project that crawls
[books.toscrape.com](https://books.toscrape.com) and produces a single JSON file
containing **all 1000 books** with a well-defined schema.

That site exists specifically for scraping practice, so you can hammer it without
guilt — but be polite anyway (see [Rules](#rules)). It's a static HTML sandbox: no
JavaScript rendering, no login, no anti-bot defenses. Perfect for learning the
mechanics without fighting the site.

**Deliverables:**

1. A Git repository containing the Scrapy project.
2. The output file `books.json` produced by your spider.
3. Four category files from Level 5: `travel.json`, `poetry.json`,
   `historical-fiction.json`, `mystery.json`.

---

## Levels

Work through these in order. Each one is a working scraper — don't jump to the end.

### Level 1 — One page

Create the project and a spider that extracts every book from the homepage
(20 books). Get `title`, `price`, and `product_url` printed to the console.

```bash
pip install scrapy
scrapy startproject bookstore
cd bookstore
scrapy genspider books books.toscrape.com
scrapy crawl books
```

### Level 2 — Pagination

Follow the "next" link until there are no more pages. You should now have 1000
items from 50 pages.

Sanity check:

```bash
scrapy crawl books -O books.json
python -c "import json; print(len(json.load(open('books.json'))))"   # 1000
```

### Level 3 — Detail pages

The listing page doesn't have everything. For each book, follow the link to its
product page and pull the full record described in [Schema](#schema): UPC,
category, description, tax fields, review count, and so on.

### Level 4 — Clean data

Raw HTML strings are not the deliverable. `"£51.77"` must become `51.77`.
`"In stock (22 available)"` must become `22`. `"Three"` must become `3`.

Do this with **Items** (`items.py`) and either **ItemLoaders** with input/output
processors or an **item pipeline** (`pipelines.py`). Add a pipeline that drops or
logs any item failing validation (missing UPC, negative price, rating outside
1–5).

### Level 5 — Crawl by category

Add a **second spider** called `category` that scrapes only one category, chosen
at runtime:

```bash
scrapy crawl category -a name=poetry -O poetry.json
```

Spider arguments arrive as attributes on `self`, so `-a name=poetry` gives you
`self.name_arg` (careful — `self.name` is the spider's own name, so call your
argument something else, or you'll break the spider).

Run it against these four categories. The counts are real, so you can verify your
work exactly:

| Category | URL slug | Books | Listing pages |
|---|---|---|---|
| Travel | `travel_2` | 11 | 1 |
| Poetry | `poetry_23` | 19 | 1 |
| Historical Fiction | `historical-fiction_4` | 26 | 2 |
| Mystery | `mystery_3` | 32 | 2 |

Category URLs follow this pattern:

```
https://books.toscrape.com/catalogue/category/books/poetry_23/index.html
```

Two of these fit on one page and two need pagination, which is the point — your
spider has to handle both without special-casing either.

Map friendly names to slugs with a dictionary at the top of the spider, and exit
with a clear error message if the user passes a name that isn't in it. Guessing
the numeric suffix is impossible, so hardcoding the mapping is the right call
here.

Output four files: `travel.json`, `poetry.json`, `historical-fiction.json`,
`mystery.json`. They use the same schema as `books.json` — reuse your item,
your pipeline, and your parsing code. If you find yourself copy-pasting the
detail-page parser into the second spider, stop and move it somewhere both
spiders can import.

---

## Schema

One JSON array, one object per book, 1000 objects. Field names exactly as below.

| Field | Type | Notes |
|---|---|---|
| `title` | string | Full title, from the product page (the listing page truncates it) |
| `price` | number | GBP, no currency symbol, 2 decimals |
| `price_excl_tax` | number | From the product information table |
| `price_incl_tax` | number | From the product information table |
| `tax` | number | From the product information table |
| `availability` | integer | Number of copies in stock, parsed out of the text |
| `in_stock` | boolean | `true` when `availability > 0` |
| `rating` | integer | 1–5, converted from the word in the CSS class |
| `category` | string | From the breadcrumb, e.g. `"Poetry"` |
| `upc` | string | Unique per book — use it to check for duplicates |
| `product_type` | string | Always `"Books"` on this site, but extract it anyway |
| `num_reviews` | integer | From the product information table |
| `description` | string or null | `null` when a book has no description |
| `image_url` | string | Absolute URL, not the `../../` relative one |
| `product_url` | string | Absolute URL of the product page |

### Example record

```json
{
  "title": "A Light in the Attic",
  "price": 51.77,
  "price_excl_tax": 51.77,
  "price_incl_tax": 51.77,
  "tax": 0.0,
  "availability": 22,
  "in_stock": true,
  "rating": 3,
  "category": "Poetry",
  "upc": "a897fe39b1053632",
  "product_type": "Books",
  "num_reviews": 0,
  "description": "It's hard to imagine a world without A Light in the Attic...",
  "image_url": "https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

### JSON Schema

Use this to validate your output if you want to be thorough
(`pip install jsonschema`).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "array",
  "minItems": 1000,
  "maxItems": 1000,
  "items": {
    "type": "object",
    "required": [
      "title", "price", "price_excl_tax", "price_incl_tax", "tax",
      "availability", "in_stock", "rating", "category", "upc",
      "product_type", "num_reviews", "description", "image_url", "product_url"
    ],
    "additionalProperties": false,
    "properties": {
      "title":          { "type": "string", "minLength": 1 },
      "price":          { "type": "number", "minimum": 0 },
      "price_excl_tax": { "type": "number", "minimum": 0 },
      "price_incl_tax": { "type": "number", "minimum": 0 },
      "tax":            { "type": "number", "minimum": 0 },
      "availability":   { "type": "integer", "minimum": 0 },
      "in_stock":       { "type": "boolean" },
      "rating":         { "type": "integer", "minimum": 1, "maximum": 5 },
      "category":       { "type": "string", "minLength": 1 },
      "upc":            { "type": "string", "pattern": "^[a-f0-9]{16}$" },
      "product_type":   { "type": "string" },
      "num_reviews":    { "type": "integer", "minimum": 0 },
      "description":    { "type": ["string", "null"] },
      "image_url":      { "type": "string", "format": "uri" },
      "product_url":    { "type": "string", "format": "uri" }
    }
  }
}
```

---

## Acceptance criteria

Your submission passes when all of these are true:

- [ ] `scrapy crawl books -O books.json` regenerates the file from scratch.
- [ ] `books.json` has exactly 1000 objects.
- [ ] Every object validates against the JSON Schema above.
- [ ] All 1000 `upc` values are unique.
- [ ] All 50 categories appear in the data.
- [ ] Numbers are JSON numbers, not strings. No `"£"` anywhere in the file.
- [ ] `description` is `null` for books without one — not `""`, not missing.
- [ ] No `Â` characters anywhere in the file (see [Gotchas](#gotchas)).
- [ ] The crawl runs with `DOWNLOAD_DELAY` set and `ROBOTSTXT_OBEY = True`.
- [ ] `scrapy crawl category -a name=<x>` works for all four categories.
- [ ] The four category files have 11, 19, 26 and 32 objects respectively.
- [ ] Every object in a category file has that category in its `category` field.
- [ ] Every book in the category files also appears in `books.json`, same UPC.
- [ ] An unknown category name fails with a readable message, not a traceback.
- [ ] The repo has a `README.md` explaining how to install and run it.
- [ ] The repo has a `requirements.txt` and a `.gitignore`.
- [ ] No secrets, no `venv/`, no `.scrapy/` cache committed.

### Self-check script

Drop this in `check.py` at the repo root and run it before submitting.

```python
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
```

---

## Gotchas

These are the things that will actually cost you time. Read them before you get
stuck, not after.

**Rating lives in the class attribute.** The markup is
`<p class="star-rating Three">` with no text content. Extract the class, split it,
map the word to a number. There is no digit anywhere in the HTML.

**The `Â£` problem.** The site declares one encoding and serves another, so prices
often come through as `Â£51.77`. Since you're stripping the symbol and casting to
float anyway, a regex like `r"[\d.]+"` sidesteps it entirely. If you see `Â` in
your output, your parsing is too naive.

**Listing titles are truncated.** The `<a>` text on the listing page is cut off,
but the `title` attribute has the full string — and the product page `<h1>` is
always complete. Prefer the product page.

**Relative URLs everywhere.** Links look like `../../../book_1000/index.html`.
Use `response.follow()` or `response.urljoin()` and never string concatenation.

**Some books have no description.** `#product_description` is simply absent.
Don't let that raise, and don't let it produce an empty string.

**The description is a sibling, not a child.** It sits in a `<p>` *after* the
`#product_description` div, so you need something like
`response.css("#product_description ~ p::text")`.

**Availability text varies in spacing.** Extract with a regex on the digits rather
than slicing at fixed positions.

**Category comes from the breadcrumb**, third item — not from the sidebar and not
from the URL.

**Single-page categories have no "next" link at all.** Travel and Poetry fit on
one page, so the pagination element is simply absent from the HTML. If your
pagination code assumes the link exists, those two will crash while Mystery and
Historical Fiction work fine.

**All books have zero tax and identical excl/incl prices.** That's not a bug in
your scraper, that's just the fixture data. Extract the fields anyway.

**Use `-O` not `-o`.** Lowercase `-o` *appends* to the file, so re-running the
crawl gives you 2000 items. Uppercase `-O` overwrites.

---

## Rules

- Scrapy only. No `requests` + `BeautifulSoup` loop pretending to be a crawler.
  The point is to learn the framework: spiders, items, pipelines, settings.
- Set a `DOWNLOAD_DELAY` (0.25s is fine) and keep `ROBOTSTXT_OBEY = True`.
  Set a real `USER_AGENT` identifying your project.
- No hardcoded page count. `range(1, 51)` is banned — follow the "next" link.
  A crawler that breaks when the site adds a page isn't a crawler.
- Don't commit `books.json` generated by hand or edited by hand.
- Everything you learn here transfers to real targets, where the rules are
  different: check the site's terms, respect `robots.txt`, throttle hard, and
  don't scrape personal data. This sandbox is free practice precisely because
  most sites aren't.

---

## Suggested repo layout

```
books-scraper/
├── README.md              # how to install and run
├── requirements.txt
├── .gitignore
├── check.py
├── books.json             # the deliverable
├── travel.json
├── poetry.json
├── historical-fiction.json
├── mystery.json
└── bookstore/
    ├── scrapy.cfg
    └── bookstore/
        ├── __init__.py
        ├── items.py       # Book item definition
        ├── parsers.py     # shared parsing, used by both spiders
        ├── pipelines.py   # cleaning + validation
        ├── settings.py
        └── spiders/
            ├── __init__.py
            ├── books.py       # whole catalogue
            └── category.py    # one category, -a name=...
```

---

## Reference

- Scrapy tutorial: https://docs.scrapy.org/en/latest/intro/tutorial.html
- Selectors: https://docs.scrapy.org/en/latest/topics/selectors.html
- Item pipelines: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
- `scrapy shell "https://books.toscrape.com"` — your best friend. Test every
  selector here before putting it in the spider.

---

## Submitting

Send the Git repository URL and the five JSON files. Include in your README:

- How long the full crawl takes.
- One thing that broke and how you found it.
- One thing you'd do differently if the site had 1,000,000 books instead of 1000.
