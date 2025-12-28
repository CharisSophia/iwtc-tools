# Raw Source Indexing – Design Overview

This document defines the design, scope, and responsibilities of the raw source indexing tooling implemented in `iwtc-tools`. It exists to capture intent and constraints separately from executable notebooks.

The corresponding execution notebook is:
- `notebooks/IWTC_Raw_Source_Indexing.ipynb`

Readers should treat this document as the conceptual contract for the indexing workflow. The notebook implements this design.

---

## Purpose and scope

This tooling supports indexing **raw source materials for a campaign world** using an evidence-first model. It generates **draft indexes** that segment and label unstructured source material, including raw session notes, auto-generated session transcripts, play-by-post transcripts, planning notes, and recollections, to support later human refinement and editorial use.

The tooling is parameterized by campaign world via explicit configuration supplied as an input. World-specific vocabulary, locations, arc cues, and related indexing semantics are defined in configuration files owned by the world repository (e.g., under `_meta/`), rather than being hard-coded into the tooling.

The outputs produced are work-in-progress draft indexes. They are reproducible and are written into ignored locations within the world file structure. These draft indexes are intended to be reviewed and curated by a human, producing curated indexes that are committed to the world repository and used by downstream tooling and agents.

This tooling does not modify any curated indexes or canonical materials tracked in version control. It has no authority to publish, interpret, or author in-world material. Decisions about inclusion, interpretation, and narrative significance remain the responsibility of human editors.

---

## Inputs and assumptions

### Inputs

The indexing process operates on raw source materials for a campaign world. Expected inputs include, but are not limited to:

- Raw session notes (e.g., longform narrative notes)
- Auto-generated session transcripts
- Play-by-post (PbP) transcripts
- Planning notes
- Recollections and retrospective summaries

Inputs may originate in different formats and levels of structure. Initial development assumes common text-based formats (e.g., Markdown, DOCX, or extracted plain text), with format-specific handling treated as an implementation detail rather than a conceptual constraint.

World-specific configuration is provided as an explicit input to the indexing process. Configuration files are owned by the world repository (e.g., under `_meta/`) and define vocabulary, locations, arc cues, source discovery roots, and other indexing semantics required to interpret the raw source materials in a world-aware manner.

### Assumptions

- Raw source materials are treated as authoritative records of play or planning, but may be incomplete, inconsistent, or internally contradictory.
- Chronology, session boundaries, and narrative continuity may be implicit rather than explicitly marked in the source material.
- Indexing decisions are evidence-based and conservative; the tooling does not attempt to resolve ambiguities or impose narrative interpretation.
- The generated draft indexes are expected to be reviewed, corrected, and refined by a human before any downstream use.
- Not all raw sources are assumed to be suitable for indexing; exclusion or partial indexing of inputs is an acceptable outcome.

---

## Indexing outputs

The indexing process produces **draft indexes** that describe the structure and contents of raw source materials in a machine-readable, evidence-linked form. Draft indexes are intended to support human refinement and downstream tooling; they are not themselves canonical references.

At a minimum, draft indexes capture:

- Identification of the indexed source material
- Segmentation of the source into indexable units
- Labels or classifications applied to each unit
- Explicit evidence references supporting each segmentation and label
- Indicators where ambiguity or uncertainty exists

Draft indexes may evolve in structure over time as heuristics and requirements mature. However, all draft indexes must remain traceable to the underlying raw sources and reproducible from those sources given the same configuration inputs.

The specific on-disk representation of draft indexes is an implementation detail and may change as the tooling evolves.

---

## Indexing workflow overview

The indexing workflow is human-directed. Automated steps propose structure and scaffolding; a human controls inputs, interpretation, and curation.

1. A human selects a world repository and provides an explicit world-specific configuration file as input.
2. A human provides a source file specification (paths and/or globs) identifying what to index. If no file specification is provided, the tooling lists candidate sources discovered under config-defined source roots and requests a human selection before proceeding.
3. The tooling loads and normalizes each selected input into a stable, line-addressable representation suitable for evidence citation.
4. The tooling proposes segment boundaries and candidate labels using conservative, evidence-first heuristics.
5. The tooling attaches explicit evidence to each proposed boundary and label.
6. The tooling emits work-in-progress draft indexes into ignored locations within the world file structure.
7. A human reviews, refines, and curates draft indexes outside the tooling, producing curated indexes committed to the world repository.

### Optional assistive behavior

The tooling may optionally assist with vocabulary maintenance:

- Identifying candidate vocabulary terms (e.g., proper nouns or recurring capitalized phrases) not present in the effective world vocabulary
- Emitting a lightweight vocabulary proposal file that mirrors the expected world vocabulary structure
- Writing such proposals to ignored locations for rapid human review

Vocabulary proposals are non-authoritative by design and may be partially accepted, modified, or discarded entirely by the human.

### Iteration model

For most users, iteration consists of updating world configuration and vocabulary files and rerunning the tooling to generate improved draft indexes for review and curation.

Over time, indexing heuristics implemented in code may also evolve to better support common source patterns and use cases. Such changes are part of tool development and are not assumed of world authors or editors.
