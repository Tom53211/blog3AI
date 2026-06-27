# Claude Code Instructions

## Committing

Use `/commit` for the full commit workflow.

Key rules always in effect:
- Run `git status` + `git diff` before committing — never guess what changed
- Use [Conventional Commits](https://www.conventionalcommits.org/) format: `type(scope): summary`
- Scopes for this project: `frontend`, `scraper`, `backend` — omit if cross-cutting
- Split logically independent changes into separate commits
- Never commit `.env`, `*.pem`, `*.key`, `credentials.json`, or any secret/credential file
- Never push unless explicitly asked

Pre-commit hooks run `detect-secrets` — if they fire, stop and investigate before retrying.
