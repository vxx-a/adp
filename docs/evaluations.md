# Skill evaluations

Run behavioral cases in disposable projects. The [fixtures](../tests/fixtures/skills.json) supply requests and initial files; [the runner](../scripts/evaluate_skills.py) prepares projects and checks observable outcomes. It does not invoke an agent or prove which skills it loaded.

From the ADP checkout, in one shell session:

```sh
RUN_DIR="$(mktemp -d /tmp/adp-eval.XXXXXX)"
python3 -B scripts/evaluate_skills.py prepare setup-new "$RUN_DIR/setup-new"
python3 -B scripts/evaluate_skills.py prepare setup-existing "$RUN_DIR/setup-existing"
python3 -B scripts/evaluate_skills.py prepare setup-unsafe "$RUN_DIR/setup-unsafe"
python3 -B scripts/evaluate_skills.py prepare partial-delivery "$RUN_DIR/partial-delivery"
```

Each case creates `project/`, `request.md`, and `baseline.json` under its workspace. Preparation refuses an existing workspace. Give a fresh agent the case's `project/` as its working directory and the exact request from `request.md`. Do not supply the expected skills or inherit the maintainer conversation. If native discovery is unavailable, use the installed-file fallback described in [installation](../README.md#use); record that intervention.

After the agent finishes:

```sh
python3 -B scripts/evaluate_skills.py check "$RUN_DIR/setup-new"
python3 -B scripts/evaluate_skills.py check "$RUN_DIR/setup-existing"
python3 -B scripts/evaluate_skills.py check "$RUN_DIR/setup-unsafe"
python3 -B scripts/evaluate_skills.py check "$RUN_DIR/partial-delivery"
```

Checking executes fixture Python and the partial-delivery test suite after preservation checks. Inspect generated code before running it. Keep evaluation work isolated from live credentials and services.

The helper case recognizes a direct `python3` script command with optional `-B`, `-u`, `-E`, `-s`, `-S`, `-I`, `-O`, `-OO`, or `-X dev`. Other command forms need manual validation. Check design-before-edit ordering from the run evidence; a completed setup plan may be pruned and need not remain in the final tree.

| Case | Required outcome |
|---|---|
| `setup-new` | Integrate instructions and discovery, preserve source, establish the affected baseline, and stop after setup |
| `setup-existing` | Preserve project rules/imports and unrelated Claude configuration; migrated links, commands, and symlinks still reach their original resources |
| `setup-unsafe` | Report the escaping resource as a blocker; leave that skill and external resource unchanged |
| `partial-delivery` | Select implementation from the ordinary request; implement/test add, reconcile current docs, preserve multiply and its unfinished plan, and stop |

Retain the host/version, installed product fingerprint and source identity, invocation method, exact request, actual files loaded, intervention, findings, commands/results, and stop/blocker outcome with the run outside the disposable project. Independently inspect semantic accuracy, selected skills, and stopping; the checker cannot establish these. An unchanged unsafe fixture passes only its preservation check, not proof that an agent attempted setup or reported the blocker.

The aggregate local check tests the runner's refusal and failure detection, not agent behavior. Direct-file execution, native skill discovery, different hosts, and hosted operations are separate validation claims. Native discovery, additional hosts, and the new testing, UI, operations, maintenance, and vulnerability-search skills have not received behavioral host qualification. Local acceptance does not imply those paths were exercised.

## Maintainer regression scenarios

These are ADP product-evaluation cases, not mandatory acceptance criteria for installed projects. Select affected scenarios when changing ADP's operations or monitoring guidance. Prepare isolated fixtures or authorized test environments; retain the host, invocation, candidate, results, and limits with the evaluation.

### Operations guidance

- New/existing setup, customizations, unchanged rerun, scope boundaries, access expiry, partial provisioning, cleanup failure, and uncertain outcomes.
- Native branch/tag/check/review protection, frozen release scope, actual merge identity, stabilization/abandoned-release reconciliation, and trusted evidence producers.
- Production trailing main, successive hotfixes after failure, hotfix racing publication/rollout, supersession, stale predecessor, and required forward-ports.
- Unpublished staging candidate versus published production release; staging replacement during tests; interrupted side effects; same-source rebuilds; forged evidence.
- Revoked queued authorization, expired evidence, configuration/schema drift, partial publication, and timed-out migrations under the selected locks.
- Garbage collection retaining active/recovery assets, compatible recovery/restoration, configured notification/schedule delivery, and monitoring cases below.


### Monitoring guidance

healthy service versus live process with failed flow, no traffic, dependency/release regression; stale/missing signals, collector/scheduler loss, failed routes, unavailable access/tools; stalled agents despite heartbeats, repeated failures, exhausted budgets, unauthorized-action evidence, false completion, unknown effects; duplicate alerts, missed acknowledgment, maintenance expiry, recovery without storms; sensitive/malicious telemetry, wrong targets, and write probes excluded from read scope.
