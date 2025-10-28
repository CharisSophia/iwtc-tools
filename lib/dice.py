"""
IWTC Dice Engine
- Supports NdM +/- K/D operators:
    3d6+2
    4d6kh3   (keep highest 3)
    4d6kl3   (keep lowest 3)
    4d6dh1   (drop highest 1)
    4d6dl1   (drop lowest 1)
- Advantage/Disadvantage helpers for d20 checks:
    roll_adv(5)  -> 1d20 with +5, take higher
    roll_dis(-1) -> 1d20 with -1, take lower
- Returns both a machine-friendly dict and a pretty string.
"""

from __future__ import annotations
import random, re
from dataclasses import dataclass
from typing import List, Literal, Tuple

# ---------- parsing ----------

DICE_RE = re.compile(
    r"""
    ^\s*
    (?P<n>\d*)d(?P<faces>\d+)            # e.g., 3d6  or d20
    (?:
        (?P<op>kh|kl|dh|dl) (?P<count>\d+)   # keep/drop highest/lowest
    )?
    (?P<mod>[+-]\d+)?                    # +2 or -1
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)

Selector = Literal["kh", "kl", "dh", "dl"]

@dataclass
class RollResult:
    expr: str                 # original expression (normalized)
    n: int                    # number of dice
    faces: int                # die faces
    rolls: List[int]          # raw rolls
    selected: List[int]       # kept dice after K/D rules
    dropped: List[int]        # dropped dice after K/D rules
    modifier: int             # +/- modifier
    subtotal: int             # sum(selected)
    total: int                # subtotal + modifier
    detail: str               # human-friendly detail string

def _apply_selector(rolls: List[int], sel: Selector | None, k: int | None) -> Tuple[List[int], List[int]]:
    if not sel or not k:
        return rolls[:], []
    indexed = list(enumerate(rolls))
    # Sort with indices to get deterministic drops when equal
    if sel in ("kh", "dh"):
        indexed.sort(key=lambda t: (t[1], t[0]), reverse=True)  # highest first
    else:
        indexed.sort(key=lambda t: (t[1], t[0]))                # lowest first
    if sel in ("kh", "kl"):
        keep = indexed[:k]
        drop = indexed[k:]
    else:  # dh/dl
        drop = indexed[:k]
        keep = indexed[k:]
    # Restore original ordering inside each list
    keep.sort(key=lambda t: t[0])
    drop.sort(key=lambda t: t[0])
    return [v for _, v in keep], [v for _, v in drop]

def parse(expr: str):
    m = DICE_RE.match(expr.strip())
    if not m:
        raise ValueError(f"Bad dice expression: {expr!r}")
    n = int(m.group("n") or 1)
    faces = int(m.group("faces"))
    sel = m.group("op")
    k = int(m.group("count")) if m.group("count") else None
    mod = int(m.group("mod") or 0)
    if n <= 0 or faces <= 0:
        raise ValueError("Dice count and faces must be positive.")
    if k is not None and (k < 0 or k > n):
        raise ValueError("Keep/Drop count must be between 0 and n.")
    return n, faces, sel, k, mod

# ---------- rolling ----------

def roll(expr: str, rng: random.Random | None = None) -> RollResult:
    """
    Roll an expression like '4d6kh3+2' or 'd20-1'.
    """
    n, faces, sel, k, mod = parse(expr)
    r = rng or random
    rolls = [r.randint(1, faces) for _ in range(n)]
    selected, dropped = _apply_selector(rolls, sel, k)
    subtotal = sum(selected) if selected else sum(rolls)
    total = subtotal + mod

    # Build a readable detail string
    parts = []
    if sel and k is not None:
        parts.append(f"{n}d{faces}{sel}{k}")
    else:
        parts.append(f"{n}d{faces}")
    if mod:
        parts.append(f"{mod:+d}")
    norm = "".join(parts)

    # format like: [4, 2, 6, 5] -> keep [6,5,4], drop [2]  +2  = 17
    rolls_str = f"{rolls}"
    kd_str = ""
    if dropped:
        kd_str = f" -> keep {selected} | drop {dropped}"
    elif selected and selected != rolls:
        kd_str = f" -> keep {selected}"
    mod_str = f" {mod:+d}" if mod else ""
    detail = f"{norm}: {rolls_str}{kd_str}{mod_str} = {total}"

    return RollResult(
        expr=norm,
        n=n,
        faces=faces,
        rolls=rolls,
        selected=selected if selected else rolls,
        dropped=dropped,
        modifier=mod,
        subtotal=subtotal,
        total=total,
        detail=detail,
    )

# ---------- d20 helpers ----------

def roll_adv(modifier: int = 0, rng: random.Random | None = None) -> RollResult:
    """1d20 with advantage; returns the kept die + modifier."""
    r = rng or random
    r1, r2 = r.randint(1, 20), r.randint(1, 20)
    kept = max(r1, r2)
    total = kept + modifier
    detail = f"1d20 adv: [{r1}, {r2}] -> keep {kept}{modifier:+d} = {total}"
    return RollResult(
        expr=f"1d20 (adv){modifier:+d}" if modifier else "1d20 (adv)",
        n=2, faces=20,
        rolls=[r1, r2],
        selected=[kept],
        dropped=[min(r1, r2)],
        modifier=modifier,
        subtotal=kept,
        total=total,
        detail=detail,
    )

def roll_dis(modifier: int = 0, rng: random.Random | None = None) -> RollResult:
    """1d20 with disadvantage; returns the kept die + modifier."""
    r = rng or random
    r1, r2 = r.randint(1, 20), r.randint(1, 20)
    kept = min(r1, r2)
    total = kept + modifier
    detail = f"1d20 dis: [{r1}, {r2}] -> keep {kept}{modifier:+d} = {total}"
    return RollResult(
        expr=f"1d20 (dis){modifier:+d}" if modifier else "1d20 (dis)",
        n=2, faces=20,
        rolls=[r1, r2],
        selected=[kept],
        dropped=[max(r1, r2)],
        modifier=modifier,
        subtotal=kept,
        total=total,
        detail=detail,
    )
