---
name: adp-completion
description: Verify feature or scoped change completion against acceptance, independent review, evidence, and reconciled documentation.
---

# Feature completion

Read scope, requirements, plan when applicable, acceptance criteria, current docs, candidate revision/diff, target branch, and evidence. Follow the shared [workflow](../../adp/development.md). Release preparation and release-readiness requests use [adp-release](../adp-release/SKILL.md), which owns release qualification.

1. Map acceptance criteria to implemented behavior and meaningful checks. Verify affected design, architecture, and overview describe the implemented portion. List missing work and discrepancies.
2. Verify applicable project testing/security gates and independent reviews on the candidate. Apply the shared review requirements; do not self-certify missing independent review or count failed/unavailable required checks as passes.
3. Verify per-scope documentation reconciliation. Resolve gaps, retain lasting decisions and product constraints, keep reports with the change review, prune completed plan items, and retain unfinished work.
4. Report feature ready or blocked with candidate, acceptance results, commands/results, reviews, failures/retries, unavailable checks, environment limits, and remaining work.

Stop at the authorized step boundary. Readiness does not authorize another roadmap item, commit, PR, merge, publication, or deployment. Git delivery uses [adp-git](../adp-git/SKILL.md); source/local checks do not establish deployed behavior.
