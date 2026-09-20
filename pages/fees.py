import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Fee Statements",
    page_icon="💲",
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
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FEES_CSV = BASE_DIR.parent / "data" / "fees.csv"
LOGO_PATH = BASE_DIR.parent / "assets" / "logo.jfif"        # path as given


# ============================================================
# DATA
# ============================================================

fees_df = pd.read_csv(FEES_CSV, dtype=str).fillna("")


def format_date(date_str: str, fmt: str = "%d %b %Y") -> str:
    if not date_str:
        return ""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime(fmt)
    except ValueError:
        return date_str


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

/* ---------- List header: back "Home" / title / refresh ---------- */

div.stVerticalBlock[class*="st-key-fees_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 8px;
    margin-bottom: 16px;
}

div.stVerticalBlock[class*="st-key-fees_header_row"] > div:nth-child(2) {
    flex: 1;
}

.fees-header-title {
    font-size: 21px;
    font-weight: 700;
    text-align: center;
}

div[class*="st-key-fees_home_back"] .stButton > button {
    background: transparent;
    color: #ffffff;
    border: none;
    font-size: 18px;
    font-weight: 600;
    padding: 0 4px;
    box-shadow: none;
}

div[class*="st-key-fees_refresh"] .stButton > button,
div[class*="st-key-fees_detail_back"] .stButton > button,
div[class*="st-key-fees_download_top"] .stButton > button {
    background: #262626;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    width: 40px;
    height: 40px;
    font-size: 17px;
    padding: 0;
}

div[class*="st-key-fees_detail_back"] .stButton > button {
    background: transparent;
    font-size: 26px;
    font-weight: 300;
}

div[class*="st-key-fees_refresh"] .stButton > button:hover,
div[class*="st-key-fees_download_top"] .stButton > button:hover {
    background: #333333;
}

/* ---------- Tabs: Current / History / Receipts ---------- */

div.stVerticalBlock[class*="st-key-fees_tabs"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    background: #1a1a1a;
    border-radius: 16px;
    padding: 6px;
    margin-bottom: 18px;
}

div.stVerticalBlock[class*="st-key-fees_tabs"] > div {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-fees_tabs"] .stButton > button {
    width: 100%;
    background: transparent;
    color: #999999;
    border: none;
    border-radius: 12px;
    padding: 10px 6px;
    font-weight: 600;
    font-size: 14px;
}

div[class*="st-key-fees_tabs"] .stButton > button[kind="primary"] {
    background: #ffffff !important;
    color: #000000 !important;
}

/* ---------- Receipt list rows ---------- */

div.stVerticalBlock[class*="st-key-fee_row_"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 10px;
    background: #161616;
    border: 1px solid #262626;
    border-left: 3px solid #ffffff;
    border-radius: 16px;
    padding: 14px 14px;
    margin-bottom: 12px;
}

div.stVerticalBlock[class*="st-key-fee_row_"] > div:nth-child(1) {
    flex: 1;
    min-width: 0;
}

.fee-row-content {
    display: flex;
    align-items: center;
    gap: 14px;
}

.fee-row-icon {
    position: relative;
    background: #262626;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.fee-row-icon-badge {
    position: absolute;
    bottom: -3px;
    right: -3px;
    background: #21c25e;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    color: #ffffff;
    border: 2px solid #161616;
}

.fee-row-text { min-width: 0; }

.fee-row-number {
    font-weight: 700;
    font-size: 17px;
    color: #ffffff;
}

.fee-row-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 4px;
    color: #999999;
    font-size: 13px;
}

.fee-row-pdf-pill {
    background: #163d25;
    color: #45e878;
    padding: 2px 8px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 11px;
}

div[class*="st-key-fee_row_"] .stButton > button {
    background: #262626;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    width: 38px;
    height: 38px;
    font-size: 16px;
    padding: 0;
}

div[class*="st-key-fee_row_"] .stButton > button:hover {
    background: #333333;
}

/* ---------- Receipt detail: title block under the header ---------- */

.fees-detail-title-wrap {
    text-align: center;
    margin-bottom: 16px;
}

.fees-detail-title {
    font-size: 19px;
    font-weight: 700;
    color: #ffffff;
}

.fees-detail-subtitle {
    color: #999999;
    font-size: 14px;
    margin-top: 2px;
}

/* ---------- Receipt detail: doc card (same shape as id-card.py) ---------- */

.fees-doc-card {
    background: #1a1a1a;
    border-radius: 20px;
    border: 1px solid #2c2c2c;
    box-shadow: 0 8px 25px rgba(0,0,0,.5);
    overflow: hidden;
    margin-bottom: 16px;
}

.fees-doc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 20px 16px 20px;
    gap: 12px;
}

.fees-doc-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
}

.fees-doc-icon {
    background: #7a1f1f;
    color: #ffffff;
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    flex-shrink: 0;
}

.fees-doc-title {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 260px;
}

.fees-doc-subtitle {
    color: #999999;
    font-size: 13px;
    margin-top: 2px;
}

.fees-verified-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #163d25;
    color: #45e878;
    padding: 7px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 13px;
    white-space: nowrap;
    flex-shrink: 0;
}

.fees-toolbar {
    display: flex;
    align-items: center;
    gap: 18px;
    background: #232323;
    padding: 12px 20px;
    color: #cccccc;
    font-size: 14px;
}

.fees-page-box {
    background: #2f2f2f;
    border-radius: 6px;
    padding: 3px 10px;
    color: #ffffff;
    font-weight: 600;
}

.fees-toolbar-spacer { flex: 1; }
.fees-toolbar-icon { font-size: 16px; color: #cccccc; }

/* ---------- Receipt detail: the white printed slip ---------- */

.fees-slip-wrap {
    background: #ffffff;
    color: #111111;
    padding: 24px 18px;
}

.fees-slip {
    max-width: 480px;
    margin: 0 auto;
    font-size: 12.5px;
    line-height: 1.5;
    border: 1px solid #333333;
    padding: 16px;
}

.fees-slip-caption {
    text-align: center;
    font-weight: 600;
    margin-bottom: 10px;
}

.fees-slip-topline {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 6px;
}

.fees-slip-logo-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.fees-slip-logo-row img {
    width: 56px;
    height: 56px;
    object-fit: contain;
    flex-shrink: 0;
}

.fees-slip-institute {
    font-weight: 700;
}

.fees-slip-program-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 4px;
}

.fees-slip-line { margin: 5px 0; }
.fees-slip-underline {
    border-bottom: 1px solid #333333;
    padding-bottom: 1px;
    font-weight: 600;
}

.fees-slip-amount-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 12px 0;
}

.fees-slip-amount-box {
    border: 1px solid #333333;
    padding: 4px 10px;
    font-weight: 700;
    white-space: nowrap;
}

.fees-slip-printed {
    text-align: right;
    font-size: 11px;
    margin-bottom: 4px;
}

.fees-slip ol {
    margin: 6px 0 0 0;
    padding-left: 16px;
    font-size: 10.5px;
    line-height: 1.5;
}

.fees-slip ol li { margin-bottom: 4px; }

.fees-slip-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 10.5px;
}

.fees-slip-missing-logo {
    color: #999999;
    font-size: 11px;
}

/* ---------- Bottom action row (download / share on detail view) ---------- */

div.stVerticalBlock[class*="st-key-fees_actions_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
}

div.stVerticalBlock[class*="st-key-fees_actions_row"] > div {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-fees_actions_row"] .stButton > button,
div[class*="st-key-fees_actions_row"] .stDownloadButton > button {
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

div[class*="st-key-fees_actions_row"] .stButton > button:hover,
div[class*="st-key-fees_actions_row"] .stDownloadButton > button:hover {
    background: #232323;
}

@media (max-width: 600px) {
    .fees-doc-title { max-width: 170px; font-size: 14px; }
}

</style>
""")


# ============================================================
# SESSION STATE
# ============================================================

if "fees_tab" not in st.session_state:
    st.session_state.fees_tab = "Receipts"

if "selected_receipt" not in st.session_state:
    st.session_state.selected_receipt = None


# ============================================================
# RECEIPT SLIP HTML (the white printed-looking document)
#
# Program, payment mode, "On Accounts of", and student/father
# names are shown with their VALUES overridden per your latest
# instructions, even though the field labels/structure below are
# still based on the original UIE-style layout. "Class",
# "Uni Account No", and "Annual Charges" have been removed
# entirely to match the current fees.csv columns. Book No. and
# the plain numeric Receipt No. are shown separately from the
# UIE-style receipt_no this app still uses internally to identify
# which row of fees.csv is open.
# ============================================================

def render_receipt_slip(row: dict) -> str:

    if LOGO_PATH.exists():
        encoded_logo = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        logo_html = f'<img src="data:image/jpeg;base64,{encoded_logo}">'
    else:
        logo_html = (
            '<div class="fees-slip-missing-logo">'
            f'Logo not found — place it at assets/{LOGO_PATH.name}'
            '</div>'
        )

    date_display = format_date(row["date"], "%d-%m-%Y")

    return f"""
    <div class="fees-slip-wrap">
        <div class="fees-slip">

            <div class="fees-slip-caption">(Student Copy)</div>

            <div class="fees-slip-topline">
                <div>Receipt No. <span class="fees-slip-underline">{row['physical_receipt_no']}</span></div>
                <div>Book No. <span class="fees-slip-underline">{row['book_no']}</span></div>
                <div>Dated <span class="fees-slip-underline">{date_display}</span></div>
            </div>

            <div class="fees-slip-logo-row">
                {logo_html}
                <div class="fees-slip-institute">HINDU COLLEGE , AMRITSAR</div>
            </div>

            <div class="fees-slip-program-row">
                <div>Program : <span class="fees-slip-underline">{row['program']}</span></div>
                <div>Year/Semester <span class="fees-slip-underline">{row['year_semester']}</span></div>
            </div>

            <div class="fees-slip-line">
                Roll No. <span class="fees-slip-underline">{row['roll_no']}</span>
            </div>

            <div class="fees-slip-line">
                Received With Thanks from Mr. / Ms.
                <span class="fees-slip-underline">{row['student_name']}</span>
                S/D/o Sh. <span class="fees-slip-underline">{row['father_name']}</span>
            </div>

            <div class="fees-slip-line">
                On Accounts of <span class="fees-slip-underline">{row['on_accounts_of']}</span>
            </div>

            <div class="fees-slip-line">
                In form of Cash/Draft/Pay Order/On line (Specify)
                <span class="fees-slip-underline">{row['payment_mode']}</span>
            </div>

            <div class="fees-slip-amount-row">
                <div class="fees-slip-amount-box">Rs. {row['amount']}/-</div>
                <div>(In words) Rs. <span class="fees-slip-underline">{row['amount_words']}</span></div>
            </div>

            <div class="fees-slip-printed">Printed on : {row['printed_on']}</div>

            <div class="fees-slip-footer">
                <div><i>Powered by ERP Department</i></div>
                <div>Issued By: {row['issued_by']}</div>
            </div>

        </div>
    </div>
    """


# ============================================================
# ACTUAL DOWNLOADABLE PDF
#
# Generated on the fly from the same row data as the on-screen
# slip above, using reportlab — the download button works
# immediately without needing a pre-existing static PDF file
# placed on disk. Mirrors the current HTML slip's fields exactly
# — no Terms & Conditions section, since that isn't on the slip
# anymore either.
# ============================================================

def build_receipt_pdf(row: dict) -> bytes:

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=22 * mm, rightMargin=22 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=10, leading=14)
    center = ParagraphStyle("center", parent=normal, alignment=TA_CENTER)
    right = ParagraphStyle("right", parent=normal, alignment=TA_RIGHT, fontSize=8)
    institute = ParagraphStyle("institute", parent=normal, fontName="Helvetica-Bold", fontSize=11)
    small = ParagraphStyle("small", parent=normal, fontSize=8, leading=11)

    date_display = format_date(row["date"], "%d-%m-%Y")

    elements = [
        Paragraph("(Student Copy)", center),
        Spacer(1, 6),
        Table(
            [[
                Paragraph(f"Receipt No. <u>{row['physical_receipt_no']}</u>", normal),
                Paragraph(f"Book No. <u>{row['book_no']}</u>", normal),
                Paragraph(f"Dated <u>{date_display}</u>", normal),
            ]],
            colWidths=[55 * mm, 55 * mm, 55 * mm],
        ),
        Spacer(1, 8),
    ]

    if LOGO_PATH.exists():
        logo_flowable = RLImage(str(LOGO_PATH), width=16 * mm, height=16 * mm)
    else:
        logo_flowable = Paragraph("(logo missing)", small)

    logo_table = Table(
        [[logo_flowable, Paragraph("HINDU COLLEGE , AMRITSAR", institute)]],
        colWidths=[20 * mm, 145 * mm],
    )
    logo_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    elements.append(logo_table)
    elements.append(Spacer(1, 8))

    elements.append(Table(
        [[
            Paragraph(f"Program : <u>{row['program']}</u>", normal),
            Paragraph(f"Year/Semester <u>{row['year_semester']}</u>", normal),
        ]],
        colWidths=[120 * mm, 45 * mm],
    ))
    elements.append(Spacer(1, 4))

    elements.append(Paragraph(f"Roll No. <u>{row['roll_no']}</u>", normal))
    elements.append(Paragraph(
        f"Received With Thanks from Mr. / Ms. <u>{row['student_name']}</u> "
        f"S/D/o Sh. <u>{row['father_name']}</u>", normal
    ))
    elements.append(Paragraph(f"On Accounts of <u>{row['on_accounts_of']}</u>", normal))
    elements.append(Paragraph(
        f"In form of Cash/Draft/Pay Order/On line (Specify) <u>{row['payment_mode']}</u>", normal
    ))
    elements.append(Spacer(1, 8))

    amount_table = Table(
        [[
            Paragraph(f"<b>Rs. {row['amount']}/-</b>", normal),
            Paragraph(f"(In words) Rs. <u>{row['amount_words']}</u>", normal),
        ]],
        colWidths=[35 * mm, 130 * mm],
    )
    amount_table.setStyle(TableStyle([
        ("BOX", (0, 0), (0, 0), 0.75, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(amount_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"Printed on : {row['printed_on']}", right))
    elements.append(Spacer(1, 10))

    elements.append(Table(
        [[
            Paragraph("<i>Powered by ERP Department</i>", small),
            Paragraph(f"Issued By: {row['issued_by']}", small),
        ]],
        colWidths=[90 * mm, 75 * mm],
    ))

    doc.build(elements)
    return buffer.getvalue()


# ============================================================
# RECEIPT DETAIL VIEW
# ============================================================

def render_receipt_detail(receipt_no: str):

    matches = fees_df[fees_df["receipt_no"] == receipt_no]
    if matches.empty:
        st.error("Receipt not found.")
        st.session_state.selected_receipt = None
        return
    row = matches.iloc[0].to_dict()

    receipt_pdf_bytes = build_receipt_pdf(row)
    pdf_file_name = f"{receipt_no}.pdf"

    with st.container(key="fees_header_row"):

        if st.button("‹", key="fees_detail_back"):
         st.session_state.selected_receipt = None
         st.rerun()

        render(f"""
        <div class="fees-detail-title-wrap">
            <div class="fees-detail-title">{receipt_no} ({format_date(row['date'])})</div>
            <div class="fees-detail-subtitle">PDF Document</div>
        </div>
        """)

        st.download_button(
            "⬇",
            data=receipt_pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf",
            key="fees_download_top",
        )

    render(f"""
    <div class="fees-doc-card">
        <div class="fees-doc-header">
            <div class="fees-doc-header-left">
                <div class="fees-doc-icon">📄</div>
                <div>
                    <div class="fees-doc-title">{receipt_no} ({format_date(row['date'])})...</div>
                    <div class="fees-doc-subtitle">Fee Receipt</div>
                </div>
            </div>
            <div class="fees-verified-pill">✓ Verified</div>
        </div>
        <div class="fees-toolbar">
            <span>Page</span>
            <span class="fees-page-box">1</span>
            <span>/ 1</span>
            <span class="fees-toolbar-spacer"></span>
            <span class="fees-toolbar-icon">🔖</span>
            <span class="fees-toolbar-icon">🔍</span>
            <span class="fees-toolbar-icon">⚙️</span>
        </div>
        {render_receipt_slip(row)}
    </div>
    """)

    with st.container(key="fees_actions_row"):
        st.download_button(
            "⬇\nDownload",
            data=receipt_pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf",
            key="fees_download_bottom",
        )

        if st.button("📤\nShare", key="fees_share_bottom"):
            st.toast("Share option selected")


# ============================================================
# LIST VIEW
# ============================================================

def render_receipt_row(row: dict):
    with st.container(key=f"fee_row_{row['receipt_no']}"):

        render(f"""
        <div class="fee-row-content">
            <div class="fee-row-icon">
                📄
                <div class="fee-row-icon-badge">✓</div>
            </div>
            <div class="fee-row-text">
                <div class="fee-row-number">{row['receipt_no']}</div>
                <div class="fee-row-meta">
                    <span>📅 {format_date(row['date'])}</span>
                    <span class="fee-row-pdf-pill">PDF</span>
                </div>
            </div>
        </div>
        """)

        if st.button("→", key=f"fee_open_{row['receipt_no']}"):
            st.session_state.selected_receipt = row["receipt_no"]
            st.rerun()


def render_fees_list():

    with st.container(key="fees_header_row"):

        if st.button("‹ Home", key="fees_home_back"):
            st.switch_page("pages/dashboard.py")

        render('<div class="fees-header-title">Fee Statements</div>')

        if st.button("⟳", key="fees_refresh"):
            st.rerun()

    with st.container(key="fees_tabs"):

        for tab_label, tab_icon in [("Current", "📄"), ("History", "🕐"), ("Receipts", "🗐")]:
            if st.button(
                f"{tab_icon} {tab_label}",
                key=f"fees_tab_{tab_label}",
                type="primary" if st.session_state.fees_tab == tab_label else "secondary",
            ):
                st.session_state.fees_tab = tab_label
                st.rerun()

    if st.session_state.fees_tab != "Receipts":
        render(
            f'<div style="color:#888; text-align:center; padding:40px 10px;">'
            f'{st.session_state.fees_tab} view is coming soon.</div>'
        )
        return

    for _, row in fees_df.iterrows():
        render_receipt_row(row.to_dict())


# ============================================================
# MAIN PAGE ROUTING
# ============================================================

if st.session_state.selected_receipt is None:
    render_fees_list()
else:
    render_receipt_detail(st.session_state.selected_receipt)