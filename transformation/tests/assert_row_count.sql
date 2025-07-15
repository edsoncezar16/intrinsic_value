-- tests/assert_row_count_is_one.sql
-- This test fails if the input relation does not contain exactly given row(s).
-- It works for both sources and models.
-- Usage:
--   - assert_row_count: {count: 1}
--   - assert_row_count: {count: 5}
{% set expected = config.get(
    'count',
    0
) %}
SELECT
    1
FROM
    {{ ref(
        model.name
    ) if model.resource_type == 'model'
    ELSE source(
        model.source_name,
        model.name
    ) }}
HAVING
    COUNT(*) != {{ expected }}
