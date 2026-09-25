# Bounded autoresearch pattern

Autoresearch is a controlled search over changes, not permission for an agent
to run indefinitely or rewrite an entire project. Keep the loop legible and
reversible.

## Pre-flight

Record:

- the frozen baseline command and baseline result;
- one primary metric, its direction, and the acceptance threshold;
- the exact editable files or parameters;
- the data/task split and seed policy;
- the conditions reserved for confirmation, outside candidate selection;
- per-run timeout, total run count or wall-clock budget, and resource ceiling;
- the artifact directory and required log fields;
- actions that need a human gate, such as publishing, deleting data, spending
  money, changing credentials, or contacting an external service.

Reject the loop if the baseline cannot run, the primary metric is undefined,
the output is not independently inspectable, or the proposed change can alter
the evaluation itself.

## Per-run loop

1. Propose one small, named change and state its expected effect.
2. Capture the pre-change revision and configuration, and save the executable
   candidate as a commit or complete patch/source snapshot before running it.
3. Run the declared command under the fixed budget.
4. Validate that outputs are complete, finite, and from the frozen split.
   A crashed, timed-out, or incomplete candidate is a recorded failed trial;
   charge its cost and restore the known state before the next proposal.
5. Record metrics, duration, resource use, logs, artifacts, and failure reason.
6. Keep a change only under the predeclared rule; otherwise restore or mark it
   discarded so the next proposal starts from a known state.

Keep/discard is evidence for this run, not a claim of general superiority.
After selection, run the baseline and selected change on pre-reserved tasks,
data, or independent repetitions using the frozen evaluator. Keep these
confirmation conditions out of candidate selection and label both phases.

## Stop conditions

Stop at the first of: budget exhaustion; a broken evaluator or data drift;
the predeclared consecutive infrastructure-failure threshold; a breached
guardrail or unexplained metric regression; safety or authorization boundary;
or a result that requires a new hypothesis. An ordinary candidate crash or
missing output ends that trial, not the whole loop. Preserve the partial
ledger and say why the loop stopped.

For literature-only questions, use the same proposal and evidence discipline
for source searches, but do not simulate numerical experiments. For project
adaptation, the local project's runner and review gates take precedence over
this generic pattern.
