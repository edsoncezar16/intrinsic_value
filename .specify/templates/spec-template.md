# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Affected Pipeline Layers *(mandatory)*

<!--
  Mark every layer this feature touches. A change to a mart requires marking
  Gold AND any Silver models it depends on that need updating.
-->

| Layer | Module | Affected? | Notes |
|-------|--------|-----------|-------|
| Bronze | `ingestion/` | ☐ Yes / ☐ No | dlt pipeline changes |
| Silver | `transformation/models/staging/` | ☐ Yes / ☐ No | staging model changes |
| Gold | `transformation/models/marts/` | ☐ Yes / ☐ No | mart model / macro changes |
| Orchestration | `orchestration/` | ☐ Yes / ☐ No | Dagster asset / job / resource changes |
| App | `app/` | ☐ Yes / ☐ No | Streamlit page / helper changes |

**Data contract impact**: ☐ Additive only (safe) / ☐ Breaking change (requires downstream coordination)

---

## User Scenarios & Testing *(mandatory)*

<!--
  User stories should be prioritized journeys ordered by importance.
  Each story must be independently testable — implementing one alone should
  still yield a usable result.

  For data pipeline features, "user" may be an analyst querying the mart,
  a Dagster run materializing an asset, or an end user of the Streamlit app.
-->

### User Story 1 — [Brief Title] (Priority: P1)

[Describe this journey in plain language — who does what and what they see]

**Why this priority**: [Value delivered and why it comes first]

**Independent Test**: [How to verify this story works on its own — e.g., "Run `uv run dbt run -s intrinsic_value` and query the mart; column X is present and non-null"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 — [Brief Title] (Priority: P2)

[Describe this journey]

**Why this priority**: [Value and rationale]

**Independent Test**: [How to verify independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed]

### Edge Cases

- What happens when a ticker has no yfinance data (e.g., delisted stock)?
- What happens when a dlt load produces zero rows?
- What happens when [boundary condition specific to this feature]?
- How does the Streamlit app behave when the mart returns no qualifying companies?

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific capability]
- **FR-002**: System MUST [specific capability]
- **FR-003**: [Additional requirement]

### dbt / Data Requirements *(include if transformation layer is affected)*

- New models MUST have `not_null` and `unique` tests on `ticker` in their `_models.yml`
- New sources MUST be declared in a `_<source>__sources.yml` file under the relevant staging folder
- Column names MUST follow `snake_case`
- [Any feature-specific data contract requirement]

### App Requirements *(include if app layer is affected)*

- UI changes MUST support both Portuguese (BR) and English label sets via `app/helpers/lang.py`
- New pages MUST be placed in `app/pages/` and follow the existing Streamlit multipage convention
- [Any feature-specific UI requirement]

### Key Entities *(include if feature introduces new data)*

- **[Entity]**: [What it represents, key attributes, which layer it lives in]

---

## Success Criteria *(mandatory)*

- **SC-001**: [Measurable outcome — e.g., "Mart query returns intrinsic value for all tickers in the Google Sheet within 5s"]
- **SC-002**: [Data quality outcome — e.g., "No null values in `margin_of_safety` for companies with positive earnings"]
- **SC-003**: [User-facing outcome — e.g., "Portfolio page displays correct share counts for a given capital input"]

---

## Assumptions

- [e.g., "Google Sheet schema remains unchanged"]
- [e.g., "MotherDuck connection is available during Dagster runs"]
- [e.g., "yfinance returns `regularMarketPreviousClose` for all B3 tickers in the sheet"]
- [Any scope boundary — e.g., "Mobile layout is out of scope"]
