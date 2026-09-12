import streamlit as st
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Date Sheet",
    page_icon="🗓️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# HTML RENDER HELPER
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# DATA — the two date sheets are shown as their actual scanned
# images rather than a rebuilt table, so whatever is printed on
# the real notice (formatting, stamps, signatures, etc.) is what
# the student sees.
# ============================================================

HOUSE_TEST_IMAGE = "images/HOUSE TEST (SEM-2).jpg"
PRACTICAL_IMAGE = "images/Practical 2026 [SEM-2].jpg"


# ============================================================
# CSS — light theme, matching the reference screenshot rather
# than the app's usual dark theme (same approach used for
# login.py, which also intentionally breaks from the dark theme).
# ============================================================

render("""
<style>

.stApp {
    background: #000000;
    color: #111111;
}

.block-container {
    max-width: 720px;
    padding: 0;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* Header bar */
.ds-header-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    flex: 1;
    text-align: center;
}

/* Wraps the header row + tab section together so there's no
   visible white gap (Streamlit's default spacing between
   sibling elements) between the two dark bars — they read as
   one continuous bar instead of two separate divided boxes. */
div.stVerticalBlock[class*="st-key-ds_top_bar"] {
    gap: 0 !important;
}

div.stVerticalBlock[class*="st-key-ds_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    background: #000000;
    padding: 12px 16px;
    gap: 8px;
}

/* Back / refresh buttons rendered as real st.button widgets,
   restyled to look like the round dark icon buttons in the
   reference image. */
div[class*="st-key-ds_back"] .stButton > button,
div[class*="st-key-ds_refresh"] .stButton > button {
    background: #1c1c1c;
    color: #ffffff;
    border: none;
    border-radius: 50%;
    width: 42px;
    height: 42px;
    font-size: 18px;
    padding: 0;
}

div[class*="st-key-ds_back"] .stButton > button:hover,
div[class*="st-key-ds_refresh"] .stButton > button:hover {
    background: #333333;
}

/* The title's own element-container should take up the middle
   space between the two round buttons. */
div.stVerticalBlock[class*="st-key-ds_header_row"] > div:nth-child(2) {
    flex: 1;
}

/* Wraps the tab label + button row together so Streamlit's
   default gap between sibling elements doesn't show as a seam
   between them (same fix applied to the dashboard's course card). */
div.stVerticalBlock[class*="st-key-ds_tab_section"] {
    gap: 0 !important;
}

/* Tab row — the label sits above the two buttons (its own
   render() line), and the button row's ONLY children are the two
   buttons themselves, sized equally. This mirrors the exact
   pattern already confirmed working for the bottom nav bar and
   the timetable day selector; mixing a text label into the same
   flex row as the buttons (the previous version) collapsed one
   button to near-zero width instead. */
.ds-tab-label {
    color: #ffffff;
    font-size: 15px;
    white-space: nowrap;
    background: #111111;
    padding: 18px 16px 20px 16px;
}

div.stVerticalBlock[class*="st-key-ds_tabs"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
    background: #111111;
    padding: 0 16px 18px 16px;
}

div.stVerticalBlock[class*="st-key-ds_tabs"] > div[data-testid="stElementContainer"] {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-ds_tabs"] .stButton > button {
    width: 100%;
    background: #2a2a2a;
    color: #cfcfcf;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 12px 10px;
}

div[class*="st-key-ds_tabs"] .stButton > button[kind="primary"] {
    background: #ffffff !important;
    color: #000000 !important;
}

/* Image display area — centered with breathing room so the
   scanned date sheet reads clearly on the page. */
.ds-image-wrap {
    padding: 24px 16px 40px 16px;
    text-align: center;
}

.ds-image-wrap img {
    border-radius: 12px;
    border: 1px solid #dddddd;
}

.ds-empty {
    color: #888888;
    padding: 30px 16px;
    text-align: center;
}

</style>
""")


# ============================================================
# TOP BAR (header + tab selector)
# (No st.columns — same reason as everywhere else in this app:
# it stacks vertically on a narrow screen. Both sections are
# wrapped in one shared keyed container so the two dark bars sit
# flush against each other with no visible white seam between
# them, per the CSS gap:0 rule above.)
# ============================================================

with st.container(key="ds_top_bar"):

    with st.container(key="ds_header_row"):

        if st.button("‹", key="ds_back"):
            st.switch_page("dashboard.py")

        render('<div class="ds-header-title">Date Sheet</div>')

        if st.button("⟳", key="ds_refresh"):
            st.rerun()

    if "datesheet_tab" not in st.session_state:
        st.session_state.datesheet_tab = "House Test"

    with st.container(key="ds_tab_section"):

        render('<div class="ds-tab-label">Select&nbsp;Date&nbsp;Sheet</div>')

        with st.container(key="ds_tabs"):

            if st.button(
                "House Test",
                key="ds_tab_house_test",
                use_container_width=True,
                type="primary" if st.session_state.datesheet_tab == "House Test" else "secondary",
            ):
                st.session_state.datesheet_tab = "House Test"
                st.rerun()

            if st.button(
                "Practical",
                key="ds_tab_practical",
                use_container_width=True,
                type="primary" if st.session_state.datesheet_tab == "Practical" else "secondary",
            ):
                st.session_state.datesheet_tab = "Practical"
                st.rerun()


# ============================================================
# IMAGE DISPLAY
# ============================================================

active_tab = st.session_state.datesheet_tab
image_path = HOUSE_TEST_IMAGE if active_tab == "House Test" else PRACTICAL_IMAGE

if os.path.exists(image_path):
    render('<div class="ds-image-wrap">')
    st.image(image_path, use_container_width=True)
    render('</div>')
else:
    render(f'<div class="ds-empty">Couldn\'t find the image at "{image_path}".</div>')