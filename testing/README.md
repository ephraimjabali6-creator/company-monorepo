Testing Strategy

Principles:
- Red-green regression testing: keep tests small and deterministic; require green before merge.
- Regression suites are split: unit, integration, e2e, fuzzing, chaos.
- Automated nightly full-regression runs with alerts for semantic drift.
- Test manifests published to teams/manifests so other teams can run the tests locally.

Plans:
- Maintain a CI test matrix (language-based jobs included in .github/workflows).
- Add fuzzing harnesses for critical APIs.
- Run blue/red team exercises and automate common attack vectors into regression checks.