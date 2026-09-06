import streamlit as st


def render_bottom_nav(active: str):
    """Fixed bottom navigation bar, shared by every page.

    active: one of "marks", "dashboard", "timetable", "performance"
    — whichever page is currently open gets highlighted.

    NOTE: this deliberately does NOT use st.columns. Streamlit's
    columns/horizontal-block implementation stacks vertically on
    narrow screens using internal testids/classes that turned out
    not to match what two rounds of guessing assumed. Instead we
    put four buttons directly inside st.container(key="bottom_nav")
    and force THAT container — which we've confirmed (via DevTools)
    reliably renders as div.stVerticalBlock with our st-key-* class,
    wrapping each widget in div[data-testid="stElementContainer"] —
    into a flex row ourselves. That's structure we know for certain
    exists on this Streamlit version, so it can't silently fail the
    way the columns-based approach did.
    """

    st.markdown("""
    <style>

    /* The container(key="bottom_nav") wrapper itself: pin it to the
       bottom of the screen, and lay its children out as a single
       row that can never wrap or stack, at any screen size. */
    div.stVerticalBlock[class*="st-key-bottom_nav"] {
        position: fixed !important;
        left: 50% !important;
        bottom: 0 !important;
        transform: translateX(-50%) !important;
        width: min(720px, 100%) !important;
        background: #171717 !important;
        border-top: 1px solid #292929 !important;
        padding: 8px 10px 10px 10px !important;
        z-index: 999999 !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 4px !important;
    }

    /* Each button's own wrapper — one per nav icon — shares the
       row equally instead of stacking. */
    div.stVerticalBlock[class*="st-key-bottom_nav"] > div[data-testid="stElementContainer"] {
        flex: 1 1 0px !important;
        width: auto !important;
        min-width: 0 !important;
    }

    /* Icon buttons inside the nav bar — sized on the small side so
       the bar stays compact and doesn't eat into page content. */
    div.stVerticalBlock[class*="st-key-bottom_nav"] .stButton > button {
        background: transparent;
        border: none;
        color: #eeeeee;
        font-size: 20px;
        border-radius: 35px;
        padding: 6px 0;
        width: 100%;
        box-shadow: none;
    }

    div.stVerticalBlock[class*="st-key-bottom_nav"] .stButton > button:hover {
        background: rgba(255,255,255,0.06);
        color: #ffffff;
    }

    /* Highlighted / active tab */
    div.stVerticalBlock[class*="st-key-bottom_nav"] .stButton > button[kind="primary"] {
        background: #454545 !important;
        color: #ffffff !important;
        border-color: #454545 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container(key="bottom_nav"):

        if st.button(
            "◎",
            key="nav_marks",
            use_container_width=True,
            type="primary" if active == "marks" else "secondary",
        ):
            st.switch_page("marks.py")

        if st.button(
            "🏠",
            key="nav_home",
            use_container_width=True,
            type="primary" if active == "dashboard" else "secondary",
        ):
            st.switch_page("dashboard.py")

        if st.button(
            "📅",
            key="nav_timetable",
            use_container_width=True,
            type="primary" if active == "timetable" else "secondary",
        ):
            st.switch_page("timetable.py")

        if st.button(
            "📊",
            key="nav_performance",
            use_container_width=True,
            type="primary" if active == "performance" else "secondary",
        ):
            st.switch_page("performance.py")