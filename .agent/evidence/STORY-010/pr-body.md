## STORY-010 — Rate limiting on authentication endpoints

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_login_blocks_after_10_requests_in_15_minutes` — 429 + Retry-After header |
| AC-2 | PASS | `test_graceful_degradation_on_redis_failure` — requests allowed through |
| AC-3 | PASS | `test_register_blocks_after_5_requests_in_1_hour` — 429 + Retry-After header |

### Test results
Unit: 13/13 passing
Integration: 0/0
Regression: 0 newly failing

### Coverage
Overall: 75.95%
New code: 100% (rate_limit.py already at 100% from STORY-003; tests added here exercise all paths)

### Security
Snyk: not installed
Semgrep: not installed
- Rate limiting is itself a security hardening measure against brute force
- Retry-After header informs clients when to retry — prevents unnecessary load
- Graceful degradation ensures availability over security (logged warning when Redis is down)

### Deliberate decisions
- Per-IP rate limiting (not per-user) — IP extracted from request.client.host
- Redis INCR/EXPIRE pattern for sliding window — simple and well-understood
- Graceful degradation: when Redis is unavailable, requests are allowed through with a warning log — availability > strict enforcement
- Per-route configuration allows different limits on login (10/15min), register (5/1hr), refresh (20/15min)

### Files changed
**Python API (1 file)**
- `tests/unit/test_auth_rate_limiting.py` — 13 tests covering allow/block/degrade/config

Note: The rate_limit.py middleware was created in STORY-003. This story adds comprehensive test coverage and verifies the per-endpoint configuration applied in auth routes.
