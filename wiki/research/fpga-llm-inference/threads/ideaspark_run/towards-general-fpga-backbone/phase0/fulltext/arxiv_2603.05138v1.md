# Standardizing Access to Heterogeneous Quantum Backends: A Case Study on Cloud Service Integration with QDMI

paper_id: arxiv:2603.05138v1
tier: T3
source_used: failed
warning: fetch raised IncompleteRead: IncompleteRead(81920 bytes read, 8065 more expected)

## Intro

With an increasingly diverse portfolio of quantum backends, the adoption of standardized interfaces has become a key prerequisite for scalable access and interoperability within quantum software stacks. The Quantum Device Management Interface (QDMI) addresses this challenge and is emerging as one of the de facto standards for hardware abstraction, enabling the unified management not only of individual Quantum Processing Units (QPUs) but also of complete full-stack cloud services. This paper presents a case study demonstrating the integration of QDMI with Amazon Braket, a quantum computing cloud service that provides a single access point to a wide range of hardware technologies. By treating the cloud service itself as a unified device, the proposed implementation enables management of the complete task lifecycle - ranging from authentication and circuit submission to result retrieval - across Braket's heterogeneous set of simulators and hardware backends. We detail the engineering insights gained from this integration and present a hands-on example workflow, ultimately paving the way for integrated access to cloud-hosted quantum resources from QDMI-enabled software stacks.

## Method


