# lib/roll_adapter.py (patched parts)
from __future__ import annotations
from typing import Dict, Any, List, Union
from lib.dice import roll

def ability_mod(score: int) -> int:
    return (score - 10) // 2

def _normalize_damage_list(dmg: Union[List[str], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Accepts either:
      - ["1d6+2", "2d6"] OR
      - [{"expr":"1d6+2","type":"slashing"}, ...]
    Returns a list of dicts with at least {"expr": "...", "type": ""}.
    """
    out: List[Dict[str, Any]] = []
    if not isinstance(dmg, list):
        return out
    for item in dmg:
        if isinstance(item, str):
            out.append({"expr": item, "type": ""})
        elif isinstance(item, dict):
            expr = item.get("expr") or item.get("dice") or item.get("damage_dice") or ""
            dtype = item.get("type") or item.get("damage_type") or ""
            # If the dict already uses "expr", keep it; if not, try "dice"/"damage_dice"
            if not expr and "expr" in item and isinstance(item["expr"], str):
                expr = item["expr"]
            if expr:
                out.append({"expr": expr, "type": dtype})
    return out

def roll_strength_save(mon: Dict[str, Any]) -> Dict[str, Any]:
    saves = mon.get("saving_throws", {})
    if "str" in saves:
        mod = int(saves["str"])
        detail = "STR save (explicit)"
    else:
        mod = ability_mod(int(mon["abilities"]["str"]))
        detail = "STR mod (default)"
    expr = f"1d20{mod:+d}"
    res = roll(expr)
    return {"expr": expr, "result": res, "modifier_detail": detail}

def pick_attack(mon: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns {'name', 'to_hit', 'damage': [{'expr','type'}, ...]}.
    If to_hit missing, compute max(STR, DEX) mod + proficiency as a fallback.
    """
    atk = mon.get("attack", {}) or {}
    name = atk.get("name", "Attack")
    to_hit = atk.get("to_hit")
    dmg_raw = atk.get("damage") or []
    dmg = _normalize_damage_list(dmg_raw)

    if to_hit is None:
        abil = mon.get("abilities", {})
        str_mod = ability_mod(int(abil.get("str", 10)))
        dex_mod = ability_mod(int(abil.get("dex", 10)))
        pb = int(mon.get("proficiency_bonus", 2))
        to_hit = max(str_mod, dex_mod) + pb

    return {"name": name, "to_hit": int(to_hit), "damage": dmg}

def roll_attack(atk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Rolls to-hit and each damage component.
    Returns:
      {'to_hit_expr','to_hit','damage': [{'expr','type','result'}...]}
    """
    to_hit_expr = f"1d20{atk['to_hit']:+d}"
    to_hit_res = roll(to_hit_expr)

    dmg_results = []
    for d in _normalize_damage_list(atk.get("damage", [])):
        dmg_results.append({
            "expr": d["expr"],
            "type": d.get("type", ""),
            "result": roll(d["expr"])
        })

    return {
        "to_hit_expr": to_hit_expr,
        "to_hit": to_hit_res,
        "damage": dmg_results
    }
