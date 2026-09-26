# OpenResearch adapter

Use this skill for the learning route, causal technology map, understanding
check, and study design. OpenResearch owns the tools and artifacts of a project
run. These notes describe the verified OpenResearch CLI v0.2.10 interface.

## Learning and source work

For a domain orientation, make the method-family map and prerequisite route
first. Use `orx-lit-review` and its enabled discovery and paper-reading commands
when original scientific literature is needed to substantiate a mechanism or
historical turn. Keep its retrieval and citation rules; this skill determines
what the learner needs to understand and how to check understanding. A request
for a literature review alone belongs to `orx-lit-review`.

## Experiments

- Freeze the prediction, primary metric, split, confirmation conditions, and
  total resource budget before candidate selection. Use `orx-experiment-tree`
  for branches, frozen nodes, and the inherited run command; `orx-evidence`
  for persisted logs; and `orx-reports` for durable outputs. The CSV ledger here
  is optional and must not replace those records.
- Reserve confirmation data before searching. Evaluate the baseline and chosen
  candidate under the same reserved conditions after selection. Label
  confirmation nodes separately when the tree's fixed command and environment
  already support that split. If confirmation needs a different command or
  environment, use a separate fixed-contract project or independent run; do
  not edit an answered node or change the run command within an OpenResearch
  experiment tree. Record the candidate commit and the confirmation evidence.
- Count every launch and repair against the declared time and cost budget.
  OpenResearch v0.2.10 has no `--timeout` for `--backend local`; a time limit
  written only in the brief is not enforced. Put the limit in the actual fixed
  runner or select a backend that supports `--timeout`, then verify how a
  timed-out run appears in `orx runs` and `orx logs`.

## Comparing this skill with a control

OpenResearch can mirror installed coding-agent and plugin skills into its
catalog. Uploaded skills also apply to every project in the active
`ORX_DATA_DIR` and are copied into each session again on later turns. For a
control without this upload, use a separate `ORX_DATA_DIR` for each arm, or
complete the control before importing the ZIP. In either design, isolate the
agent/plugin skill sources that OpenResearch can mirror. Inspect the catalog,
those sources, and each session's native skills directory; for Codex sessions
the upload path is `.agents/skills/research-workflow/`. Verify the control's
actual skill exposure and avoid selecting this skill there. A same-named Codex
plugin can remain visible to the agent even when the upload appears in the
catalog; check the path the agent actually reads. Use matched tasks
and count all attempts. An A/B result is uninterpretable if either arm's
actual skill exposure is unknown.

On Windows, the isolated Codex home links files from the user's `CODEX_HOME`.
When symlink creation is unavailable, OpenResearch falls back to hard links,
which cannot cross volumes. Put `ORX_DATA_DIR` on the same volume as
`CODEX_HOME` for a Codex session; the error otherwise appears when a turn
starts, even though the skill ZIP imported and appeared in the dashboard.

Interface references: [OpenResearch v0.2.10 skill import](https://github.com/alphaXiv/OpenResearch/blob/v0.2.10/src/commands/library.rs),
[user skill storage and session copy](https://github.com/alphaXiv/OpenResearch/blob/v0.2.10/src/local/user_skills.rs),
[bundled skill lookup](https://github.com/alphaXiv/OpenResearch/blob/v0.2.10/src/commands/skill.rs), and
[local backend contract](https://github.com/alphaXiv/OpenResearch/blob/v0.2.10/agent-skills/orx-compute/references/local.md).
