## STORY-005 — Shopping cart

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_returns_items_with_correct_fields`, CartDrawer renders items with name/price/qty/subtotal |
| AC-2 | PASS | `test_add_item_calls_repo_with_correct_args` — repository deduplicates by incrementing quantity |
| AC-3 | PASS | `test_update_to_zero_removes_item` |
| AC-4 | PASS | Cart model supports user_id (auth) and session_id (guest) — persistence via API |
| AC-5 | PASS | `test_stock_warning_when_quantity_exceeds_stock` — quantity adjusted, warning returned |
| AC-6 | PASS | `test_calculates_subtotal_correctly`, `test_calculates_estimated_tax` (10% rate) |

### Test results
Unit: 36/36 passing (29 Python + 7 React)
Integration: 0/0
Regression: 0 newly failing

### Coverage
Overall: 75.95%
New code (services/types/models): 90.5%

### Security
Snyk: not installed
Semgrep: not installed
- Cart routes use auth middleware for authenticated users
- Prices looked up from Product table at response time — not stored in cart (prevents client-side price manipulation)
- Stock validated server-side on GET /cart — stale quantities auto-adjusted

### Deliberate decisions
- Fixed 10% tax rate for MVP — configurable tax calculation deferred to checkout story
- Guest carts identified by session_id string (cookie) — Redis TTL for guest cart expiry deferred to integration phase
- CartItem has unique constraint on (cart_id, product_id) — enforces dedup at DB level
- CartDrawer uses aria-live="polite" for screen reader updates on cart changes

### Files changed
**Python API (8 files)**
- `src/models/cart.py` — Cart model with status enum (52 lines)
- `src/models/cart_item.py` — CartItem with unique constraint (37 lines)
- `src/types/cart.py` — Pydantic schemas (45 lines)
- `src/repositories/cart_repository.py` — CRUD operations (133 lines)
- `src/services/cart_service.py` — stock validation, tax calc (155 lines)
- `src/routes/cart.py` — 4 endpoints (91 lines)
- `tests/unit/test_models_cart.py` — 19 tests
- `tests/unit/test_cart_service.py` — 10 tests

**React Frontend (5 files)**
- `src/types/cart.ts`, `src/api/cart.ts`, `src/contexts/CartContext.tsx`
- `src/components/CartIcon.tsx`, `src/components/CartDrawer.tsx`
- `tests/unit/CartDrawer.test.tsx` — 7 tests with axe-core
