# Frozen RAG source packet

Snapshot checked 2026-09-26. These six primary papers provide the same bounded
evidence to both pilot arms. The notes paraphrase each paper's abstract; follow
the versioned link for full methods and experimental conditions. Reported
comparisons are results of the authors' stated benchmarks, not universal
rankings. This packet does not contain a proposed lesson order or a worked
example.

| ID | Primary source and exact locator | Bounded evidence available for the task |
| --- | --- | --- |
| S1 | Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, [arXiv:2005.11401v4](https://arxiv.org/abs/2005.11401v4), 2021-04-12, abstract | The paper combines a sequence-to-sequence model's parametric memory with a dense Wikipedia index accessed by a neural retriever. It contrasts conditioning on the same retrieved passages for a whole output sequence with allowing different passages per token. Its motivation includes access to knowledge, provenance and updateability; reported gains are on the paper's knowledge-intensive tasks. |
| S2 | Karpukhin et al., *Dense Passage Retrieval for Open-Domain Question Answering*, [arXiv:2004.04906v3](https://arxiv.org/abs/2004.04906v3), 2020-09-30, abstract | Sparse TF-IDF/BM25 retrieval was an established open-domain QA baseline. The paper learns dense query and passage representations with a dual encoder and reports higher top-20 passage retrieval accuracy than a strong Lucene-BM25 baseline on its evaluated datasets. That result does not establish that dense search is always preferable to lexical search. |
| S3 | Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, [arXiv:2307.03172v3](https://arxiv.org/abs/2307.03172v3), 2023-11-20, abstract | In multi-document QA and key-value retrieval experiments, moving relevant information within a long input changed model performance: middle positions often fared worse than beginning or end positions. This shows a measured long-context use failure; it is not a proof that every model or task needs retrieval. |
| S4 | Asai et al., *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*, [arXiv:2310.11511v1](https://arxiv.org/abs/2310.11511v1), 2023-10-17, abstract | The authors identify a limitation of always adding a fixed number of passages even when retrieval is unnecessary or passages are irrelevant. Self-RAG trains reflection tokens for on-demand retrieval and critique during generation. Its reported advantages are for the evaluated model sizes and tasks. |
| S5 | Sarthi et al., *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*, [arXiv:2401.18059v1](https://arxiv.org/abs/2401.18059v1), 2024-01-31, abstract | Short contiguous chunks can miss a document's wider context. RAPTOR embeds, clusters and summarizes chunks recursively into a retrieval tree so inference can retrieve across abstraction levels. Its reported gains are from the paper's controlled QA comparisons. |
| S6 | Ru et al., *RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation*, [arXiv:2408.08067v2](https://arxiv.org/abs/2408.08067v2), 2024-08-17, abstract | The paper evaluates retrieval and generation components separately because whole-system scores can hide failure causes. It introduces diagnostic metrics and reports a meta-evaluation plus experiments on eight RAG systems. Its metrics are a proposed evaluation method, not a guarantee of answer correctness. |

The sources support claims about these methods and experiments. They do not
provide a complete 2026 market inventory, a production cost comparison, or
evidence that any particular learner has understood RAG.
