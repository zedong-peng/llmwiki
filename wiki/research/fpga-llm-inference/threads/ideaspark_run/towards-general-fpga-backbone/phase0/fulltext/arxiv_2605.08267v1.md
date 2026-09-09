# Execution Envelopes: A Shared Admission Contract for Backend AI Execution Requests

paper_id: arxiv:2605.08267v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

Modern AI platforms do not handle one kind of execution. They handle model deployment, online inference, data preparation, evaluation jobs, workflow steps, agent runtime actions, and internal maintenance tasks. The systems challenge is not only that each class of work has different resource needs. It is also that admission semantics drift across services. Identity may be normalized in one place, resource ask fields may be rich in another, governance hints may exist only in logs, and backend-resolved allocations may not be recorded in a common shape at all.
This fragmentation matters because shared backend concerns increasingly sit at admission time. Operators want a stable place to attach request logging, guardrail hooks, resource accounting, policy-driven model governance, and eventually richer forms of execution control. But if every backend path encodes “who asked for what” differently, then each new concern has to reconstruct the same contract repeatedly.
Why this matters now is that agentic platforms are no longer composed only of static deployment and inference endpoints. They increasingly mix delegated workflows, retrieval jobs, model lifecycle actions, and runtime tool execution under one operational control plane. Once those paths share identity, tenancy, and governance surfaces, the lack of a shared execution-admission description becomes more than a code-quality annoyance. It becomes a platform-level blind spot. The backend may know who the requester was, and it may eventually know what runtime target was selected, while still lacking one durable object that says what execution was originally being admitted and how that request changed as backend resolution proceeded.
This paper proposes a narrow systems primitive for that gap: the
execution envelope
. The envelope is an internal admission object that records:
•
who asked;
•
what execution was requested;
•
what scope or governance hints accompanied the request;
•
what resources were requested;
•
what resources and routing details the backend ultimately granted.
The proposal is intentionally constrained. It is not a scheduler, not a placement engine, not a new public API payload, and not a replacement for authorization. It is a shared descriptive contract built early enough in the request path that later systems do not need to reverse engineer intent and context after the fact.
The contribution of the paper is fourfold. First, it argues that current AI backends have a missing admission primitive distinct from both authorization and scheduling. Second, it specifies a concrete envelope model, invariants, and lifecycle. Third, it defends a deployment strategy in which the envelope is proven on one path,
POST /serving/deploy_model
, before wider rollout. Fourth, it positions the design relative to adjacent work in usage control, analyzable authorization, admission control, and large-scale cluster scheduling.

## Method

Most mature backends already have some notion of request context. They know identity, tenant, request ID, and perhaps the service entrypoint. What they often lack is a normalized description of the requested execution itself.
The problem can be stated simply:
backend identity is often normalized earlier than backend execution.
This asymmetry creates several operational issues.
2.1
Repeated reconstruction
When every service-specific path encodes execution shape differently, each new concern—logging, governance, admission policy, or accounting—must reconstruct the same request semantics locally.
2.2
Loss of original intent
Many systems preserve the final resource decision but not the caller’s original ask, or vice versa. That makes later reasoning about oversubscription, denial, or narrowing much harder.
2.3
Premature coupling
Without a narrow shared contract, teams often jump too quickly from “we need consistent admission semantics” to “we need a new scheduler” or “we need a new authorization model.” Those are larger and riskier changes. The execution envelope is intended to separate the admission-description problem from both.
2.4
Degraded-path opacity
The failure mode is not only inconsistency. It is opacity under change. Backends regularly narrow requests, bind them to specific runtimes, or reject them after partial resolution. If there is no common admission artifact, those transitions become local implementation facts rather than platform-visible state. Later operators can often recover the final outcome or the original caller, but not the path between them. In contemporary AI backends, that gap matters because many governance questions are about the transition itself: what the caller asked for, what was denied or narrowed, and what the backend ultimately permitted.
