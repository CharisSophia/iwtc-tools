# Raw Source Indexing – Design Overview

This document defines the design, scope, and responsibilities of the raw source indexing workflow implemented in `iwtc-tools`.

Raw source indexing translates unstructured campaign materials into structured, reproducible index tables. It performs structural extraction only. It does not interpret narrative meaning.

The corresponding execution notebook is:
- `notebooks/IWTC_Raw_Source_Indexing.ipynb`

Readers should treat this document as the conceptual contract for the indexing workflow. The notebook implements this design.

---

## Purpose and scope

This notebook indexes raw campaign source materials using an evidence-first model. It translates unstructured materials—session notes, transcripts, play-by-post logs, planning notes, and recollections—into structured draft index tables.

The workflow is parameterized per campaign world via explicit configuration. World-specific vocabulary and indexing semantics are defined in the world repository (e.g., under `_meta/`) and are not hard-coded into the tooling.

The outputs are reproducible draft indexes written to non-canonical locations. These drafts are intended for human review and curation before promotion to version-controlled canonical indexes.

This notebook does not modify curated indexes or canonical materials. It does not interpret narrative meaning or make editorial decisions. Human editors retain authority over inclusion, interpretation, and narrative significance.

---


## Indexing workflow overview

The indexing workflow is human-directed. Automation proposes structure; humans control scope, interpretation, and curation.

1. A human selects a world repository and supplies its configuration file.
2. A human specifies which source materials to index. If none are specified, the tooling enumerates configured source roots and requests explicit selection.
3. The tooling loads selected sources into a stable, line-addressable representation suitable for evidence citation.
4. The tooling proposes segment boundaries and candidate labels using conservative, evidence-first heuristics.
5. Each proposed boundary and label is accompanied by explicit source evidence.
6. The tooling emits draft index artifacts to non-canonical locations.
7. A human reviews and curates those drafts into canonical, version-controlled indexes.

### Optional vocabulary assistance

The tooling may optionally:

- Identify recurring candidate vocabulary not present in the current world vocabulary.
- Emit a structured vocabulary proposal file for human review.

Vocabulary proposals are always non-authoritative and require explicit human acceptance.

### Iteration model

Typical iteration consists of refining configuration and vocabulary files and rerunning the tooling to regenerate draft indexes.

Heuristic improvements in the tooling are part of tool development and do not alter the authority model: interpretation and publication remain human responsibilities.

---

## Assumptions

- Raw source materials are treated as authoritative records of play or planning, but may be incomplete, inconsistent, or internally contradictory.
- Chronology, session boundaries, and narrative continuity may be implicit rather than explicitly marked.
- Indexing is conservative and evidence-based. The tooling does not resolve ambiguities or impose narrative interpretation.
- Draft indexes require human review and curation before downstream use.
- Some sources may be excluded or only partially indexed; complete coverage is not assumed.
- The tooling fails fast on structural configuration errors, but degrades conservatively on content ambiguity.

---

## Inputs

The indexing process operates on raw campaign source materials, including:

- Session notes
- Auto-generated transcripts
- Play-by-post transcripts
- Planning notes
- Retrospective summaries

Inputs may vary in format and structure. The tooling assumes text-extractable sources; format-specific handling is an implementation detail, not a conceptual requirement.

An explicit world repository descriptor (e.g., under `_meta/`) defines:

- world root
- source discovery roots
- working drafts location
- canonical index location
- vocabulary files

The descriptor establishes the filesystem contract between the tooling and the world repository. All indexing behavior is constrained by what it declares.

---

## Indexing outputs

The indexing process produces draft indexes that describe the structure and contents of raw source materials in a machine-readable, evidence-linked form. These artifacts are scaffolding for human review and downstream tooling; they are not canonical references.

### Structural content

Draft indexes capture:

- Identification of indexed sources
- Segmentation into stable, addressable units
- Labels or classifications applied to those units
- Explicit evidence supporting each segmentation and label
- Signals of ambiguity where detected

### Design constraints

All draft indexes must:

- Remain reproducible from raw sources given the same descriptor configuration
- Preserve traceability back to underlying evidence
- Use explicit artifact versioning; schema or structural meaning changes require a version increment

The on-disk representation of draft indexes is an implementation detail and may evolve over time.
