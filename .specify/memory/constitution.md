# Intrinsic Value Constitution

## I. Medallion Layer Integrity

Every piece of data flows through exactly three layers and no layer may be skipped:

- **Bronze** (`ingestion/`) — raw loads only; no business logic; dlt pipelines write to `google_sheets.*` and `yfinance.*` schemas
- **Silver** (`transformation/models/staging/`) — clean and rename raw fields; one staging model per source table; no joins across sources
- **Gold** (`transformation/models/marts/`) — business logic and joins live here; materialized as tables in the `analytics` schema

A feature that touches Gold MUST trace its inputs back to Silver; Silver MUST trace to Bronze. Cross-layer shortcuts (e.g., a mart reading directly from a raw dlt table) are forbidden.

## II. Module Separation and Dependency Direction

The four modules form a strict one-way dependency chain:

```
ingestion → transformation → orchestration ← app
```

- `ingestion/` has no imports from other project modules
- `transformation/` (dbt) depends only on tables produced by `ingestion/`
- `orchestration/` imports from both `ingestion/` and wraps `transformation/`
- `app/` reads only from DuckDB/MotherDuck; it MUST NOT import from `ingestion/`, `transformation/`, or `orchestration/`

Violating this direction introduces circular dependencies and breaks independent deployability.

## III. Data Contract Safety

dbt staging models and dlt pipelines define the data contracts for this project.

- Renaming or removing a column in a staging model is a **breaking change** — it requires updating all downstream mart models and the Streamlit app in the same feature branch
- Adding a new dlt source requires: a new `ingestion/` pipeline, a new `_sources.yml` entry, and at least one staging model
- All new dbt models MUST have a corresponding `_<source>__models.yml` entry with at minimum a description and a `not_null` test on the primary key

## IV. Naming Conventions

| Artifact | Convention | Example |
|----------|-----------|---------|
| Python files | `snake_case` | `yfinance_pipeline.py` |
| Python functions/variables | `snake_case` | `market_info`, `ingest_yfinance` |
| dbt staging models | `stg_<source>__<resource>` | `stg_yfinance__market_info` |
| dbt mart models | plain `snake_case` noun | `intrinsic_value` |
| dbt sources YAML | `_<source>__sources.yml` | `_yfinance__sources.yml` |
| dbt models YAML | `_<source>__models.yml` | `_yfinance__models.yml` |
| Dagster assets | descriptive group names matching layer | `bronze`, `silver`, `gold` |
| dbt schemas | `staging` (silver), `analytics` (gold) | — |

## V. Commit Style

All commits MUST follow Conventional Commits:

- `feat:` — new capability visible to users or analysts
- `fix:` — correction to existing behaviour
- `refactor:` — structural change with no behaviour change
- `chore:` — tooling, CI, dependency updates
- `docs:` — documentation only

Scope is optional but encouraged when the change is module-specific: `fix(ingestion):`, `feat(transformation):`, `chore(app):`.

## VI. Dependency Management

- All project dependencies are managed via `uv` using `pyproject.toml` and `uv.lock`
- The app has a separate `app/requirements.txt` for its Streamlit Cloud deployment — keep it in sync when adding app-layer dependencies
- Never pin a dependency without a comment explaining why (the existing `duckdb<1.3.0` pin exists for MotherDuck compatibility)
- Python version is 3.12; do not use syntax or APIs unavailable in 3.12

## VII. Testing

- dbt schema tests (YAML-based `not_null`, `unique`, `accepted_values`) are the primary test mechanism for the transformation layer
- New mart models MUST have at minimum `not_null` and `unique` tests on `ticker`
- Python unit tests (`pytest`) are not currently in use; if introduced, place them in `tests/` at the project root and register the command in CI
- Manual validation via `uv run dagster dev` and inspecting Dagster UI is the accepted integration test for orchestration changes

## VIII. CI/CD and Deployment

- The `deploy.yml` workflow deploys **orchestration only** on push to `main`; app changes are excluded via `paths-ignore`
- The app (`app/`) is deployed separately (Streamlit Cloud); changes there do not trigger the Dagster deploy
- The dbt manifest is cached in S3 (`intrinsic-value-dbt-manifests`) and must be regenerated via `dagster-dbt project prepare-and-package` before any dbt structural changes ship
- Branch deployments use a MotherDuck clone of prod; never write to `md:prod_*` directly in development

## Governance

This constitution supersedes all other practices in this repository. Any amendment requires:
1. Updating this file with the new rule
2. Updating `CLAUDE.md` if the change affects agent guidance
3. A `chore:` commit with a clear rationale

All feature specs and implementation plans must include a **Constitution Check** section that explicitly verifies compliance with sections I–VIII above.

**Version**: 1.0.0 | **Ratified**: 2026-04-30 | **Last Amended**: 2026-04-30
