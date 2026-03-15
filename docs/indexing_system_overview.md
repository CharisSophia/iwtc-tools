# IWTC Tools – Indexing System Overview

This document describes the conceptual architecture of the indexing system implemented in `iwtc-tools`.

The indexing system converts campaign materials and curated world knowledge into structured artifacts that support discovery, analysis, and world navigation.

The system is designed to separate three different concerns:

- **evidence extraction** from source materials
- **structural representation** of relationships
- **semantic interpretation** of the campaign world

Automation assists with extraction and structure, while humans remain responsible for interpretation.


---

# Architectural layers

The indexing system operates as a set of loosely coupled workflows. Each workflow performs a distinct transformation and produces reproducible artifacts.

At a high level the architecture can be viewed as the following sequence:
```campaign materials
↓
raw source indexing
↓
canonical index artifacts
↓
graph indexing
↓
evidence graph
↓
semantic indexing
↓
semantic graph```

Query workflows operate alongside these layers to allow exploration and inspection of the generated artifacts.

---

# Workflows

The indexing system currently consists of the following workflows.

| Workflow | Role |
|--------|--------|
| Raw Source Indexing | Translate campaign materials into structured evidence indexes |
| Index Querying | Inspect and explore index artifacts |
| Graph Indexing | Translate index artifacts into a structural evidence graph |
| Graph Querying | Traverse and analyze the evidence graph |
| Semantic Indexing | Translate curated world relationships into a semantic graph |

Each workflow is implemented as a separate notebook within `iwtc-tools`.

---

# Evidence vs semantic knowledge

The system intentionally distinguishes between **evidence** and **meaning**.

Evidence describes what appears in campaign materials.

Semantic knowledge describes what the world means.

These concepts are represented by two complementary graph layers.

### Evidence graph

The evidence graph is derived directly from indexed campaign materials.

It represents structural relationships visible in the sources, such as:

- entities appearing in the same session
- mentions within documents
- references between characters and places

The evidence graph supports exploratory analysis and relationship discovery.

### Semantic graph

The semantic graph represents curated world knowledge.

Relationships in this graph are defined by human interpretation, such as:

- membership in a faction
- alliances between organizations
- locations associated with characters
- ownership or control of artifacts

This graph expresses the intended structure of the campaign world.

---

# Human-directed interpretation

The indexing system deliberately avoids automatic narrative interpretation.

Automation can identify patterns and structural signals, but interpretation remains a human responsibility.

Semantic relationships are therefore curated in explicit world data tables before being translated into semantic graph artifacts.

This design ensures that:

- narrative meaning remains under human control
- graph artifacts remain reproducible
- evidence and interpretation remain clearly separated

---

# Design philosophy

The indexing system follows several guiding principles.

**Evidence first**  
Source materials are preserved and indexed before interpretation occurs.

**Human interpretation**  
Automation assists discovery but does not assign narrative meaning.

**Reproducible artifacts**  
All graph structures are generated from source data through deterministic workflows.

**Layered architecture**  
Evidence extraction, structural representation, and semantic interpretation are implemented as separate workflows.

This structure allows the indexing system to scale as the campaign world grows while remaining transparent and maintainable.