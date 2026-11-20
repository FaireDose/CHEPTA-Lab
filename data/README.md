# Catalogue data

| File | What it is |
|---|---|
| [sources.json](sources.json) | Every paper or book Lab uses: reference, where it can be read, licence and whether it may be released |
| [candidates.json](candidates.json) | The process families considered, what each needs from CHEPTA, and what blocks it |
| [upstream.json](upstream.json) | The CHEPTA version Lab runs (the pin is in package.json) and the older versions earlier runs used |
| [ISSUES_AND_ROUTES.md](ISSUES_AND_ROUTES.md) | What the cases taught: one row per problem (separation, reaction, plant), the routes papers used and whether CHEPTA can do them |

Check after any change: `python scripts/validate_catalog.py`.
