{% macro compute_intrinsic_value(
        d,
        e,
        roe,
        r,
        gt,
        n
    ) %}
    {# Compute growth rate g = (1 - d/e) * roe #}
    {% set g = (1 - (d / e)) * roe %}
    {% if g < gt %}
        {{ d * (
            1 + g
        ) / (
            r - g
        ) }}
    {% else %}
        {# Transient factor = sum of discounted growing dividends #}
        {% set transient_factor = 0 %}
        {% for i in range(
                1,
                n + 1
            ) %}
            {% set term = d * ((1 + g) / (1 + r)) ** i %}
            {% set transient_factor = transient_factor + term %}
        {% endfor %}

        {# Final year dividend #}
        {% set d_n = d * (
            1 + g
        ) ** n %}
        {# Payout ratios #}
        {% set payout_ratio_now = 1 - g / roe %}
        {% set payout_ratio_terminal = 1 - gt / roe %}
        {% set payout_scale = payout_ratio_terminal / payout_ratio_now %}
        {# Adjusted terminal dividend and terminal value #}
        {% set adjusted_terminal_dividend = d_n * payout_scale %}
        {% set terminal_value = adjusted_terminal_dividend * (
            1 + gt
        ) / (
            r - gt
        ) %}
        {% set terminal_pv = terminal_value / (
            1 + r
        ) ** n %}
        {{ transient_factor + terminal_pv }}
    {% endif %}
{% endmacro %}
