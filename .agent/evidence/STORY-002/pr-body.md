## STORY-002 — Product detail page

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_returns_product_detail_for_valid_uuid`, `test_returns_category_info`, `test_returns_all_images` |
| AC-2 | PASS | `test_updates_main_image_when_thumbnail_clicked` |
| AC-3 | PASS | `test_caps_value_at_max`, `test_shows_warning_when_value_exceeds_stock` |
| AC-4 | PASS | `test_raises_not_found_for_missing_product`, `test_shows_404_text`, `test_has_a_link_back_to_catalogue` |
| AC-5 | PARTIAL | Add to Cart button present in UI; cart wiring deferred to STORY-005 |

### Test results
Unit: 19/19 passing (6 Python + 13 React)
Integration: 0/0
Regression: 0 newly failing

### Coverage
Overall: 75.95%
New code: 100%

### Security
Snyk: not installed
Semgrep: not installed
- Product ID validated as UUID via FastAPI Path param — prevents injection
- 422 returned for malformed UUIDs, 404 for valid but non-existent

### Deliberate decisions
- ImageGallery uses simple useState for selected index — no need for a reducer
- QuantitySelector caps at stock on input change, not on blur, for immediate feedback
- NotFoundPage is a shared component reused by the catch-all route

### Files changed
**Python API (2 files)**
- `src/types/product_detail.py` — ProductDetailResponse schema (25 lines)
- `tests/unit/test_product_detail_route.py` — 6 tests

**React Frontend (6 files)**
- `src/hooks/useProduct.ts` — single product fetcher
- `src/components/ImageGallery.tsx` — main image + thumbnails
- `src/components/QuantitySelector.tsx` — capped input with warning
- `src/components/NotFoundPage.tsx` — 404 with catalogue link
- `src/pages/ProductDetailPage.tsx` — detail page composition
- `tests/unit/ProductDetailPage.test.tsx` — 13 tests with axe-core
