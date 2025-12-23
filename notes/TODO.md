# IWTC – Working To-Do Queue

This is the active, unblocked task list across **iwtc-tools**, **iwtc-world**, and **bryncross-world**.

---

## Repository Hygiene & Baseline

- Add / finalize README.md for `iwtc-world`
- Add `.gitkeep` (or README stubs) for `_meta/indexes/` and `_meta/docs/`
- Sanity-check `.gitignore` in all three repos
- Commit world repo structural baseline
- Commit tools repo config skeleton

---

## Tool Configuration

- Create `configs/worlds/example.yaml` in `iwtc-tools`
- Create local (untracked) `configs/worlds/iwtc.yaml`
- Create local (untracked) `configs/worlds/bryncross.yaml`
- Decide naming / placement for index outputs

---

## Environment and Notebook Maintenance

- Set up / rebuild the `iwtc-tools` virtual environment (`.venv`)
- Ensure JupyterLab and `ipykernel` are installed in the venv
- Register a stable Jupyter kernel for `iwtc-tools`
  - e.g. “IWTC Tools (py3.11)”
- Refactor existing notebooks to reflect the repo rename  
  (`iwtc-lab` → `iwtc-tools`)
- Refactor notebooks to support multi-world configuration
- Update `IWTC_Tools_Setup.ipynb` to include:
  - `jq` installation via Homebrew
  - `jq --version` verification
  - (optional) example JSON sanity check

---

## Indexing Design (Evidence-First)

- Decide first indexable folders in `iwtc-world`
- Define initial evidence document index JSON schema
- Complete PbP transcript entries in `document_index.json`
- First manual indexing dry run (read-only, no writes)
- Begin raw session notes indexing
  - apply “session × storyline = document” rule

---

## Architecture & Documentation

- Add minimal `ARCHITECTURE.md` to `iwtc-tools`
- Document evidence-first indexing philosophy
- Document document-unit rules (link to Document Units v1)

---

## World Structure Rationalization

- Rationalize world directory structures
  - Define IWTC as the structural standard
  - Map Bryncross’s medieval-themed names onto that standard
  - Account for Bryncross-specific content:
    - PC / NPC character records
    - Homebrewed monster statblocks
    - Fully built location data
  - Decide where flavor naming lives:
    - folder names vs metadata / aliases

---

## Notes

- Bryncross = best-case dataset (clean PbP, early structure)
- IWTC = worst-case dataset (long-running, messy capture)
- Tooling must work for both
