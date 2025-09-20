# Security Policy

Why:
  Maintain a clear, versioned reference for how security issues (including dependency vulnerabilities) are identified, triaged, and remediated while honoring the project's strict offline and single-database constraints.
Where:
  Lives at repository root so GitHub can surface it automatically in the Security tab; referenced by CI security audit step and future contributor guidelines.
How:
  Defines supported versions, reporting channels, triage SLAs, dependency management approach (pinning + periodic audit), and remediation workflow integrated with the docstring and performance quality gates.

## Supported Versions

| Version | Status        |
|---------|---------------|
| main    | Actively maintained (security + bug fixes) |
| legacy/* branches | No guarantees; upgrade recommended |

## Reporting a Vulnerability

1. Open a private advisory (preferred) or create an issue with minimal reproduction details (avoid sensitive info).
2. Provide: Affected package/version, CVE (if known), impact summary, and suggested fix version.
3. Expect initial triage response within 72 hours.

## Dependency Management Strategy

- All runtime dependencies are pinned in `requirements.txt` (and derivative minimal/base lists) to ensure deterministic offline installs.
- Weekly (or pre-release) security audit via CI (pip-audit or equivalent) validates current pins.
- Moderate findings: addressed in the next minor patch unless active exploit context exists.
- High/Critical findings: patched immediately with a hotfix branch and rapid release tag.

## Remediation Workflow

1. Identify vulnerable package and fixed version range.
2. Create a branch `security/<package>-<version-bump>`.
3. Update pin(s) across `requirements*.txt` consistently.
4. Run: tests, docstring enforcement, performance benchmarks.
5. Update `CHANGELOG.md` under Unreleased -> Security.
6. Tag release (e.g., vX.Y.Z+security.1) after merge to `main`.

## Current Open Items

- Moderate advisory (Dependabot alert #2) under investigation. Pending confirmation of affected package & fixed version; scheduled for next maintenance cycle.

## Verification & Audit Trails

- CI pipeline enforces: tests (functional reliability), performance guard (latency regression detection), doc coverage (architectural clarity), security audit (dependency health).
- Changes to security-sensitive code or dependency versions must reference this policy in commit messages for traceability.

## Offline Constraint Considerations

- All updates must remain installable without external network calls at runtime (only during setup). No on-demand remote fetching allowed.
- If a vulnerability fix introduces a transitive dependency that violates offline constraints, evaluate vendoring or alternate patch strategy.

## Contact

For questions or clarifications, open a discussion thread referencing this SECURITY.md.
