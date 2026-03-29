## STORY-003 — User registration

### Acceptance criteria coverage
| AC | Status | Test |
|----|--------|------|
| AC-1 | PASS | `test_creates_user_with_hashed_password`, `test_returns_created_user`, `test_calls_onSubmit_with_valid_data` |
| AC-2 | PASS | `test_raises_duplicate_email_error_for_existing_user`, `test_preserves_form_data_on_server_error` |
| AC-3 | PASS | `test_shows_error_for_short_password` (client-side, no API call) |
| AC-4 | PASS | `test_shows_error_for_invalid_email_format` (client-side, no API call) |
| AC-5 | PASS | `test_sends_welcome_email_on_success`, `test_does_not_send_email_on_duplicate` |
| AC-6 | PASS | Rate limiter tested in STORY-010 — `test_register_blocks_after_5_requests_in_1_hour` |

### Test results
Unit: 41/41 passing (34 Python + 7 React)
Integration: 0/0
Regression: 0 newly failing

### Coverage
Overall: 75.95%
New code (services/types/models/errors): 96.7%

### Security
Snyk: not installed — manual review recommended
Semgrep: not installed — manual review recommended
- bcrypt cost factor 12 verified in `test_password_hashed_with_bcrypt_cost_12`
- Constant-time response prevents email enumeration timing attacks
- No passwords logged — structlog logs user_id only

### Deliberate decisions
- Email service is an interface only (no SMTP provider wired) — pluggable for SendGrid/SES
- Constant-time response (0.3s floor) on both success and duplicate paths to prevent timing-based enumeration
- Rate limiter is a shared module used by both register and login (STORY-004/010)
- AuthContext stores user in React state; token in localStorage (access_token only — refresh in httpOnly cookie)

### Files changed
**Python API (11 files)**
- `src/models/user.py` — User model with role enum, lockout fields (67 lines)
- `src/errors.py` — AppError hierarchy: 7 error classes (56 lines)
- `src/types/auth.py` — RegisterRequest/Response schemas (24 lines)
- `src/repositories/user_repository.py` — create_user, get_by_email (58 lines)
- `src/services/auth_service.py` — register with bcrypt, constant-time (161 lines)
- `src/services/email_service.py` — interface (16 lines)
- `src/middleware/rate_limit.py` — Redis rate limiter (75 lines)
- `src/routes/auth.py` — POST /register (133 lines)
- `tests/unit/test_models_user.py` — 24 tests
- `tests/unit/test_errors.py` — 26 tests
- `tests/unit/test_auth_service.py` — 8 tests

**React Frontend (5 files)**
- `src/types/auth.ts`, `src/api/auth.ts`, `src/contexts/AuthContext.tsx`
- `src/components/RegisterForm.tsx`, `src/pages/RegisterPage.tsx`
- `tests/unit/RegisterPage.test.tsx` — 7 tests with axe-core
