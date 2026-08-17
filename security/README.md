Security Program Overview

Teams:
- Encryption Engineering: key management, libs, algorithm selection, side-channel awareness.
- Cybersecurity Operations: IDS/IPS, logging, incident response, blue team playbooks.
- Red Team: adversarial testing, threat emulation, attack-surface exercises.
- Secure Development: SAST, dependency scanning, threat modeling during design.

Requirements & Automation:
- Automated dependency scanning (Snyk/OSS Index/Dependabot)
- CI SAST steps and secret scanning
- Regular red-team engagements and postmortem-runbooks
- Hardware-aware tests for memory-safety and compiler optimization side effects

Notes:
- Security is the largest team and owns threat model and incident response; cross-team manifests must include security sign-off gates.