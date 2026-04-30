# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]  
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command.

---

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

---

## Technical Context

| Field | Value |
|-------|-------|
| **Language** | Python 3.12 |
| **Package manager** | uv (`pyproject.toml` + `uv.lock`) |
| **Orchestration** | Dagster 1.11+ / Dagster Cloud (serverless PEX) |
| **Ingestion** | dlt with MotherDuck destination |
| **Transformation** | dbt-core + dbt-duckdb |
| **Database** | DuckDB (local dev) / MotherDuck (prod) |
| **App framework** | Streamlit |
| **Testing** | dbt YAML schema tests; no pytest currently |
| **CI/CD** | GitHub Actions (`deploy.yml`, `branch_deployments.yml`) |
| **Affected layers** | [Bronze / Silver / Gold / Orchestration / App — from spec] |

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] **I. Medallion Integrity** — Data flows Bronze → Silver → Gold with no layer skipped
- [ ] **II. Module Separation** — Dependency direction `ingestion → transformation → orchestration ← app` respected
- [ ] **III. Data Contract Safety** — Breaking changes (column renames/removals) are coordinated across all downstream layers in this branch
- [ ] **IV. Naming Conventions** — `snake_case` Python files, `stg_<source>__<resource>` staging models, `_<source>__models.yml` YAML files
- [ ] **V. Commit Style** — Conventional Commits used; scope prefix added if module-specific
- [ ] **VI. Dependency Management** — New deps added via `uv add`; `app/requirements.txt` updated if app layer is affected
- [ ] **VII. Testing** — New mart models have `not_null` + `unique` tests on `ticker` in their `_models.yml`
- [ ] **VIII. CI/CD** — Understand whether this change triggers `deploy.yml` (orchestration), Streamlit deploy (app), or both

---

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (if new entities)
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks command)
```

### Source Code (affected modules only — delete unused sections)

```text
# Bronze layer (ingestion)
ingestion/
├── <new_pipeline>.py         # new dlt pipeline
└── destination.py            # shared MotherDuck destination (rarely changes)

# Silver layer (transformation/staging)
transformation/models/staging/<source>/
├── _<source>__sources.yml    # source declaration
├── _<source>__models.yml     # model docs + tests
└── stg_<source>__<resource>.sql

# Gold layer (transformation/marts)
transformation/models/marts/app/
├── _app__models.yml          # model docs + tests
└── <mart_model>.sql

# Macros (if intrinsic value formula changes)
transformation/macros/
└── <macro_name>.sql

# Orchestration
orchestration/defs/
├── ingestion.py              # dlt asset definitions
└── transformation.py         # dbt asset definitions

# App
app/
├── Intrinsic.py              # main page
├── pages/<new_page>.py       # new Streamlit page (if any)
└── helpers/
    ├── lang.py               # PT-BR / EN label strings
    ├── load.py               # DuckDB query helpers
    └── state.py              # session state helpers
```

---

## Phase 0: Research

*Goal: understand what already exists before writing any code.*

- [ ] Read existing models/pipelines in all affected layers
- [ ] Check dbt manifest for current asset dependencies: `uv run dbt ls --select <model>`
- [ ] Verify MotherDuck schema in dev: `uv run dagster dev` → inspect asset catalog
- [ ] Identify any breaking changes vs. additive changes

---

## Phase 1: Design

*Goal: produce the data model, contracts, and quickstart before any implementation.*

### Data Model (`data-model.md`)

- Source tables affected and their schemas
- New or modified dbt models and their columns
- Mart output shape (columns, types, grain)

### Contracts (`contracts/`)

- dbt source YAML declarations for any new raw tables
- dbt model YAML with column-level docs and tests
- App query interface (SQL or SQLAlchemy used in `app/helpers/load.py`)

### Quickstart (`quickstart.md`)

Commands to run the feature end-to-end in a local environment:

```bash
# 1. Install / sync deps
uv sync

# 2. Run ingestion (if Bronze layer changes)
uv run python -m ingestion.<pipeline_module>

# 3. Run dbt (if Silver/Gold changes)
uv run dbt run --profiles-dir transformation --project-dir transformation -s <model_selector>
uv run dbt test --profiles-dir transformation --project-dir transformation -s <model_selector>

# 4. Start Dagster locally (if orchestration changes)
uv run dagster dev

# 5. Start Streamlit app (if app changes)
cd app && streamlit run Intrinsic.py
```

---

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., mart reads from raw table] | [reason] | [why staging model is insufficient] |
