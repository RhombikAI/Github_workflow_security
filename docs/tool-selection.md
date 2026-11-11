# Security scanner evaluation

**Status:** Scanner set approved by project owner; thresholds and remaining policy decisions pending
**Reviewed:** 2026-11-10
**Constraints:** Public GitHub repository, free tools only, Python managed with `uv`, no fork-based contributions or merge queues.

## Recommendation at a glance

Use a small set of command-line scanners on disposable GitHub-hosted runners. The proposed set is Gitleaks CLI for secrets, `pip-audit` for Python dependency advisories, Bandit for Python static analysis, Trivy for container and Dockerfile/configuration checks, and `zizmor` plus `actionlint` for workflow security and syntax.

The owner approved this free CLI tool set. Initial M3 implementation starts with Gitleaks CLI, `pip-audit`, and Bandit. Current pinned candidates are Gitleaks 8.30.1 (Linux x64 release SHA-256 verified against upstream metadata), `pip-audit` 2.10.1, and Bandit 1.9.4. Pin every third-party GitHub Action to a reviewed full commit SHA. Do not rely on floating tags such as `latest` in the required workflow.

## Candidate evaluation

| Category | Recommended candidate | Inputs and coverage | Licensing/cost | Data, permissions, output, and failure behavior | Limitations and version plan |
|---|---|---|---|---|---|
| Secrets | [Gitleaks CLI](https://github.com/gitleaks/gitleaks) | Scans Git commit patches in the PR base-to-head range, including secrets added then removed in a later PR commit. | CLI repository is MIT licensed; no paid service is required. The Gitleaks Action wrapper is excluded because its v2 license changed. | Runs locally in the job with read-only checkout. JSON reporting and `--redact` are used. A finding or scanner error fails the job. | Pin Gitleaks 8.30.1 and verify the upstream Linux x64 release SHA-256. Fetch full Git history. Record runtime from the initial CI run. |
| Dependencies | [pip-audit](https://github.com/pypa/pip-audit) with `uv export` | Exports the committed lock to a fully pinned requirements file, then audits direct and transitive runtime, development, and explicitly locked build-group packages. | Apache-2.0; free CLI. | Owner approved public advisory lookup using package/version data; application source is not uploaded. JSON output is saved. A finding or service/scanner error fails the job. | Pin `pip-audit` 2.10.1 and the build tool group in `uv.lock`. Record service/database availability and runtime. |
| Static analysis | [Bandit](https://github.com/PyCQA/bandit) | Scans Python source under `src/` for common security issues. Produces rule IDs, severity/confidence, locations, and context. | Apache-2.0; free software. | Runs locally without credentials or source upload. JSON output is saved after code snippets are removed. A finding or scanner error fails the job. | Pin Bandit 1.9.4 in `uv.lock`. Initial scope is `src/`; severity/confidence thresholds need owner approval. Record runtime from the initial CI run. |
| Container image | [Trivy](https://github.com/aquasecurity/trivy) image scan | Scan the exact image built by the PR job for supported operating-system and application packages. Record the image reference and immutable image ID/digest. | Apache-2.0; free CLI. | Scans a local image and downloads its vulnerability database; do not push the image to a registry. JSON reports are supported. Configure explicit exit behavior so blocking findings or scanner/database failures fail the job. | Detection depends on package metadata and database freshness. Keep the image local; no registry credentials. Pin the binary and database behavior, and report the database timestamp/version when available. |
| Configuration | [Trivy](https://github.com/aquasecurity/trivy) config scan | Scan the Dockerfile and supported infrastructure files for known misconfiguration rules. | Same scanner and license as image scanning; no extra paid service. | Local CLI scan; JSON report and nonzero threshold configuration are available. Findings are reported separately from image package vulnerabilities. | Rule coverage varies by format. Verify at least two unsafe fixtures and corrected versions. Document unsupported files and any intentional exclusions. |
| Workflow security | [zizmor](https://github.com/zizmorcore/zizmor) | Static analysis for GitHub Actions workflows, including risky permissions, untrusted input use, and unsafe workflow patterns. | MIT; free CLI. | Runs locally against workflow files; does not require repository write permissions. JSON/SARIF reporting is available. Configure blocking rules explicitly; failures to run or produce a valid report fail the gate. | Cannot prove that workflow code is unchanged or replace independent review. Pin the release/action by reviewed SHA and document the rule configuration. |
| Workflow syntax | [actionlint](https://github.com/rhysd/actionlint) | Validates GitHub Actions workflow syntax and expression/context usage; complements the security rules from zizmor. | MIT; free CLI. | Runs locally; emits actionable diagnostics and a failing exit code for validation errors. No credentials or source upload required. | Syntax validation is not a security proof. Pin the binary version and run on every PR that can affect workflows or called scripts. |

## Alternatives and selection notes

- **TruffleHog** can scan Git history, but its current upstream project is AGPL-3.0. Keep it as an alternative only if the owner approves that license for this assignment.
- **GitHub's built-in security products** are not the baseline choice: the assignment must be adaptable and compare tools directly, and repository/plan feature availability has not been confirmed.
- **Semgrep** is not selected for this small Python demo; Bandit provides a simpler, Python-focused starting point. Revisit if the real target language or rule needs exceed Bandit's coverage.
- Avoid duplicate dependency scanners until the owner asks for additional coverage. Trivy's image scan complements `pip-audit` by scanning the built image and OS packages.

## Data and permission summary

| Tool | Source code leaves CI? | Required credential/permission | External data/network |
|---|---|---|---|
| Gitleaks CLI | No upload required by the CLI scan. | Read checkout only. | Tool binary download at setup; verify checksum. |
| `uv export` + `pip-audit` | No source upload required. | Read checkout only. | PyPI vulnerability data lookup; package/version metadata is queried. |
| Bandit | No. | Read checkout only. | None during scan after pinned tool installation. |
| Trivy | No image upload; image stays local to runner. | Read checkout and local container engine access within the disposable runner. No Docker socket mount into untrusted privileged containers. | Vulnerability database download. |
| zizmor | No. | Read checkout only. | None during analysis after pinned installation. |
| actionlint | No. | Read checkout only. | None during analysis after pinned installation. |

All PR jobs should declare `permissions: contents: read` unless a documented job-specific need is approved. Keep report artifacts redacted and use an owner-approved retention period. Do not add write permissions for PR comments; a CI summary and artifacts are sufficient.

## Version, output, and runtime controls

- Pin exact scanner versions. For third-party Actions, pin a reviewed full commit SHA and record the corresponding release tag in a comment or tool inventory.
- Verify downloaded tool checksums/signatures where the publisher provides them. Keep an update process that reviews releases and changes in rules.
- Produce machine-readable output where supported: JSON for Gitleaks, `pip-audit`, Bandit, and Trivy; SARIF/JSON for zizmor. Keep actionlint diagnostics in the job log/summary unless a stable parser is added.
- Record tool version, checked commit SHA, completion state, report path, and database freshness where applicable.
- Owner target: complete PR security scans within five minutes. The workflow jobs have five-minute timeouts; record observed durations and optimize if they exceed the target. The initial M3 CI run measures Gitleaks, `pip-audit`, and Bandit. Trivy, zizmor, and actionlint are not implemented yet, so their runtimes remain TBD.
- Owner approved report retention of 10–15 days; the workflow uses 14 days.
- Treat a missing lockfile, unsupported manifest, unavailable vulnerability service/database, malformed report, timeout, or unexpectedly skipped scan as a failure or explicitly justified not-applicable result.

## Owner approval required

1. Confirm severity/confidence thresholds and severity mappings across tools.
2. Confirm that public GitHub-hosted runners and their current free usage fit the project. GitHub's current billing docs say standard hosted runners are free for public repositories; recheck before rollout.

## Primary references

- [GitHub Actions runner billing](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [Gitleaks README and CLI](https://github.com/gitleaks/gitleaks)
- [Gitleaks CLI license](https://github.com/gitleaks/gitleaks/blob/master/LICENSE)
- [Gitleaks Action README](https://github.com/gitleaks/gitleaks-action)
- [pip-audit README and supported project inputs](https://github.com/pypa/pip-audit), including [fully pinned requirements mode](https://github.com/pypa/pip-audit#pip-audit-cant-authenticate-to-my-third-party-index)
- [uv export documentation](https://docs.astral.sh/uv/concepts/projects/export/)
- [Bandit](https://github.com/PyCQA/bandit)
- [Trivy license](https://github.com/aquasecurity/trivy/blob/main/LICENSE), [image scanning](https://github.com/aquasecurity/trivy/blob/main/docs/guide/target/container_image.md), and [misconfiguration scanning](https://github.com/aquasecurity/trivy/blob/main/docs/guide/scanner/misconfiguration/index.md)
- [zizmor](https://github.com/zizmorcore/zizmor)
- [zizmor output formats and exit codes](https://docs.zizmor.sh/usage/)
- [actionlint](https://github.com/rhysd/actionlint)
