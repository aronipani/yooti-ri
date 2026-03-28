# Human Decision Gates — yooti-ri

## G1 PM Sign-Off (before sprint)
- [ ] All stories have Given/When/Then ACs
- [ ] Definition of Done per story
- [ ] Ambiguity blockers resolved
FAIL: sprint does not start

## G2 Architecture Review (Days 1-2)
- [ ] ADRs approved
- [ ] .plan files reviewed for M/L stories
- [ ] No breaking cross-system changes without approval
FAIL: code generation does not begin

## G3 Developer PR Review (Days 6-8)
- [ ] Code matches intent
- [ ] No out-of-scope file changes
- [ ] Patterns consistent
- [ ] No hardcoded secrets
APPROVE: continue | REQUEST CHANGES: agent corrects | REJECT: replan

## G4 QA Sign-Off (Day 9)

Run: yooti qa:review STORY-NNN

### Hard gates (any failure = automatic reject)
| Gate | Threshold | Evidence file |
|------|-----------|---------------|
| Unit tests | 100% pass | test-results.json |
| Integration tests | 100% pass | test-results.json |
| Zero regressions | 0 newly failing | regression-diff.json |
| Overall coverage | >= 80% | coverage-summary.json |
| New code coverage | >= 90% | coverage-summary.json |
| CRITICAL security | 0 findings | security-scan.json (Snyk) |
| HIGH security | 0 findings | security-scan.json (Snyk) |
| Semgrep | 0 findings | security-scan.json |
| Accessibility | 0 violations | accessibility.json (if frontend) |

### Soft gates (QA judgement — review required)
| Gate | Target | Evidence file |
|------|--------|---------------|
| Mutation score | >= 85% | mutation-score.json |

FAIL (hard gate): agent generates more tests, reruns Phase 5
FAIL (soft gate): QA reviews and decides — approve or reject with notes

## G5 Deployment Approval (Day 10)
- [ ] Staging stable > 30 min
- [ ] Smoke tests passing
- [ ] p99 latency within 20% of prod baseline
- [ ] Rollback plan confirmed
GO: deploy | NO-GO: hold
