---
title: Compiled Lexical Retrieval and RAG Benchmarks
domain: research
area: misc
type: note
status: active
updated: 2026-04-19
tags: [research-thread, retrieval, grep, bm25, dense, bright, coral, ragchecker, grepqa]
---
# Compiled Lexical Retrieval and RAG Benchmarks

## Context

This thread started from the observation that coding agents and docs assistants often use direct search primitives such as `grep`, `find`, and pattern matching instead of a classic "embed corpus first, then retrieve" RAG pipeline.

The concrete local motivation was:
- `grepqa` already works well on LoCoMo-style memory retrieval
- there was uncertainty about whether that result is just a memory-specific trick
- there was uncertainty about how much of the idea is already covered by prior work such as BRIGHT, conversational RAG benchmarks, and query rewriting papers

## Key Judgments

1. The broad idea "LLM helps retrieval" is not new.
   Prior work already covers query rewriting, free-form reasoning-as-query, boolean query generation, and tool-style search workflows.
   References:
   [[../papers/query-optimization-survey-2024]], [[../papers/rag-fusion-2023]], [[../papers/bright-2025]], [[../papers/autobool-2026]], [[../papers/mintlify-chromafs-2026]]

2. `grepqa` should not be framed as "LLM as retrieval" in the generic sense.
   The more precise framing is:
   - LLM as **query compiler**
   - lexical / symbolic backend as **retrieval executor**
   References:
   [[../papers/bright-2025]], [[../papers/autobool-2026]], [[../papers/lotus-2025]], [[../papers/palimpzest-2024]]

3. The strongest claim is not "grep beats RAG."
   The stronger claim is:
   - structured lexical compilation is a useful retrieval representation
   - and it may be preferable to free-form reasoning queries in some regimes
   References:
   [[../papers/bright-2025]], [[../papers/coral-2024]], [[../papers/multi-turn-conversational-rag-2026]]

4. The current `grepqa` contribution is more about **query representation** than about BM25.
   BM25, grep, boolean filtering, and related lexical engines are backend choices.
   References:
   [[../papers/bright-2025]], [[../papers/autobool-2026]]

5. The most promising long-term framing is something like:
   - compiled retrieval
   - retrieval as query compilation
   - executable lexical retrieval programs
   References:
   [[../papers/lotus-2025]], [[../papers/palimpzest-2024]], [[../papers/mintlify-chromafs-2026]]

## Definitions / Clarifications

### Query formulation vs retrieval engine

It was important to separate:
- **Query formulation**: what query or predicate is generated
- **Retrieval engine**: how that query is executed

Examples:
- rewrite = query formulation
- CoT reasoning query = query formulation
- generated keyword predicate = query formulation
- BM25 = retrieval engine
- grep = retrieval engine
- dense retrieval = retrieval engine

### CoT reasoning query

A CoT reasoning query is not a hypothetical answer in the HyDE sense.

It is closer to:
- LLM writes a reasoning-style expanded query
- that rewritten text is then passed to a retriever such as BM25

BRIGHT is the clearest current reference point for this pattern.
References:
[[../papers/bright-2025]], [[../papers/rag-fusion-2023]], [[../papers/query-optimization-survey-2024]]

### BM25 vs grep

BM25 and grep are at the same abstraction layer even though they behave differently.

- `grep` is a hard lexical / pattern matcher:
  - does the term or regex appear?
  - where does it appear?
- `BM25` is a soft lexical ranker:
  - how much lexical evidence does each retrieval unit contain?
  - which units should rank highest?

So both are retrieval executors, but:
- grep is more exact and filter-like
- BM25 is more ranked and overlap-weighted

### Dense retrieval

Dense retrieval uses embeddings:
- encode query into a vector
- encode each retrieval unit into a vector
- rank by vector similarity

So the practical contrast is:
- grep / BM25: lexical matching
- dense: semantic similarity
References:
[[../papers/multi-turn-conversational-rag-2026]], [[../papers/personalize-before-retrieve-2025]], [[../papers/recollection-familiarity-retrieval-2026]]

### Retrieval unit matters

BM25 does not decide whether the unit is:
- a whole document
- a passage
- a paragraph
- a sentence
- a dialogue turn

That is decided by corpus segmentation / indexing.

Practical implication:
- for BRIGHT, document or passage-level units are natural
- for LoCoMo, turn-level or small window-level units are more natural

## What BRIGHT changed in the reasoning

BRIGHT matters because it already shows that:
- LLM-generated reasoning queries can improve retrieval
- BM25 plus reasoning is a serious baseline, not a toy idea
References:
[[../papers/bright-2025]]

This weakens the novelty of any claim like:
- "LLM-generated lexical hints help retrieval"

But it does **not** kill `grepqa`.

What remains open:
- whether structured keyword / boolean / typed predicates beat free-form reasoning queries
- whether lexical query compilation can be more controllable and cheaper than reasoning-text augmentation
- when lexical programs beat dense retrieval, and when they fail
Related references:
[[../papers/bright-2025]], [[../papers/autobool-2026]], [[../papers/multi-turn-conversational-rag-2026]], [[../papers/ragchecker-2024]]

## Role of the new papers added to `misc/papers`

### [[papers/bright-2025]]

Used as the main benchmark reference for reasoning-intensive retrieval.

Key relevance to this thread:
- explicit `reasoning query + retriever` setup
- direct novelty pressure on generic "LLM improves BM25" claims
- strong candidate benchmark for generalizing `grepqa` beyond memory

### [[papers/coral-2024]]

Used as the main conversational RAG benchmark reference.

Key relevance:
- multi-turn retrieval with topic shift
- response generation plus citation labeling
- good testbed for whether lexical query compilation survives beyond static retrieval

### [[papers/ragchecker-2024]]

Used as the evaluation-diagnosis reference.

Key relevance:
- separates retrieval quality from answer quality
- useful if future experiments need to show not only better final answers, but also:
  - higher claim recall
  - better context precision
  - lower noise sensitivity

## Current View of `grepqa`

`grepqa` should probably evolve along one of these paths:

1. **Structured lexical query compilation**
   Compare:
   - original query
   - free-form reasoning query
   - keyword predicates
   - boolean / typed predicates

2. **Compiled retrieval**
   Let the LLM choose between:
   - grep-like lexical matching
   - BM25-style ranking
   - metadata filters
   - dense retrieval

3. **Regime map paper**
   Study when each retrieval style wins:
   - lexical-faithful
   - paraphrastic
   - temporal / metadata-heavy
   - compositional
   - dispersed multi-answer

References for these directions:
- structured lexical compilation: [[../papers/autobool-2026]], [[../papers/bright-2025]]
- operator / compiled retrieval framing: [[../papers/lotus-2025]], [[../papers/palimpzest-2024]], [[../papers/mintlify-chromafs-2026]]
- regime-sensitive retrieval and routing: [[../papers/multi-turn-conversational-rag-2026]], [[../papers/recollection-familiarity-retrieval-2026]], [[../papers/personalize-before-retrieve-2025]]

## References / Evidence

The most important local references for this thread are:

- [[../papers/bright-2025]]
  Main evidence that free-form reasoning queries can materially improve retrieval, and that BM25 plus reasoning is already a real benchmark baseline.

- [[../papers/coral-2024]]
  Main conversational RAG benchmark reference for testing whether retrieval methods survive multi-turn history and topic shift.

- [[../papers/ragchecker-2024]]
  Main diagnosis reference for separating retrieval improvements from generation-side effects.

- [[../papers/autobool-2026]]
  Strong prior for LLM-generated executable boolean queries as a retrieval object in its own right.

- [[../papers/mintlify-chromafs-2026]]
  Industrial evidence that agentic retrieval can be mediated through search primitives such as `grep`, `cat`, and filesystem navigation.

- [[../papers/lotus-2025]]
  Declarative / systems-side reference point for query operators and execution planning over unstructured or semi-structured data.

- [[../papers/palimpzest-2024]]
  Broader declarative AI workload framing; useful for positioning "compiled retrieval" beyond a single benchmark.

- [[../papers/multi-turn-conversational-rag-2026]]
  Useful reference for retrieval-regime differences and the instability of some rewrite-heavy methods.

- [[../papers/personalize-before-retrieve-2025]]
  Reference for query-side expansion as a primary lever rather than a post-retrieval fix.

- [[../papers/recollection-familiarity-retrieval-2026]]
  Reference for routing / adaptive retrieval strategy rather than one fixed retrieval mode.


## Suggested Next Steps

1. Build a clean experiment matrix:
   - original query
   - reasoning query
   - keyword predicate
   - boolean / typed predicate

2. Test across at least three regimes:
   - LoCoMo / LongMemEval
   - BRIGHT
   - CORAL

3. Use RAGChecker-style diagnostics whenever end-to-end generation is involved.

4. Keep the future paper claim narrow and defensible:
   - not "LLM retrieval is new"
   - but "structured lexical query compilation is a distinct and useful retrieval representation"

## Open Questions

- Can structured predicates consistently outperform free-form reasoning queries on BRIGHT?
- On conversational RAG, when does lexical query compilation survive topic shift?
- Should `grepqa` stay lexical-only, or become a compiler that can route to lexical and dense backends?
