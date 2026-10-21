---
name: adp-git
description: Commit scoped changes, open or update a pull request, or merge an authorized validated candidate into a named branch using the project Git workflow.
---

# Git delivery

Read the request, project instructions, current status/diff, remotes and branch targets, and [Git policy](../../adp/ci-cd/git-policy.md). Apply shared [authorization](../../adp/rules.md#working-with-the-user), [testing gates](../../adp/testing.md#gates), and [review requirements](../../adp/development.md#ownership-and-review). Implementation-only authorization does not imply commit, push, PR, or merge authorization; an explicit delivery request covers its necessary actions within the named scope.

1. Establish the requested action and source/target. Inspect existing staged changes and unrelated work; resolve ambiguity that would change included content or destination. Use the provider's configured tools and existing branch conventions.
2. For commit, inspect the exact intended diff, run the configured commit gate, stage explicit paths/hunks, verify the index, and commit that content. Preserve unrelated staged changes; never sweep them into the commit. Do not rewrite shared history.
3. For a requested PR, run applicable pre-PR checks, inspect for secrets/unrelated files, push only the intended branch, and create/update the PR with the concrete problem, resulting behavior, scope, evidence, and limits. Opening a PR may precede hosted reviews; report pending gates. Use independent security-first reviews before claiming merge readiness.
4. For an authorized merge, validate the combined candidate and required reviews/checks, recheck target freshness and scope, then merge through the protected workflow. Changed content or target returns through affected gates. Record the actual resulting revision; do not bypass protection or substitute source-only evidence.
5. Report commit identity, branch/PR link or merged revision, checks and pending blockers. Stop after the requested action. Release readiness/publication/deployment use [adp-release](../adp-release/SKILL.md) under their own authorization.
