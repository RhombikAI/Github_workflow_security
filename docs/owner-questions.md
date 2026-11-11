# Questions for the repository owner

These answers close the remaining Phase A and Phase B decisions and keep the initial M3 scanner work aligned with the repository's policy.

## M1: requirements, design, and tool selection

1. What severity/confidence thresholds and exception process do you approve before Phase E implements the merge gate?
2. The scanner jobs have five-minute timeouts to meet your PR scan target. If actual runs exceed the target, should I optimize the workflow or request a longer limit?

## M2: ownership and repository protections

`@RhombikAI` was confirmed as code owner, and `basic-checks` is the only required check for now. The owner asked how to configure protections; steps are in `branch-protection.md`.

1. Should the rule for `main` require PRs, one independent approval, code-owner review, dismissal of stale approvals, and approval of the latest reviewable push?
2. You answered “no” to blocking direct pushes, force pushes, and branch deletion. Do you want all three actions to remain allowed, or did “no” refer only to force pushes and deletion? Requiring PRs blocks direct pushes unless bypass is granted.
3. Will you configure a classic branch protection rule or a ruleset for `main`?
4. Can you review and merge the draft PR for the design, demo app, templates, branch-protection guide, and initial scanner work?
5. When `security-gate` exists, should it replace or supplement the current required `basic-checks` check?
6. Who can provide or operate a normal contributor account to verify the merge and push restrictions?

## M3: scanner operation

1. Should lower-severity findings fail individual scanner checks during this initial phase, or should jobs report them while the final blocking policy remains undecided? Scanner execution failures will still fail the check.

Repository settings and policy approvals remain owner-controlled; this document records questions and does not apply settings or approve exceptions.
