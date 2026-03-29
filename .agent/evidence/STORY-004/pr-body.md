## STORY-004 — Sign in and out

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_valid_credentials_return_tokens`, `test_creates_session_on_success` |
| AC-2 | PASS | `test_generic_error_message_on_bad_credentials` — "Incorrect email or password" |
| AC-3 | PASS | `test_logout_revokes_session` — server-side session invalidation |
| AC-4 | PASS | `test_expired_token_raises_error` — expired JWT returns 401 |
| AC-5 | PASS | `test_ten_failures_lock_account`, `test_locked_account_raises_authentication_error` |

### Test results
Unit: 30/30 passing (24 Python + 6 React)
Integration: 0/0
Regression: 0 newly failing

### Coverage
Overall: 75.95%
New code (services/models): 91.2%

### Security
Snyk: not installed
Semgrep: not installed
- Refresh token stored in httpOnly cookie (not localStorage) — XSS-resistant
- Server-side session revocation on logout — token cannot be reused
- Account lockout after 10 failures for 30 minutes — brute force protection
- Generic "Incorrect email or password" error — no user enumeration

### Deliberate decisions
- JWT access token (24h) + refresh token (30d in httpOnly cookie) — standard pattern
- Session model stores token_hash (SHA-256), not the raw token — defence in depth
- Account lockout is per-user (failed_login_count on User model), not per-IP (that's STORY-010)
- ProtectedRoute redirects to /login?expired=true for session expiry messaging

### Files changed
**Python API (8 files)**
- `src/models/session.py` — Session model (33 lines)
- `src/services/token_service.py` — JWT create/decode (51 lines)
- `src/repositories/session_repository.py` — create/revoke/validate (68 lines)
- `src/middleware/auth.py` — require_auth dependency (62 lines)
- `src/types/login.py` — LoginRequest/Response schemas (20 lines)
- `tests/unit/test_models_session.py` — 15 tests
- `tests/unit/test_login_route.py` — 9 tests
- `tests/unit/test_auth_middleware.py` — 4 tests

**React Frontend (4 files)**
- `src/components/LoginForm.tsx`, `src/components/Header.tsx`
- `src/components/ProtectedRoute.tsx`, `src/pages/LoginPage.tsx`
- `tests/unit/LoginPage.test.tsx` — 6 tests with axe-core
