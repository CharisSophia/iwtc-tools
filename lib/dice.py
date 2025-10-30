# lib/dice.py
from __future__ import annotations
import random
import re
from dataclasses import dataclass
from typing import List, Tuple

_DICE_RE = re.compile(
    r"""
    (?P<sign>[-+]?)                      # optional leading sign
    (?:
        (?:
            (?P<count>\d+)?              # optional count (e.g., 4 in 4d6)
            d
            (?P<sides>\d+)               # sides (e.g., 6 in d6)
            (?P<keep>(?:k[hl]\d+)?)      # optional keep-high/keep-low (e.g., kh3, kl2)
        )
        |
        (?P<const>\d+)                   # or a plain constant
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

@dataclass
class Result:
    total: int
    detail: str

def _roll_one_die(sides: int) -> int:
    if sides <= 0:
        raise ValueError(f"Bad dice expression: die with {sides} sides")
    return random.randint(1, sides)

def _apply_keep(rolls: List[int], keep_spec: str) -> Tuple[List[int], List[int]]:
    """Return (kept, dropped) according to keep spec like 'kh3' or 'kl2'."""
    if not keep_spec:
        return rolls[:], []
    keep_spec = keep_spec.lower()
    m = re.match(r"k([hl])(\d+)", keep_spec)
    if not m:
        return rolls[:], []
    which, n_str = m.groups()
    n = int(n_str)
    if n <= 0:
        return [], rolls[:]
    indexed = list(enumerate(rolls))
    if which == "h":
        indexed.sort(key=lambda t: t[1], reverse=True)
    else:
        indexed.sort(key=lambda t: t[1])
    kept_idx = set(i for i, _ in indexed[:n])
    kept, dropped = [], []
    for i, val in enumerate(rolls):
        (kept if i in kept_idx else dropped).append(val)
    return kept, dropped

def _parse_terms(expr: str):
    expr = expr.strip().replace(" ", "")
    if not expr:
        raise ValueError("Bad dice expression: empty")
    terms = []
    pos = 0
    while pos < len(expr):
        m = _DICE_RE.match(expr, pos)
        if not m:
            # show a helpful slice near the error
            raise ValueError(f"Bad dice expression: '{expr[pos:pos+12]}'")
        sign = -1 if m.group("sign") == "-" else 1
        if m.group("const"):
            const = int(m.group("const"))
            terms.append(("const", sign, const, None, None))
        else:
            count = int(m.group("count")) if m.group("count") else 1
            sides = int(m.group("sides"))
            keep = m.group("keep") or ""
            terms.append(("dice", sign, count, sides, keep))
        pos = m.end()
    return terms

def roll(expr: str) -> Result:
    """
    Roll a composite dice expression like:
      '1d20+5', '2d8+1d4+3', '4d6kh3', '1d20-1', 'd20+2'
    Returns Result(total, detail).
    """
    terms = _parse_terms(expr)
    pieces = []
    running_total = 0

    for kind, sign, a, b, keep in terms:
        if kind == "const":
            val = sign * a
            running_total += val
            pieces.append(f"{'+' if sign>0 else '-'}{abs(a)}")
        else:
            count, sides = a, b
            rolls = [_roll_one_die(sides) for _ in range(count)]
            kept, dropped = _apply_keep(rolls, keep)
            subtotal = sum(kept if keep else rolls)
            subtotal *= sign

            # Build detail
            if keep:
                kept_str = ",".join(str(x) for x in kept) if kept else ""
                drop_str = ",".join(str(x) for x in dropped) if dropped else ""
                roll_str = f"[{kept_str}]" + (f"~[{drop_str}]" if drop_str else "")
            else:
                roll_str = "[" + ",".join(str(x) for x in rolls) + "]"

            op = "+" if sign > 0 else "-"
            term_str = f"{op}{count}d{sides}{keep or ''}{roll_str}"
            pieces.append(term_str)

            running_total += subtotal

    # Clean up leading '+' in detail
    detail = "".join(pieces)
    if detail.startswith("+"):
        detail = detail[1:]
    return Result(total=running_total, detail=detail)

def roll_adv(expr: str) -> Result:
    """Roll the entire expression twice and keep the higher total."""
    r1 = roll(expr)
    r2 = roll(expr)
    winner = r1 if r1.total >= r2.total else r2
    detail = f"adv({expr}): [{r1.detail}] vs [{r2.detail}] -> {winner.total}"
    return Result(total=winner.total, detail=detail)

def roll_dis(expr: str) -> Result:
    """Roll the entire expression twice and keep the lower total."""
    r1 = roll(expr)
    r2 = roll(expr)
    loser = r1 if r1.total <= r2.total else r2
    detail = f"dis({expr}): [{r1.detail}] vs [{r2.detail}] -> {loser.total}"
    return Result(total=loser.total, detail=detail)
