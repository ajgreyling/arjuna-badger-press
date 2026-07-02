#!/usr/bin/env python3
"""arjunabadger.press leak-scan — the estate-wide Sentinel gate (Incident-001 doctrine).

The default posture (AJ, 2026-06-28): assume the world is hostile (nation-state + a bounty on the
founder). Every repo gets this gate. For the press (a publishing repo), the shipped surface is the
books + the static site. This blocks two classes from shipping:

  1. SECRETS — real API-key / token / private-key shapes.
  2. PROTECTED FULL-NAME IDENTIFIERS of real people on the PUBLISHED surface (books/site) — the
     doxxing + consent class. First-name characters in the prose are the author's editorial call and
     are NOT gated; the gate catches the high-signal LEGAL identifiers (full name) + named ventures.

Exit non-zero on any finding so CI / a pre-commit hook BLOCKS it. Pure stdlib.
  python3 scripts/leak_scan.py            # scan tracked files
  python3 scripts/leak_scan.py --staged   # pre-commit: scan staged files only
"""
from __future__ import annotations
import os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SECRETS = [
    (r"sk-[a-zA-Z0-9]{20,}", "OpenRouter/OpenAI-style API key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub token"),
    (r"xox[baprs]-[a-zA-Z0-9-]{10,}", "Slack token"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key block"),
]
# Protected real-person LEGAL identifiers (full names) + named private ventures. First-name only is
# the author's call (a memoir character), deliberately NOT gated.
PROTECTED_IDENTIFIERS = [
    "Ferdie Lochner", "Dr Ferdie Lochner", "Bertus Swanepoel", "Coenie Louw", "TwinShield",
]
# The scanner names the protected identifiers itself; SECURITY.md is the doctrine doc whose whole
# job is to catalogue them. Both are repo-internal (never copied into the deployed site/public/
# surface), so listing the names there is the policy working, not a leak. Exempt both.
ALLOW = {"scripts/leak_scan.py", "SECURITY.md"}

def _files(staged):
    cmd = ["git","diff","--cached","--name-only"] if staged else ["git","ls-files"]
    return [l for l in subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True).stdout.splitlines() if l]

def scan(files):
    out=[]
    for rel in files:
        if rel in ALLOW: continue
        p=os.path.join(ROOT,rel)
        if not os.path.isfile(p): continue
        try: t=open(p,encoding="utf-8",errors="replace").read()
        except OSError: continue
        for pat,label in SECRETS:
            if re.search(pat,t): out.append(("CRITICAL",rel,f"possible {label}"))
        for ident in PROTECTED_IDENTIFIERS:
            if ident in t:
                out.append(("HIGH",rel,f"protected identifier '{ident}' (consent? de-identify?)"))
    return out

def main():
    staged = "--staged" in sys.argv
    f = scan(_files(staged))
    mode = "staged" if staged else "tracked"
    if not f:
        print(f"leak-scan ({mode}): CLEAN — no secrets or protected legal identities in the shipped surface.")
        return 0
    print(f"leak-scan ({mode}): {len(f)} finding(s) — BLOCKED:")
    for sev,rel,msg in f: print(f"  [{sev}] {rel}: {msg}")
    print("\nThe Sentinel stopped a leak (Incident-001 doctrine). Redact/de-identify before shipping.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
