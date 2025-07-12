import streamlit as st

st.set_page_config(page_title="Intrinsic", layout="wide")

# Language selector
lang = st.selectbox("Language / Idioma", ["English", "Português (BR)"], index=0)

# --- English content ---
if lang == "English":
    st.title("Intrinsic")

    st.write(
        "A portfolio construction tool for value investing on the Brazilian Stock Exchange, based on the principle of margin of safety (MoS)."
    )

    st.header("Methodology")

    st.markdown(
        """
        This app estimates the intrinsic value of stocks using a **two-stage dividend discount model (DDM)**, based on the approach presented in
        [*Corporate Finance (4th Edition)*](https://www.amazon.com/Corporate-Finance-Stephen-Ross/dp/0078034779) by Ross, Westerfield, and Jaffe.
        
        The **margin of safety (MoS)** is defined as:

        $$
        \\text{MoS} = 1 - \\frac{\\text{Market Price}}{\\text{Intrinsic Value}}
        $$

        The model distinguishes two valuation regimes based on the implied growth rate:

        - Let \\( g = (1 - d/e) \\cdot ROE \\)

        - **If** \\( g < g_t \\): use the **Gordon Growth Model**:

        $$
        V = d \\cdot \\frac{1 + g}{r - g}
        $$

        - **If** \\( g \\geq g_t \\): apply a two-stage DDM with payout scaling:

            1. Transient phase: \\( n \\) years of high growth  
            2. Terminal phase: perpetual growth at \\( g_t \\), adjusted for converging payout

        The terminal dividend is scaled to reflect the transition from initial payout \\( 1 - g/ROE \\) to terminal payout \\( 1 - g_t/ROE \\):

        $$
        \\text{Payout Scale} = \\frac{1 - g_t / ROE}{1 - g / ROE}
        $$

        Full formula:

        $$
        V = \\sum_{i=1}^{n} d \\cdot \\left(\\frac{1 + g}{1 + r}\\right)^i
        + \\left[d \\cdot (1 + g)^n \\cdot \\text{Payout Scale} \\cdot \\frac{1 + g_t}{r - g_t}\\right] \\cdot \\left(\\frac{1}{1 + r}\\right)^n
        $$

        *Note: If dividends or earnings are negative, intrinsic value is conservatively set to zero.*
        """
    )

    st.header("Portfolio Construction")

    st.markdown(
        """
        Only companies with **margin of safety above 50%** are included.

        Portfolio weights are computed with:

        $$
        \\text{Weight} = 2 \\times \\text{MoS} - 1
        $$

        Final weights are normalized to 1, and share counts are based on the user-defined total capital.
        """
    )

    st.header("Acknowledgements")

    st.markdown(
        """
        The author thanks the maintainers of [Fundamentus](https://www.fundamentus.com.br/index.php), which provides structured and reliable access to the fundamentals of Brazilian public companies.
        """
    )

# --- Brazilian Portuguese content ---
else:
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

        O dividendo terminal é ajustado para refletir a transição do payout inicial \\( 1 - g/ROE \\) ao payout terminal \\( 1 - g_t/ROE \\):

        $$
        \\text{Fator de Escala} = \\frac{1 - g_t / ROE}{1 - g / ROE}
        $$

        Fórmula completa:

        $$
        V = \\sum_{i=1}^{n} d \\cdot \\left(\\frac{1 + g}{1 + r}\\right)^i
        + \\left[d \\cdot (1 + g)^n \\cdot \\text{Fator de Escala} \\cdot \\frac{1 + g_t}{r - g_t}\\right] \\cdot \\left(\\frac{1}{1 + r}\\right)^n
        $$

        *Nota: Caso dividendos ou lucros sejam negativos, o valor intrínseco é fixado em zero por precaução.*
        """
    )

    st.header("Construção do Portfólio")

    st.markdown(
        """
        Apenas empresas com **margem de segurança superior a 50%** são incluídas.

        Os pesos do portfólio são calculados com:

        $$
        \\text{Peso} = 2 \\times \\text{MoS} - 1
        $$

        Os pesos finais são normalizados para somar 1, e o número de ações a comprar é calculado com base no capital total informado pelo usuário.
        """
    )

    st.header("Agradecimentos")

    st.markdown(
        """
        Agradecimentos aos mantenedores do site [Fundamentus](https://www.fundamentus.com.br/index.php), que oferecem acesso estruturado e confiável aos fundamentos das empresas listadas na B3.
        """
    )
