{% macro compute_intrinsic_value(
    past_5yr_net_earnings,
    current_5yr_net_earnings,
    risk_free_rate,
    terminal_growth_rate
) %}
    -- transient period
    {% set obs_growth_expr = "(" ~ current_5yr_net_earnings ~ "::float / " ~ past_5yr_net_earnings ~ "::float) ^ (0.2) - 1.0" %}
    {% set transient_growth_expr = "(" ~ terminal_growth_rate ~ " + (" ~ obs_growth_expr ~ ")) / 2.0" %}
    {% set geom_factor_expr = "(1.0 + (" ~ transient_growth_expr ~ ")) / (1.0 + " ~ risk_free_rate ~ ")" %}
    {% set transient_terms = [] %}
    {% for i in range(1, 6) %}
        {% do transient_terms.append("POWER(" ~ geom_factor_expr ~ ", " ~ i ~ ")") %}
    {% endfor %}
    {% set transient_sum_expr = transient_terms | join(' + ') %}
    -- steady period
    {% set steady_sum_expr = "(1.0 + (" ~ terminal_growth_rate ~ ")) / ((" ~ risk_free_rate ~ ") - (" ~ terminal_growth_rate ~ "))" %}

    {% set steady_earnings_expr = "POWER(" ~ geom_factor_expr ~ ", 5)" %}

    case
        when {{ past_5yr_net_earnings }} <= 0
          or {{ current_5yr_net_earnings }} <= 0
          or {{ past_5yr_net_earnings }} is null
          or {{ current_5yr_net_earnings }} is null
        then 0.0
        else (
            ({{ current_5yr_net_earnings }}::float / 5.0)
            * ({{ transient_sum_expr }} + {{ steady_earnings_expr }} * {{ steady_sum_expr }})
        )
    end
{% endmacro %}
