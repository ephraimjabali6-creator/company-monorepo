Environment & Deployment Guidelines

- Use environment-specific configuration files and a secrets manager (Vault, GitHub Secrets) — never commit secrets.
- Validate config at startup: fail-fast with clear diagnostics.
- Provide a "configuration manifest" per service in teams/manifests so devs and ops share expectations.
- Use containerization and pin runtime versions in CI to reduce drift.
- Provide wrapper scripts (scripts/run_tests.ps1) to run cross-language validations locally.
- For cloud-free options, services can be run locally or deployed to free tiers (Railway/free-tier, Fly, Heroku free alternatives where available) — adapt deploy scripts per target.
