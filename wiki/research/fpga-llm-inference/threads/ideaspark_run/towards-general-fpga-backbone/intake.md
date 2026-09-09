# Intake: Towards a General FPGA Backbone for LLM Inference

## User question

Assess whether the current Towards idea is research-worthy and sharpen it into one reviewer-defensible contribution using the Idea Spark workflow.

## Current private-system facts

- Contribution type: systems / FPGA architecture and runtime integration.
- Application boundary: unchanged llama.cpp/GGML application and real GGML graph.
- Claimed integration mechanism: native GGML FPGA backend, explicit support query, accepted operator/type/shape contract, XRT runtime, resident tensor state, and replaceable RTL/HLS operator ABI.
- Strictness contract: an accepted node must execute on FPGA or fail explicitly; silent CPU fallback is not allowed in the declared scope.
- Current validated scope: Gemma 3 1B F16 on one Alveo U280; 11 operator families; 112 c64/c512 graph signatures; 2,422/2,422 accepted development-board dispatches and zero fallback.
- Current missing evidence: second model, automatic model compiler, coarse graph fusion, matched power, model-level quality, per-signature FPGA numerical replay, and a replacement that improves end-to-end inference.
- Matched result: FPGA prefill pp512 is 302.13 s versus CPU 1.32 s (228.5x slower); FPGA decode ITL tg128 is 759.88 ms versus CPU 60.62 ms (12.54x slower).
- Runtime expansion: pp512 has 1,626 GGML calls but 224,936 XRT launches; tg128 has 104,877 calls and 202,530 launches. XRT wait is 96.25% and 79.58% of profiled operator time respectively.
- The existing backend traverses nodes in order and waits after internal launch batches. Eliminating MUL_MAT alone has Amdahl ceilings of 1.229x prefill and 1.424x decode.
- Existing closest systems: DFX, FlightLLM, Spatial LLM, EdgeLLM, StreamTensor, CODO, TeLLMe, FAST-Prefill, and FlexLLM.
- CODO and StreamTensor already compile/fuse large dataflow units. Therefore generic whole-block fusion, dataflow optimization, or another FPGA LLM accelerator is not a defensible novelty claim by itself.
- Candidate residue: preserve the real GGML/framework boundary, explicit support/no-fallback semantics, artifact identity and replaceable implementation contract while collapsing accepted node sequences into coarse persistent FPGA regions.

## Decision needed

Determine whether the current paper can stand on integration/evidence alone. If not, identify the one load-bearing mechanism and minimal falsification experiment required to turn it into a publishable paper without claiming unmatched throughput or inferred portability.
