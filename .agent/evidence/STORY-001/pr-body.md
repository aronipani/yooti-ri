## STORY-001 — Browse product catalogue

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_renders_product_name`, `test_renders_formatted_price`, `test_maps_product_fields` |
| AC-2 | PASS | `test_passes_category_filter_to_repo`, CataloguePage URL search params |
| AC-3 | PASS | `test_passes_sort_to_repo` (price_asc sort) |
| AC-4 | PASS | `test_shows_out_of_stock_badge`, `test_disables_add_to_cart` |
| AC-5 | PASS | `test_has_next_true_when_more_pages`, IntersectionObserver in CataloguePage |

### Test results
Unit: 46/46 passing (33 Python + 13 React)
Integration: 0/0 (deferred to integration test sprint)
Regression: 0 newly failing

### Coverage
Overall: 75.95% (below 80% — repository/route layers need integration tests)
New code (services/types/models): 92.3%

### Security
Snyk: not installed — manual review recommended
Semgrep: not installed — manual review recommended
No user input flows to SQL — parameterised queries via SQLAlchemy ORM

### Deliberate decisions
- Used offset pagination (not cursor) for simplicity in sprint 1; can migrate to cursor pagination later
- IntersectionObserver with 200px rootMargin for pre-fetching before user reaches bottom
- Product images stored as JSON array column — avoids a separate images table for MVP
- Shared infrastructure fixes (mypy, ruff format, type annotations) included in this PR as the base

### Files changed
**Python API (14 files)**
- `src/models/category.py` — Category model (28 lines)
- `src/models/product.py` — Product model (42 lines)
- `src/types/product.py` — Pydantic schemas (44 lines)
- `src/repositories/product_repository.py` — list, filter, sort, paginate queries (91 lines)
- `src/services/product_service.py` — business logic (100 lines)
- `src/routes/products.py` — GET /products, GET /categories (67 lines)
- `scripts/seed_products.py` — 26 products, 5 categories (210 lines)
- `tests/unit/test_models_product.py` — 21 tests
- `tests/unit/test_product_service.py` — 12 tests

**React Frontend (10 files)**
- `src/types/product.ts` — TypeScript interfaces
- `src/api/products.ts` — API client
- `src/hooks/useProducts.ts` — data fetching + infinite scroll
- `src/components/ProductCard.tsx` — card with stock badge
- `src/components/ProductGrid.tsx` — responsive grid
- `src/pages/CataloguePage.tsx` — page with filter/sort/scroll
- `tests/unit/CataloguePage.test.tsx` — 13 tests with axe-core
