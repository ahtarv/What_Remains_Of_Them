import random

RARITIES = {
    "SSR": {"base_rate": 0.03, "color": "bold magenta"}, #3%
    "SR": {"base_rate": 0.12, "color": "bold yellow"}, #10%
    "R": {"base_rate": 0.85, "color": "bold green"} #87%
}

#PITY config

HARD_PITY = 78 #guaranted SSR at this pull
SOFT_PITY =  58 #soft pity starts here, rate increases
SOFT_PITY_INC = 0.06 #rate increase per pull afet soft pity

#Pity state

class PityCounter:
    def __init__(self): 
        self.pulls_since_ssr = 0
        self.pulls_since_sr = 0

    def to_dict(self):
        return {
            "pulls_since_ssr": self.pulls_since_ssr,
            "pulls_since_sr": self.pulls_since_ssr
        }

    def from_dict(self, data):
        self.pulls_since_ssr = data.get("pulls_since_ssr", 0)
        self.pulls_since_sr = data.get("pulls_since_sr", 0)


#core pull logic

def _get_ssr_rate(pulls_since_ssr: int) -> float:
    """Returns current SSR rate accounting for soft pity."""
    if pulls_since_ssr >= HARD_PITY - 1:
        return 1.0  # hard pity — guaranteed
    if pulls_since_ssr >= SOFT_PITY:
        bonus = (pulls_since_ssr - SOFT_PITY + 1) * SOFT_PITY_INC
        return min(RARITIES["SSR"]["base_rate"] + bonus, 1.0)
    return RARITIES["SSR"]["base_rate"]

def _roll_rarity(pity: PityCounter) -> str:
    """Roll a rarity tier based on current pity state."""
    ssr_rate = _get_ssr_rate(pity.pulls_since_ssr)
    sr_rate = RARITIES["SR"]["base_rate"]

    roll = random.random()

    if roll < ssr_rate:
        return "SSR"
    elif roll < ssr_rate + sr_rate:
        return "SR"
    else:
        return "R"

def _update_pity(pity: PityCounter, rarity: str):
    """Update pity counters after a pull"""
    if rarity == "SSR":
        pity.pulls_since_ssr = 0
    elif rarity == "SR":
        pity.pulls_since_ssr += 1
        pity.pulls_since_sr = 0
    else:
        pity.pulls_since_ssr += 1
        pity.pulls_since_sr += 1

def single_pull(roster: list, pity: PityCounter) -> dict:
    """
    Perform a single pull.
    Returns a dict with the pulled entity and updated pity info
    """
    rarity = _roll_rarity(pity)
    _update_pity(pity, rarity)
    #FIlter roster by rarity and pick random entity
    pool = [e for e in roster if e["rarity"] == rarity]
    entity = random.choice(pool) if pool else {"name": "Unknown Entity", "rarity": rarity}

    return {
        "entity": entity,
        "rarity": rarity,
        "pity_ssr": pity.pulls_since_ssr,
        "pity_sr": pity.pulls_since_sr,
        "soft_pity_active": pity.pulls_since_ssr >= SOFT_PITY,
        "hard_pity_active": pity.pulls_since_ssr >= HARD_PITY - 1
    }

def ten_pull(roster: list, pity: PityCounter) -> list:
    """
    Perform a 10 - pull with SR guarantee on 10th if none in batc.
    Return list of 10 pull results
    """
    results = []

    for i in range(10):
        if i == 9 and all(r["rarity"] == "R" for r in results):
            rarity = "SR"
            _update_pity(pity, rarity)
            pool = [e for e in roster if e["rarity"] == rarity]
            entity = random.choice(pool) if pool else {"name": "Unknown Entity", "rarity": rarity}
            results.append({
                "entity": entity,
                "rarity": rarity,
                "pity_ssr": pity.pulls_since_ssr,
                "pity_sr": pity.pulls_since_sr,
                "soft_pity_active": pity.pulls_since_ssr >= SOFT_PITY,
                "hard_pity_active": pity.pulls_since_ssr >= HARD_PITY - 1
            })

        else:
            results.append(single_pull(roster, pity))
    return results

if __name__ == "__main__":
    # Dummy roster to test
    test_roster = [
        {"name": "The Ashen Widow",    "rarity": "SSR"},
        {"name": "Hollowed Sentinel",  "rarity": "SSR"},
        {"name": "The Pale Cartographer", "rarity": "SR"},
        {"name": "Ember Wraith",       "rarity": "SR"},
        {"name": "Fractured Shade",    "rarity": "R"},
        {"name": "Rot Pilgrim",        "rarity": "R"},
        {"name": "Nameless Soldier",   "rarity": "R"},
    ]

    pity = PityCounter()

    print("=== 10 PULL TEST ===")
    results = ten_pull(test_roster, pity)
    for r in results:
        star = {"SSR": "★★★★★", "SR": "★★★★☆", "R": "★★★☆☆"}[r["rarity"]]
        print(f"  {star} {r['entity']['name']} ({r['rarity']}) — pity: {r['pity_ssr']}")

    print(f"\n=== PITY STATUS ===")
    print(f"  Pulls since SSR : {pity.pulls_since_ssr}")
    print(f"  Pulls since SR  : {pity.pulls_since_sr}")
    print(f"  Soft pity active: {pity.pulls_since_ssr >= SOFT_PITY}")