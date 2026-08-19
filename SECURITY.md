# Security posture — assume-breach (estate default)

> **Standing law (AJ, 2026-06-28): this is the default posture for the WHOLE estate**, not one repo.
> The threat model is a hostile world — frontier nation-state pen-testers + a dark-web bounty on the
> founder. We do not pretend to be unhackable against that (no one is); we **shrink the surface, make
> a breach loud and provable, keep the irreversible out of a compromised agent's reach, and catch the
> leak on the way out.** Origin doctrine: `congosky-cloud/klaus/fabric/SENTINEL_LESSONS.md`.

## The five doctrines (every repo inherits them)
1. **No real person's legal name on a published/public surface without consent.** First-name
   characters in a memoir are the author's call; full legal names + private ventures are de-identified
   until consent. Consent is recorded, scoped and attributed — never assumed, never blanket.
   (This repo: **Ferdie Lochner / Dr Ferdie Lochner — consent given**, attested by AJ 2026-08-19,
   scoped to `books/the-sheltering-desert/`. The name stays in `PROTECTED_IDENTIFIERS`; the
   `CONSENTED` register in `leak_scan.py` only widens it for the paths he agreed to, so the same
   name in another book still stops the build.)
2. **Assume the shipped surface is curl-able.** The pre-ship `leak_scan.py` gate fails CI if a secret
   or protected identifier is about to ship.
3. **Verify what you load; no custom crypto.** SRI on every external script; pinned dependencies.
4. **Secrets / the encoded self never enter git.** Pre-commit gate (`scripts/install-hooks.sh` where
   present); `.gitignore` the secret class.
5. **The human is the soft target.** The Sentinel catches the author's own slip (a name in a commit)
   as surely as an attacker's probe.

## This repo
- `scripts/leak_scan.py` — the pre-ship gate (run it; CI runs it on every push).
- `.github/workflows/leak-scan.yml` — CI enforcement.
- Books de-identified: full legal name → first-name character; named private venture genericized.
