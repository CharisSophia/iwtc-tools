# lib/statblock_loader.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import json
from ruamel.yaml import YAML

_yaml = YAML(typ="safe")

# Import your validator (from earlier)
from lib.statblock_schema import validate_statblock

# Optional centralized paths (use lib.paths if you created it)
try:
    from lib.paths import DATA, ROOT
    DATA_DIR = DATA
except Exception:
    DATA_DIR = Path.home() / "iwtc-lab" / "data"

SEARCH_ORDER = [
    DATA_DIR / "homebrew",   # YAML (editable)
    DATA_DIR / "licensed",   # JSON (read-only)
    DATA_DIR / "srd",        # JSON (read-only)
]

def _find_file(monster: str) -> Optional[Path]:
    slug = monster.strip().lower().replace(" ", "-")
    for base in SEARCH_ORDER:
        for ext in (".yaml", ".yml", ".json"):
            p = base / "monsters" / f"{slug}{ext}"
            if p.exists():
                return p
    return None

def _load_any(path: Path) -> Dict[str, Any]:
    if path.suffix.lower() in (".yaml", ".yml"):
        return _yaml.load(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")

def _normalize_to_v1(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize arbitrary SRD/JSON formats into your statblock.v1 schema.
    If input already matches v1 (your YAML), this should be a no-op.
    Extend this mapping as needed for your chosen SRD JSON source.
    """
    # Fast path: looks like it's already v1 (your YAML shape)
    if "actions" in doc and isinstance(doc.get("hp"), dict) and "abilities" in doc:
        return doc

    # Example mapping for a typical SRD JSON (adjust keys to your chosen source)
    # Expected common JSON keys: name, size, type, alignment, armor_class, hit_points, hit_dice, speed{...},
    # abilities as STR/DEX..., prof_bonus, actions list with attack/damage breakdown.
    v1: Dict[str, Any] = {}
    v1["name"] = doc.get("name")
    v1["size"] = doc.get("size")
    v1["type"] = doc.get("type")
    v1["alignment"] = doc.get("alignment") or "unaligned"
    # AC: many JSON sources use armor_class (int or list). Simplify to int.
    ac = doc.get("ac", doc.get("armor_class"))
    if isinstance(ac, list) and ac:
        ac = ac[0].get("value", ac[0])
    v1["ac"] = int(ac) if isinstance(ac, (int, str)) else 10
    # HP
    v1["hp"] = {
        "formula": doc.get("hp", {}).get("formula") or doc.get("hit_dice") or "1d8",
        "average": doc.get("hp", {}).get("average") or doc.get("hit_points")
    }
    # Speed
    speed = doc.get("speed", {})
    if isinstance(speed, dict):
        v1["speed"] = {k: int(v) for k, v in speed.items() if isinstance(v, (int, float, str)) and str(v).isdigit()}
    else:
        v1["speed"] = {"walk": 30}
    # Abilities
    abilities = doc.get("abilities") or {
        "str": doc.get("strength", 10),
        "dex": doc.get("dexterity", 10),
        "con": doc.get("constitution", 10),
        "int": doc.get("intelligence", 10),
        "wis": doc.get("wisdom", 10),
        "cha": doc.get("charisma", 10),
    }
    v1["abilities"] = {k.lower(): int(v) for k, v in abilities.items()}
    # Proficiency
    v1["proficiency_bonus"] = int(doc.get("proficiency_bonus", 2))
    # Optional maps
    v1["skills"] = doc.get("skills") or {}
    v1["saves"]  = doc.get("saving_throws", doc.get("saves", {})) or {}
    v1["senses"] = doc.get("senses", {})
    v1["languages"] = doc.get("languages", []) or []
    v1["challenge"] = str(doc.get("challenge", doc.get("challenge_rating", ""))) or None

    # Actions → normalize attacks
    v1_actions = []
    for a in doc.get("actions", []):
        entry = {"name": a.get("name"), "type": "action"}
        atk = a.get("attack") or a.get("attack_bonus")
        dmg = a.get("damage") or a.get("damage_roll") or a.get("damage_dice")
        # Heuristic: if there is an attack bonus or damage dice, treat as attack
        if atk is not None or dmg is not None:
            entry["type"] = "attack"
            attack_block: Dict[str, Any] = {"to_hit": None, "damage": []}
            # to_hit
            if isinstance(atk, dict) and "to_hit" in atk:
                attack_block["to_hit"] = int(str(atk["to_hit"]).replace("+",""))
            else:
                # JSON often stores attack_bonus as a number
                ab = a.get("attack_bonus")
                if ab is not None:
                    attack_block["to_hit"] = int(ab)
            # damage lines
            if isinstance(dmg, list):
                for d in dmg:
                    dice = d.get("damage_dice") or d.get("formula") or d.get("dice")
                    dtype = d.get("damage_type") or d.get("type") or "bludgeoning"
                    if isinstance(dtype, dict):
                        dtype = dtype.get("name", "bludgeoning")
                    if dice:
                        attack_block.setdefault("damage", []).append({"type": str(dtype), "formula": str(dice)})
            elif isinstance(dmg, str):
                attack_block["damage"] = [{"type": "bludgeoning", "formula": dmg}]
            entry["attack"] = attack_block
        # Optional text
        if "desc" in a and "text" not in entry:
            entry["text"] = a["desc"]
        v1_actions.append(entry)

    v1["actions"] = v1_actions
    # Traits/reactions/legendary
    v1["traits"] = [{"name": t.get("name"), "text": t.get("desc","")} for t in doc.get("special_abilities", [])]
    v1["reactions"] = [{"name": r.get("name"), "text": r.get("desc","")} for r in doc.get("reactions", [])]
    v1["legendary_actions"] = [{"name": l.get("name"), "text": l.get("desc","")} for l in doc.get("legendary_actions", [])]
    # Provenance (optional)
    v1["source"] = doc.get("source") or "SRD"
    v1["schema_version"] = "statblock.v1"
    return v1

def load_statblock(monster: str) -> Tuple[Dict[str, Any], Path]:
    path = _find_file(monster)
    if not path:
        raise FileNotFoundError(f"Statblock not found for '{monster}' in {', '.join(str(p) for p in SEARCH_ORDER)}")
    raw = _load_any(path)
    norm = _normalize_to_v1(raw)
    errs = validate_statblock(norm)
    if errs:
        raise ValueError(f"{path.name} invalid:\n- " + "\n- ".join(errs))
    return norm, path

def save_homebrew(monster_slug: str, data_v1: Dict[str, Any]) -> Path:
    """Write only under homebrew. Raises if target would be SRD or licensed."""
    target = DATA_DIR / "homebrew" / "monsters" / f"{monster_slug}.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    # Validate before writing
    errs = validate_statblock(data_v1)
    if errs:
        raise ValueError("Refusing to write invalid statblock:\n- " + "\n- ".join(errs))
    _yaml.dump(data_v1, target.open("w", encoding="utf-8"))
    return target
