import streamlit as st


def render_bottom_nav(active: str):
    """Fixed bottom navigation bar, shared by every page.

    active: one of "marks", "dashboard", "timetable", "performance"
    — whichever page is currently open gets highlighted.
    """

    st.markdown("""
    <style>

    /* Pin the whole nav bar container to the bottom of the screen,
       centered, matching the width used across the app. */
    div[class*="st-key-bottom_nav"] {
        position: fixed;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        width: min(720px, 100%);
        background: #171717;
        border-top: 1px solid #292929;
        padding: 10px 14px 16px 14px;
        z-index: 999999;
    }

    /* Icon buttons inside the nav bar */
    div[class*="st-key-bottom_nav"] .stButton > button {
        background: transparent;
        border: none;
        color: #eeeeee;
        font-size: 24px;
        border-radius: 35px;
        padding: 8px 0;
        width: 100%;
        box-shadow: none;
    }

    div[class*="st-key-bottom_nav"] .stButton > button:hover {
        background: rgba(255,255,255,0.06);
        color: #ffffff;
    }

    /* Highlighted / active tab */
    div[class*="st-key-bottom_nav"] .stButton > button[kind="primary"] {
        background: #454545 !important;
        color: #ffffff !important;
        border-color: #454545 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container(key="bottom_nav"):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(
                "◎",
                key="nav_marks",
                use_container_width=True,
                type="primary" if active == "marks" else "secondary",
            ):
                st.switch_page("marks.py")

        with col2:
            if st.button(
                "🏠",
                key="nav_home",
                use_container_width=True,
                type="primary" if active == "dashboard" else "secondary",
            ):
                st.switch_page("dashboard.py")

        with col3:
            if st.button(
                "📅",
                key="nav_timetable",
                use_container_width=True,
                type="primary" if active == "timetable" else "secondary",
            ):
                st.switch_page("timetable.py")

        with col4:
            if st.button(
                "📊",
                key="nav_performance",
                use_container_width=True,
                type="primary" if active == "performance" else "secondary",
            ):
                st.switch_page("performance.py")