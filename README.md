Polyglot Company Monorepo

This repository is a scaffold for a resilient, security-first, polyglot engineering organization. It includes:
- services/api: FastAPI (Python) service with tests
- services/go: Minimal Go microservice
- apps/web: simple web UI placeholder
- apps/native: Electron native UI placeholder
- infra: Docker Compose for local orchestration
- .github/workflows: CI to run tests across languages
- teams/: documentation for managers and teams (CEO, CTO, CISO, etc.)
- security/: blue/red team guidance and automation pointers
- testing/: testing strategy including red-green regression testing
- deploy/: environment and deployment best-practices

Next steps:
1. Install required runtimes (Python 3.10+, Go, Node.js, and optionally Electron tooling).
2. From repo root, run scripts\run_tests.ps1 to validate the basic services.
3. Tailor each service to project needs; CI is preconfigured for basic validation.

This scaffold is intentionally minimal but complete enough to run local validations and be extended into a production-grade multi-team system.