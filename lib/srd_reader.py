# lib/srd_reader.py
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional, List
import json
import os
import re

# Project root resolution: ENV override → default ~/iwtc-lab
IWTC_ROOT = Path(os.environ.get("IWTC_ROOT", Path.home() / "iwtc-lab"))

SRD_DIRS = [
    IWTC_ROOT / "data" / "srd" / "2024",
    IWTC_ROOT / "data" / "srd" / "2014",
]

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def _find_monsters_files() -> List[Path]:
    files: List[Path] = []
    for d in SRD_DIRS:
        if d.exists():
            for p in sorted(d.glob("*.json")):
                if re.search(r"monster", p.name, re.IGNORECASE):
                    files.append(p)
    return files

def _by_name_casefold(name: str, arr: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    n = name.casefold()
    for x in arr:
        if isinstance(x, dict) and x.get("name", "").casefold() == n:
            return x
    return None

def load_monster_raw(name: str) -> Dict[str, Any]:
    """
    Returns the raw JSON object for a monster from SRD (search 2024 then 2014).
    Raises FileNotFoundError if not found anywhere.
    """
    files = _find_monsters_files()
    for f in files:
        data = _load_json(f)
        # 5e-bits/5e-database uses an array of dicts for monsters resources.
        if isinstance(data, list):
            hit = _by_name_casefold(name, data)
            if hit:
                hit["_source_file"] = f  # provenance
                return hit
        # Some datasets use {"results":[...]}
        if isinstance(data, dict) and "results" in data and isinstance(data["results"], list):
            hit = _by_name_casefold(name, data["results"])
            if hit:
                hit["_source_file"] = f
                return hit
    raise FileNotFoundError(f"Monster '{name}' not found in SRD monsters JSON: {files}")

def _stat(d: Dict[str, Any], k: str, fallback: int = 10) -> int:
    v = d.get(k) or d.get(k.upper()) or d.get(k.capitalize())
    try:
        return int(v)
    except Exception:
        return fallback

def _ability_mod(score: int) -> int:
    return (score - 10) // 2

def _first_attack_action(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Heuristic: pick the first 'actions' entry that looks like a weapon attack.
    We accept entries with 'attack_bonus' or 'damage_dice' / 'damage' present.
    """
    actions = raw.get("actions") or []
    for a in actions:
        if not isinstance(a, dict):
            continue
        if any(k in a for k in ("attack_bonus", "damage_dice", "damage")):
            return a
    return None

def _extract_damage_formulas(a: Dict[str, Any]) -> List[str]:
    """
    Produce a list of damage dice strings like ["1d6+2", "2d6"] from common SRD shapes.
    We favor explicit dice strings; if not present, return empty list.
    """
    out: List[str] = []
    # Common fields
    if isinstance(a.get("damage_dice"), str):
        out.append(a["damage_dice"])
    # Some datasets use a list of damage objects with dice/type/bonus
    dmg = a.get("damage")
    if isinstance(dmg, list):
        for d in dmg:
            # strings or dicts with damage_dice / damage_bonus
            if isinstance(d, str):
                # last-ditch: extract NdM(+K) by regex
                m = re.search(r"\b\d+d\d+(?:\s*[+\-]\s*\d+)?\b", d)
                if m:
                    out.append(m.group(0).replace(" ", ""))
            elif isinstance(d, dict):
                dice = d.get("damage_dice") or d.get("dice") or d.get("damage_roll")
                bonus = d.get("damage_bonus")
                if isinstance(dice, str):
                    s = dice
                    if isinstance(bonus, int) and bonus != 0:
                        s = f"{s}{'+' if bonus>0 else ''}{bonus}"
                    out.append(s)
    # Last fallback: try to parse from desc text (not perfect, but helpful)
    if not out and isinstance(a.get("desc"), str):
        for m in re.finditer(r"\b\d+d\d+(?:\s*[+\-]\s*\d+)?\b", a["desc"]):
            out.append(m.group(0).replace(" ", ""))
    # Deduplicate but keep order
    seen = set()
    uniq = []
    for s in out:
        if s not in seen:
            uniq.append(s)
            seen.add(s)
    return uniq

def normalize_minimal(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize just enough fields for rolling:
      - name
      - abilities (str,dex,con,int,wis,cha)
      - saving_throws map if present
      - proficiency bonus (best-effort, default 2)
      - one attack (to_hit, damage formulas list)
    """
    out: Dict[str, Any] = {}
    out["name"] = raw.get("name", "Unknown")
    # Abilities
    out["abilities"] = {
        "str": _stat(raw, "strength", 10),
        "dex": _stat(raw, "dexterity", 10),
        "con": _stat(raw, "constitution", 10),
        "int": _stat(raw, "intelligence", 10),
        "wis": _stat(raw, "wisdom", 10),
        "cha": _stat(raw, "charisma", 10),
    }
    # Proficiency bonus (various keys in the wild)
    pb = raw.get("proficiency_bonus") or raw.get("prof_bonus") or raw.get("proficiency") or 2
    try:
        out["proficiency_bonus"] = int(pb)
    except Exception:
        out["proficiency_bonus"] = 2

    # Saving throws (many shapes; normalize keys to str/dex/...)
    saves = raw.get("saving_throws") or raw.get("saves") or {}
    norm_saves = {}
    if isinstance(saves, dict):
        for k, v in saves.items():
            kk = k.strip().lower()[:3]  # "strength" -> "str"
            try:
                norm_saves[kk] = int(v)
            except Exception:
                pass
    out["saving_throws"] = norm_saves

    # One attack
    a = _first_attack_action(raw) or {}
    to_hit = a.get("attack_bonus")
    try:
        to_hit = int(to_hit) if to_hit is not None else None
    except Exception:
        to_hit = None
    dmg_list = _extract_damage_formulas(a)

    out["attack"] = {
        "name": a.get("name", "Attack"),
        "to_hit": to_hit,                 # may be None; adapter can compute fallback
        "damage": dmg_list               # list of dice strings
    }

    # provenance
    src = raw.get("_source_file")
    if src:
        out["_source_file"] = str(Path(src))
    return out
