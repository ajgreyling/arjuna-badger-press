#!/usr/bin/env python3
"""Typeset RESONANCE — African Gold Trilogy · Book One (Atkinson Hyperlegible)."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.argv = ["typeset_trilogy_covers.py", "resonance"]
runpy.run_path(str(REPO / "design" / "typeset_trilogy_covers.py"), run_name="__main__")
