# Performance tests

## Scope

Test stated latency, throughput, and capacity requirements when a change could affect them. Use project load targets to decide scope.

## Inputs

- Target traffic, data volume, concurrency, latency, and resource limits.
- Affected paths, representative data, baseline revision, and repeatable test environment.

## Steps

1. Select the affected workloads and measurable acceptance thresholds. Missing targets block claims that performance requirements pass.
2. Compare baseline and candidate using the same data, resources, dependency versions, and workload. Keep these runs isolated from unrelated work.
3. Measure relevant latency percentiles, throughput, errors, and resource use at the stated load, including sustained or burst behavior when required.
4. Verify correctness during load, especially duplicate handling, concurrent writes, and queue completion where applicable.
5. Repeat enough to distinguish a regression from run-to-run variation. Record warmup, duration, sample counts, and environment differences.

## Output and gate

- Candidate meets the specified targets without correctness failures.
- Baseline and candidate measurements, workload, environment, commands, and limitations recorded.
- Results apply to the tested load and environment.
