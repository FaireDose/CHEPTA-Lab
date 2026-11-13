#!/usr/bin/env python3
"""Compare the 0.6.1 and 0.6.2 outputs of every B2 run (leaf by leaf, exact), list extrapolations/estimated pairs.
Writes results-chepta-0.6.2/comparison.json. Reads files only; no CHEPTA imports."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compare_common import compare
compare(Path(__file__).resolve().parent)
