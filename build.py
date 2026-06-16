#!/usr/bin/env python3
"""
build.py — NGC Tuesday Night Men's League 2026
Run this after adding a new weekly CSV to the data/ folder.
It rebuilds league_data.json and updates the embedded data in index.html.

Usage:
    python build.py
"""

import json
import os
import re
import glob

# ─── Team map (derived from Week 1 scorecard pairings) ───
TEAM_MAP = {
    "1":  {"players": ["Dave D", "Ken B"],            "name": "Dave/Ken"},
    "2":  {"players": ["Herb P", "Russ P"],            "name": "Herb/Russ"},
    "3":  {"players": ["Bryan L", "Cory S"],           "name": "Bryan/Cory"},
    "4":  {"players": ["Scott N", "John C"],           "name": "Scott/John"},
    "5":  {"players": ["Bruce S", "Tom M"],            "name": "Bruce/Tom"},
    "6":  {"players": ["David M", "Pickles -"],        "name": "David/Pickles"},
    "7":  {"players": ["John L", "John M"],            "name": "John/John"},
    "8":  {"players": ["Paul K", "Tom N"],             "name": "Paul/Tom"},
    "9":  {"players": ["Troy C", "Bill P"],            "name": "Troy/Bill"},
    "10": {"players": ["Mark S", "Ray King"],          "name": "Mark/Ray"},
    "11": {"players": ["Andy S", "Rodney S"],          "name": "Andy/Rodney"},
    "12": {"players": ["Boomer -", "Steve M"],         "name": "Boomer/Steve"},
    "13": {"players": ["Steve G", "Joe J"],            "name": "Steve/Joe"},
    "14": {"players": ["Ben C", "Bill T"],             "name": "Ben/Bill"},
    "15": {"players": ["Tom K", "Charlie M"],          "name": "Tom/Charlie"},
    "16": {"players": ["Gary M", "Gavin M"],           "name": "Gary/Gavin"},
    "17": {"players": ["Andrew George", "Jeff George"],"name": "Andrew/Jeff"},
    "18": {"players": ["Tim C", "Travis C"],           "name": "Tim/Travis"},
    "19": {"players": ["Bill B", "Jim Mott"],          "name": "Bill/Jim"},
    "20": {"players": ["Don J", "Matt -"],             "name": "Don/Matt"},
    "21": {"players": ["Dan B", "Schetter -"],         "name": "Dan/Schetter"},
    "22": {"players": ["Derek -", "Rich -"],           "name": "Derek/Rich"},
}

# CSV filename → (week label, date string)
# Add a new entry here each week
WEEK_FILES = [
    ("Week_1_May_19_2026__3_.csv",  "Week 1", "May 19, 2026"),
    ("Week_2_May_26_2026.csv",       "Week 2", "May 26, 2026"),
    ("Week_3_June_2_2026.csv",       "Week 3", "June 2, 2026"),
    ("Week_4_June_9_2026.csv",       "Week 4", "June 9, 2026"),
    # Add next week here:
    # ("Week_5_June_16_2026.csv",    "Week 5", "June 16, 2026"),
]


def parse_week(filepath, label, date):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        lines = [l.strip().replace("\r", "") for l in f.readlines()]

    week = {
        "label": label,
        "date": date,
        "matchPoints": {},
        "skins": {},
        "handicaps": {},
        "scorecards": [],
    }

    # ── Handicaps from scorecard rows ──
    for l in lines:
        parts = [p.strip() for p in l.split(",")]
        if len(parts) > 3 and parts[1] and "Tee" in parts[1] and parts[0]:
            try:
                week["handicaps"][parts[0]] = float(parts[2])
            except ValueError:
                week["handicaps"][parts[0]] = 0.0

    # ── Match points & skins ──
    mode = None
    current_team = None
    for l in lines:
        if l == "Team Matchplay":
            mode = "match"
            current_team = None
            continue
        if l == "Team Skins":
            mode = "skins"
            current_team = None
            continue
        if mode is None:
            continue
        parts = [p.strip() for p in l.split(",")]
        if not l or parts[0] == "Team":
            continue
        if parts[0].isdigit() and (len(parts) < 2 or parts[1] == ""):
            current_team = parts[0]
            try:
                val = float(parts[2])
            except (ValueError, IndexError):
                val = 0.0
            if mode == "match":
                week["matchPoints"][current_team] = val
            else:
                week["skins"][current_team] = val
        if mode == "skins" and l == "" and current_team:
            mode = None

    # ── Scorecards ──
    i = 0
    while i < len(lines):
        if "Nahma Golf Club" in lines[i] and i > 100:
            par = None
            players = []
            j = i + 1
            while j < min(i + 60, len(lines)):
                l = lines[j]
                parts = [p.strip() for p in l.split(",")]
                if parts[0] == "Par":
                    par = []
                    for k in range(3, 12):
                        try:
                            par.append(int(parts[k]))
                        except (ValueError, IndexError):
                            par.append(None)
                elif len(parts) > 3 and parts[1] and "Tee" in parts[1] and parts[0]:
                    scores = []
                    for k in range(3, 12):
                        try:
                            scores.append(int(parts[k]))
                        except (ValueError, IndexError):
                            scores.append(None)
                    try:
                        hdcp = float(parts[2])
                    except ValueError:
                        hdcp = 0.0
                    players.append({"name": parts[0], "handicap": hdcp, "scores": scores})
                elif l == "" and players:
                    break
                j += 1
            if par and players:
                week["scorecards"].append({"par": par, "players": players})
            i = j
        else:
            i += 1

    return week


def build():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    all_weeks = []

    print("Building league data...\n")
    for fname, label, date in WEEK_FILES:
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            print(f"  ⚠️  Missing: {path} — skipping")
            continue
        week = parse_week(path, label, date)
        all_weeks.append(week)
        print(f"  ✅ {label} ({date}): "
              f"{len(week['matchPoints'])} teams, "
              f"{len(week['handicaps'])} players, "
              f"{len(week['scorecards'])} scorecards")

    output = {"teamMap": TEAM_MAP, "weeks": all_weeks}

    # Write league_data.json
    json_path = os.path.join(data_dir, "league_data.json")
    with open(json_path, "w") as f:
        json.dump(output, f, separators=(",", ":"))
    print(f"\n  📄 Written: {json_path}")

    # Update embedded data in index.html
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    json_str = json.dumps(output, separators=(",", ":"))
    match = re.search(r'const LEAGUE = \{.*?\};', html, flags=re.DOTALL)

    if not match:
        print("  ⚠️  Could not find LEAGUE data block in index.html to update")
    else:
        new_html = html[:match.start()] + f'const LEAGUE = {json_str};' + html[match.end():]
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  📄 Updated: {html_path}")

    print(f"\n✅ Done — {len(all_weeks)} weeks processed.")
    print("\nNext steps:")
    print("  git add data/ index.html")
    print('  git commit -m "Add Week N"')
    print("  git push")


if __name__ == "__main__":
    build()
