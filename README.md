# What Remains of Them

> *You are a scholar. You do not collect heroes. You collect what's left.*

A dark fantasy gacha roguelike for the terminal. Pure ASCII. No fan service. No energy systems. Just atmosphere, mechanics, and what remains.

---

## Preview

**Splash Screen**
```
╔══════════════════════════════════════════════╗
║                                              ║
║         W H A T   R E M A I N S             ║
║                  O F   T H E M              ║
║                                              ║
║         ·  ·  ·  ·  ·  ·  ·  ·  ·          ║
║                                              ║
║           You are a scholar.                 ║
║           You do not collect heroes.         ║
║           You collect what's left.           ║
║                                              ║
║         ·  ·  ·  ·  ·  ·  ·  ·  ·          ║
║                                              ║
║              v0.1 — early binding            ║
║                                              ║
╚══════════════════════════════════════════════╝
```

**Binding Result**
```
╔═══════════════  BINDING COMPLETE  ═══════════════╗
║    . · . · .                                     ║
║     ·  ___  ·                                    ║
║    · /. . .\ ·                                   ║
║     | ·   · |                                    ║
║     |   ~   |                                    ║
║    · \·····/ ·                                   ║
║    · /     \ ·                                   ║
║   · / · · · \ ·                                  ║
║     ·       ·                                    ║
║      · · · ·                                     ║
║                                                  ║
║   ★★★★☆  FRACTURED SHADE                         ║
║   A Memory With No Owner                         ║
║                                                  ║
║   The scholar's notes are unusually short for    ║
║ this entry. Just three words: 'Do not linger.'   ║
║                                                  ║
║   RARITY: SR                                     ║
╚══════════════════════════════════════════════════╝
```

**Scholar's Journal (Pity Counter)**
```
╔════════════════ [ PITY COUNTER ] ════════════════╗
║                                                  ║
║   Binding attempts since last SSR :  1           ║
║   Binding attempts since last SR  :  1           ║
║                                                  ║
║   ────────────────────────────────               ║
║                                                  ║
║   SSR guaranteed in :  69 pulls                  ║
║   SR  guaranteed in :  9 pulls                   ║
║                                                  ║
║   ────────────────────────────────               ║
║                                                  ║
║   Soft pity :  begins in 57 pulls                ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

**Bound Entities (Collection)**
```
══════════════ BOUND ENTITIES ══════════════

 1.  ★★★★☆  Ember Wraith
 2.  ★★★★☆  The Fractured Judge
 3.  ★★★★☆  Rot Pilgrim
 4.  ★★★★☆  Fractured Shade
 5.  ★★★☆☆  Last Hymn                     x2
 6.  ★★★☆☆  The Mute Herald
 7.  ★★★☆☆  Greymantle
 8.  ★★★☆☆  The Waiting Room
 9.  ★★★☆☆  Hollow Lullaby
10.  ★★★☆☆  Thinthread

Total bindings: 11  ·  Unique: 10
```

---

## Design Philosophy

- **Full pity transparency** — the scholar tracks everything, nothing is hidden
- **SSR and SR pity are independent** — getting one never resets the other
- **No duplicates** within a single 10 pull
- **No energy system** — play as long as you want
- **No timers, no FOMO, no artificial gates**
- **No fan service** — atmosphere and mechanics first

---

## Stack

- Python 3.13
- `rich` — terminal rendering
- `sqlite3` — save data *(coming soon)*

---

## Project Structure
```
what-remains-of-them/
├── main.py
├── core/
│   ├── gacha.py        # pull engine, pity, rates
│   └── entities.py     # character definitions
├── ui/
│   └── terminal.py     # all rendering
├── data/
│   └── roster.json     # 15 entities across SSR / SR / R
└── saves/
    └── .gitkeep
```

---

## Running the Game
```bash
pip install rich
python ui/terminal.py
```

---

## Current State — v0.1

- [x] Gacha pull engine with soft + hard pity
- [x] 15 unique entities across 3 rarity tiers
- [x] Full terminal UI with ASCII art reveals
- [x] Scholar's Journal pity screen
- [x] Collection viewer
- [ ] Save / load system
- [ ] Combat loop
- [ ] Roguelike run structure

---

## Built by

One scholar. One terminal. No budget. No team.

*Solo dev project — v0.1 early binding.*
