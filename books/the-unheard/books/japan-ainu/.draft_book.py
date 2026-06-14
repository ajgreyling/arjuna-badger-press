#!/usr/bin/env python3
"""Draft the Japan novel chapter-by-chapter via metered Opus, with rolling continuity.
Resumable: skips chapters already in build/chapters/. Checkpoints build/state.json.
After each chapter: append a compressed story-state line (continuity) + a cheap firewall lint.
Run: python3 .draft_book.py            (drafts all remaining)
     python3 .draft_book.py ch-07      (force-redraft one chapter)
"""
import os, sys, json, re, time, urllib.request, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CANON = ROOT / "canon"
BUILD = ROOT / "build"
CHAPDIR = BUILD / "chapters"
CHAPDIR.mkdir(parents=True, exist_ok=True)
STATE = BUILD / "state.json"

def load_env():
    for line in open(ROOT.parents[3] / ".env"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); os.environ.setdefault(k, v)

def anthropic(prompt, system, max_tokens=8000, retries=4):
    key = os.environ["ANTHROPIC_API_KEY"]; model = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
    body = {"model": model, "max_tokens": max_tokens, "system": system,
            "messages": [{"role": "user", "content": prompt}]}
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request("https://api.anthropic.com/v1/messages",
                data=json.dumps(body).encode(),
                headers={"content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
            r = urllib.request.urlopen(req, timeout=600)
            return json.load(r)["content"][0]["text"]
        except Exception as e:
            last = e
            wait = 8 * (attempt + 1)
            sys.stderr.write(f"  [retry {attempt+1}/{retries} in {wait}s: {type(e).__name__} {str(e)[:120]}]\n")
            time.sleep(wait)
    raise last

load_env()
outline = json.loads((BUILD / "outline.json").read_text())
chapters = outline["chapters"]
spine = "\n".join(f"- {s}" for s in outline.get("continuity_spine", []))
cast = outline["cast"]

# compact cast block for every prompt
def cast_block():
    crew = "; ".join(f"{c['name']} (reads {c['layer']})" for c in cast["crew"])
    leads = "; ".join(f"{l['name']} ({l['people']}, {l.get('role','')})" for l in cast["local_leads"])
    keep = "; ".join(f"{k['name']} ({k['craft']})" for k in cast.get("keepers", []))
    a = cast["antagonist"]
    return (f"CREW: {crew}.\nLOCAL LEADS (the camera belongs to them): {leads}.\n"
            f"KEEPERS: {keep}.\nFLATTENING FORCE: {a['name']} — {a.get('wants','')}.\n"
            f"JAKOBUS: the road, NO POV, seen only from outside; brother/uncle; defers to the leads; stands guard.")

SYSTEM = (
    "You are the prose engine (the Anthropic/Opus draft role) of an autonomous literary-thriller "
    "engine, drafting one chapter of a finished novel in *The Unheard* series. You write publishable, "
    "propulsive, literary close-third prose — the register of the series' existing books (warm, exact, "
    "unsentimental, set-piece-driven; 'less emphasis, more trust; less explanation, more dramatic "
    "embodiment'). You obey the canon and the firewalls as absolute law. You output ONLY the chapter "
    "prose in Markdown (a single '# Chapter N — Title' header then the prose), no notes, no commentary."
)

VOICE = """VOICE & CRAFT (binding):
- Close third on the chapter's POV character. The CAMERA belongs to the local leads and the crew — NEVER
  to Jakobus (he is seen only from outside; no interiority for him, ever).
- Literary-propulsive: scenes PLAY in full (dialogue, action, sensory ground), never summarised. Dramatise,
  don't report. Earn every emotional beat; no telling the reader what to feel.
- Warm, funny, modern, specific. The leads and crew are real people — flawed, ordinary, self-determining —
  NOT symbols or inspiration-posters. The marginalised are the experts of their own story.
- Anti-machine-tells: avoid the almost-emotion hedge, the tidy reframe ("Not X. Y."), the "something"
  hedge, "the way", stacked em-dashes as a tic, "filed it away". Plain, embodied, varied sentences.
- The theme (the map is a lie of omission; love the real plural thing more than the postcard) is carried,
  NEVER preached. No lecture; let scenes mean.
- ~{tw} words for this chapter. End on a clean beat that hands forward to the next chapter."""

FIREWALLS = """FIREWALLS (ABSOLUTE — a violation fails the chapter):
- BURAKU: the community and its location are FICTIONALISED — NEVER name or geolocate a real present-day
  buraku community. NEVER use the slurs (eta/hinin/kawata) in the narrative voice (only a clearly-marked
  bigot in quoted speech, signposted, and even then sparingly). A buraku 'reveal' is NEVER a thrill — it
  is the violence it depicts; the strand resolves WITHOUT an outsider exposé (Tōru is named on his OWN
  terms). The hidden-hands link is ONLY the documented one: leather for armour + skins for taiko drums
  (NOT swords — that is folk-myth, never state it).
- AINU: language isolate, animist (kamuy); recognised as Indigenous only 2019 (shallow); 1899 assimilation
  law (repealed 1997). Population/speaker numbers are CONTESTED — never a flat figure. Museum ≠ living
  people. NO fresh traditional Ainu facial tattoos on any character. No 'inu'/dog slur in the narrative
  voice. iyomante (bear ceremony) reverent, never staged as colour.
- BUSHIDO: a real-but-CONSTRUCTED tradition (Nitobe 1900, English, for Westerners, shaped like European
  chivalry, WWII-weaponised; plural Edo reality, most samurai bureaucrats). The narrative voice NEVER
  adopts the 'we Japanese'/homogeneity/timeless-mystical-code framing. Love the real thing; never sneer.
- THE WONDER (Ishi-no-Hōden): ~500-ton worked welded TUFF (not granite); the 'float' is an ENGINEERED
  effect (hidden central pedestal over a water basin); purpose GENUINELY UNSOLVED (2005 laser survey).
  NEVER any Ancient-Aliens / supernatural / woo framing.
- JAKOBUS: tattoo = his 5th, a GREAT WAVE held at full weight that does NOT break (power held soft),
  hand-poked by a JAPANESE HORISHI (NOT an Ainu hand). The buried G-nod ('danger held soft') stays PURE
  STORY — NO symbols, NO equation, NO mention of physics; at most ONE quiet earned double-duty line.
  His belt knives are confiscated under Japanese carry law (disarmed all book); the gifted blade is a
  LEGAL kitchen/field knife. The Lexus LX is BORROWED, silent, hands-empty — a light grace-note, not a
  gear segment. Keep all Jakobus beats PERIPHERAL — the camera stays on the locals.
- DODGE BOTH failure modes: (1) the exotic postcard; (2) the opposite — solemn 'mystical-ancient-Japan'
  awe or a gawking-foreigner exposé is the SAME dehumanising coin."""

def read_state():
    if STATE.exists(): return json.loads(STATE.read_text())
    return {"done": [], "rolling_summary": ""}

def write_state(s): STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False))

def summarise(chapter_text, prev_summary, cid):
    """Compress story-state forward via the cheaper OpenAI model (continuity role)."""
    key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("OPENAI_MODEL", "gpt-4.1")
    sys_p = ("You compress a novel's running story-state for continuity. Output 4-7 terse bullet lines: "
             "what changed, who learned/decided what, any new fact later chapters must honor, where people "
             "physically are now, and Jakobus's state (tattoo/knife/Lexus). No prose, just the bullets.")
    usr = f"PRIOR STATE:\n{prev_summary or '(none yet)'}\n\nNEW CHAPTER ({cid}):\n{chapter_text[:9000]}\n\nUpdated running state (bullets):"
    body = {"model": model, "max_tokens": 600, "messages": [
        {"role": "system", "content": sys_p}, {"role": "user", "content": usr}]}
    try:
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
            data=json.dumps(body).encode(),
            headers={"content-type": "application/json", "authorization": f"Bearer {key}"})
        r = urllib.request.urlopen(req, timeout=180)
        return json.load(r)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        sys.stderr.write(f"  [summarise fell back to truncation: {type(e).__name__}]\n")
        return (prev_summary + f"\n- {cid}: drafted.")[-2000:]

FORCE = sys.argv[1] if len(sys.argv) > 1 else None
state = read_state()
cb = cast_block()

for idx, ch in enumerate(chapters):
    cid = ch["id"]
    outpath = CHAPDIR / f"{cid}.md"
    if outpath.exists() and cid != FORCE:
        continue
    tw = ch.get("target_words", 3000)
    prev_tail = ""
    if idx > 0:
        p = CHAPDIR / f"{chapters[idx-1]['id']}.md"
        if p.exists():
            prev_tail = p.read_text()[-1400:]
    nxt = chapters[idx+1] if idx + 1 < len(chapters) else None
    nxt_hint = f"{nxt['id']}: {nxt.get('summary','')[:200]}" if nxt else "(this is the final chapter — land the resolution)"

    prompt = f"""Draft **{cid} — {ch['title']}** of the novel *The Way That Was Invented* (*The Unheard*: Japan).

{cb}

THIS CHAPTER (from the locked, approved outline):
- POV: {ch.get('pov','')}
- Beat / relay node: {ch.get('beat','')} / {ch.get('relay_node','')}
- Unheard thread: {ch.get('unheard_thread','')}   |   Jakobus beat: {ch.get('jakobus_beat','none')}
- Place/wonder: {ch.get('wonder_or_place','')}
- WHAT HAPPENS (dramatise this in full): {ch.get('summary','')}
- Continuity to establish/honor here: {ch.get('continuity_notes','')}

BINDING CONTINUITY SPINE (whole book):
{spine}

STORY SO FAR (rolling state — honor it; do not contradict):
{state.get('rolling_summary') or '(this is the opening)'}

{("PREVIOUS CHAPTER ENDED:\n…" + prev_tail) if prev_tail else ""}

NEXT CHAPTER will be: {nxt_hint}
(Hand toward it cleanly; do NOT write it.)

{VOICE.format(tw=tw)}

{FIREWALLS}

Now write {cid} in full — ONLY the chapter (a '# Chapter ...' header line then the prose), ~{tw} words."""

    sys.stderr.write(f"\n=== drafting {cid} ({ch['title']}) target ~{tw}w ...\n")
    t0 = time.time()
    text = anthropic(prompt, SYSTEM, max_tokens=min(8000, int(tw * 2.2)))
    text = text.strip()
    # ensure a header
    if not text.lstrip().startswith("#"):
        text = f"# Chapter {idx} — {ch['title']}\n\n" + text
    outpath.write_text(text + "\n")
    wc = len(text.split())
    sys.stderr.write(f"    wrote {cid}: {wc} words in {int(time.time()-t0)}s\n")

    # quick firewall lint (cheap, local) — flags, never blocks; logged for the read pass
    low = text.lower()
    flags = []
    for slur in [" eta ", "hinin", "kawata", "burakumin are dirty"]:
        if slur in low: flags.append(f"possible-slur:{slur.strip()}")
    if re.search(r"ancient alien|extraterrestrial|levitat|anti-gravity", low): flags.append("woo-near-stone")
    if "granite" in low and "tuff" in low and cid == "ch-09": pass
    elif "ishi-no-h" in low and "granite" in low: flags.append("stone-granite-not-tuff")
    if flags:
        (BUILD / "lint.log").open("a").write(f"{cid}: {', '.join(flags)}\n")
        sys.stderr.write(f"    ⚠ lint: {', '.join(flags)}\n")

    # roll continuity forward + checkpoint
    state["rolling_summary"] = summarise(text, state.get("rolling_summary", ""), cid)
    if cid not in state["done"]: state["done"].append(cid)
    write_state(state)

sys.stderr.write(f"\nDONE. {len(state['done'])}/{len(chapters)} chapters drafted.\n")
print(json.dumps({"done": state["done"], "total": len(chapters)}))
