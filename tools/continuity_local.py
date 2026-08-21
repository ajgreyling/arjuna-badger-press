#!/usr/bin/env python3
"""Deterministic continuity checks for a book's chapters. Free, local, no model call.

This is NOT a replacement for tools/continuity_audit.py, which reads the whole book
with a model and finds semantic contradictions ("he is in Accra in ch-12 and Nairobi
on the same afternoon in ch-13"). This catches the mechanical class only — the bugs a
find-and-replace or a late edit introduces, which is exactly the class that a
whole-book model read is wasted on and a script is perfect for.

It exists because a sweep to vary an over-used number silently desynchronised three
cross-chapter facts in this repo, and none of them were visible from inside a chapter.

Usage:
    python3 tools/continuity_local.py books/<book> [--facts FILE]

FACTS FILE (optional): one per line, `label = regex`. Every distinct captured value
is reported; a fact that should be constant across the book and isn't is a finding.
"""
from __future__ import annotations
import argparse, glob, os, re, sys, collections

def load_facts(path):
    facts={}
    if not path or not os.path.exists(path): return facts
    for ln in open(path,encoding='utf-8'):
        ln=ln.strip()
        if not ln or ln.startswith('#') or '=' not in ln: continue
        k,v=ln.split('=',1); facts[k.strip()]=v.strip()
    return facts

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('book'); ap.add_argument('--facts')
    a=ap.parse_args()
    chdir=os.path.join(a.book,'build','chapters')
    files=sorted(glob.glob(os.path.join(chdir,'ch-*.md')))
    if not files: sys.exit(f"no chapters under {chdir}")
    text={os.path.basename(f):open(f,encoding='utf-8').read() for f in files}
    findings=0

    # 1. chapter numbering + POV header integrity
    print("== headers ==")
    for i,(name,t) in enumerate(text.items(),1):
        m=re.match(r'#\s*(\d+)\s*—\s*(.+)',t.strip().split('\n')[0])
        if not m:
            print(f"  MALFORMED HEADER {name}: {t.strip().split(chr(10))[0][:60]}"); findings+=1; continue
        n=int(m.group(1)); exp=int(name[3:5])
        if n!=exp: print(f"  NUMBER MISMATCH {name}: header says {n}"); findings+=1
        if not re.search(r'^>\s*\*\*\[[A-Z]\]\*\*', t, re.M):
            print(f"  NO POV TAG {name}"); findings+=1
    if findings==0: print("  ok — all headers well formed and numbered")

    # 2. declared facts that must be constant
    facts=load_facts(a.facts)
    if facts:
        print("\n== constant facts ==")
        for label,pat in facts.items():
            hits=collections.defaultdict(list)
            for name,t in text.items():
                for m in re.finditer(pat,t,re.I):
                    hits[m.group(0).lower()].append(name)
            if not hits:
                print(f"  ABSENT  {label}"); findings+=1
            elif len(hits)>1:
                print(f"  CONFLICT {label}:"); findings+=1
                for v,where in hits.items():
                    print(f"      {v!r} in {', '.join(sorted(set(where))[:4])}")
            else:
                v,where=next(iter(hits.items()))
                print(f"  ok      {label}: {v!r} ({len(where)}x)")

    # 3. near-duplicate paragraphs (stdlib; no embeddings)
    print("\n== near-duplicate paragraphs ==")
    paras=[]
    for name,t in text.items():
        for p in t.split('\n\n'):
            p=p.strip()
            if len(p.split())>=25 and not p.startswith(('#','>','|','`')):
                paras.append((name,p))
    def shingles(s):
        w=re.findall(r'[a-z]+',s.lower())
        return {tuple(w[i:i+5]) for i in range(len(w)-4)}
    sh=[(n,p,shingles(p)) for n,p in paras]
    dupes=0
    for i in range(len(sh)):
        for j in range(i+1,len(sh)):
            a1,p1,s1=sh[i]; a2,p2,s2=sh[j]
            if not s1 or not s2: continue
            jac=len(s1&s2)/len(s1|s2)
            if jac>0.35:
                print(f"  {jac:.0%} {a1} ~ {a2}\n      {p1[:88]}…\n      {p2[:88]}…")
                dupes+=1; findings+=1
    if dupes==0: print("  ok — no paragraph pairs above 35% shingle overlap")

    print(f"\n{findings} finding(s)")
    return 1 if findings else 0

if __name__=='__main__':
    sys.exit(main())
