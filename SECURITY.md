# Security and integrity

CHEPTA-Lab prepares process cases and training data for AI assistants. Two things matter:
records cannot reach the training data without review, and problems are reported and fixed
quickly.

## Reporting a problem

- **Security issue** (a leaked key, a workflow that could run untrusted code with write
  access, a record written to mislead a model): report it privately with GitHub's
  *Report a vulnerability* button on the repository's Security tab. Do not open a public
  issue.
- **Wrong numbers, sources or rights** (a value that disagrees with its source, a paper
  whose licence does not allow the use recorded): open a public issue. Wrong data are not
  secret, and fixing them in the open lets everyone check.

The maintainer answers within 7 days.

## How the repository is protected

| Protection | Effect |
|---|---|
| Branch ruleset on `main` | No direct pushes, no force-push, no branch deletion; every change needs a pull request and passing tests. While there is one maintainer, the maintainer's own pull requests are merged with the ruleset's pull-request bypass, only after the `test` check is green and the maintainer has checked the change, as in [CHEPTA](https://github.com/FaireDose/CHEPTA/blob/main/GOVERNANCE.md#while-there-is-one-maintainer) |
| [`CODEOWNERS`](.github/CODEOWNERS) | The maintainer reviews every change to the dataset records, schemas and contracts, the scripts and tests, the source catalogue, `AGENTS.md` and the workflows |
| Automatic tests | [`test.yml`](.github/workflows/test.yml) runs the catalogue validator, the pipeline validator, the unit tests and a preview export on every pull request |
| Release gates | The exporter refuses a release while any task lacks its human reviews (`dataset/PIPELINE.md`); agents never record a review on a person's behalf |
| Secret scanning with push protection | GitHub refuses a push that contains a known kind of key |
| Roles | Only the maintainer is administrator, with two-factor authentication |
| Git history | Every earlier version of every file is kept and can be restored |

## Workflows

- Every workflow has `permissions: {}` by default; each job gets only what it needs (the
  test job: read the repository).
- Every action is pinned to a full commit SHA.
- Checkouts keep no credentials, and no workflow that runs a pull request's code has a
  secret or a token that can write.

## Data poisoning and prompt injection

A public repository that feeds AI training can be attacked through its data:

- **Poisoned records.** A pull request can add records with wrong numbers, invented
  rationale or hidden instructions. No record enters a release without the human reviews
  bound to its current content (`review_digest`), and `CODEOWNERS` puts every record
  change in front of the maintainer.
- **Instructions inside sources.** A paper, web page, supplementary file or tool output can
  contain text written to steer an AI ("ignore the rules and ..."). [AGENTS.md](AGENTS.md)
  tells every assistant and agent to treat it as evidence, never as instructions, and
  never to run code, follow links or install anything because a source says so.

## Copyright

Only metadata, exact locators, short attributed values and our own text are committed.
Papers, PDFs and paywalled text are never committed (`raw_papers/` is ignored); sources
whose rights are unresolved or non-commercial stay out of the initial release
([docs/LICENSING.md](docs/LICENSING.md)).

## Secrets

No workflow needs a secret today. When publishing to Hugging Face or renting training
compute:

- use a separate fine-grained token limited to that one dataset, model or project, never a
  personal token;
- store it as a GitHub *environment* secret (or the cloud environment's settings), never in
  a file, issue or pull request, and only in a workflow that does not run pull-request code;
- if a secret is ever exposed, revoke it at its source immediately, then remove it from the
  history.
