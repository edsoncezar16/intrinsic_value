{% macro compute_intrinsic_value(
    past_5yr_net_earnings,
    current_5yr_net_earnings,
    risk_free_rate,
    terminal_growth_rate
) %}
    {% set obs_growth_expr = "(" ~ current_5yr_net_earnings ~ "::float / " ~ past_5yr_net_earnings ~ "::float) ^ (1.0 / 10.0) - 1.0" %}
    {% set transient_growth_expr = "(" ~ terminal_growth_rate ~ " + (" ~ obs_growth_expr ~ ")) / 2.0" %}
    {% set geom_factor_expr = "(1.0 + (" ~ transient_growth_expr ~ ")) / (1.0 + " ~ risk_free_rate ~ ")" %}

    {% set transient_terms = [] %}
    {% for i in range(1, 11) %}
        {% do transient_terms.append("POWER(" ~ geom_factor_expr ~ ", " ~ i ~ ")") %}
    {% endfor %}
    {% set transient_sum_expr = transient_terms | join(' + ') %}

    {% set steady_factor_expr = "POWER(1.0 + (" ~ transient_growth_expr ~ "), 10) * (1.0 + " ~ terminal_growth_rate ~ ") / (" ~ risk_free_rate ~ " - " ~ terminal_growth_rate ~ ")" %}

    case
        when {{ past_5yr_net_earnings }} <= 0
          or {{ current_5yr_net_earnings }} <= 0
          or {{ past_5yr_net_earnings }} is null
          or {{ current_5yr_net_earnings }} is null
        then 0.0
        else (
            ({{ current_5yr_net_earnings }}::float / 5.0)
            * ({{ transient_sum_expr }} + {{ steady_factor_expr }})
        )
    end
{% endmacro %}
