# IWTC Tools – TODO & Roadmap

This file tracks structural and architectural work for the IWTC toolchain.

It is organized into:
- Active Work (in progress or next focus)
- V1 Enhancements (intentional future improvements)
- Longer-Term Architecture
- Completed Milestones (historical record)

---

Current system state: V0 indexing complete, graph and semantic layers operational. Incremental rebuild pipeline is operational for canonical indexes and graphs.

---

# System Roadmap

Current phase: Structural semantics complete; preparing narrative semantics.

Next system capabilities:

- Narrative semantics (path -> explanation)
- Investigation workflows built on semantic paths
- Evidence surfacing from graph queries

Later roadmap:

- Temporal modeling
- Knowledge-state modeling
- Narrative reveal modeling

---

# Active Engineering Work

## Narrative Semantics Bootstrap

Goal: begin modeling narrative structure beyond structural world relationships.

- [ ] Define first-pass narrative semantics scope
- [ ] Decide canonical artifact(s) for narrative semantics
- [ ] Parse session note headers for scene/date/location context
- [ ] Propagate header-derived context into chunk-level metadata
- [ ] Identify event-bearing chunk candidates
- [ ] Define minimal event / scene classification scheme
- [ ] Determine how narrative semantics should relate to evidence vs semantic graph layers

Notes:
- Start with session notes first; they carry the strongest explicit scene metadata
- Focus on date/location/scene context before richer event interpretation
- Do not yet attempt full narrative relationship modeling

---

### Investigation Workflows

Goal: support DM-style investigation queries that return explainable evidence chains.

- [ ] Implement path explanation queries
- [ ] Return supporting chunk/file evidence for graph traversals
- [ ] Prototype investigation-style queries (entity -> evidence -> session)

---

## Evidence Surface Improvements

- [ ] Add snippet-addressable metadata to chunk nodes
- [ ] Add relpath + line offsets to chunk exports
- [ ] Enable direct evidence display from queries

---

# Known Issues and Data Debt (log as discovered)

This section is for problems noticed during graph/query work that do not block V0 progress, but must be tracked so they do not get lost.

## Relationship coverage gaps
- [ ] Missing semantic relationships lead to incomplete or suboptimal path discovery (e.g., Victor <-> Evaine).
- [ ] Some entities rely on indirect or structural paths due to absent direct or narrative relationships.
- [ ] Relationship modeling is currently structural; narrative-level connections are not yet represented.

## Structural modeling limits
- [ ] Organizational and role modeling may still be incomplete or uneven across factions.
- [ ] Some relationship types (e.g., narrative events, shared history) are not yet represented.

## Evidence usability gaps
- [ ] Chunk nodes do not yet carry snippet-addressable metadata (e.g., relpath + start_line/end_line OR chunk_text). Needed for DM-friendly evidence outputs in Q2+.

## Incremental index updates
- [ ] Create a mapping to translate non-algorithmic indexes between chunk versions.
- [ ] Reformat Kavar notes, rechunk to new index version, map narrative index to new chunk ids.

---

# V1 Enhancements Backlog

These are intentionally deferred until V0 is stable.

## Context Enrichment

- [ ] Parse Markdown headers to capture session titles
- [ ] Capture location/section context per chunk
- [ ] Attach session number and/or date metadata
- [ ] Capture PbP timestamps where available
- [ ] Handle ambiguous vocabulary with could_refer_to

## Temporal Modeling

- [ ] Add ordering metadata (session sequence)
- [ ] Add time-aware graph modeling
- [ ] Support "state at time T" queries

## Knowledge Modeling

- [ ] Model "who could know X at time Y"
- [ ] Model player vs character knowledge separation
- [ ] Explore belief-state modeling for major reveals

---

# Architecture & Documentation

- [x] Create `indexing_system_overview.md` (v0.6)
- [ ] Document indexing philosophy (evidence-first model)
- [ ] Document graph design philosophy (node/edge semantics)
- [x] Cross-link design documents to system overview (v0.6)
- [ ] Document incremental rebuild notebook usage and phase contracts

---

# Repository Hygiene

- [ ] Add minimal README for each repo
- [ ] Standardize descriptor documentation
- [ ] Clean up legacy world structure assumptions

---

# Completed Milestones

## Environment & Setup

- [x] Rebuilt `iwtc-tools` virtual environment
- [x] Installed Jupyter + ipykernel in venv
- [x] Registered stable kernel
- [x] Refactored notebooks for multi-world configuration
- [x] Standardized descriptor-driven paths

## Evidence-First Indexing (V0)

- [x] Defined document index schema
- [x] Completed PbP transcript indexing
- [x] Indexed session notes
- [x] Generated:
  - `index_chunk_to_entities_v0.csv`
  - `index_entity_to_chunks_v0.csv`
  - `index_player_to_chunks_v0.csv`
  - `index_source_files_v0.csv`
- [x] Built `IWTC_Index_Query_V0.ipynb`

## Graph Indexing (V0)

- [x] Designed graph node schema
- [x] Designed graph edge schema
- [x] Built `IWTC_Graph_Indexing.ipynb`
- [x] Exported `graph_nodes_v0.csv`
- [x] Exported `graph_edges_v0.csv`
- [x] Validated graph integrity

## Semantic Indexing (V0)

- [x] Defined semantic relationship model (v0.6)
- [x] Built `IWTC_Semantic_Indexing.ipynb` (v0.6)
- [x] Exported `graph_semantic_nodes_v0.csv` (v0.6)
- [x] Exported `graph_semantic_edges_v0.csv` (v0.6)
- [x] Verified semantic graph integrity (v0.6)

## Structural Semantics (V0.7)

- [x] Integrated `world_relationships` into semantic graph (v0.7)
- [x] Implemented predicate system (reverse, class, cost) (v0.7)
- [x] Built path-based semantic querying (Q4) (v0.7)
- [x] Implemented cost-based path ranking (v0.7)
- [x] Added structural penalties (kinship, historical) (v0.7)
- [x] Modeled organizational structures (offices, roles, hierarchy) (v0.7)
- [x] Validated structural semantic behavior across scenarios (v0.7)

## Graph Query Layer

Goal: make graph artifacts usable for discovery and investigation.

- [x] Expand `IWTC_Graph_Querying.ipynb` (v0.7)
- [x] Validate traversal correctness (v0.7)

Notes:
- Traversal logic is currently embedded in Q4
- Helper functions will be extracted later if needed

## Incremental Rebuild Pipeline

- [x] Build `IWTC_Incremental_Rebuild.ipynb`
- [x] Implement descriptor/path resolution for canonical rebuilds
- [x] Implement timestamp-based change detection
- [x] Load and normalize canonical vocabulary tables
- [x] Add basic vocabulary consistency validation
- [x] Build canonical vocabulary lookup for entity linking
- [x] Rebuild source-derived indexes:
  - `index_source_files_v0.csv`
  - `index_chunk_to_entities_v0.csv`
  - `index_entity_to_chunks_v0.csv`
- [x] Rebuild evidence graph outputs:
  - `graph_evidence_nodes_v0.csv`
  - `graph_evidence_edges_v0.csv`
- [x] Rebuild semantic graph outputs:
  - `graph_semantic_nodes_v0.csv`
  - `graph_semantic_edges_v0.csv`
- [x] Standardize phase boundaries, logging, and cleanup behavior

---

# Guiding Principle

V0 focuses on structural clarity and reproducibility.

V1 adds semantic richness only after structural stability is proven.