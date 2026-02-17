
# Index Querying – Design Overview

This document defines the design, scope, and responsibilities of the index querying tooling implemented in `iwtc-tools`. It defines how canonical index artifacts are loaded, validated, and composed for structured querying.

The corresponding execution notebook is:
- `notebooks/IWTC_Index_Querying.ipynb`

Readers should treat this document as the authoritative description of how querying operates over existing index artifacts. The notebook implements this design.

---

## Purpose and scope

This tooling supports querying previously generated index artifacts for a campaign world.

It operates only on:

- Canonical index CSV artifacts declared in the world repository descriptor
- Canonical vocabulary files declared in the same descriptor

This notebook does not perform indexing or modify canonical materials.  
It provides a read-only, deterministic interface for structured questions over indexed world data.

Example questions include:

- Where does entity X appear?
- What entities appear in file Y?
- What chunks are associated with player Z?
- What entities co-occur with entity X?

No write operations occur and no canonical outputs are produced.


---

## Querying workflow

The querying workflow is DM-driven and interactive.

1. A human selects a world repository and index version.
2. The notebook loads and validates required index artifacts.
3. The notebook loads vocabulary tables (entities required; others optional).
4. The notebook defines query primitives (stable building blocks).
5. The notebook exposes practical query recipes built from those primitives.
6. The human edits parameters and runs recipes to explore indexed material.

The preload and primitive sections are typically run without modification.  
Query recipes are intended to be edited during use.

Querying is exploratory and iterative. A dungeon master may refine vocabulary files, regenerate index artifacts, re-run the notebook, or compare results across index versions. The querying notebook itself remains read-only and deterministic across runs.

---

## Assumptions

- Index artifacts were generated from raw sources using the indexing notebook.
- Index artifacts are reproducible and not manually edited.
- Vocabulary files are human-maintained and may include additional columns.
- Query results reflect index evidence only and do not imply narrative interpretation.

This notebook is strictly read-only and operates only on existing index and vocabulary artifacts.

---

## Inputs

Querying operates on previously generated **index artifacts** stored under the world repository’s configured `indexes.path`.

### Required

- Canonical index tables describing:
  - entity-to-chunk mappings
  - chunk-to-entity mappings
  - player-to-chunk mappings (if applicable)
  - source file metadata

These artifacts must correspond to a single, explicit index version.

### Optional

- World vocabulary files declared in the repository descriptor
  - entity definitions
  - alias mappings
  - author mappings
  - player/character mappings

Vocabulary files are human-maintained and may evolve over time.  
Querying tolerates schema variation through semantic column mapping.

---

## Outputs

Querying produces **in-memory analytical results only**.

Typical outputs include:

- Identifiers (chunks, entities, players, files)
- Filtered or aggregated views of index tables
- Sorted or formatted representations for inspection

Results are ephemeral and exploratory.

Querying does not publish, mutate, or regenerate index artifacts.
It is an analytical layer over existing indexes, not a production workflow.
