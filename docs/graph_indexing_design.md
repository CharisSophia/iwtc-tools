# Graph indexing design (V0)

## What this is
This describes the first "graph build" notebook: `IWTC_Graph_Indexing_V0.ipynb`.

Its job is to take the existing V0 indexes and produce graph-ready artifacts a DM can use later for questions like:
- "Who is connected to what?"
- "What is central to this cluster of events?"
- "Who overlaps with whom, and where?"

This notebook is a build step. It does not answer questions directly.

## Scope (V0)
V0 produces graph artifacts from existing index tables:
- chunk -> entities
- entity -> chunks
- player -> chunks
- chunk -> file

V0 does NOT attempt:
- plotline detection
- timeline ordering beyond "in the same chunk/file"
- semantic disambiguation (e.g., "temple" meaning different things)
- visualization

Those belong in query notebooks or later versions.

## Inputs
V0 assumes you already ran the raw indexing notebook and have these artifacts under `indexes.path`:
- `index_chunk_to_entities_<v>.csv`
- `index_entity_to_chunks_<v>.csv`
- `index_player_to_chunks_<v>.csv`
- `index_source_files_<v>.csv`

Vocabulary tables (entities/aliases/authors/pc map) may exist and may be loaded, but graph build does not require them to function.

## Outputs
V0 writes graph-ready artifacts back under `indexes.path` (or a subfolder), versioned the same way as the indexes.

Minimum outputs:
- `graph_nodes_<v>.csv`
- `graph_edges_<v>.csv`

Optional outputs (not required for V0, but allowed later):
- a serialized graph file (e.g., pickle)

## Graph model (V0)
Nodes are identified by stable string IDs.
Recommended node IDs:
- entities: `person_henry`, `faction_hands`, etc. (whatever is already in the index)
- players: `player_crowe`, etc.
- chunks: `chunk_<chunk_id>`
- files: `file:<relpath>`

Edges are directed and typed. Minimal edge types:
- entity_in_chunk (entity -> chunk)
- player_in_chunk (player -> chunk)
- chunk_in_file (chunk -> file)

Co-occurrence edges (entity <-> entity) are intentionally NOT required in V0. They can be derived later from entity_in_chunk edges.

## Why this helps
Once nodes/edges exist, a query notebook can do things like:
- "neighbors of X"
- "top connections for X"
- "entities that bridge two clusters"
- "find overlap and pull source lines for context"

The build notebook keeps the artifacts consistent and reproducible.
