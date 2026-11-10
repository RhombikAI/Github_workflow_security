# Questions for the repository owner

These answers close the remaining Phase A and Phase B decisions and keep the initial M3 scanner work aligned with the repository's policy.

## M1: requirements, design, and tool selection

1. Can you confirm the project setup recorded in `design.md`: public GitHub repository, free-only tools and CI, owner reviews/merges PRs, and no fork-based contributions or merge queues?
2. Is the Flask health-endpoint demo and Python 3.14 baseline acceptable? If not, which framework or supported Python version should be used?
3. Do you approve the proposed free CLI tools: Gitleaks, `pip-audit`, Bandit, Trivy, zizmor, and actionlint? Are there any license, download-source, or organization policies that disallow one of them?
4. Should dependency auditing cover runtime dependencies only, or also development and build dependencies?
5. Are the documented data flows acceptable: package names/versions sent to public advisory services, Trivy's vulnerability database downloaded by the runner, and no source upload to scanner services?
6. What report/artifact retention period should CI use? The initial workflow proposes seven days pending your decision.
7. What maximum runtime should a normal PR security check target? The first scanner run records elapsed times for the initial tools; full six-category timings will follow as M3 continues.
8. Do you approve the draft severity/confidence thresholds and exception process in `design.md`, or should they change before Phase E implements the merge gate?

## M2: ownership and repository protections

9. Should `.github/CODEOWNERS` assign review to `@RhombikAI`, or is there a specific owner username/team that should own workflows, scanner config, security scripts, exceptions, and CODEOWNERS?
10. Can you review and merge the draft PR for the design, demo app, templates, branch-protection guide, and initial scanner work?
11. Will you configure a classic branch protection rule or a ruleset for `main`?
12. Do you approve requiring PRs, one independent approval, code-owner review, dismissal of stale approvals, and approval of the latest reviewable push?
13. Which status checks should be required now? The existing `basic-checks` is available; the initial M3 checks are `secret-scan` and `python-security`. When the Phase E `security-gate` exists, should it replace or supplement those checks?
14. Should force pushes and branch deletion be blocked for `main`, and which accounts (if any) may bypass the requirements?
15. Who can provide or operate a normal contributor account to verify that a failing PR cannot merge and a direct push to `main` is blocked?

## M3: scanner operation

16. May the initial scanner PR run with the proposed tool versions while the wider tool proposal is under review, or do you want approval before any scanner runs?
17. Are GitHub-hosted Ubuntu runners permitted to download the scanner releases and public vulnerability databases during CI?
18. Should lower-severity findings fail individual scanner checks during this initial phase, or should the jobs report them while the final blocking policy remains undecided? Scanner execution failures will still fail the check.
19. Should generated JSON reports be retained as seven-day GitHub Actions artifacts, or should CI retain only the job summary?

Repository settings and policy approvals remain owner-controlled; this document records questions and does not apply settings or approve exceptions.
