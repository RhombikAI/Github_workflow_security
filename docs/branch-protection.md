# Branch protection setup for `main`

**Owner action required:** Omar does not have repository settings access. The owner must apply these settings and verify them with an ordinary contributor account.

**Owner decisions recorded:** `@RhombikAI` is the confirmed code owner. `basic-checks` is the only check approved as required for now. The answer “no” to blocking direct pushes, force pushes, and branch deletion needs clarification before configuring a rule: requiring PRs prevents direct pushes by design, so the two preferences cannot both be honored.

## Steps for the repository owner

1. Open `RhombikAI/Github_workflow_security` on GitHub and select **Settings**. The owner or an administrator must have permission to edit repository rules.
2. Under **Rules**, choose **Rulesets** and select **New branch ruleset**. A classic alternative is **Branches** → **Add branch protection rule**.
3. Name the rule, target the branch pattern `main`, and leave the ruleset active.
4. Select **Require a pull request before merging**. Set the approval count and review requirements only after confirming them. To require the confirmed `@RhombikAI` owner on owned files, enable code-owner review.
5. Under required status checks, select `basic-checks`. Do not require `secret-scan` or `python-security` yet; those scans have not completed a GitHub PR run. Add the final `security-gate` later if approved and verified.
6. Set bypass access only for the accounts the owner intends to exempt. Save the rule, then verify it as a normal contributor.

GitHub documents the detailed screens for [creating a branch ruleset](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) and [managing a branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

## Configure a rule for `main`

In the repository settings, create either a classic branch protection rule or a branch ruleset targeting only `main`. Keep the rule active and limit bypass access to the minimum necessary.

Set these requirements:

1. Require a pull request before merging; this blocks direct pushes to `main` for contributors who cannot bypass the rule. Confirm this because the owner's latest answer about blocking direct pushes was “no.”
2. Require at least one approval from someone other than the author.
3. Require code-owner review. Confirm the intended owner/team in `.github/CODEOWNERS` before enabling this.
4. Dismiss stale approvals and require approval of the latest reviewable push, so relevant new commits receive review.
5. Require the `basic-checks` status check. The owner has selected this as the only required check for now. Add `secret-scan` and `python-security` only after their GitHub PR runs are reviewed; add `security-gate` later if approved and verified.
6. Block force pushes and branch deletion only if the owner confirms that preference; the answer received so far was “no.”
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
