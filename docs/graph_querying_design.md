# Graph Querying – Design Overview

This document defines the design and responsibilities of graph querying tooling in `iwtc-tools`.

Graph querying operates on graph artifacts (nodes + edges) derived from canonical indexes. It answers questions by treating edges as grammatical statements (subject–predicate–object) and combining them into structured chains of evidence.

The corresponding execution notebook is:
- `notebooks/IWTC_Graph_Querying.ipynb`

This document is the conceptual contract for how grammatical edge statements are composed to support DM-driven exploration of indexed world structure. The notebook implements this design.


---

## Purpose and scope

Graph querying supports DM-driven exploration of indexed world structure using graph traversal and weighted relationships.

The key value-add over index querying is traversal:
- multi-hop relationships ("Victor -> Party -> Bre")
- reverse traversal ("follow an edge backwards")
- weighted strength ("how strongly connected?")

Graph querying does not interpret narrative truth. It produces evidence-based structural signals and makes the traversal steps visible so a DM can judge meaning.

---

## Querying workflow

1. A human selects a world repository and graph version.
2. The notebook loads canonical graph artifacts (nodes + edges) as DataFrames.
3. The notebook constructs an in-memory graph (networkx) for traversal.
4. The notebook defines traversal primitives (stable building blocks).
5. The notebook provides query recipes that combine primitives.
6. The human edits parameters and runs recipes to explore structure.

Recipes explicitly label:
- hop count (1-hop, 2-hop, 3-hop)
- directionality (forward vs reverse predicate traversal)
- use of weights (direct weight vs aggregated scoring)

---

## Assumptions

- Graph artifacts were generated from canonical index artifacts and are reproducible.
- Node IDs are stable identifiers (e.g., "person_victor", "chunk_169784", "file:_local/...").
- Edge predicates define the graph grammar and are traversable in both directions when useful.
- Weights represent frequency (e.g., shared chunk count), not narrative importance.

Graph querying is evidence-first: any "connection strength" is a heuristic built from edge structure and weights, surfaced transparently to the DM.

---

## Inputs

Graph querying operates on a previously constructed graph representation of the indexed world.

Required:

- A stable set of graph nodes representing world objects (entities, chunks, files, vocabulary, etc.)
- A stable set of graph edges expressing relationships as subject–predicate–object statements, with optional weights

Optional:

- Canonical index tables and vocabulary artifacts may be loaded to enrich display, expand labels, or provide contextual summaries, but they are not required for grammatical traversal itself.

Graph querying assumes that the graph artifacts were generated from a single, explicit index version and reflect the evidence-first structure of those indexes.


---

## Outputs

Graph querying produces in-memory analytical results only, such as:
- ranked lists of related entities
- path explanations (the actual hops taken)
- subgraphs ("Victor neighborhood within 2 hops")
- overlap summaries (shared neighbors, shared chunks)
- context pointers (chunk IDs and file/line commands for inspection)

No files are written by default. Any export is explicit and optional.

---

## Core recipe: "How well does Victor likely know Bre?"

This recipe estimates structural familiarity using multiple signals:

A) Direct co-occurrence signal (1-hop, weighted)
- If an edge exists: "person_victor cooccurs_with person_bre"
- Use `weight` as the primary strength signal.

B) Shared context signal (2-hop, weighted via neighbors)
- Shared neighbors in the entity co-occurrence graph:
  - entities that co-occur with both Victor and Bre
  - optionally weighted by neighbor edge weights
- Report top shared neighbors and their contributions.

C) Social-group proxy signal (multi-hop, unweighted or lightly weighted)
- If Victor and Bre never share a chunk, they can still be structurally "close" by:
  - co-occurring with the same group entities (e.g., "org_party", factions)
  - or being connected through strong intermediaries (Aren, Henry, etc.)
- This is computed as best short paths and shared high-strength intermediates.

The recipe returns:
- a combined score (transparent components, not a single opaque number)
- an explanation table of the strongest paths/signals
- explicit notes when reverse traversal or multi-hop was required.

---

## Learning goals surfaced by the notebook

Every recipe callout includes:
- "Hops used: N"
- "Reverse traversal used: yes/no"
- "Weight used: yes/no"
- "Why this is needed" (one sentence, DM-readable)

The notebook is designed to teach graph thinking by making traversal structure visible.
