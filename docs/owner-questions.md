# Questions for the repository owner

These answers close the remaining Phase A and Phase B decisions and keep the initial M3 scanner work aligned with the repository's policy.

## M1: requirements, design, and tool selection

1. What severity/confidence thresholds and exception process do you approve before Phase E implements the merge gate?
2. The scanner jobs have five-minute timeouts to meet your PR scan target. If actual runs exceed the target, should I optimize the workflow or request a longer limit?

## M2: ownership and repository protections

9. Should `.github/CODEOWNERS` assign review to `@RhombikAI`, or is there a specific owner username/team that should own workflows, scanner config, security scripts, exceptions, and CODEOWNERS?
10. Can you review and merge the draft PR for the design, demo app, templates, branch-protection guide, and initial scanner work?
11. Will you configure a classic branch protection rule or a ruleset for `main`?
12. Do you approve requiring PRs, one independent approval, code-owner review, dismissal of stale approvals, and approval of the latest reviewable push?
13. Which status checks should be required now? The existing `basic-checks` is available; the initial M3 checks are `secret-scan` and `python-security`. When the Phase E `security-gate` exists, should it replace or supplement those checks?
14. Should force pushes and branch deletion be blocked for `main`, and which accounts (if any) may bypass the requirements?
15. Who can provide or operate a normal contributor account to verify that a failing PR cannot merge and a direct push to `main` is blocked?

## M3: scanner operation

16. Should lower-severity findings fail individual scanner checks during this initial phase, or should jobs report them while the final blocking policy remains undecided? Scanner execution failures will still fail the check.

Repository settings and policy approvals remain owner-controlled; this document records questions and does not apply settings or approve exceptions.
