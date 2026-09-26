# Blind RAG artifact rubric

Freeze this rubric before the first scored turn. Give the grader the two outputs
under random labels, the common prompt, and `rag-source-pack.md`; hide the arm,
skill instruction, and generation order until both scores and cited passages
are recorded. Score the teaching artifact, not learner improvement.

For each dimension use the same anchors: 0 = absent or materially wrong; 1 =
named without a usable explanation; 2 = partly correct with a consequential
gap; 3 = correct and usable with a minor gap; 4 = complete, clear, and directly
checkable against the task and source pack. Record a short supporting passage
and a short missing or conflicting passage for every score.

| Dimension | Checks for a score of 4 |
| --- | --- |
| Source and citation fidelity | Central technical claims identify the correct frozen primary source; the material distinguishes supported facts from inference and leaves unsupported claims open. |
| Retrieval-to-answer mechanism | Explains indexing, query/retrieval, evidence selection, prompt use, generation, and citation or verification as a connected pipeline, including where errors enter. |
| Traceable worked example | Uses one small example whose documents, query, retrieved evidence, answer, and a failure or uncertainty can be checked by hand without invented evidence. |
| Failure modes and practical decisions | Explains when RAG suits a small task and addresses retrieval misses, misplaced evidence, and unsupported or unfaithful answers with practical checks. |
| Prerequisite route and transfer checks | Separates historical method progression from learning order, fits the two-hour route, and includes two new-situation questions with defensible answers and a clear note that no learner response was measured. |

An unsupported central claim is a correctness failure regardless of the sum.
Apply the approximately 2,200 Chinese-character body limit separately and
record violations. Compare total scores only after the correctness decision.
