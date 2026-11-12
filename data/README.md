# Catalogue data

| File | What it is |
|---|---|
| [sources.json](sources.json) | Every paper or book Lab uses: reference, where it can be read, licence and whether it may be released |
| [candidates.json](candidates.json) | The process families considered, what each needs from CHEPTA, and what blocks it |
| [upstream.json](upstream.json) | The CHEPTA version Lab runs (now `chepta@0.6.0` from npm) and the older commits earlier runs used |

Check after any change: `python scripts/validate_catalog.py`.
