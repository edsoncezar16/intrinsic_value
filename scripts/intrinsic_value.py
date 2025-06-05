def compute_intrinsic_value(
    past_5yr_net_earnings: float,
    current_5yr_net_earnings: float,
    risk_free_rate: float,
    terminal_growth_rate: float = 0.0378,
) -> float:
    """Computes the intrinsic value of a company based on a two-stage discounted cash flow:

    1. First stage with a 10 years transient period with growth at the arithmetic mean between
    the terminal growth rate and the observed growth rate.

    2. Steady-state with a terminal growth rate.

    Parameters:
        past_5yr_net_earnings: rolling 20Q window cumulative net earnings ending 40 quarters back.

        current_5yr_net_earnings: rolling 20Q window cumulative net earnings ending on the last quarter.

        risk_free_rate: an interest rate that we could safely achieve if we were to choose a fixed-income investment.
        For B3, could be taken as the long-term inflation-protected government bond.

        terminal_growth_rate: a very conservative estimate of the long-term growth rate for a company.
        For B3, could be taken from this -> https://data.worldbank.org/indicator/NY.GDP.MKTP.KD?end=2023&locations=BR&start=1960&view=chart
        Whence the default value given.

    Returns:
        The intrinsic value as the discounted cash flow with the given parameters.
    """
    observed_growth_rate: float = (
        current_5yr_net_earnings / past_5yr_net_earnings
    ) ** (1.0 / 10.0) - 1.0

    transient_period_growth_rate: float = (
        terminal_growth_rate + observed_growth_rate
    ) / 2.0
    transient_geometric_factor: float = (1.0 + transient_period_growth_rate) / (
        1.0 + risk_free_rate
    )
    transient_period_factor: float = 0.0
    for i in range(1, 11):
        transient_period_factor += transient_geometric_factor**i
    # second stage
    steady_period_factor: float = (1.0 + terminal_growth_rate) / (risk_free_rate - terminal_growth_rate)
    return (
        current_5yr_net_earnings
        / 5.0
        * (
            transient_period_factor
            + (1.0 + transient_period_growth_rate) ** 10 * steady_period_factor
        )
    )


def main() -> None:
    past_earnings: str = input(
        "Enter with the 5yr cumulative net earnings of the company from 10 years ago: "
    )
    current_earnings: str = input(
        "Enter with the 5yr avg net earnings of the company from the last year: "
    )
    interest_rate: str = input("Enter with your desired risk-free rate for discount: ")
    intrinsic_value: float = compute_intrinsic_value(
        float(past_earnings),
        float(current_earnings),
        float(interest_rate),
    )
    print(f"\nThe computed intrinsic value was: {round(intrinsic_value)}")


if __name__ == "__main__":
    main()
