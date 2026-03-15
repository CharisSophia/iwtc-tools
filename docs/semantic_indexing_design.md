# Semantic Indexing – Design Overview

This document defines the design, scope, and responsibilities of the semantic indexing workflow implemented in `iwtc-tools`.

Semantic indexing translates curated world relationships into a semantic graph layer suitable for downstream graph analysis and traversal.

The corresponding execution notebook is:

- `notebooks/IWTC_Semantic_Indexing.ipynb`

Readers should treat this document as the conceptual contract for semantic indexing. The notebook implements this design.

For an overview of how this workflow fits into the broader indexing system, see:

- `docs/indexing_system_overview.md`

---

# Purpose and scope

Semantic indexing introduces a **curated knowledge layer** for a campaign world.

Earlier workflows in the indexing system operate on evidence extracted from campaign materials. Those workflows preserve what appears in source documents and how those signals connect structurally.

Semantic indexing performs a different role: it translates **human-curated world knowledge** into a graph-ready representation.

The workflow supports two closely related goals:

- assisting discovery of potential relationships using evidence signals
- translating curated relationships into semantic graph artifacts

Semantic indexing therefore bridges the gap between:

- evidence-first indexing
- structural graph traversal

It allows a campaign world to have both:

- an **evidence graph** derived from indexed sources
- a **semantic graph** representing curated world relationships


---

# Semantic indexing workflow

Semantic indexing is a human-directed workflow.

Automation assists discovery and structural translation.  
Humans retain authority over meaning and interpretation.

At a conceptual level the workflow proceeds as follows:

1. Evidence signals from canonical index artifacts are analyzed to identify potential entity relationships.
2. Candidate relationships are produced for human review.
3. Humans curate canonical relationship statements describing the world.
4. The curated relationship table is translated into semantic graph artifacts.

Discovery and interpretation are intentionally separated.

Discovery proposes possible relationships based on evidence.

Interpretation assigns meaning through curated predicates.


---

# Assumptions

Semantic indexing operates under the following assumptions:

- Canonical index artifacts already exist and were generated from raw sources.
- Canonical index artifacts remain evidence-first and are not manually edited.
- Canonical world relationships are human-curated.
- Semantic interpretation policies are maintained separately from world facts.

Semantic indexing does not infer narrative meaning automatically.

It translates curated relationships into a form suitable for structural graph analysis.


---

# Inputs

Semantic indexing operates on previously generated index artifacts and curated world data declared in the world repository descriptor.

Typical inputs include:

- canonical index artifacts
- canonical entity vocabulary
- curated world relationships
- semantic policy tables

All inputs are treated as read-only.


---

# Outputs

Semantic indexing produces graph artifacts representing curated world relationships.

These artifacts form the **semantic relationship graph layer**.

Nodes represent entities participating in curated relationships.

Edges represent subject–predicate–object statements describing those relationships.

Semantic graph artifacts are written to `working_drafts` for review before optional promotion to canonical storage.


---

# Relationship to other workflows

Semantic indexing operates alongside the other indexing workflows in `iwtc-tools`.

| Workflow | Purpose |
|--------|--------|
| Raw Source Indexing | Extract evidence from campaign materials |
| Index Querying | Query evidence tables |
| Graph Indexing | Construct an evidence graph from index artifacts |
| Graph Querying | Traverse graph structure for exploratory analysis |
| Semantic Indexing | Translate curated world knowledge into a semantic graph |

Evidence graphs describe **what appears in the sources**.

Semantic graphs describe **what the world means**.


---

# Design philosophy

Semantic indexing follows the same architectural principles as the rest of the indexing system:

- evidence-first indexing
- human-controlled interpretation
- reproducible artifact generation
- explicit promotion of canonical artifacts

Automation proposes structure.

Humans define meaning.