# Git Commit

Inspect changes and commit following Conventional Commits. Only commit when explicitly asked.

## Step 1 — Inspect (run in parallel)

```bash
git status
git diff
git diff --staged
git log -5 --oneline
```

## Step 2 — Secret scan

Before staging anything, check for:

**Files (never stage):** `.env`, `.env.*`, `*.pem`, `*.key`, `credentials.json`, `serviceAccount*.json`, `firebase-adminsdk*.json`, `secrets.toml`, `.pypirc`

**Content patterns in diff:** `sk-`, `AKIA`, `AIza`, `ghp_`, `gho_`, `xoxb-`, PEM block headers, passwords/tokens in URLs or config literals

If found: STOP, warn the user with file path + pattern (not the value), suggest `.gitignore` or env vars, only proceed after explicit user confirmation.

## Step 3 — Commit format

```
<type>(<optional scope>): <short imperative summary>

<optional body — why, not what>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `build`, `perf`

**Scopes:** `frontend`, `scraper`, `backend` — omit if cross-cutting

**Rules:** imperative mood, ≤72 chars, no trailing period, body only when "why" isn't obvious from the diff

**Examples:**
- `feat(scraper): add DeepMind blog parser`
- `fix(frontend): prevent duplicate article cards`
- `chore: update firebase deploy config`

## Step 4 — Multiple commits

Split when changes are logically independent (feature + tests, refactor + feature, chore + feat):

1. `git add <paths>` for first logical group
2. Commit with its message
3. `git status` to verify
4. Repeat for remaining groups

## Step 5 — Execute

```bash
git add <relevant-files>
git commit -m "$(cat <<'EOF'
type(scope): summary

Optional body.
EOF
)"
git status
```

Never: modify `git config`, use `--no-verify`, force-push to main, amend pushed commits.
