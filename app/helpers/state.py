import streamlit as st

DEFAULT_LANG = "Português (BR)"
LANG_OPTIONS = ["Português (BR)", "English"]

DEFAULT_ALLOCATION_MODE = "Ações individuais"
ALLOCATION_OPTIONS = {
    "Português (BR)": ["Lotes padrão da B3 (100 ações)", "Ações individuais"],
    "English": ["Standard B3 lots (100 shares)", "Individual shares"],
}


def init_session_state():
    """Initialize session state for language and allocation mode."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = DEFAULT_LANG
    if "allocation_mode" not in st.session_state:
        st.session_state["allocation_mode"] = DEFAULT_ALLOCATION_MODE


def language_selector():
    """Render a language selector and update session state."""
    lang = st.selectbox(
        "Idioma / Language",
        LANG_OPTIONS,
        index=LANG_OPTIONS.index(st.session_state["lang"]),
    )
    st.session_state["lang"] = lang
    return lang


def allocation_mode_selector(label: str):
    """Render allocation mode radio button based on current language."""
    lang = st.session_state["lang"]
    options = ALLOCATION_OPTIONS[lang]
    default = st.session_state.get("allocation_mode", options[0])

    mode = st.radio(
        label,
        options=options,
        index=options.index(default),
        horizontal=True,
    )
    st.session_state["allocation_mode"] = mode
    return mode
