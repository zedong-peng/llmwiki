# Right-to-Act: A Pre-Execution Non-Compensatory Decision Protocol for AI Systems

paper_id: arxiv:2604.24153v1
tier: T3
source_used: html_arxiv
warning: none

## Intro

AI systems are moving from advisory outputs toward executable decisions. In agentic and tool-using systems, model outputs may trigger fund transfers, account restrictions, database operations, infrastructure changes, procurement workflows, or other actions with legal, financial, operational, or reputational consequences.
A common architecture can be summarized as follows:
AI decision
→
\rightarrow
validation
→
\rightarrow
execution
.
The validation step may include access control, safety filters, policy checks, risk scoring, compliance rules, or post-hoc audit. These mechanisms are necessary. However, they do not fully answer a different question:
Should this decision be allowed to exist as an executable event at all?
This paper argues that this question defines a distinct architectural gap. Existing paradigms evaluate whether a user is allowed, whether an output is harmful, whether a policy is violated, or whether observed system behavior falls within certified risk bounds. A pre-action legitimacy boundary instead evaluates whether the AI-generated decision has earned the right to proceed toward execution before ordinary validation or certification is treated as sufficient.
The goal is not to replace authorization, safety, runtime governance, or certification. The goal is to formalize a missing condition before execution:
the right to act
. We call this gap the
Pre-Action Legitimacy Gap
.
1.1  Contributions
This paper makes four contributions:
1.
It defines the pre-action legitimacy problem as a distinct computational and architectural problem for AI systems that act in the world.
2.
It formalizes a non-compensatory Right-to-Act decision boundary using minimal constraint notation that avoids implementation-specific details.
3.
It proves a non-equivalence theorem: compensatory scoring systems cannot guarantee pre-action legitimacy when required constraints must hold individually.
4.
It provides a case study showing how the proposed boundary changes the outcome of a high-confidence, policy-compliant account suspension decision.

## Method

Definition 1
(Pre-Action Legitimacy Gap)
.
The Pre-Action Legitimacy Gap is the absence of a formal mechanism that determines, prior to execution, whether an AI-generated decision has the right to exist as an executable event.
The gap is easiest to see in cases where a decision is:
•
authorized by identity or role;
•
compliant with an explicit policy;
•
scored as low risk or high confidence;
•
still inappropriate, premature, unjustified, or structurally invalid in context.
Examples include disabling an account without sufficient contextual verification, executing a payment when authority exists but justification is incomplete, or allowing an AI agent to take irreversible infrastructure action under ambiguous state. In such cases, the failure is not merely a safety failure, a policy failure, or an authorization failure. It is a legitimacy failure at the execution boundary.
