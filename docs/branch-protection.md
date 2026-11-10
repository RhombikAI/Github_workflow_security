# Branch protection setup for `main`

**Owner action required:** Omar does not have repository settings access. The owner must apply these settings and verify them with an ordinary contributor account.

## Configure a rule for `main`

In the repository settings, create either a classic branch protection rule or a branch ruleset targeting only `main`. Keep the rule active and limit bypass access to the minimum necessary.

Set these requirements:

1. Require a pull request before merging; block direct pushes to `main`.
2. Require at least one approval from someone other than the author.
3. Require code-owner review. Confirm the intended owner/team in `.github/CODEOWNERS` before enabling this.
4. Dismiss stale approvals and require approval of the latest reviewable push, so relevant new commits receive review.
5. Require status checks after their exact names appear on a PR. The current baseline check is `basic-checks`. The initial security jobs are `secret-scan` and `python-security`; require them after the owner accepts the scanner proposal and confirms their behavior. When the final `security-gate` is implemented in Phase E, require that stable check as well.
6. Block force pushes and branch deletion.
7. Restrict bypass privileges. Do not allow ordinary contributors to bypass the checks or review requirements.

If the owner chooses to require the branch to be up to date before merging, enable that setting only after confirming its effects on the team's workflow.

## Verify the settings

Use a normal contributor account, not an administrator:

1. Confirm that a direct push to `main` is rejected.
2. Open a test PR with a deliberately failing check and confirm that merging is blocked.
3. Push a new commit after approval and confirm that stale approval/review requirements are enforced.
4. Confirm the code-owner review is requested for a workflow or security-policy change.
5. Record the rule or ruleset, required check names, test PR/run links, and any bypass exceptions in the project handover notes.

Do not merge the intentionally failing test PR. Keep the test isolated and close it after verification.

GitHub references: [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches) and [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets).
