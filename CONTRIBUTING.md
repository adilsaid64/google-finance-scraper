# Contributing

## Development Setup

1. Clone the repository
2. Install [uv](https://docs.astral.sh/uv/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Install the project and dev dependencies (creates `.venv` and uses `uv.lock` when present):

   ```bash
   uv sync --extra dev
   ```

   Equivalent to what CI does:

   ```bash
   uv venv
   uv pip install -e ".[dev]"
   ```

4. (Optional) Install pre-commit hooks: `uv run pre-commit install`

## Code Style

- Use Ruff for lint and format; run it via `uv run` so you use the same tools as CI.
- Pre-commit hooks will run automatically on commit (if installed).
- Follow conventional commits for commit messages.

## Local checks (same as CI)

After `uv sync --extra dev`, run:

```bash
uv run ruff check --exit-non-zero-on-fix src/
uv run ruff format --check src/
uv run pytest -q
```

The quickstart step (live network):

```bash
uv run python examples/quickstart.py
```

You can chain the CI-equivalent checks (no network) in one line:

```bash
uv run ruff check --exit-non-zero-on-fix src/ && uv run ruff format --check src/ && uv run pytest -q
```

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new features (minor version bump)
- `fix:` bug fixes (patch version bump)
- `perf:` performance improvements (patch version bump)
- `refactor:` code refactoring (patch version bump)
- `docs:` documentation changes (no version bump)
- `test:` adding tests (no version bump)
- `chore:` maintenance tasks (no version bump)

Breaking changes: Add `!` after type (major version bump)
