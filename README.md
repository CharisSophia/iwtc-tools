# IWTC Lab

Local Jupyter-based development environment for **Iron Wolf Trading Company** tools.

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

Launch command:
```bash
/usr/local/opt/python@3.11/bin/python3.11 -W ignore -m jupyter lab
