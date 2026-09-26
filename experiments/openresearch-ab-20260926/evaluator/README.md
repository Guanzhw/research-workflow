# External evaluator

Keep this directory outside every agent's fixture snapshot. Give agents only `fixture/` and the development feedback you elect to share. Preserve an unchanged copy of this evaluator for both A/B arms.

Run the baseline or a candidate on the three fixed development datasets:

```powershell
python -B evaluator/evaluate.py dev --solution fixture/solution.py --output dev-report.json
```

The default is 1,800,000 rows per dataset, two runs per dataset, a 120-second per-run timeout, and a 512 MiB Windows Job Object memory limit. Both modes check that no arguments and a missing input produce nonzero exit codes, then run five fixed correctness cases: empty input, rows with no boolean true, escaped and Unicode tenant names, an empty tenant name, and large signed sums. Successful runs must have empty stdout. The report records contract checks separately; they do not enter any throughput median. The oracle holds expected bytes in evaluator memory, never in the candidate-readable temporary directory. Reports include input, expected-output, solution, and evaluator SHA-256 hashes; elapsed time; rows and input MiB per second for timed datasets; and peak job memory. The dataset median uses passing timed runs only. Generation and reference calculation are outside timed samples. `--rows`, `--repeats`, `--timeout-sec`, and `--memory-mib` allow small local checks; record every override when comparing arms.

For final confirmation, the operator privately sets `OPENRESEARCH_HOLDOUT_SEEDS` to two distinct positive integer seeds, each with distinct, nonzero low 32 bits different from the dev seeds. Choose them outside the agent workspace; do not send them or the confirmation inputs to either agent. The evaluator removes the seed variable from the solution subprocess environment and redacts the seeds from the confirmation report. Use the same private seeds for both arms:

```powershell
$env:OPENRESEARCH_HOLDOUT_SEEDS = '<private-seed-1>,<private-seed-2>'
python -B evaluator/evaluate.py confirm --operator-confirm --solution fixture/solution.py --output confirm-report.json
Remove-Item Env:OPENRESEARCH_HOLDOUT_SEEDS
```

Run `python -B evaluator/evaluate.py selftest --output evaluator/preflight-report.json` to check timeout, process-tree termination, the memory limit, wrong output, exit code 1, unexpected stdout, and invalid invocation handling on the local Windows host. The memory test checks that an allocation fails under 64 MiB and succeeds under 512 MiB; Windows' peak job memory counter may include a denied allocation and can therefore exceed the configured limit.
