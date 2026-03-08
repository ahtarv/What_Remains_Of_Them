# core/gacha.py
import random
import json
import os

# ─── Rarity Configuration ────────────────────────────────────────────────────

RARITIES = {
    "SSR": {"base_rate": 0.03, "color": "bold magenta"},
    "SR":  {"base_rate": 0.12, "color": "bold yellow"},
    "R":   {"base_rate": 0.85, "color": "bold green"},
}

HARD_PITY      = 70
SOFT_PITY      = 58
SOFT_PITY_INC  = 0.06


# ─── Roster Loader ───────────────────────────────────────────────────────────

def load_roster() -> list:
    """Load character roster from data/roster.json"""
    base_dir     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    roster_path  = os.path.join(base_dir, "data", "roster.json")

    with open(roster_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["roster"]


# ─── Pity State ──────────────────────────────────────────────────────────────

class PityCounter:
    def __init__(self):
        self.pulls_since_ssr = 0
        self.pulls_since_sr  = 0

    def to_dict(self):
        return {
            "pulls_since_ssr": self.pulls_since_ssr,
            "pulls_since_sr":  self.pulls_since_sr,
        }

    def from_dict(self, data):
        self.pulls_since_ssr = data.get("pulls_since_ssr", 0)
        self.pulls_since_sr  = data.get("pulls_since_sr",  0)

    def display(self):
        """Returns a dict of pity info for the UI to display."""
        return {
            "pulls_since_ssr":    self.pulls_since_ssr,
            "pulls_since_sr":     self.pulls_since_sr,
            "ssr_guaranteed_in":  HARD_PITY - self.pulls_since_ssr,
            "sr_guaranteed_in":   10 - (self.pulls_since_sr % 10),
            "soft_pity_active":   self.pulls_since_ssr >= SOFT_PITY,
            "soft_pity_in":       max(0, SOFT_PITY - self.pulls_since_ssr),
        }


# ─── Core Pull Logic ─────────────────────────────────────────────────────────

def _get_ssr_rate(pulls_since_ssr: int) -> float:
    """Returns current SSR rate accounting for soft pity."""
    if pulls_since_ssr >= HARD_PITY - 1:
        return 1.0
    if pulls_since_ssr >= SOFT_PITY:
        bonus = (pulls_since_ssr - SOFT_PITY + 1) * SOFT_PITY_INC
        return min(RARITIES["SSR"]["base_rate"] + bonus, 1.0)
    return RARITIES["SSR"]["base_rate"]


def _roll_rarity(pity: PityCounter) -> str:
    """Roll a rarity tier based on current pity state."""
    ssr_rate = _get_ssr_rate(pity.pulls_since_ssr)
    sr_rate  = RARITIES["SR"]["base_rate"]

    roll = random.random()

    if roll < ssr_rate:
        return "SSR"
    elif roll < ssr_rate + sr_rate:
        return "SR"
    else:
        return "R"


def _update_pity(pity: PityCounter, rarity: str):
    """Update pity counters after a pull — SSR and SR track independently."""
    if rarity == "SSR":
        pity.pulls_since_ssr = 0
        # SR pity is NOT reset on SSR — they are independent
    elif rarity == "SR":
        pity.pulls_since_ssr += 1
        pity.pulls_since_sr  = 0
    else:
        pity.pulls_since_ssr += 1
        pity.pulls_since_sr  += 1


def _pick_entity(roster: list, rarity: str, exclude: list = []) -> dict:
    """Pick a random entity of given rarity, optionally excluding duplicates."""
    pool = [
        e for e in roster
        if e["rarity"] == rarity and e["id"] not in exclude
    ]
    # fallback to full pool if exclusions emptied it
    if not pool:
        pool = [e for e in roster if e["rarity"] == rarity]

    return random.choice(pool)


def single_pull(roster: list, pity: PityCounter) -> dict:
    """Perform a single pull. Returns result dict."""
    rarity = _roll_rarity(pity)
    _update_pity(pity, rarity)
    entity = _pick_entity(roster, rarity)

    return {
        "entity": entity,
        "rarity": rarity,
        "pity":   pity.display(),
    }


def ten_pull(roster: list, pity: PityCounter) -> list:
    """
    Perform 10 pulls.
    - Guarantees at least SR if no SR/SSR in first 9 pulls
    - No duplicate entities within the same 10 pull
    """
    results    = []
    seen_ids   = []

    for i in range(10):
        no_good_pull = all(r["rarity"] == "R" for r in results)

        if i == 9 and no_good_pull:
            # Force SR on 10th pull
            rarity = "SR"
            _update_pity(pity, rarity)
            entity = _pick_entity(roster, rarity, exclude=seen_ids)
        else:
            rarity = _roll_rarity(pity)
            _update_pity(pity, rarity)
            entity = _pick_entity(roster, rarity, exclude=seen_ids)

        seen_ids.append(entity["id"])
        results.append({
            "entity": entity,
            "rarity": rarity,
            "pity":   pity.display(),
        })

    return results


# ─── Quick Test ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    roster = load_roster()
    pity   = PityCounter()

    print("\n=== WHAT REMAINS OF THEM ===")
    print(f"Roster loaded: {len(roster)} entities\n")

    print("=== 10 PULL TEST ===")
    results = ten_pull(roster, pity)
    for r in results:
        star = {"SSR": "★★★★★", "SR": "★★★★☆", "R": "★★★☆☆"}[r["rarity"]]
        print(f"  {star}  {r['entity']['name']:<28} ({r['rarity']})")

    print(f"\n=== SCHOLAR'S JOURNAL ===")
    p = pity.display()
    print(f"  Pulls since last SSR : {p['pulls_since_ssr']}")
    print(f"  Pulls since last SR  : {p['pulls_since_sr']}")
    print(f"  SSR guaranteed in    : {p['ssr_guaranteed_in']} pulls")
    print(f"  SR guaranteed in     : {p['sr_guaranteed_in']} pulls")
    print(f"  Soft pity active     : {p['soft_pity_active']}")
    if not p['soft_pity_active']:
        print(f"  Soft pity starts in  : {p['soft_pity_in']} pulls")