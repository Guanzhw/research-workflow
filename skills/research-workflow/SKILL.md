---
name: research-workflow
description: Learn an unfamiliar domain and test engineering ideas through primary-source research, reuse of existing tools, and bounded, auditable experiments. Use for cross-domain research plans, project adaptations, and autoresearch loops.
---

# Research Workflow

Help the user learn enough to make an engineering decision and then test it. Adapt the workflow to the field and the user's goal; a publication is optional. Use the local project's protocol and working tools as the execution authority.

## Select the task path

- **Learn a domain:** frame a concrete question, compare primary sources, explain the mechanism with a worked example or small reproduction, and record what remains uncertain. Use `templates/learning-note.md` when a learning handoff will help.
- **Investigate a solution:** inventory existing open methods, tools, templates and datasets. Check their actual scope, license, version, prerequisites, maintenance and smallest runnable example. Test promising candidates when feasible. Record a reuse / adapt / build decision with a specific gap before adding new infrastructure. Read `references/source-map.md` for method and tool candidates.
- **Run an engineering study:** state a falsifiable prediction; freeze baseline, data or task split, conditions, main metric, failures, resource budget and acceptance rule before inspecting results. Execute the real project workflow, retain every attempt, independently check key outputs, and review the conclusion.
- **Adapt an existing project:** read its current README, protocol, runner, registry and review gates first. Keep its domain metrics and artifacts authoritative. Add only the missing study design, evidence or bounded automation layer.

Paths may combine in one task. Literature-only work ends with a supported learning or selection decision; do not invent an experiment.

## Complete a cycle

1. Write the learning goal, practical decision, scope and evidence that would change the decision. Distinguish a source's claim from an observation you made.
2. Search original documentation, implementations and relevant research. In an evidence matrix, record URL, version or commit, date, exact locator, claim supported, evidence type and limitation. Give the user a mechanism explanation they can check.
3. Inspect reusable options before designing a new runtime. Prefer a small trial of the best candidate over a speculative framework comparison. Explain the chosen reuse, adapter or new component and the reason.
4. For an experiment, write the predicted direction and disconfirming observation. Freeze comparison, primary endpoint, secondary metrics, aggregation, seeds, environment, split, budget and stopping rule; reserve confirmation conditions outside candidate selection and run a baseline or sanity check.
5. If an agent iterates, restrict editable files or parameters, total attempts or wall time, per-run timeout, resource ceiling, and keep/discard rule. Change one reviewable factor at a time. Read `references/autoresearch-boundary.md` for the detailed pattern.
6. Preserve a complete ledger: run ID, executable candidate source commit or patch/snapshot, exact command/config, change, seed, duration and cost, metric, artifact paths or hashes, status and failure reason. Treat missing or invalid candidate results as explicit failures that count against the budget. After choosing a candidate, confirm it on pre-reserved tasks, data or independent repetitions using the frozen evaluator.
7. Recompute important metrics from raw outputs where possible. Compare matched conditions, inspect failures and counterexamples, distinguish observation from interpretation, and request independent review when a consequential claim or project rule warrants it.
8. State what was learned, the remaining uncertainty, and the smallest useful next round or stopping decision. If evaluation changes, start a new round and rerun its baseline.

Use only templates that improve the handoff: `templates/research-brief.md`, `templates/evidence-matrix.csv`, `templates/learning-note.md`, `templates/run-ledger.csv`, and `templates/analysis-review.md`. Keep the result readable by someone who did not run it.
