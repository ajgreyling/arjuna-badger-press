#!/usr/bin/env python3
"""Merge the Japan book chapters -> build/BOOK.md (+ novelcrafter), then run a continuity +
firewall sweep across the whole manuscript. Mirrors HBT tools/merge_book.py front-matter logic.
Run: python3 .merge_and_check.py
Exit 0 always (report-only, like the engine's 'measure & alarm'); writes build/CONTINUITY_REPORT.md.
"""
import sys, re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CANON = ROOT / "canon"
BUILD = ROOT / "build"
CHAPDIR = BUILD / "chapters"

def chapters():
    return sorted(CHAPDIR.glob("ch-*.md"))

# ---- MERGE (front matter = DEDICATION_BOOK.md + FOREWORD.md if present, then chapters) ----
def merge():
    files = chapters()
    if not files:
        print("no chapters", file=sys.stderr); return None
    front = ""
    for fn in ("DEDICATION_BOOK.md", "FOREWORD.md"):
        p = CANON / fn
        if p.exists():
            front += p.read_text(encoding="utf-8").rstrip() + "\n\n"
    prose = "\n\n".join(f.read_text(encoding="utf-8").rstrip() for f in files)
    (BUILD / "BOOK.md").write_text(front + prose + "\n", encoding="utf-8")
    (BUILD / "BOOK.novelcrafter.md").write_text(prose + "\n", encoding="utf-8")
    wc = len((front + prose).split())
    print(f"[merge] BOOK.md: {len(files)} chapters, ~{wc} words")
    return files, wc

# ---- CONTINUITY + FIREWALL SWEEP ----
def sweep(files):
    rep = ["# CONTINUITY + FIREWALL REPORT — *The Way That Was Invented*\n"]
    issues = []
    warns = []
    narrative_files = [f for f in files if f.stem != "ch-99"]
    full = "\n".join(f.read_text() for f in files)
    narrative = "\n".join(f.read_text() for f in narrative_files)
    low = narrative.lower()

    outline = json.loads((BUILD / "outline.json").read_text())
    cast = outline["cast"]
    # canonical names that must appear / stay spelled consistently
    names = [c["name"].split()[0] for c in cast["crew"]] + \
            [l["name"].split()[0] for l in cast["local_leads"]] + \
            [k["name"].split()[0] for k in cast.get("keepers", [])]
    names = [n for n in names if len(n) > 2]

    # 1) FIREWALL: slurs in narration (allow only if clearly in quoted dialogue is hard to detect;
    #    flag ALL occurrences for human eyes)
    for slur in ["eta", "hinin", "kawata", "yotsu"]:
        # word-boundary, avoid 'meta','beta','christmas' etc for 'eta'
        hits = len(re.findall(rf"\b{slur}\b", low))
        if slur == "eta":
            # 'eta' is too common as substring; only count standalone slur-ish uses near buraku context
            hits = len(re.findall(r"\beta\b", low))
        if hits:
            issues.append(f"FIREWALL/slur: '{slur}' appears {hits}× — verify NONE are in narrative voice (only signposted bigot dialogue allowed).")

    # 2) FIREWALL: woo near the stone
    for w in ["ancient alien", "extraterrestrial", "anti-gravity", "antigravity", "levitat", "supernatural force", "alien technology"]:
        if w in low:
            issues.append(f"FIREWALL/woo: '{w}' present — the floating stone must stay grounded (engineered float, unsolved purpose, NO woo).")

    # 3) FIREWALL: stone called granite (it's tuff)
    for m in re.finditer(r"granite", low):
        seg = low[max(0, m.start()-120):m.start()+120]
        if "ishi" in seg or "float" in seg or "stone" in seg or "tuff" in seg:
            # tuff nearby = likely the correcting line ("not granite"); flag only if 'not granite' absent
            if "not granite" not in seg and "isn't granite" not in seg:
                warns.append("CHECK/stone: 'granite' near the floating stone — confirm it's the corrective ('not granite'), not a misattribution (it's welded tuff).")
                break

    # 4) FIREWALL: swords as the buraku hidden-hand (folk-myth) — flag 'sword' within ~80 chars of buraku/leather-hands framing
    for m in re.finditer(r"(wrapped|polished|made|forged).{0,40}(sword|katana)", low):
        seg = low[max(0,m.start()-160):m.start()+120]
        if any(k in seg for k in ["buraku","outcast","unnamed hand","hidden hand","tōru","toru","drum-maker","tanner","leather"]):
            # allow explicit rejections of the sword-craft myth (ch-14: "Not the swords")
            if re.search(r"\bnot\b.{0,24}(the )?(sword|sword[s]?|katana)", seg) or "leave it out" in seg or "folk" in seg and "story" in seg:
                continue
            issues.append("FIREWALL/hidden-hands: a buraku/unnamed-hands passage ties to SWORD-making (folk-myth). Must be armour-LEATHER + taiko drum-SKINS only.")
            break

    # 5) JAKOBUS: tattoo must be the WAVE from a horishi, not Ainu; no fresh Ainu facial tattoo on a character
    if "tattoo" in low or "ink" in low or "horishi" in low or "tebori" in low:
        if "wave" not in low:
            warns.append("CHECK/Jakobus: tattoo scenes present but 'wave' motif not found — confirm the 5th tattoo is the great wave.")
        # crude Ainu-tattoo-on-character check
        if re.search(r"ainu.{0,40}tattoo|tattoo.{0,40}(her|his) (face|mouth|lips)", low):
            warns.append("CHECK/Ainu-firewall: a facial/Ainu tattoo reference near a character — verify NO fresh traditional Ainu facial tattoo is inked on anyone.")

    # 6) NAME CONSISTENCY: each locked name should appear; flag any that never show (dropped char) — info only
    for n in sorted(set(names)):
        if n.lower() not in low:
            warns.append(f"INFO/name: locked name '{n}' never appears in the prose (dropped or renamed?).")

    # 7) crude POV-for-Jakobus leak: first-person/interiority cues immediately around 'Jakobus' — heuristic
    leak = len(re.findall(r"jakobus (thought|felt|knew|remembered|wondered|realised|realized)\b", low))
    if leak:
        warns.append(f"CHECK/POV: {leak}× 'Jakobus thought/felt/...' — he has NO POV; interiority must be inferred from outside, not stated. Verify these read as observed, not internal.")

    # ---- assemble ----
    rep.append(f"Chapters merged: **{len(files)}** (narrative **{len(narrative_files)}** + backmatter).  Total ~{len(full.split())} words.\n")
    rep.append("## Hard issues (fix before publish)\n")
    rep += [f"- ❌ {i}" for i in issues] or ["- ✅ none flagged by the automated sweep."]
    rep.append("\n## Checks / warnings (human eyes)\n")
    rep += [f"- ⚠ {w}" for w in warns] or ["- ✅ none."]
    rep.append("\n## Continuity spine (verify against the prose by reading)\n")
    rep += [f"- {s}" for s in outline.get("continuity_spine", [])]
    rep.append("\n> Narrative firewall (ch-00–ch-18 only). Backmatter (ch-99) names slurs and rejected framings in an author note — excluded from automated slur/woo/sword scans.\n")
    rep.append("> Automated sweep is a LEAD, not a verdict. The binding check is reading the prose. "
               "Sensitivity read (Ainu + buraku-literate + tattoo-world) remains a required gate before publication.")
    (BUILD / "CONTINUITY_REPORT.md").write_text("\n".join(rep))
    print(f"[sweep] {len(issues)} hard issues, {len(warns)} warnings -> build/CONTINUITY_REPORT.md")
    return issues, warns

if __name__ == "__main__":
    m = merge()
    if m:
        files, _ = m
        sweep(files)
