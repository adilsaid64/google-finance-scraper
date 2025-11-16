# Contributing

## Development Setup

1. Clone the repository
2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Create virtual environment: `uv venv`
4. Activate environment: `source .venv/bin/activate`
5. Install in development mode: `uv pip install -e ".[dev]"`
6. Install pre-commit hooks: `pre-commit install`

## Code Style

- Use `ruff` for linting and formatting: `ruff check src/` and `ruff format src/`
- Pre-commit hooks will run automatically on commit
- Follow conventional commits for commit messages

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
