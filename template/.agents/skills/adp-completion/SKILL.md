---
name: adp-completion
description: Verify feature or requested release readiness against acceptance, independent review, evidence, and reconciled documentation without implying deployment.
---

# Completion

Read scope, requirements, plan, acceptance criteria, current docs, candidate revision/diff, target branch, and available evidence. Follow the shared [workflow](../../adp/development.md). If release scope is unclear, complete feature review first and ask before assembling a release.

1. Map acceptance criteria to implemented behavior and meaningful checks. Verify affected design, architecture, and overview describe the implemented portion. Required behavior, docs, and evidence must agree; list missing work and discrepancies.
2. Verify applicable project testing/security gates and independent reviews on the candidate. PRs require two independent reviewers and security first. Do not self-certify missing independent review or count failed/unavailable required checks as passes.
3. When release preparation is requested, combine intended changes, identify the exact candidate and previous release, reassess interacting contracts/callers/shared docs, and refresh invalidated evidence. Run the project's release gates; absent release definitions block release readiness.
4. Verify per-scope documentation reconciliation already happened. Resolve gaps, retain lasting decisions and product constraints in current docs, keep security reports with the change review, prune completed plan items, and retain unfinished work.
5. Report feature ready, release ready, or blocked with candidate, acceptance results, commands/results, independent reviews, failures/retries, unavailable checks, environment limits, and remaining work. For releases include configuration, migrations, and recovery requirements.

Stop at the authorized step boundary. Readiness does not authorize another roadmap item, merge, publication, or deployment. Source/local checks do not establish deployed behavior.
