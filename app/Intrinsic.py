import streamlit as st
from helpers import state, lang

st.set_page_config(page_title="Intrinsic", layout="wide")

# Initialize session state and language
state.init_session_state()
lang_code = state.language_selector()
L = lang.get_labels()[lang_code]

# ---- Page Content ----
if lang_code == "Português (BR)":
    st.title("Intrinsic")

    st.write(
        "Uma ferramenta para construção de portfólios de ações com base na margem de segurança, voltada ao mercado brasileiro."
    )

    st.header("Metodologia")

    st.markdown(
        """
        Este aplicativo estima o **valor intrínseco** das ações utilizando um modelo de **Desconto de Dividendos em Dois Estágios (DDM)**, conforme apresentado no livro
        [*Corporate Finance – 4ª Edição*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779), de Ross, Westerfield e Jaffe.
        
        A **margem de segurança (MoS)** é calculada como:

        $$
        \\text{MoS} = 1 - \\frac{\\text{Preço de Mercado}}{\\text{Valor Intrínseco}}
        $$

        O modelo distingue dois regimes de avaliação com base na taxa de crescimento implícita:

        - Seja \\( g = (1 - d/e) \\cdot ROE \\)

        - **Se** \\( g < g_t \\): usa-se o **modelo de crescimento perpétuo de Gordon**:

        $$
        V = d \\cdot \\frac{1 + g}{r - g}
        $$

        - **Se** \\( g \\geq g_t \\): aplica-se um modelo de dois estágios com ajuste no payout:

            1. Fase transitória de \\( n \\) anos com alto crescimento  
            2. Valor terminal com crescimento perpétuo \\( g_t \\), ajustado para convergência no payout

        O dividendo terminal é ajustado para refletir a transição do payout inicial \\( 1 - g/ROE \\) ao payout terminal \\( 1 - g_t/ROE \\).
        """
    )

    st.header("Agradecimentos")
    st.markdown(
        """
        O autor agradece aos mantenedores dos sites
        [Fundamentus](https://www.fundamentus.com.br/index.php) e [TradingView](https://br.tradingview.com), que fornece dados fundamentais estruturados e confiáveis sobre ações brasileiras.
        """
    )

else:
    st.title("Intrinsic")

    st.write(
        "A portfolio construction tool for value investing on the Brazilian Stock Exchange, based on the concept of margin of safety (MoS)."
    )

    st.header("Methodology")

    st.markdown(
        """
        The app estimates the intrinsic value of stocks based on a **two-stage dividend discount model (DDM)**, as detailed in
        [*Corporate Finance (4th Edition), by Ross, Westerfield, and Jaffe*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779).

        The **margin of safety (MoS)** is calculated as:

        $$
        \\text{MoS} = 1 - \\frac{\\text{Market Price}}{\\text{Intrinsic Value}}
        $$

        The model switches based on the implied growth rate \\( g = (1 - d/e) \\cdot ROE \\):

        - **If** \\( g < g_t \\), use the perpetual growth formula:

        $$
        V = d \\cdot \\frac{1 + g}{r - g}
        $$

        - **If** \\( g \\geq g_t \\), use a two-stage approach with payout scaling:
            1. Transient growth for \\( n \\) years  
            2. Terminal value scaled for long-run payout convergence

        The final dividend is adjusted to reflect the transition from initial to terminal payout.
        """
    )

    st.header("Acknowledgements")
    st.markdown(
        """
        The author thanks the maintainers of
        [Fundamentus](https://www.fundamentus.com.br/index.php) and [TradingView](https://br.tradingview.com), which provides structured access to reliable
        fundamental data for Brazilian equities.
        """
    )
