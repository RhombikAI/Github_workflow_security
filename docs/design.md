# Pull request security workflow design

**Status:** Draft for project-owner review  
**Prepared:** 2026-11-10
**Repository:** `RhombikAI/Github_workflow_security`

## 1. Goal

Build a reusable GitHub Actions workflow that checks pull requests for security issues before the owner merges them. A passing gate means the configured checks completed and passed; it does not prove that the application is vulnerability-free.

The repository is public on GitHub, with `main` as its default branch. The tool budget is free-only. The project owner reviews and merges pull requests. Fork-based contributions and merge queues are out of scope. The owner confirmed the Flask demo, Python 3.14 baseline, free scanners, and public advisory lookup using package/version data without source upload. Dependency auditing should cover runtime, development, and build dependencies where locked; the build tool is explicitly included in a `uv` dependency group. Artifact retention is 14 days, within the owner's 10–15 day range, and the PR security scan target is five minutes. `uv` manages the project environment, dependencies, and lockfile. Omar can push the implementation branch and a basic CI run has passed, but no PR has been opened yet. Omar does not have repository settings access. The connected GitHub integration listed no rulesets but could not read classic branch protection, so protection status remains unverified.

## 2. Proposed demo application

Use a small Flask application with one health endpoint, one automated test, a `pyproject.toml` and committed `uv.lock`, a Dockerfile, and a fictional `.env.example`. Use `uv` for project operations; do not commit `.venv/`. Keep the sample free of external services and credentials.

The application is a fixture for exercising scanners, not a production service. Keep vulnerable test cases isolated to dedicated branches or inert fixture files. Do not publish a vulnerable image or merge a deliberately vulnerable test change.

## 3. Scope and boundaries

The PR workflow will cover:

- Secret exposure in the PR commit history.
- Vulnerabilities in direct and transitive Python dependencies.
- Python static security findings.
- Operating-system and application packages in the exact container image built for the PR.
- Dockerfile and any later-supported infrastructure configuration.
- GitHub Actions syntax and workflow security.

The work excludes deployments, Hetzner administration, live penetration testing, production data, production credentials, and changes to RuleCast or Hetzner.

Treat PR code, commit contents, titles, branch names, descriptions, and other event metadata as untrusted. Never interpolate PR metadata directly into shell source. Do not expose secrets or grant PR jobs write, merge, deployment, server, or repository-administration access. Do not run untrusted code with `pull_request_target`, mount the host Docker socket, or use privileged test containers.

Run PR checks on disposable GitHub-hosted runners. Start with read-only token permissions; add any permission only to the job that needs it and document why. Do not persist checkout credentials when later steps do not need them. Keep PR caches and artifacts separate from any future privileged release or deployment workflow. Pin third-party actions to reviewed full commit SHAs and scanner binaries to reviewed versions; verify checksums where upstream publishes them.

The repository is public, so standard GitHub-hosted runners are currently documented as free for public repositories. This does not make paid scanner services or premium add-ons acceptable; the proposal uses local command-line tools and public data sources only. Recheck billing and platform settings with the owner before implementation.

## 4. Proposed PR flow

1. A contributor pushes a branch and opens or updates a PR against `main`.
2. GitHub Actions runs the applicable scanners and records the commit SHA and scanner versions.
3. Each scanner reports a status and a useful, redacted finding report.
4. A stable `security-gate` evaluates every required result. It fails on a blocking finding, scanner error, timeout, invalid or missing report, or unexpected skip.
5. The contributor fixes findings on the branch; checks rerun for the new commit.
6. The project owner reviews the change and merges only after the required checks and review are satisfied.

Workflow and security-policy changes receive the same checks and an independent owner review. A PR cannot lower the effective policy by editing its own exception or scanner configuration.

No fork workflow or merge-queue event is planned. If that scope changes, the workflow design must be reviewed before adding the trigger.

## 5. Initial policy proposal

This is a proposal for owner approval, not an adopted repository policy:

| Result | Proposed behavior |
|---|---|
| Detected secret | Block; redact the value in logs and reports. A real exposed credential must be revoked or rotated; deleting the file alone is insufficient. |
| High or critical dependency/container vulnerability | Block unless a valid owner-approved exception applies. A missing fix still requires an explicit decision. |
| Serious, high-confidence Python finding | Block. |
| Serious workflow or configuration finding | Block. |
| Lower-severity finding | Report for owner review. |
| Scanner crash, timeout, missing/invalid output, or unexpected skip | Block. |
| Expired, malformed, or PR-added unapproved exception | Block. |

Map each tool's severity and confidence fields to this policy explicitly. Do not treat scanner severity labels as equivalent. The owner approves thresholds and exceptions; Omar must not approve his own exception.

## 6. Reports and data handling

Every result should say what was scanned, the tool/version, checked commit, completion status, findings and locations, remediation, and whether the result blocks merging. Save machine-readable reports where supported and a short job summary. Redact secret-looking values. The owner approved 14-day artifact retention and a five-minute PR scan target.

Scanners run in the CI environment. The planned dependency audit queries public vulnerability data using package/version information; it does not need application source upload. Container scanning uses the locally built image and a downloaded vulnerability database; do not publish the image. Confirm network endpoints and report retention during implementation.

## 7. Owner decisions and verification still needed

- Confirm proposed severity thresholds and exception process.
- Confirm who applies and verifies required PR, review, code-owner, check, force-push, deletion, and bypass settings. Omar does not have repository-options access, so these settings cannot be verified by him.
- Confirm the CODEOWNERS reviewer account or team. The current repository owner account is `@RhombikAI`; confirm it is the intended code owner.
- Confirm the CODEOWNERS reviewer account or team and any runner restrictions.
- Apply the settings in [branch-protection.md](branch-protection.md). Omar cannot change repository settings.
- Verify branch creation, PR opening, CI on a PR, and the block on merging a deliberately failing PR. The basic CI push run passed, but branch-protection enforcement has not been exercised.

See [owner-questions.md](owner-questions.md) for questions that need answers before the proposed policy and protection settings are finalized.

## 8. Limitations

These checks reduce common risks but do not prove the application is secure. Static rules can miss issues or raise false positives; vulnerability data can be stale or unavailable; image scanning only covers detected packages; and a required check name alone does not prove its implementation was not changed. Independent review and protected ownership of workflow/policy files remain necessary.
