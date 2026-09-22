import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
from pages.theme import THEME_CSS


NAV_ITEMS = [
    ("⬛", "Dashboard", "dashboard", "pages/dashboard.py"),
    ("📊", "Marks", "marks", "pages/marks.py"),
    ("📅", "Timetable", "timetable", "pages/timetable.py"),
    ("📈", "Performance", "performance", "pages/performance.py"),
]


def render_sidebar(active: str):
    """Persistent left sidebar, shared by every page.

    active: one of the id strings in NAV_ITEMS above (e.g. "dashboard").

    Built the same proven way as every other fixed-position element in
    this app (the old bottom nav bar, the timetable day-selector): a
    single st.container(key=...) forced into a fixed-position column
    via CSS, rather than Streamlit's own st.sidebar (which this app
    deliberately doesn't use, since it comes with its own default
    chrome/behavior we'd have to fight).
    """

    st.markdown(THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <style>

    /* Push all normal page content right so it never sits under the
       fixed sidebar. */
    .block-container {
        padding-left: 280px !important;
        max-width: 1300px;
        padding-top: 24px;
    }

    /* Settings is pinned to the sidebar's own bottom edge via
       absolute positioning against the sidebar's fixed positioning
       context — more reliable here than a flex-grow spacer, which
       wasn't actually filling the remaining height in this nested
       container structure. */
    div.stVerticalBlock[class*="st-key-hc_sidebar"] {
        position: fixed !important;
        top: 0;
        left: 0;
        bottom: 0;
        width: 240px !important;
        background: var(--hc-surface);
        border-right: 1px solid var(--hc-border);
        padding: 28px 16px 20px 16px;
        display: block !important;
        z-index: 999999;
        overflow-y: auto;
    }

    div.stVerticalBlock[class*="st-key-hc_bottom_section"] {
        position: absolute;
        bottom: 20px;
        left: 16px;
        right: 16px;
    }

    .hc-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 19px;
        font-weight: 800;
        color: var(--hc-text);
        margin-bottom: 28px;
        padding-left: 6px;
    }

    .hc-logo-icon {
        font-size: 22px;
    }

    div.stVerticalBlock[class*="st-key-hc_sidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        background: transparent;
        border: none;
        color: var(--hc-text-soft);
        font-weight: 600;
        font-size: 14px;
        padding: 10px 12px;
        border-radius: var(--hc-radius-sm);
        margin-bottom: 2px;
    }

    div.stVerticalBlock[class*="st-key-hc_sidebar"] .stButton > button:hover {
        background: var(--hc-bg);
        color: var(--hc-text);
    }

    div.stVerticalBlock[class*="st-key-hc_sidebar"] .stButton > button[kind="primary"] {
        background: var(--hc-purple-soft) !important;
        color: var(--hc-purple-text) !important;
    }

    @media (max-width: 900px) {
        div.stVerticalBlock[class*="st-key-hc_sidebar"] { display: none !important; }
        .block-container { padding-left: 24px !important; }
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container(key="hc_sidebar"):

        st.markdown(
            '<div class="hc-logo"><span class="hc-logo-icon">🎓</span> HC NEXUS</div>',
            unsafe_allow_html=True,
        )

        for icon, label, item_id, target_page in NAV_ITEMS:
            if st.button(
                f"{icon}  {label}",
                key=f"hc_nav_{item_id}",
                type="primary" if item_id == active else "secondary",
            ):
                if target_page:
                    st.switch_page(target_page)

        with st.container(key="hc_bottom_section"):

            if st.button("⚙️  Settings", key="hc_nav_settings", type="primary" if active == "settings" else "secondary"):
                st.switch_page("pages/settings.py")