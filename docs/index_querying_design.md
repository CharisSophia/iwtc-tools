# Index Querying – Design Overview

This document defines the design, scope, and responsibilities of the index querying tooling implemented in `iwtc-tools`. It exists to capture intent and constraints separately from executable notebooks.

The corresponding execution notebook is:
- `notebooks/IWTC_Index_Querying.ipynb`

Readers should treat this document as the conceptual contract for the querying workflow. The notebook implements this design.

---

## Purpose and scope

This tooling supports querying previously generated **draft index artifacts (V0)** for a campaign world.

It operates strictly on machine-generated index CSV artifacts produced by:

- `IWTC_Raw_Source_Indexing.ipynb`

This notebook does not perform indexing.  
It does not modify canonical materials.  
It does not interpret narrative significance.

Its purpose is to allow a dungeon master or editor to ask structured questions of the index data, such as:

- Where does entity X appear?
- What entities appear in file Y?
- What chunks are associated with player Z?
- What entities co-occur with entity X?

The querying workflow is read-only and deterministic.  
It performs no write operations and produces no canonical outputs.

---

## Inputs and assumptions

### Required inputs

Querying operates on previously generated index artifacts stored under the world repository’s configured `indexes.path`.

At minimum, the following artifacts must exist:

- `index_entity_to_chunks_vN.csv`
- `index_chunk_to_entities_vN.csv`
- `index_player_to_chunks_vN.csv`
- `index_source_files_vN.csv`

The version suffix (`vN`) must match the version specified in the notebook parameters.

### Optional inputs

The following vocabulary artifacts may be present:

- `vocab_entities.csv`
- `vocab_aliases.csv`
- `vocab_author_aliases.csv`
- `vocab_map_player_character.csv`

Vocabulary files are human-authored and may evolve over time.  
Querying tolerates schema variation through semantic column mapping.

### Assumptions

- Index artifacts were generated from raw sources using the indexing notebook.
- Index artifacts are reproducible and not manually edited.
- Vocabulary files are human-maintained and may contain additional columns.
- Query results reflect index evidence only; they do not interpret narrative meaning.

---

## Querying outputs

This notebook produces in-memory query results only.

Outputs may include:

- Sets of chunk IDs
- Lists of entity IDs
- Filtered dataframe views of index tables
- Sorted and formatted views for inspection

No files are written.
No draft indexes are modified.
No curated indexes are produced.

The notebook is an analytical tool, not a publishing tool.

---

## Querying workflow overview

The querying workflow is DM-driven and interactive.

1. A human selects a world repository and index version.
2. The notebook loads and validates required index artifacts.
3. The notebook loads vocabulary tables (entities required, others optional).
4. The notebook defines query primitives (building blocks).
5. The notebook combines primitives into practical query patterns.
6. The human runs interactive queries to explore indexed material.

The querying model is compositional:

- Primitive functions return IDs or filtered index rows.
- Higher-level patterns combine primitives to answer practical questions.
- The user may inspect intermediate results to refine exploration.

---

## Boundaries and non-goals

This tooling does not:

- Re-index raw sources
- Modify index artifacts
- Interpret ambiguous names
- Resolve narrative contradictions
- Infer chronology beyond what indexes provide
- Write new artifacts to disk

All querying is evidence-based and limited to what the draft indexes contain.

---

## Iteration model

Querying is typically iterative and exploratory.

A dungeon master may:

- Refine vocabulary files
- Regenerate index artifacts
- Re-run the querying notebook
- Compare results across index versions

Over time, additional query patterns may be added to the notebook, but the foundational contract remains:

**Querying is read-only, index-based, and world-configured.**
