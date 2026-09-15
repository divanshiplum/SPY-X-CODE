import streamlit as st
import base64
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student ID Card",
    page_icon="🪪",
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
# THE ACTUAL ID CARD IMAGE
# Place the scanned/exported ID card image at this path.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ID_CARD_IMAGE_PATH = BASE_DIR / "images" / "id-card.jpeg"


# ============================================================
# CSS
# ============================================================

render("""
<style>

.stApp {
    background: #0d0d0d;
    color: #ffffff;
}

.block-container {
    max-width: 720px;
    padding: 14px 14px 30px 14px;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* ---------- Header row: back / icon+title / share / more ---------- */

div.stVerticalBlock[class*="st-key-idcard_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 8px;
    margin-bottom: 18px;
}

div.stVerticalBlock[class*="st-key-idcard_header_row"] > div:nth-child(2) {
    flex: 1;
}

.idcard-title-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.idcard-title-icon {
    background: #262626;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.idcard-title-text {
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
}

div[class*="st-key-idcard_back"] .stButton > button {
    background: transparent;
    color: #ffffff;
    border: none;
    font-size: 28px;
    font-weight: 300;
    width: 40px;
    height: 40px;
    padding: 0;
    box-shadow: none;
}

div[class*="st-key-idcard_share_top"] .stButton > button,
div[class*="st-key-idcard_more"] .stButton > button {
    background: #262626;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    width: 40px;
    height: 40px;
    font-size: 17px;
    padding: 0;
}

div[class*="st-key-idcard_back"] .stButton > button:hover {
    color: #cccccc;
}

div[class*="st-key-idcard_share_top"] .stButton > button:hover,
div[class*="st-key-idcard_more"] .stButton > button:hover {
    background: #333333;
}

/* ---------- Meta row: Official Document pill + label ---------- */

.idcard-meta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.idcard-official-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #163d25;
    color: #45e878;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 15px;
}

.idcard-meta-label {
    color: #999999;
    font-size: 15px;
}

/* ---------- Document card ---------- */

.idcard-doc-card {
    background: #1a1a1a;
    border-radius: 20px;
    border: 1px solid #2c2c2c;
    box-shadow: 0 8px 25px rgba(0,0,0,.5);
    overflow: hidden;
}

.idcard-doc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 22px 18px 22px;
    gap: 12px;
}

.idcard-doc-header-left {
    display: flex;
    align-items: center;
    gap: 14px;
    min-width: 0;
}

.idcard-doc-icon {
    background: #ffffff;
    color: #111111;
    width: 46px;
    height: 46px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}

.idcard-doc-title {
    font-size: 19px;
    font-weight: 700;
    color: #ffffff;
}

.idcard-doc-subtitle {
    color: #999999;
    font-size: 14px;
    margin-top: 2px;
}

.idcard-valid-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #163d25;
    color: #45e878;
    padding: 7px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 14px;
    white-space: nowrap;
    flex-shrink: 0;
}

.idcard-toolbar {
    display: flex;
    align-items: center;
    gap: 18px;
    background: #232323;
    padding: 12px 22px;
    color: #cccccc;
    font-size: 15px;
}

.idcard-page-box {
    background: #2f2f2f;
    border-radius: 6px;
    padding: 3px 10px;
    color: #ffffff;
    font-weight: 600;
}

.idcard-toolbar-spacer { flex: 1; }

.idcard-toolbar-icon { font-size: 17px; color: #cccccc; }

.idcard-image-wrap {
    background: #ffffff;
    padding: 26px 18px;
    display: flex;
    justify-content: center;
}

.idcard-image-wrap img {
    max-width: 100%;
    border-radius: 4px;
}

.idcard-missing {
    color: #888888;
    text-align: center;
    padding: 60px 20px;
    font-size: 15px;
}

/* ---------- Bottom action row ---------- */

div.stVerticalBlock[class*="st-key-idcard_actions_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
    margin-top: 20px;
}

div.stVerticalBlock[class*="st-key-idcard_actions_row"] > div {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-idcard_actions_row"] .stButton > button {
    width: 100%;
    background: #1a1a1a;
    color: #cccccc;
    border: 1px solid #2c2c2c;
    border-radius: 16px;
    padding: 16px 4px;
    white-space: pre-line;
    line-height: 1.7;
    font-size: 13px;
    font-weight: 600;
}

div[class*="st-key-idcard_actions_row"] .stButton > button:hover {
    background: #232323;
}

@media (max-width: 600px) {
    .idcard-title-text { font-size: 18px; }
    .idcard-doc-title { font-size: 17px; }
    div[class*="st-key-idcard_actions_row"] .stButton > button { font-size: 11px; padding: 14px 2px; }
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

with st.container(key="idcard_header_row"):

    if st.button("‹", key="idcard_back"):
        st.switch_page("dashboard.py")

    render("""
    <div class="idcard-title-group">
        <div class="idcard-title-icon">💳</div>
        <div class="idcard-title-text">Student ID Card</div>
    </div>
    """)

    if st.button("⬆", key="idcard_share_top"):
        st.toast("Share option selected")

    if st.button("⋯", key="idcard_more"):
        st.toast("More options")


# ============================================================
# META ROW
# ============================================================

render("""
<div class="idcard-meta-row">
    <div class="idcard-official-pill">✅ Official Document</div>
    <div class="idcard-meta-label">College ID Card</div>
</div>
""")


# ============================================================
# DOCUMENT CARD
#
# The image (or the missing-file message) is embedded directly
# inside the SAME HTML string as the rest of the card below —
# not as a separate st.image() call or a later render() call —
# because each st.markdown() call is parsed by the browser as
# its own independent HTML fragment. An unclosed <div> in one
# call does NOT actually contain content from a later, separate
# call; they'd render as visually separate boxes instead of one
# continuous card. Embedding the image as a base64 data URI
# inside one single HTML block guarantees correct nesting (same
# technique already used for the profile photo in dashboard.py).
# ============================================================

if ID_CARD_IMAGE_PATH.exists():
    encoded = base64.b64encode(ID_CARD_IMAGE_PATH.read_bytes()).decode()
    id_card_body_html = f"""
    <div class="idcard-image-wrap">
        <img src="data:image/jpeg;base64,{encoded}">
    </div>
    """
else:
    id_card_body_html = """
    <div class="idcard-missing">
        ID card image not found — place it at
        images/id-card.jpeg to display it here.
    </div>
    """

render(f"""
<div class="idcard-doc-card">

    <div class="idcard-doc-header">
        <div class="idcard-doc-header-left">
            <div class="idcard-doc-icon">💳</div>
            <div>
                <div class="idcard-doc-title">Student ID Card</div>
                <div class="idcard-doc-subtitle">PDF Document &bull; Tap to interact</div>
            </div>
        </div>
        <div class="idcard-valid-pill">● Valid</div>
    </div>

    <div class="idcard-toolbar">
        <span>Page</span>
        <span class="idcard-page-box">1</span>
        <span>/ 1</span>
        <span class="idcard-toolbar-spacer"></span>
        <span class="idcard-toolbar-icon">🔖</span>
        <span class="idcard-toolbar-icon">🔍</span>
        <span class="idcard-toolbar-icon">⚙️</span>
    </div>

    {id_card_body_html}

</div>
""")


# ============================================================
# BOTTOM ACTION ROW
# ============================================================

with st.container(key="idcard_actions_row"):

    if st.button("📤\nShare", key="idcard_share_btn"):
        st.toast("Share option selected")

    if st.button("📥\nSave", key="idcard_save_btn"):
        st.toast("ID Card is ready to save")

    if st.button("⤢\nFullscreen", key="idcard_fullscreen_btn"):
        st.toast("Fullscreen option selected")

    if st.button("⟳\nRefresh", key="idcard_refresh_btn"):
        st.rerun()