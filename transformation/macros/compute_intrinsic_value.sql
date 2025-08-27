{% macro compute_intrinsic_value(
        d,
        e,
        roe,
        r,
        gt,
        n
    ) %}
    {% set growth_rate = "(1 - (" ~ d ~ " / NULLIF(" ~ e ~ ", 0))) * " ~ roe %}
    {% set payout_ratio_now = "1 - (" ~ growth_rate ~ " / " ~ roe ~ ")" %}
    {% set payout_ratio_terminal = "1 - (" ~ gt ~ " / " ~ roe ~ ")" %}
    {% set payout_scale = "(" ~ payout_ratio_terminal ~ ") / (" ~ payout_ratio_now ~ ")" %}
    {% set transient_term = " SELECT SUM(" ~ d ~ " * POWER(1 + (" ~ growth_rate ~ "), i) / POWER(1 + " ~ r ~ ", i)) FROM UNNEST(GENERATE_SERIES(1, " ~ n ~ ")) AS t(i) " %}
    {% set d_n = d ~ " * POWER(1 + (" ~ growth_rate ~ "), " ~ n ~ ")" %}
    {% set adjusted_terminal_dividend = "(" ~ d_n ~ ") * (" ~ payout_scale ~ ")" %}
    {% set terminal_value = "(" ~ adjusted_terminal_dividend ~ ") * (1 + " ~ gt ~ ") / (" ~ r ~ " - " ~ gt ~ ")" %}
    {% set terminal_pv = "(" ~ terminal_value ~ ") / POWER(1 + " ~ r ~ ", " ~ n ~ ")" %}
    (
        CASE
            WHEN {{ e }} <= 0 THEN 0
            WHEN {{ roe }} < 0 THEN 0
            WHEN {{ growth_rate }} < {{ gt }} THEN {{ d }} * (1 + ({{ growth_rate }})) / ({{ r }} - ({{ growth_rate }}))
            ELSE (
                {{ transient_term }}
            ) + (
                {{ terminal_pv }}
            )
        END
    )
{% endmacro %}
