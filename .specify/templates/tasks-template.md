---
description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `data-model.md`, `contracts/`

**Organization**: Tasks are grouped by pipeline layer and then by user story. Complete lower layers before higher layers — Bronze before Silver before Gold before App.

## Format: `[ID] [P?] [Layer/Story] Description`

- **[P]**: Can run in parallel with other [P] tasks (different files, no shared state)
- **[Layer]**: Which module this task belongs to — `[Bronze]`, `[Silver]`, `[Gold]`, `[Orch]`, `[App]`
- **[Story]**: Which user story (US1, US2, US3…)
- Include exact file paths in every task description

## Key Commands

```bash
# Dependency management
uv sync                          # install/update all deps
uv add <package>                 # add a new dep to pyproject.toml

# dbt (run from project root)
uv run dbt run   --profiles-dir transformation --project-dir transformation -s <selector>
uv run dbt test  --profiles-dir transformation --project-dir transformation -s <selector>
uv run dbt ls    --profiles-dir transformation --project-dir transformation -s <selector>

# Dagster local dev
uv run dagster dev               # starts UI at http://localhost:3000

# Streamlit local dev
cd app && streamlit run Intrinsic.py

# dlt pipeline (run directly)
uv run python -m ingestion.<pipeline_module>
```

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration only.
  
  Replace them with actual tasks based on:
  - Affected layers from spec.md (Bronze / Silver / Gold / Orchestration / App)
  - User stories from spec.md (with priorities P1, P2, P3…)
  - Entities from data-model.md
  - Contracts from contracts/
  
  Follow the layer ordering: Bronze → Silver → Gold → Orchestration → App.
  Within a layer, group by user story so each story is independently testable.
  DO NOT keep these sample tasks in the generated tasks.md.
  ============================================================================
-->

---

## Phase 1: Setup

**Purpose**: Branch and environment preparation — always required.

- [ ] T001 Verify `uv sync` installs cleanly on this branch
- [ ] T002 [P] Run `uv run dbt ls --profiles-dir transformation --project-dir transformation` to confirm current manifest is valid
- [ ] T003 [P] Confirm local DuckDB file exists at `intrinsic.duckdb` or create it via a Dagster materialize

---

## Phase 2: Bronze — Ingestion Changes *(skip if no ingestion changes)*

**Purpose**: Add or modify dlt pipelines that write raw data to DuckDB/MotherDuck.

**Checkpoint**: Raw table(s) visible in DuckDB after running the pipeline.

- [ ] T010 [Bronze] [US1] Create/modify pipeline in `ingestion/<pipeline>.py`
- [ ] T011 [Bronze] [US1] Update `ingestion/destination.py` if destination config changes
- [ ] T012 [Bronze] [US1] Run pipeline locally and verify raw table in DuckDB: `uv run python -m ingestion.<module>`
- [ ] T013 [P] [Bronze] [US2] Additional Bronze task (if applicable)

---

## Phase 3: Silver — Staging Models *(skip if no new sources or column changes)*

**Purpose**: Add or update dbt staging models that clean and rename raw fields.

**Checkpoint**: `uv run dbt run -s staging.*` succeeds; `uv run dbt test -s staging.*` passes.

- [ ] T020 [Silver] [US1] Create/update `transformation/models/staging/<source>/_<source>__sources.yml`
- [ ] T021 [Silver] [US1] Create/update `transformation/models/staging/<source>/stg_<source>__<resource>.sql`
- [ ] T022 [Silver] [US1] Add `not_null` + `unique` tests on primary key in `_<source>__models.yml`
- [ ] T023 [Silver] [US1] Run and test: `uv run dbt run --profiles-dir transformation --project-dir transformation -s stg_<source>__<resource>`

---

## Phase 4: Gold — Mart Models *(skip if no mart changes)*

**Purpose**: Add or update dbt mart models with business logic (joins, calculations, margin of safety).

**Checkpoint**: `uv run dbt run -s marts.*` succeeds; mart query returns expected rows.

- [ ] T030 [Gold] [US1] Create/update `transformation/models/marts/app/<mart>.sql`
- [ ] T031 [Gold] [US1] Update `transformation/models/marts/app/_app__models.yml` with docs + tests
- [ ] T032 [Gold] [US1] Add/update macros in `transformation/macros/` if formula changes
- [ ] T033 [Gold] [US1] Run and test: `uv run dbt run --profiles-dir transformation --project-dir transformation -s <mart>` then `dbt test -s <mart>`

---

## Phase 5: Orchestration *(skip if no Dagster asset or job changes)*

**Purpose**: Update Dagster asset definitions to reflect new/changed dlt sources or dbt models.

**Checkpoint**: `uv run dagster dev` starts without errors; affected assets appear in the UI and materialize successfully.

- [ ] T040 [Orch] [US1] Update `orchestration/defs/ingestion.py` if new dlt assets (asset keys, group names, deps)
- [ ] T041 [Orch] [US1] Update `orchestration/defs/transformation.py` if dbt project structure changed
- [ ] T042 [Orch] [US1] Update `orchestration/definitions.py` if new resources are needed
- [ ] T043 [Orch] [US1] Start `uv run dagster dev`, navigate to asset graph, materialize affected assets, verify no errors

---

## Phase 6: App — Streamlit UI *(skip if no UI changes)*

**Purpose**: Update the Streamlit app to surface new data or new functionality.

**Checkpoint**: `streamlit run Intrinsic.py` starts; feature is visible and functional in both PT-BR and EN.

- [ ] T050 [App] [US1] Add PT-BR + EN label strings to `app/helpers/lang.py`
- [ ] T051 [App] [US1] Add query/load logic in `app/helpers/load.py` if new DuckDB query needed
- [ ] T052 [App] [US1] Implement UI in `app/pages/<page>.py` or update `app/Intrinsic.py`
- [ ] T053 [App] [US1] Start app locally (`cd app && streamlit run Intrinsic.py`), verify PT-BR layout
- [ ] T054 [App] [US1] Switch language selector to EN, verify EN layout
- [ ] T055 [App] [US1] Update `app/requirements.txt` if new app-layer dependencies were added

---

## Phase 7: Polish & Cross-Cutting

**Purpose**: Housekeeping that spans multiple layers.

- [ ] TXXX [P] Update `CLAUDE.md` if architecture or commands have changed
- [ ] TXXX Run full pipeline end-to-end per `quickstart.md` and verify output
- [ ] TXXX Confirm all dbt tests pass: `uv run dbt test --profiles-dir transformation --project-dir transformation`
- [ ] TXXX Confirm CI `deploy.yml` will pick up all changed files (check `paths-ignore` in workflow)

---

## Dependencies & Execution Order

### Layer Dependencies (non-negotiable)

```text
Phase 1: Setup
    └── Phase 2: Bronze    (if applicable)
            └── Phase 3: Silver    (if applicable)
                    └── Phase 4: Gold    (if applicable)
                            └── Phase 5: Orchestration    (if applicable)
                                    └── Phase 6: App    (if applicable)
                                            └── Phase 7: Polish
```

### Within Each Layer

- Source YAML declarations before model SQL
- Model SQL before `_models.yml` tests
- dbt `run` before `test`

### Parallel Opportunities

- Tasks marked [P] within the same phase can run simultaneously
- App label strings (`lang.py`) and query helpers (`load.py`) can be written in parallel with Gold models
- Documentation updates (Phase 7) can begin in parallel once the layer they document is complete

---

## Notes

- Skip any phase whose layer is not listed as affected in `spec.md`
- `[P]` = different files, no shared mutable state — safe to run in parallel
- Commit after each phase checkpoint, not after every individual task
- If a dbt model change is breaking (column removed/renamed), coordinate all downstream updates in the same commit
- Stop at any phase checkpoint to validate independently before proceeding
