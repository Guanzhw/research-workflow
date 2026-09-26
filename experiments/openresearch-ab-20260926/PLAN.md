# OpenResearch × research-workflow v0.3 feasibility pilot

Date: 2026-09-26. This protocol is frozen before the first scored agent turn. Any
change after that turn starts requires a new round; all earlier attempts remain
in the ledger.

## Decision and prediction

Decide whether the uploaded research-workflow skill can be invoked reliably in
OpenResearch and whether a larger matched evaluation is worth its cost. We
predict that, at the same model and task budget, it will improve the structure
and evidence of a beginner RAG teaching artifact and the auditability of a
bounded JSONL optimization attempt. A missing or wrong skill read, material
correctness regression, or disproportionate total cost would disconfirm the
case for expanding the integration. One task per arm is a feasibility check,
not an estimate of general effectiveness or learner gain.

## Arms and isolation gate

| Arm | OpenResearch library | Agent instruction |
| --- | --- | --- |
| A | No `research-workflow` upload | Identical task body, no skill trigger |
| B | Only the v0.3 ZIP upload | `/research-workflow` plus identical task body |

Both arms use the same clean `CODEX_HOME`, `gpt-6-sol` at medium reasoning,
Codex permission mode `approve-for-me`, the same OpenResearch executable, and separate
fresh `ORX_DATA_DIR` directories on C:. Each arm uses a separate Git clone from
the same fixture commit. Both receive OpenResearch's bundled skills. The
`/research-workflow` prefix is the declared intervention; the remaining task
text is byte-identical. No live web retrieval is allowed during scored tasks.

Before dispatch, capture: binary SHA, config SHA, fixture commit, uploaded ZIP
SHA, project and session IDs, catalog entry, Codex plugin inventory, global and
project skill paths, session `.agents/skills` paths, and each actually read
`SKILL.md` path and SHA. A must not expose any `research-workflow` skill; B must
read the uploaded v0.3 copy. If the gate fails, no score is assigned. Repair
the cause and restart both arms on a new equal binary, retaining the failed
attempts and setup cost.

## Matched tasks and order

1. RAG teaching: run A, then B, using `rag-prompt.md` and the same frozen local
   `rag-source-pack.md`. One turn per arm, 12 minutes maximum wall time each.
   The deliverable is teaching material, not a measured change in a learner.
2. CPU JSONL optimization: run B, then A, using `jsonl-prompt.md` and the same
   fixture baseline. Each arm has at most 30 minutes, three candidate commits,
   and one repair launch per candidate. Only `solution.py` may change. Count
   every candidate, launch, failure, retry, and discarded result.

The RAG artifact is graded blind to arm using the frozen `rag-rubric.md` on five 0–4 dimensions: source and
citation fidelity; retrieval-to-answer mechanism; traceable worked example;
failure modes and practical decisions; prerequisite route and transfer checks.
An unsupported central claim is a correctness failure. The result measures
artifact quality only. The grader records concrete supporting and failing
passages before revealing the arm.

The JSONL evaluator outside the editable fixture checks byte-identical output
against an independent oracle, enforces a 120-second process-tree wall limit
and 512 MiB job memory limit, and records peak memory. Its dev inputs and
machine are fixed for both arms; two distinct seeds are reserved for
confirmation. The primary engineering endpoint is correctness-gated median
input MiB/s on confirmation cases relative to the common baseline. A reported
performance win requires every holdout output to match, all limits to pass,
every paired comparison to favor the candidate, and median speedup >= 1.10x.
Otherwise report regression or inconclusive evidence. After both arms lock
their commits, the operator invokes the confirmation evaluator four separate
times per arm with `--repeats 1`, in baseline–selected–selected–baseline
(ABBA) order. Each invocation uses the same two private holdout seeds and gets
its own report; record the command and order. The confirmation evaluator and
seeds are never used during selection.

## Accounting and stop rule

For all four agent turns record start/end time, actual model and effort, all
token usage available (input, output, cached and total), tool-call count,
failed/retried calls, source/context volume when available, and setup time.
For each engineering run record run ID, candidate commit or patch, exact
command, fixture/evaluator hashes, seed, status, duration, peak memory,
correctness and throughput. A missing metric remains explicitly unknown.
The total cost per successful confirmed candidate includes every attempt and
preparation. Stop an arm at its time/attempt ceiling or at an isolation or
runner-integrity failure. Do not substitute a later task or favorable repeat.

## Preflight required by independent review

- Verify neither the clean Codex home nor global/project skill paths expose
  `research-workflow` to A, and inspect a real session's loaded skill paths.
- Freeze exact prompts, source pack, fixture commit, hashes, rubric, order and
  budgets before any scored turn.
- Prove the fixed evaluator kills a deliberately hung child process tree,
  rejects an incorrect output, and enforces memory limits. Baseline timing
  must be long enough to measure meaningfully.
- Run the same OpenResearch binary in both arms. If skill selection is
  ambiguous, fix it and restart both arms before scoring.

Independent plan reviewer: `/root/plan_reviewer` approved preparation subject
to these four preflight gates. Final diff, real session paths, and raw results
will receive a separate independent review.
