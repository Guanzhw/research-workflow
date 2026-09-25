# Source map

These are starting points for learning and engineering decisions, not proof
that a project or agent is effective. Check current scope, version, license,
and a smallest runnable example before adopting a tool. The repository's
`docs/landscape.md` and `docs/autoresearch-options.md` contain the dated survey.

| Source | What it contributes | Use with care |
|---|---|---|
| [The Turing Way](https://book.the-turing-way.org/) | Open and reproducible research practices; project design, versioning, environments, and collaboration. | A handbook of practices, not a field-specific analysis plan. |
| [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science) | A maintained scaffold for a new data project, including data, source, notebooks and tests. | Use for a new project; first inspect an existing project's own structure. |
| [research-hub](https://github.com/WenyuChiou/research-hub) | Individual skills for literature triage and research design; optional workflow state and Zotero integration. | Its full state machine can duplicate a project's local protocol. Try one skill against a real need first. |
| [Project TIER Protocol](https://www.projecttier.org/tier-protocol/) | A structured archive and workflow for transparent empirical research, including data, code, documentation, and auditability. | Adapt its social-science conventions to the actual data and discipline. |
| [Jupyter Book](https://jupyterbook.org/stable/get-started/build-websites/) / [Quarto](https://quarto.org/docs/books/) | Turn learning notebooks and text into a navigable resource. | A presentation layer; it does not verify experiment provenance. |
| [Snakemake](https://snakemake.readthedocs.io/en/stable/) / [DVC](https://dvc.org/doc/user-guide/experiment-management) / [MLflow](https://mlflow.org/docs/latest/ml/tracking/) | Dependency execution, data/experiment versioning, and run tracking respectively. | Adopt only for a concrete scale or traceability need after testing integration. |
| [SMAIRT template](https://github.com/PNNL-CompBio/smairt-template) | A research template organized around hypotheses, iterations, audit trails, and tracked contributions. | README says MIT, but no LICENSE file or GitHub license metadata was found on 2026-09-26; its linked cookiecutter target returned 404. Borrow ideas, not files. |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | A bounded loop: one editable surface, fixed evaluation budget, repeated experiments, and keep/discard logging. | GPU training is specialized. README says MIT, but no LICENSE file or GitHub license metadata was found on 2026-09-26; borrow the loop design, not code. |
| [OpenRepro-Agent](https://github.com/SHENAO1/OpenRepro-Agent) | An agent-oriented paper-reproduction CLI pattern with manifests, human gates, run comparison, reports, and handoff. | Treat repository behavior and provider support as versioned implementation details. |

When sources disagree, report the disagreement and follow the local project
protocol or the user's stated evaluation authority. Record source URL, commit
or version when available, and access date in the evidence matrix.
