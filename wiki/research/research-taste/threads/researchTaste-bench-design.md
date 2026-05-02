---
title: ResearchTaste-Bench Design
domain: research
area: research-taste
type: concept
status: stable
updated: 2026-04-08
tags: [benchmark-design, construct-validity, contamination, living-benchmark, research-taste]
---
# ResearchTaste-Bench Design

## One-Sentence Positioning
**ResearchTaste-Bench** is a living benchmark for research taste: it measures whether a model can judge which ideas are worth pursuing, using historical papers, objective downstream signals, contamination checks, and explicit construct validation.

## Why This Benchmark Exists
The field already has serious **execution** benchmarks:
- [[../papers/starace-2025-paperbench]]
- [[../papers/scientist-bench]]
- [[../papers/mlrc-bench-2025]]

What is still weakly measured is the upstream question:

> Before executing a project, can a model tell whether the idea is worth doing?

That is the gap this benchmark targets.

## The Core Decomposition

### AI Scientist = Taste × Execution
This area now uses a simple framing:

- **Taste**: choosing what deserves effort
- **Execution**: actually carrying the work out

The point is not that taste is the only capability. The point is that it should be measured separately from execution.

## Construct Definition
Following [[karpathy-perspective]], the benchmark operationalizes research taste as five related signals:

1. **Importance**
2. **Attackability**
3. **Timing**
4. **Elegance**
5. **Fertility**

These are design hypotheses, not fixed truth. The benchmark therefore includes a validation stage instead of assuming the factor structure is correct.

## Main Task

### Pairwise Taste Judgment
Input:
- a short field context at time `T`
- abstract A with title/author/year/venue/citations removed
- abstract B with the same masking

Question:
- Which idea is more worth investing research effort in?

Output:
- `A`, `B`, or `tie`
- a short rationale grounded in the idea's structure, not prestige cues

## Diagnostic Subtasks
The benchmark should report a main score plus diagnostic profiles.

### D1. Novelty Trap Test
Contrast:
- high novelty, low long-term impact
- lower novelty, higher long-term impact

Purpose:
- detect novelty bias, motivated by [[../papers/hindsight-novelty-bias]]

### D2. Timing Sense Test
Give the same idea under three historical field states and ask when it was most ripe.

Purpose:
- measure Karpathy-style timing/ripeness

### D3. Sleeping Beauty Detection
Show papers with weak early citation signals and ask whether they will wake up later.

Purpose:
- measure the hardest part of taste: spotting underrated future impact
- grounded in [[../papers/ke-2015-sleeping-beauty]]

### D4. Synthetic Idea Test
Use fully synthetic ideas with no real paper identity and score only for diagnosis.

Purpose:
- estimate the gap between **taste** and **parametric recall**
- diagnose whether a model is judging ideas or retrieving fame

This diagnostic should not define the main leaderboard because its ground truth is less objective.

## Ground Truth Design

### Three-Tier Ground Truth Pyramid
The benchmark uses a weighted pyramid rather than plain citation count.

#### Tier 1. Standard Impact
- based on 2-year downstream impact percentile
- lowest weight

#### Tier 2. Early Underrated
- weak early citations, strong later uptake
- medium weight

#### Tier 3. Sleeping Beauty
- clearly under-recognized early, strong later awakening
- highest weight

This solves a central flaw in citation-only evaluation: papers with delayed recognition are exactly the cases where taste should matter most.

### Composite Downstream Signal
Ground truth should combine multiple objective signals:
- late citation percentile
- inspired/follow-on work count
- survey uptake
- Sleeping Beauty index where applicable

## Primary Metrics

### Weighted Taste Accuracy
Main leaderboard metric:
- pairwise accuracy with tier weights `1x / 2x / 5x`

### Diagnostic Metrics
- **Novelty Bias**
- **Timing Accuracy**
- **SB Detection Rate**
- **Contamination Gap**

## Contamination and Circular-Evaluation Defenses
The benchmark is designed around the fact that LLM-as-judge is fragile.

### Defense 1. Blind Inputs
Strip:
- title
- author
- venue
- citation count
- year

Motivation:
- [[../papers/saraf-2025-label-bias]]
- [[../papers/li-2026-preference-leakage]]

### Defense 2. CCV-Style Contamination Check
Probe whether the model appears to know the paper identity across fresh sessions.

Motivation:
- [[../papers/ccv-contamination]]

### Defense 3. Objective Ground Truth
The final answer key should come from citation dynamics and downstream uptake, not from an LLM judge.

### Defense 4. Living Benchmark Updates
Continuously add newer papers so the evaluation set stays fresher than most training data.

Motivation:
- [[../papers/swe-bench-live]]

## Construct Validation Plan
This is what turns the benchmark from a good idea into a credible measurement instrument.

### Multi-Model IRT / Factor Analysis
Collect responses from a wide ability range of models and fit a multidimensional IRT model.

Questions to answer:
- Is research taste actually one factor or several?
- Do timing and attackability collapse into one latent dimension?
- Do novelty-trap items load on elegance, or on a distinct bias factor?

Motivation:
- [[../papers/salaudeen-2025-construct-validity]]
- [[../papers/chen-2025-irt-llm]]

### Predictive Validity
A strong benchmark score should predict at least one more realistic research judgment task:
- expert side-by-side idea ranking
- proposal selection quality
- correlation against Scientist-Bench for the same models

If the correlation with real research judgment is weak, the benchmark should be treated as a useful proxy, not a solved measurement.

## Benchmark-Reality Gap
The design explicitly admits a gap that cannot be removed:

> Pairwise judgment on blinded abstracts is not the same as deciding what to spend six months of research on.

The benchmark is still useful if it is framed honestly:
- it measures **judgment under compression**
- not full research taste in the wild

## Recommended Leaderboard Format
Report a profile matrix, not only a single score:

| Model | WTA | Novelty Bias | Timing | SB Detection | Contam. Gap |
|------|-----|--------------|--------|--------------|-------------|
| Claude-family | ... | ... | ... | ... | ... |
| GPT-family | ... | ... | ... | ... | ... |
| Human reviewer | ... | ... | ... | ... | ... |

Optional cuts:
- by field: NLP / CV / RL / theory
- by contamination level
- by time period

## Minimal Build Plan
For a first serious version:

1. Pull 2019-2022 papers from major ML venues.
2. Compute three-tier impact labels.
3. Build around 500 strong contrastive pairs.
4. Add novelty, timing, and SB diagnostic subsets.
5. Run blind evaluation across multiple model families.
6. Run one IRT study for the paper.

This is small enough to prototype quickly but strong enough to support a real paper if the validity story holds.

## What Makes This Design Different
Compared with the current landscape, this design aims to combine:

- objective downstream ground truth
- explicit contamination measurement
- living-benchmark refresh
- construct-validity analysis
- diagnostic separation of novelty bias, timing, and sleeping-beauty detection

## Related Pages
- [[research-taste]] — core concept
- [[karpathy-perspective]] — theoretical origin
- [[evaluation-approaches]] — measurement tradeoffs
- [[../comparisons/benchmark-landscape]] — where this fits
- [[../papers/gong-2025-economics-taste]] — human/model baseline
- [[../papers/why-llms-arent-scientists]] — strongest motivation
