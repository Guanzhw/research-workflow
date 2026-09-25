---
name: research-workflow
description: Learn an unfamiliar domain through a source-grounded field map, technical evolution, examples, and understanding checks. Also use for engineering research, project adaptation, and bounded autoresearch.
---

# Research Workflow

Help the user build a usable understanding of a field or make and test an engineering decision. Match the path to their goal and starting point. Use the local project's protocol and working tools as the execution authority when a project is involved.

## Select the task path

- **Enter a domain:** establish the learner's starting point, purpose, and available time; map the field and its main approaches before choosing what to study in depth. For a technical field, trace why approaches emerged, diverged, or persisted. Build a prerequisite-based learning route, teach key mechanisms with small examples, and check independent understanding. Use `templates/domain-onboarding.md` for a reusable handoff and read `references/technology-evolution.md` when tracing technical history.
- **Understand one mechanism:** compare primary sources, explain the mechanism with a worked example or small reproduction, and record its assumptions and limits. Use `templates/learning-note.md` when a focused learning handoff will help.
- **Investigate a solution:** inventory existing open methods, tools, templates and datasets. Check their actual scope, license, version, prerequisites, maintenance and smallest runnable example. Test promising candidates when feasible. Record a reuse / adapt / build decision with a specific gap before adding new infrastructure. Read `references/source-map.md` for method and tool candidates.
- **Run an engineering study:** state a falsifiable prediction; freeze baseline, data or task split, conditions, main metric, failures, resource budget and acceptance rule before inspecting results. Execute the real project workflow, retain every attempt, independently check key outputs, and review the conclusion.
- **Adapt an existing project:** read its current README, protocol, runner, registry and review gates first. Keep its domain metrics and artifacts authoritative. Add only the missing study design, evidence or bounded automation layer.

Paths may combine in one task. An orientation goal does not need an engineering decision or experiment. Move into the engineering study path only when the learner's goal calls for one.

## Enter a domain

1. Infer or ask only for missing details that change the route: the target field, prior knowledge, intended capability, time budget, and preferred depth. A learner may want an overview, the ability to read primary sources, or the ability to build something.
2. Give a compact field map: the problem the field solves, its inputs and outputs or central objects, major branches and method families, essential terms, common confusions, and current unresolved questions. Show current alternatives separately from historical chronology, and make the scope small enough to navigate.
3. In a technical field, make a **causal evolution map** before teaching today's methods as a list. For each important transition, explain the earlier constraint or failure, the new mechanism, what it enabled, what it cost, and which approaches still coexist. Attach dates and exact sources to pivotal claims; mark historical interpretation as interpretation. Keep this separate from the prerequisite map: when ideas appeared is not necessarily the order in which a beginner should learn them. Read `references/technology-evolution.md` for source and synthesis checks.
4. Turn the field map into the smallest useful learning route, ordered by prerequisites and the learner's goal. Assign a purpose and precise portion to each required source, and fit the route within the available time; cited evidence need not all become assigned reading. Teach one core mechanism at a time with a worked example, and use an old/new comparison on the same small problem when it clarifies a transition.
5. Ask the learner to explain, predict, or apply an idea in a fresh case without the answer in view. Distinguish material presented from understanding demonstrated; correct a gap and adjust the next step. End with what is understood, what is uncertain, and where to go next.

Prefer a short orientation first and deepen only the branches the learner needs. Sources and generated explanations support the teaching; a list of links or a plausible timeline alone is not the learning result.

## Investigate or test an engineering idea

For a source-only solution investigation, stop after the selection decision and its uncertainty. Use the experiment steps only when the task calls for a real study.

1. Write the practical decision, scope and evidence that would change it. Distinguish a source's claim from an observation you made.
2. Search original documentation, implementations and relevant research. In an evidence matrix, record URL, version or commit, date, exact locator, claim supported, evidence type and limitation. Give the user a mechanism explanation they can check.
3. Inspect reusable options before designing a new runtime. Prefer a small trial of the best candidate over a speculative framework comparison. Explain the chosen reuse, adapter or new component and the reason.
4. For an experiment, write the predicted direction and disconfirming observation. Freeze comparison, primary endpoint, secondary metrics, aggregation, seeds, environment, split, budget and stopping rule; reserve confirmation conditions outside candidate selection and run a baseline or sanity check.
5. If an agent iterates, restrict editable files or parameters, total attempts or wall time, per-run timeout, resource ceiling, and keep/discard rule. Change one reviewable factor at a time. Read `references/autoresearch-boundary.md` for the detailed pattern.
6. Preserve a complete ledger: run ID, executable candidate source commit or patch/snapshot, exact command/config, change, seed, duration and cost, metric, artifact paths or hashes, status and failure reason. Treat missing or invalid candidate results as explicit failures that count against the budget. After choosing a candidate, confirm it on pre-reserved tasks, data or independent repetitions using the frozen evaluator.
7. Recompute important metrics from raw outputs where possible. Compare matched conditions, inspect failures and counterexamples, distinguish observation from interpretation, and request independent review when a consequential claim or project rule warrants it.
8. State what was learned, the remaining uncertainty, and the smallest useful next round or stopping decision. If evaluation changes, start a new round and rerun its baseline.

Use only templates that improve the handoff: `templates/domain-onboarding.md`, `templates/learning-note.md`, `templates/research-brief.md`, `templates/evidence-matrix.csv`, `templates/run-ledger.csv`, and `templates/analysis-review.md`. Keep the result readable by someone who did not run it.
