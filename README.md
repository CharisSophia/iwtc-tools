# IWTC Lab

Local Jupyter-based development environment for **Iron Wolf Trading Company** tools.

> **Note:** Initial environment scaffolding and documentation produced collaboratively with ChatGPT (OpenAI GPT-5).

### Purpose
- Build and test IWTC automation (dice roller, encounter tracker, asset manager).
- Manage YAML/JSON statblock libraries.
- Maintain notebooks for data analysis and tool design.
- Record session logs and export summaries.

### Structure
iwtc-lab/
│
├── assets/ # images, tokens, maps (not tracked by git)
├── data/ # YAML/JSON for monsters, NPCs, encounters
├── lib/ # Python utility modules
├── notebooks/ # active Jupyter notebooks
├── sessions/ # exported combat logs and session notes
└── README.md


### Environment
- Python 3.11 (Homebrew)
- JupyterLab 4.x
- Optional virtualenv: `~/venvs/iwtc`

For full setup instructions, see `notebooks/IWTC_Lab_Setup.ipynb`.

Quick start:
```bash
/usr/local/opt/python@3.11/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m jupyter lab

Launch command:
```bash
/usr/local/opt/python@3.11/bin/python3.11 -W ignore -m jupyter lab```


### Data policy
- `data/homebrew/` — YAML; editable; saved by IWTC-Lab tools.
- `data/srd/` and `data/licensed/` — JSON; read-only; never modified by tools.
- All data are normalized in-memory to `statblock.v1` before use.


### Credits
Development and documentation assisted by ChatGPT (OpenAI GPT-5) as a collaborative coding partner.


### Licensing

This project includes content from the *Dungeons & Dragons* 5th Edition
System Reference Document (SRD 5.1), published by Wizards of the Coast, and
made available under the **Open Game License v1.0a**.

A full copy of the license is included in this repository as [LICENSE_OGL.pdf](LICENSE_OGL.pdf).

All SRD content is © Wizards of the Coast and used under OGL v1.0a.  
All original IWTC-Lab code and homebrew material © 2025 Charis Sophia.

