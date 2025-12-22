# IWTC-Lab  
*Iron Wolf Trading Company – Systems Sandbox*

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-OGL%201.0a%20%7C%20MIT-green.svg)](../LICENSE_OGL.html)  
[![Jupyter](https://img.shields.io/badge/Environment-Jupyter%20Lab-orange.svg)](https://jupyter.org/)

---

### Overview
**IWTC-Lab** is a self-contained Python 3.11 and Jupyter Lab environment for tabletop-RPG systems analysis, automation, and data integration.  
It provides a foundation for managing SRD and homebrew content, simulating game mechanics, and testing future AI-assisted storytelling tools.

---

### Core Capabilities
- **Reproducible Environment:**  
  Virtual environment with Jupyter Lab kernel and automated bootstrap.
- **Dice Engine:**  
  `lib.dice` supports complex expressions (`4d6kh3`, `2d8+1d4+3`), advantage/disadvantage, and detailed roll traces.
- **SRD Integration:**  
  `lib.srd_reader` imports and normalizes 2014/2024 SRD monster data from the MIT-licensed 5e-bits database with OGL compliance.
- **Rolling Framework:**  
  `lib.roll_adapter` connects statblocks to roll logic for ability saves and attacks, producing clear, auditable results.
- **Demonstration Notebook:**  
  `IWTC_Tools_Demo.ipynb` showcases end-to-end flow:
  > Bootstrap → Dice → SRD Reader → Roll Adapter → Summary

---

### Technical Highlights
- Project-root import management via `IWTC_ROOT` for portable development.  
- Provenance tracking in `_meta.yaml` (source, commit, license, timestamp).  
- Modular library design prepared for validation, YAML editing, and homebrew expansion.  
- Clean Markdown documentation and Jupyter navigation with anchor links.

---

### Next Steps
- Define and implement **`statblock.v1` JSON Schema** for validation.  
- Add **Homebrew YAML loader** for editable, local content.  
- Introduce **roll logging** for session summaries.  
- Begin development of an **IWTC Agent** for intelligent data and rules queries.

---

### Current Status
> ✅ SRD → Normalized Statblock → Rolling pipeline fully operational.  
> Architecture stable; ready for validation, homebrew, and automation layers.

---

**Author:** Charis Sophia  
**Repository:** [github.com/CharisSophia/iwtc-lab](https://github.com/CharisSophia/iwtc-lab)

