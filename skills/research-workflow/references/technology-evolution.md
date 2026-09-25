# Checking technology evolution

Use this guide to explain why methods changed and how they relate. Build a
causal account of a bounded technical question, not a list of inventions.

## Choose a useful scope

Name the problem, system, and time or deployment context. Ask what constraint a
new method addressed and whether that change matters to the learner's goal.
Expand the scope only when an enabling technology or competing route is needed
to explain the evidence.

## Select meaningful nodes

Treat a paper, release, standard, deployment, or change in operating practice
as a candidate node when it changed a mechanism, available capability, or
important constraint. For each node, record the parts that help explain it:

| Question | Record |
|---|---|
| When did it happen? | Publication or announcement, release or standard, first known use, and broader adoption as separate dates when available. Mark approximate dates. |
| What constrained the earlier system? | The resources, scale, interfaces, data, or operating conditions at that time. |
| What was the earlier route's bottleneck? | A specific limitation under those conditions, supported by evidence. |
| What changed in the mechanism? | The new operation, representation, architecture, process, or assumption. |
| What did it gain and cost? | Capabilities, tradeoffs, failure modes, and conditions where the earlier route remained useful. |
| What supports this account? | Source, version or date, exact section or artifact, supported claim, and evidence limitation. |

Dates in a paper's bibliography, a product release, first use, and widespread
adoption answer different questions. Do not use one as a substitute for
another. Adoption evidence may be incomplete, so label estimates and scope
them to the field, product, or setting actually observed.

## Connect nodes without forcing a single line

Use a timeline to orient the reader and arrows to express supported
relationships: a method addresses a named bottleneck, depends on an enabling
change, or competes with another route. State what each arrow means. A later
publication alone does not show that one method caused or replaced another.

Keep concurrent branches, hybrids, and methods that remain useful visible.
Where a system-level change depended on several enablers, show those links
rather than crediting one invention with the whole transition. If the evidence
does not establish a link, leave it as a hypothesis or omit the arrow.

## Check primary and contemporaneous evidence

Start with sources closest to the claim: original papers, specifications,
standards, patents, implementation code, release notes, and deployment
records. Use contemporaneous textbooks, competing proposals, issue trackers,
benchmarks, and operational documentation to reconstruct what constraints and
alternatives existed at the time.

Separate a source's description of its own contribution from evidence that the
mechanism worked, was independently reproduced, or was adopted in practice.
Record exact sections, versions or commits, dates, and what each source can
establish. Use the [evidence matrix](../templates/evidence-matrix.csv) when a
claim needs a fuller audit trail.

Treat a paper's related-work section as a useful lead list, not a complete
history. Its selection and framing serve the paper's argument. Follow cited
work to the original sources and check contemporaneous alternatives, including
approaches that were not selected for comparison.

## Keep the first account light

A useful short account usually needs a small causal map, a node table with
source locators, the main parallel route, and a sentence on uncertainty or
date scope. Keep claims tied to evidence and distinguish historical facts from
interpretation.

Expand the account when a decision depends on disputed priority, a claimed
causal link, adoption scale, or a changing technical interface. Then compare
additional sources, inspect versions or artifacts, or reproduce the smallest
relevant example. A literature-only question needs a supported explanation;
it does not need an experiment by default. See the
[domain-onboarding template](../templates/domain-onboarding.md) for a compact
learning handoff.
