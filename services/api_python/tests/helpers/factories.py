"""
Test data factories for yooti-ri API tests.
Add a factory for every domain model as stories are completed.
"""

import uuid
from datetime import datetime


def create_user(**overrides: object) -> dict:
    """Create a test user dict with sensible defaults."""
    return {
        "id": str(uuid.uuid4()),
        "email": "test@example.com",
        "name": "Test User",
        "created_at": datetime.now().isoformat(),
        **overrides,
    }


def create_category(**overrides: object) -> dict:
    """Create a test category dict with sensible defaults."""
    return {
        "id": str(uuid.uuid4()),
        "name": "Electronics",
        "slug": "electronics",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        **overrides,
    }


def create_product(**overrides: object) -> dict:
    """Create a test product dict with sensible defaults."""
    return {
        "id": str(uuid.uuid4()),
        "name": "Test Product",
        "description": "A test product",
        "price": "29.99",
        "stock_quantity": 10,
        "category_id": str(uuid.uuid4()),
        "thumbnail_url": "https://example.com/img.jpg",
        "images": [],
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        **overrides,
    }
