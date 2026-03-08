# ui/terminal.py
import time
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.align import Align
from rich import box
from core.gacha import load_roster, PityCounter, single_pull, ten_pull

console = Console()

# ─── Colors per rarity ───────────────────────────────────────────────────────

RARITY_STYLE = {
    "SSR": "bold magenta",
    "SR":  "bold yellow",
    "R":   "bold green",
}

RARITY_STARS = {
    "SSR": "★★★★★",
    "SR":  "★★★★☆",
    "R":   "★★★☆☆",
}

# ─── Helpers ─────────────────────────────────────────────────────────────────

def clear():
    console.clear()

def pause(msg="  [ press enter to continue ]"):
    console.print(f"\n[dim]{msg}[/dim]")
    input()

def slow_print(text, style="", delay=0.03):
    """Print text character by character for dramatic effect."""
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()

# ─── Splash Screen ───────────────────────────────────────────────────────────

def show_splash():
    clear()
    splash = """
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
"""
    console.print(Align.center(Panel(
        splash,
        border_style="dim white",
        box=box.DOUBLE
    )))
    pause("  [ press enter to open the journal ]")


# ─── Main Menu ───────────────────────────────────────────────────────────────

def show_menu(pity: PityCounter):
    clear()
    p = pity.display()
    soft_pity_str = "ACTIVE" if p['soft_pity_active'] else f"in {p['soft_pity_in']} pulls"

    console.print(Align.center(Panel(
        f"""[dim]
  ╔══════════════════════════════╗
  ║   S C H O L A R ' S         ║
  ║         J O U R N A L       ║
  ╚══════════════════════════════╝[/dim]

  [bold white]What will you do?[/bold white]

  [bold cyan]  1.[/bold cyan]  Attempt a binding         [dim](1 pull)[/dim]
  [bold cyan]  2.[/bold cyan]  Attempt 10 bindings       [dim](10 pull)[/dim]
  [bold cyan]  3.[/bold cyan]  View pity counter
  [bold cyan]  4.[/bold cyan]  View collected entities
  [bold cyan]  5.[/bold cyan]  Exit

  [dim]────────────────────────────────[/dim]
  [dim]  SSR in {p['ssr_guaranteed_in']:>2} pulls  ·  SR in {p['sr_guaranteed_in']:>2} pulls[/dim]
  [dim]  Soft pity: {soft_pity_str}[/dim]
""",
        border_style="dim white",
        box=box.DOUBLE,
        width=50,
    )))

    return input("  > ").strip()


# ─── Pull Result Display ──────────────────────────────────────────────────────

def display_single_result(result: dict):
    entity  = result["entity"]
    rarity  = result["rarity"]
    style   = RARITY_STYLE[rarity]
    stars   = RARITY_STARS[rarity]
    art     = "\n".join(entity.get("ascii_art", ["  ???  "]))

    clear()
    console.print()
    slow_print("  binding in progress . . .", style="dim", delay=0.05)
    time.sleep(0.4)
    clear()

    console.print(Align.center(Panel(
        f"""[{style}]{art}[/{style}]

[{style}]  {stars}  {entity['name'].upper()}[/{style}]
[dim]  {entity['title']}[/dim]

[italic dim]  {entity['description']}[/italic dim]

[dim]  RARITY: {rarity}[/dim]""",
        border_style=style,
        box=box.DOUBLE,
        width=52,
        title=f"[{style}] BINDING COMPLETE [{style}]",
    )))

    pause()


def display_ten_results(results: list):
    clear()
    console.print()
    slow_print("  initiating 10 bindings . . .", style="dim", delay=0.04)
    time.sleep(0.5)
    clear()

    # Show all 10 results one by one with a small delay
    console.print(Align.center(
        f"\n[dim]  ══════════════ BINDING RESULTS ══════════════[/dim]\n"
    ))

    for i, result in enumerate(results):
        entity = result["entity"]
        rarity = result["rarity"]
        style  = RARITY_STYLE[rarity]
        stars  = RARITY_STARS[rarity]

        line = f"  [{style}]{stars}[/{style}]  [bold]{entity['name']:<28}[/bold]  [dim]{rarity}[/dim]"
        console.print(line)
        time.sleep(0.15)

    # Highlight SSRs and SRs pulled
    good = [r for r in results if r["rarity"] in ("SSR", "SR")]
    if good:
        console.print(f"\n  [dim]────────────────────────────────────────────[/dim]")
        for r in good:
            style = RARITY_STYLE[r["rarity"]]
            console.print(f"  [{style}]  ★  {r['entity']['name']} — {r['entity']['title']}[/{style}]")

    pause()

    # Offer to view each good pull in detail
    if good:
        console.print("  [dim]View details for notable bindings?[/dim]")
        for r in good:
            style = RARITY_STYLE[r["rarity"]]
            ans = input(f"  View [{r['rarity']}] {r['entity']['name']}? (y/n) > ").strip().lower()
            if ans == "y":
                display_single_result(r)


# ─── Pity Screen ─────────────────────────────────────────────────────────────

def show_pity(pity: PityCounter):
    clear()
    p = pity.display()
    soft_pity_detail = "[magenta bold]ACTIVE — rates increasing[/magenta bold]" if p['soft_pity_active'] else f"[dim]begins in {p['soft_pity_in']} pulls[/dim]"

    console.print(Align.center(Panel(
        f"""[dim]
  ╔══════════════════════════════╗
  ║   S C H O L A R ' S         ║
  ║     O B S E R V A T I O N S ║
  ╚══════════════════════════════╝[/dim]

  [bold white]Binding attempts since last SSR :[/bold white]  [magenta]{p['pulls_since_ssr']}[/magenta]
  [bold white]Binding attempts since last SR  :[/bold white]  [yellow]{p['pulls_since_sr']}[/yellow]

  [dim]────────────────────────────────[/dim]

  [bold white]SSR guaranteed in :[/bold white]  [magenta]{p['ssr_guaranteed_in']} pulls[/magenta]
  [bold white]SR  guaranteed in :[/bold white]  [yellow]{p['sr_guaranteed_in']} pulls[/yellow]

  [dim]────────────────────────────────[/dim]

  [bold white]Soft pity :[/bold white]  {soft_pity_detail}
""",
        border_style="dim white",
        box=box.DOUBLE,
        width=52,
        title="[ PITY COUNTER ]",
    )))

    pause()


# ─── Entity Viewer ────────────────────────────────────────────────────────────

def show_collection(collected: list):
    if not collected:
        clear()
        console.print(Align.center(Panel(
            "\n  [dim]The journal is empty.\n  No bindings have been made.[/dim]\n",
            border_style="dim white",
            box=box.DOUBLE,
            width=52,
        )))
        pause()
        return

    # Deduplicate by id, keep track of count
    seen = {}
    for e in collected:
        eid = e["entity"]["id"]
        if eid not in seen:
            seen[eid] = {"entity": e["entity"], "rarity": e["rarity"], "count": 1}
        else:
            seen[eid]["count"] += 1

    clear()
    console.print(Align.center(
        f"\n[dim]  ══════════════ BOUND ENTITIES ══════════════[/dim]\n"
    ))

    entries = sorted(seen.values(), key=lambda x: ["SSR","SR","R"].index(x["rarity"]))
    for i, entry in enumerate(entries):
        style  = RARITY_STYLE[entry["rarity"]]
        stars  = RARITY_STARS[entry["rarity"]]
        count  = f"x{entry['count']}" if entry["count"] > 1 else "  "
        line   = f"  [dim]{i+1:>2}.[/dim]  [{style}]{stars}[/{style}]  [bold]{entry['entity']['name']:<28}[/bold]  [dim]{count}[/dim]"
        console.print(line)

    console.print(f"\n  [dim]Total bindings: {len(collected)}  ·  Unique: {len(seen)}[/dim]")
    console.print(f"\n  [dim]Enter number to view details, or press enter to go back.[/dim]")

    choice = input("  > ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        entry_list = sorted(seen.values(), key=lambda x: ["SSR","SR","R"].index(x["rarity"]))
        if 0 <= idx < len(entry_list):
            display_single_result(entry_list[idx])


# ─── Main Game Loop ───────────────────────────────────────────────────────────

def main():
    roster    = load_roster()
    pity      = PityCounter()
    collected = []

    show_splash()

    while True:
        choice = show_menu(pity)

        if choice == "1":
            result = single_pull(roster, pity)
            collected.append(result)
            display_single_result(result)

        elif choice == "2":
            results = ten_pull(roster, pity)
            collected.extend(results)
            display_ten_results(results)

        elif choice == "3":
            show_pity(pity)

        elif choice == "4":
            show_collection(collected)

        elif choice == "5":
            clear()
            console.print(Align.center(Panel(
                "\n  [dim]The journal closes.\n  What remains of them, remains.[/dim]\n",
                border_style="dim white",
                box=box.DOUBLE,
                width=52,
            )))
            break

        else:
            console.print("  [dim]The scholar pauses. That was not a valid choice.[/dim]")
            time.sleep(1)


if __name__ == "__main__":
    main()
