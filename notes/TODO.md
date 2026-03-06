# IWTC Tools – TODO & Roadmap

This file tracks structural and architectural work for the IWTC toolchain.

It is organized into:
- Active Work (in progress or next focus)
- V1 Enhancements (intentional future improvements)
- Longer-Term Architecture
- Completed Milestones (historical record)

---

# Active Work

## Graph Modeling (V0)

Goal: Export a clean graph representation from existing indexes (CSV only).

- [ ] Define node export schema (entity, chunk, file)
- [ ] Define edge export schema (entity→chunk, chunk→file, etc.)
- [ ] Build IWTC_Graph_Indexing.ipynb (bootstrap notebook)
- [ ] Export graph_nodes_v0.csv
- [ ] Export graph_edges_v0.csv
- [ ] Validate graph integrity (counts, no orphan edges)

---

## Known Issues and Data Debt (log as discovered)

This section is for problems noticed during graph/query work that do not block V0 progress, but must be tracked so they do not get lost.

### Vocabulary coverage gaps
- [ ] Missing node records in vocab files cause graph nodes with empty attrs (example: person_anthony; player_amy; player_ana; player_delta; player_kaci).

### Graph integrity quirks
- [ ] MultiDiGraph multiplicity: clarify whether parallel edges ever exist in exports, or if edges are always aggregated.

### Evidence usability gaps
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

- [ ] Create ARCHITECTURE.md (high-level system diagram)
- [ ] Document indexing philosophy (evidence-first model)
- [ ] Document graph design philosophy (node/edge semantics)

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

---

# Guiding Principle

V0 focuses on structural clarity and reproducibility.

V1 adds semantic richness only after structural stability is proven.
