## What this changes

<!-- One or two sentences, in engineering terms. Link the issue: "Closes #12". -->

## Next steps

<!-- What the maintainer should check or decide, and what comes after this pull request. -->

## Checklist for the author

- [ ] Every new number has a source with an exact locator (table, figure, page or passage), its original units and any conversion
- [ ] The rights status of every new source is recorded in `data/sources.json`; `needs_review` and `reference_only` material stays out of releases
- [ ] No papers, PDFs, copied paywalled text, API keys or credentials are committed
- [ ] A person compared each transcribed value with its source (an AI assistant never counts)
- [ ] New tasks stay `draft`; no human review is recorded on anyone's behalf
- [ ] Simulated, measured, assumed and derived quantities are kept distinguishable
- [ ] `python scripts/validate_catalog.py`, `python scripts/dataset_pipeline.py validate` and `python -m unittest discover -s tests` pass

## Checklist for the reviewer (not the author)

- [ ] I checked the cited sources against the numbers and claims in the change
- [ ] No record contains instructions aimed at an AI, invented rationale or unsupported performance claims
- [ ] Changes to schemas, scripts or workflows do not weaken the release gates or the workflow permissions
- [ ] The results are physically sensible for the stated conditions

Pull requests prepared by AI agents are reviewed like any other.
