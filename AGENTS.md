# Agent Instructions

When committing changes, follow `.cursor/rules/git-commits.mdc`:

- Inspect changes with `git status` and `git diff` before committing
- Use [Conventional Commits](https://www.conventionalcommits.org/) format
- Split into multiple commits when changes are logically independent
- Never commit secrets or sensitive files (`.env`, keys, credentials)

Pre-commit hooks run `detect-secrets` to block accidental secret commits.
