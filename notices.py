import streamlit as st
from pathlib import Path
from PyPDF2 import PdfReader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Announcements",
    page_icon="📢",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOGIN GUARD
# ============================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("login.py")


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# FILE PATHS FOR THE TWO NEW NOTICE SOURCES
#
# I've now been given both files directly, so the content below
# is transcribed from what's actually in them, not guessed. The
# PDF is still read/attached from disk at runtime (so the real
# download works and stays in sync if the file changes) — the
# excerpt text on the card is a short, curated summary rather
# than raw auto-extracted text, since a straight PyPDF2 dump
# came out with the page's column layout jumbled ("–2026" landing
# before the title, categories run together, etc.) which reads
# poorly as preview text on a card.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ZONAL_PDF_PATH = BASE_DIR / "notices" / "ITEMS FOR COMPETITION OF ZONAL YOUTH FESTIVAL.pdf"
TEEJ_IMAGE_PATH = BASE_DIR / "notices" / "WhatsApp Image 2026-09-14 at 1.31.23 PM.jpeg"

ZONAL_PDF_EXCERPT = (
    "The official item list for the Zonal Youth Festival 2026 is "
    "now available, covering Music (13 items including Classical "
    "Instrumental, Vocal Solo, Folk Song and Group Song), Theatre "
    "(Costume Parade, Mimicry, Skit, Mime, One Act Play), Dances "
    "(Gidha, Bhangra, Group Dance, Classical Dance, Choreography), "
    "Literary (Elocution, Debate, Poetical Symposium, Quiz) and "
    "Fine Arts (Painting, Cartooning, Collage, Poster Making, Clay "
    "Modelling, Rangoli, Phulkari)."
)

# Transcribed from the Hindu College, Amritsar Teej notice image.
TEEJ_NOTICE_HTML = """
<div class="notice-text">
    Hindu College, Amritsar is delighted to share that
    <strong>Teej</strong> will be celebrated in the college on
    <strong>14th August 2026 at 10:00 AM</strong>.
</div>

<div class="sub-heading">THE CELEBRATIONS WILL INCLUDE</div>

<ul>
    <li>Giddha</li>
    <li>Bhangra</li>
    <li>Singing</li>
    <li>Mehndi Competition</li>
    <li>Nail Art Competition</li>
</ul>

<div class="notice-text">
    Students interested in participating in <strong>Giddha,
    Bhangra, or Singing</strong> are requested to give their
    names to <strong>Ms. Anu Sanan</strong> or <strong>Ms
    Ravneet</strong>, and for <strong>Mehndi or Nail Art
    Competitions</strong> to <strong>Ms. Rajni</strong> in the
    Department of Cosmetology.
</div>

<div class="notice-text" style="margin-top:14px; font-weight:700; text-align:center;">
    Dr. Rakesh Kumar
    <div style="font-weight:400; color:#666; font-size:15px;">Principal</div>
</div>
"""


def get_pdf_excerpt(pdf_path: Path, max_chars: int = 320) -> str:
    """Pulls a short excerpt of real text out of the first page(s)
    of a PDF, for use as the preview text on a notice card. Returns
    a friendly placeholder message if the file isn't there yet.
    Kept as a general-purpose fallback/utility — the Zonal Youth
    Festival card below uses a hand-curated excerpt instead, since
    its raw extraction reads poorly (see note above)."""

    if not pdf_path.exists():
        return (
            "⚠️ PDF not found yet at this path — once "
            f"\"{pdf_path.name}\" is placed in the notices/ folder, "
            "this card will automatically show a real excerpt from it."
        )

    try:
        reader = PdfReader(str(pdf_path))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
            if len(text) >= max_chars:
                break

        text = " ".join(text.split())  # collapse whitespace/newlines

        if not text:
            return "⚠️ Couldn't extract any text from this PDF."

        if len(text) > max_chars:
            text = text[:max_chars].rsplit(" ", 1)[0] + "…"

        return text

    except Exception as error:
        return f"⚠️ Could not read this PDF ({error})."


# ============================================================
# CSS
# (Reconstructed to match the reference screenshots: dark page,
# dark sticky header with a back arrow / centered title / round
# refresh button, and white "notice cards" — each topped by a
# small dark pinned-label strip — holding the announcement text.)
# ============================================================

render("""
<style>

.stApp {
    background: #18191b;
    color: #eeeeee;
}

.block-container {
    max-width: 720px;
    padding: 0 0 30px 0;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* Header bar */
.notice-header-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    flex: 1;
    text-align: center;
}

div.stVerticalBlock[class*="st-key-notice_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    background: #18191b;
    padding: 14px 12px;
    gap: 8px;
    position: sticky;
    top: 0;
    z-index: 20;
}

div.stVerticalBlock[class*="st-key-notice_header_row"] > div:nth-child(2) {
    flex: 1;
}

/* Back button — plain text arrow, no background, per reference */
div[class*="st-key-notice_back"] .stButton > button {
    background: transparent;
    color: #ffffff;
    border: none;
    font-size: 30px;
    font-weight: 300;
    width: 44px;
    height: 44px;
    padding: 0;
    box-shadow: none;
}

/* Refresh button — dark rounded square, per reference */
div[class*="st-key-notice_refresh"] .stButton > button {
    background: #303134;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    width: 44px;
    height: 44px;
    font-size: 22px;
    padding: 0;
}

div[class*="st-key-notice_back"] .stButton > button:hover {
    color: #cccccc;
}

div[class*="st-key-notice_refresh"] .stButton > button:hover {
    background: #3d3e42;
}

/* Body padding to match the reference's side margins */
.notice-feed {
    padding: 0 12px;
}

/* Pinned label strip sitting on top of each notice card */
.pin-header {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #2a2b2d;
    color: #ffffff;
    padding: 14px 16px;
    border-radius: 14px 14px 0 0;
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 0.2px;
}

.pin-icon {
    background: #ffffff;
    color: #111111;
    width: 32px;
    height: 32px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

/* Announcement card */
.notice-card {
    background: #f8f8f8;
    border-radius: 0 0 16px 16px;
    padding: 20px 18px 22px 18px;
    color: #333333;
    margin-bottom: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,.18);
}

.notice-title {
    font-size: 19px;
    font-weight: 800;
    color: #222222;
    margin-bottom: 18px;
}

.notice-heading {
    font-size: 22px;
    line-height: 1.35;
    font-weight: 800;
    color: #315f8d;
    margin: 20px 0 12px 0;
}

.sub-heading {
    font-size: 18px;
    font-weight: 750;
    color: #333333;
    margin: 15px 0 7px 0;
}

.notice-text {
    font-size: 17px;
    line-height: 1.65;
    margin: 7px 0;
}

.notice-text strong { font-weight: 800; }

.notice-card ul {
    margin-top: 8px;
    padding-left: 25px;
}

.notice-card li {
    font-size: 16.5px;
    line-height: 1.6;
    margin-bottom: 7px;
}

.category-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px 18px;
    margin: 12px 0 18px 0;
}

.category { font-size: 16px; line-height: 1.45; }

.registration {
    background: #eeeeee;
    border-radius: 5px;
    padding: 12px 10px;
    margin-top: 12px;
    font-size: 16px;
    line-height: 1.55;
}

.link { color: #245da3; word-break: break-all; }

/* Attachment rows — dark rounded rows with a doc icon + chevron,
   styled from real st.download_button widgets so they actually
   download the underlying file rather than being decorative. */
div[class*="st-key-attach_"] .stDownloadButton > button {
    width: 100%;
    background: #2a2b2d;
    color: #eeeeee;
    border: none;
    border-radius: 14px;
    padding: 16px 17px;
    margin-top: 9px;
    font-size: 16px;
    text-align: left;
}

div[class*="st-key-attach_"] .stDownloadButton > button:hover {
    background: #333437;
}

/* Attribution line below a card (author + date), on the dark
   page background rather than inside the white card. */
.notice-attribution {
    display: flex;
    align-items: center;
    gap: 16px;
    color: #9a9a9a;
    font-size: 14px;
    padding: 10px 4px 22px 4px;
}

@media (max-width: 600px) {
    .notice-header-title { font-size: 19px; }
    .notice-card { padding: 18px 16px 20px; }
    .notice-heading { font-size: 21px; }
    .notice-text, .notice-card li { font-size: 16px; }
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

with st.container(key="notice_header_row"):

    if st.button("‹", key="notice_back"):
        st.switch_page("dashboard.py")

    render('<div class="notice-header-title">Announcements</div>')

    if st.button("⟳", key="notice_refresh"):
        st.rerun()


render('<div class="notice-feed">')


# ============================================================
# ANNOUNCEMENT 1 — VBYLD 2027
# ============================================================

render("""
<div class="pin-header">
    <div class="pin-icon">📌</div>
    VIKSIT BHARAT YOUNG LEADERS DIALOGUE (VBYLD)-2027
</div>

<div class="notice-card">

    <div class="notice-text">Dear Students,</div>

    <div class="notice-text">
        The Viksit Bharat Young Leaders Dialogue (VBYLD) 2027 has
        commenced with Stage I - Viksit Bharat Quiz. All eligible
        students are encouraged to participate and take the
        opportunity to progress towards the National Level.
    </div>

</div>
""")


# ============================================================
# ANNOUNCEMENT 2 — ZONAL YOUTH FESTIVAL (from the PDF)
#
# The excerpt shown here is the curated ZONAL_PDF_EXCERPT above;
# the actual PDF is still read from disk and offered as a real
# download attachment underneath.
# ============================================================

render(f"""
<div class="pin-header">
    <div class="pin-icon">📌</div>
    ITEMS FOR COMPETITION - ZONAL YOUTH FESTIVAL
</div>

<div class="notice-card">
    <div class="notice-text">{ZONAL_PDF_EXCERPT}</div>
    <div class="notice-text" style="color:#777; font-size:15px;">
        Full details are in the attached PDF below.
    </div>
</div>
""")

with st.container(key="attach_zonal"):
    if ZONAL_PDF_PATH.exists():
        st.download_button(
            "📄  ITEMS FOR COMPETITION OF ZONAL YOUTH FESTIVAL  ›",
            data=ZONAL_PDF_PATH.read_bytes(),
            file_name=ZONAL_PDF_PATH.name,
            key="attach_zonal_btn",
            use_container_width=True,
        )
    else:
        st.button(
            "📄  ITEMS FOR COMPETITION OF ZONAL YOUTH FESTIVAL  (file not found)",
            key="attach_zonal_btn",
            use_container_width=True,
            disabled=True,
        )


# ============================================================
# ANNOUNCEMENT 3 — TEEJ CELEBRATION (from the WhatsApp image,
# shown as plain text rather than the image itself, per your
# request — transcribed from the actual Hindu College, Amritsar
# notice image.)
# ============================================================

render(f"""
<div class="pin-header">
    <div class="pin-icon">📌</div>
    TEEJ CELEBRATION — HINDU COLLEGE, AMRITSAR
</div>

<div class="notice-card">
    {TEEJ_NOTICE_HTML}
</div>
""")


# ============================================================
# FOOTER
# ============================================================

render("""
<div style="text-align:center; color:#777; font-size:13px; padding:20px 4px 0 4px;">
    Last updated: 14 September 2026
</div>
""")

render('</div>')