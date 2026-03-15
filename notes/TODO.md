# IWTC Tools – TODO & Roadmap

This file tracks structural and architectural work for the IWTC toolchain.

It is organized into:
- Active Work (in progress or next focus)
- V1 Enhancements (intentional future improvements)
- Longer-Term Architecture
- Completed Milestones (historical record)

---

Current system state: V0 indexing complete, graph and semantic layers operational.

---

# System Roadmap

Current phase: Graph exploration and evidence usability.

Next system capabilities:

- Investigation workflows built on graph traversal
- Evidence surfacing from graph queries
- Improved context metadata for chunks

Later roadmap:

- Temporal modeling
- Knowledge-state modeling
- Narrative reveal modeling

---

# Active Engineering Work

## Graph Query Layer

Goal: make graph artifacts usable for discovery and investigation.

- [ ] Expand IWTC_Graph_Querying.ipynb
- [ ] Implement traversal helpers
- [ ] Validate traversal correctness

### Investigation Workflows

Goal: support DM-style investigation queries that return explainable evidence chains.

- [ ] Implement path explanation queries
- [ ] Return supporting chunk/file evidence for graph traversals
- [ ] Prototype investigation-style queries (entity → evidence → session)

## Evidence Surface Improvements

- [ ] Add snippet-addressable metadata to chunk nodes
- [ ] Add relpath + line offsets to chunk exports
- [ ] Enable direct evidence display from queries

---

# Known Issues and Data Debt (log as discovered)

This section is for problems noticed during graph/query work that do not block V0 progress, but must be tracked so they do not get lost.

## Vocabulary coverage gaps
- [ ] Missing node records in vocab files cause graph nodes with empty attrs (example: player_amy; player_ana; player_delta; player_kaci).

## Graph integrity quirks
- [ ] MultiDiGraph multiplicity: clarify whether parallel edges ever exist in exports, or if edges are always aggregated.

## Evidence usability gaps
- [ ] Chunk nodes do not yet carry snippet-addressable metadata (e.g., relpath + start_line/end_line OR chunk_text). Needed for DM-friendly evidence outputs in Q2+.

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
- [ ] Support “state at time T” queries

## Knowledge Modeling

- [ ] Model "who could know X at time Y"
- [ ] Model player vs character knowledge separation
- [ ] Explore belief-state modeling for major reveals

---

# Architecture & Documentation

- [x] Create indexing_system_overview.md
- [ ] Document indexing philosophy (evidence-first model)
- [ ] Document graph design philosophy (node/edge semantics)
- [x] Cross-link design documents to system overview

---

# Repository Hygiene

- [ ] Add minimal README for each repo
- [ ] Standardize descriptor documentation
- [ ] Clean up legacy world structure assumptions

---

# Completed Milestones

## Environment & Setup

- [x] Rebuilt iwtc-tools virtual environment
- [x] Installed Jupyter + ipykernel in venv
- [x] Registered stable kernel
- [x] Refactored notebooks for multi-world configuration
- [x] Standardized descriptor-driven paths

## Evidence-First Indexing (V0)

- [x] Defined document index schema
- [x] Completed PbP transcript indexing
- [x] Indexed session notes
- [x] Generated:
  - index_chunk_to_entities_v0.csv
  - index_entity_to_chunks_v0.csv
  - index_player_to_chunks_v0.csv
  - index_source_files_v0.csv
- [x] Built IWTC_Index_Query_V0.ipynb

## Graph Indexing (V0)

- [x] Designed graph node schema
- [x] Designed graph edge schema
- [x] Built IWTC_Graph_Indexing.ipynb
- [x] Exported graph_nodes_v0.csv
- [x] Exported graph_edges_v0.csv
- [x] Validated graph integrity

## Semantic Indexing (V0)

- [x] Defined semantic relationship model
- [x] Built IWTC_Semantic_Indexing.ipynb
- [x] Exported graph_semantic_nodes_v0.csv
- [x] Exported graph_semantic_edges_v0.csv
- [x] Verified semantic graph integrity

---

# Guiding Principle

V0 focuses on structural clarity and reproducibility.

V1 adds semantic richness only after structural stability is proven.
