"""
Seed script for products and categories.
Generates dev/test data — run against a local database.

Usage:
    python scripts/seed_products.py
"""
import uuid
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

CATEGORIES: list[dict] = [
    {"id": str(uuid.uuid4()), "name": "Electronics", "slug": "electronics"},
    {"id": str(uuid.uuid4()), "name": "Clothing", "slug": "clothing"},
    {"id": str(uuid.uuid4()), "name": "Home & Kitchen", "slug": "home-kitchen"},
    {"id": str(uuid.uuid4()), "name": "Books", "slug": "books"},
    {"id": str(uuid.uuid4()), "name": "Sports & Outdoors", "slug": "sports-outdoors"},
]

# Map slug -> id for product FK references
_cat_id = {c["slug"]: c["id"] for c in CATEGORIES}

# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

PRODUCTS: list[dict] = [
    # Electronics (8 products)
    {
        "id": str(uuid.uuid4()),
        "name": "Wireless Bluetooth Headphones",
        "description": "Over-ear noise-cancelling headphones with 30h battery life.",
        "price": "79.99",
        "stock_quantity": 150,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/headphones.jpg",
        "images": ["https://example.com/images/headphones-1.jpg", "https://example.com/images/headphones-2.jpg"],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "USB-C Charging Cable 2m",
        "description": "Braided nylon USB-C to USB-C cable, 100W PD.",
        "price": "12.99",
        "stock_quantity": 500,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/cable.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Mechanical Keyboard",
        "description": "Cherry MX Brown switches, RGB backlit, full-size.",
        "price": "129.99",
        "stock_quantity": 0,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/keyboard.jpg",
        "images": ["https://example.com/images/keyboard-top.jpg"],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "4K Webcam",
        "description": "Ultra HD webcam with auto-focus and built-in mic.",
        "price": "89.50",
        "stock_quantity": 45,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": None,
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Portable SSD 1TB",
        "description": "NVMe external SSD, USB 3.2 Gen 2, read up to 1050MB/s.",
        "price": "109.00",
        "stock_quantity": 200,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/ssd.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Discontinued MP3 Player",
        "description": "Legacy MP3 player — no longer manufactured.",
        "price": "29.99",
        "stock_quantity": 0,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": None,
        "images": [],
        "is_active": False,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Smart Power Strip",
        "description": "WiFi-enabled power strip with 4 outlets and 2 USB ports.",
        "price": "34.99",
        "stock_quantity": 80,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/powerstrip.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with adjustable DPI.",
        "price": "24.99",
        "stock_quantity": 300,
        "category_id": _cat_id["electronics"],
        "thumbnail_url": "https://example.com/images/mouse.jpg",
        "images": [],
        "is_active": True,
    },
    # Clothing (5 products)
    {
        "id": str(uuid.uuid4()),
        "name": "Cotton Crew-Neck T-Shirt",
        "description": "100% organic cotton, unisex fit, available in 8 colours.",
        "price": "19.99",
        "stock_quantity": 400,
        "category_id": _cat_id["clothing"],
        "thumbnail_url": "https://example.com/images/tshirt.jpg",
        "images": ["https://example.com/images/tshirt-black.jpg", "https://example.com/images/tshirt-white.jpg"],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Slim Fit Jeans",
        "description": "Stretch denim, mid-rise, slim tapered leg.",
        "price": "49.99",
        "stock_quantity": 120,
        "category_id": _cat_id["clothing"],
        "thumbnail_url": "https://example.com/images/jeans.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Winter Parka",
        "description": "Waterproof insulated parka rated to -20C.",
        "price": "189.00",
        "stock_quantity": 0,
        "category_id": _cat_id["clothing"],
        "thumbnail_url": "https://example.com/images/parka.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Running Socks 3-Pack",
        "description": "Moisture-wicking cushioned ankle socks.",
        "price": "14.99",
        "stock_quantity": 600,
        "category_id": _cat_id["clothing"],
        "thumbnail_url": None,
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Vintage Denim Jacket",
        "description": "Retro-washed trucker jacket — limited edition.",
        "price": "79.00",
        "stock_quantity": 0,
        "category_id": _cat_id["clothing"],
        "thumbnail_url": "https://example.com/images/denim-jacket.jpg",
        "images": [],
        "is_active": False,
    },
    # Home & Kitchen (5 products)
    {
        "id": str(uuid.uuid4()),
        "name": "Stainless Steel French Press",
        "description": "Double-wall insulated, 1L capacity.",
        "price": "34.99",
        "stock_quantity": 90,
        "category_id": _cat_id["home-kitchen"],
        "thumbnail_url": "https://example.com/images/frenchpress.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Bamboo Cutting Board Set",
        "description": "Set of 3 cutting boards in small, medium, and large.",
        "price": "27.50",
        "stock_quantity": 200,
        "category_id": _cat_id["home-kitchen"],
        "thumbnail_url": "https://example.com/images/cuttingboard.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Cast Iron Skillet 12-inch",
        "description": "Pre-seasoned cast iron skillet, oven-safe to 500F.",
        "price": "39.99",
        "stock_quantity": 75,
        "category_id": _cat_id["home-kitchen"],
        "thumbnail_url": "https://example.com/images/skillet.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Electric Kettle 1.7L",
        "description": "Fast-boil BPA-free electric kettle with auto shut-off.",
        "price": "44.99",
        "stock_quantity": 60,
        "category_id": _cat_id["home-kitchen"],
        "thumbnail_url": "https://example.com/images/kettle.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Silicone Baking Mat Set",
        "description": "Non-stick reusable baking mats, set of 2.",
        "price": "15.99",
        "stock_quantity": 0,
        "category_id": _cat_id["home-kitchen"],
        "thumbnail_url": None,
        "images": [],
        "is_active": True,
    },
    # Books (4 products)
    {
        "id": str(uuid.uuid4()),
        "name": "Designing Data-Intensive Applications",
        "description": "Martin Kleppmann. Essential reading for backend engineers.",
        "price": "42.00",
        "stock_quantity": 110,
        "category_id": _cat_id["books"],
        "thumbnail_url": "https://example.com/images/ddia.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Clean Code",
        "description": "Robert C. Martin. A handbook of agile software craftsmanship.",
        "price": "35.99",
        "stock_quantity": 85,
        "category_id": _cat_id["books"],
        "thumbnail_url": "https://example.com/images/cleancode.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "The Pragmatic Programmer",
        "description": "Andrew Hunt & David Thomas. 20th anniversary edition.",
        "price": "44.99",
        "stock_quantity": 60,
        "category_id": _cat_id["books"],
        "thumbnail_url": "https://example.com/images/pragprog.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Out-of-Print Collector Edition",
        "description": "Rare collectible — no longer available.",
        "price": "199.99",
        "stock_quantity": 0,
        "category_id": _cat_id["books"],
        "thumbnail_url": None,
        "images": [],
        "is_active": False,
    },
    # Sports & Outdoors (4 products)
    {
        "id": str(uuid.uuid4()),
        "name": "Yoga Mat 6mm",
        "description": "Non-slip TPE yoga mat with carrying strap.",
        "price": "29.99",
        "stock_quantity": 250,
        "category_id": _cat_id["sports-outdoors"],
        "thumbnail_url": "https://example.com/images/yogamat.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Resistance Band Set",
        "description": "5 bands with varying resistance levels plus door anchor.",
        "price": "22.99",
        "stock_quantity": 180,
        "category_id": _cat_id["sports-outdoors"],
        "thumbnail_url": "https://example.com/images/bands.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Insulated Water Bottle 750ml",
        "description": "Double-wall vacuum insulated, keeps cold 24h / hot 12h.",
        "price": "26.50",
        "stock_quantity": 320,
        "category_id": _cat_id["sports-outdoors"],
        "thumbnail_url": "https://example.com/images/bottle.jpg",
        "images": [],
        "is_active": True,
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Camping Hammock",
        "description": "Lightweight nylon hammock with tree straps, supports 200kg.",
        "price": "39.99",
        "stock_quantity": 0,
        "category_id": _cat_id["sports-outdoors"],
        "thumbnail_url": "https://example.com/images/hammock.jpg",
        "images": [],
        "is_active": True,
    },
]


def get_seed_data() -> dict[str, list[dict]]:
    """Return seed data dicts for categories and products."""
    now = datetime.now(tz=timezone.utc).isoformat()
    for cat in CATEGORIES:
        cat.setdefault("created_at", now)
        cat.setdefault("updated_at", now)
    for prod in PRODUCTS:
        prod.setdefault("created_at", now)
        prod.setdefault("updated_at", now)
    return {"categories": CATEGORIES, "products": PRODUCTS}


if __name__ == "__main__":
    import json

    data = get_seed_data()
    print(json.dumps(data, indent=2))  # noqa: T201 — seed script, stdout is intentional
