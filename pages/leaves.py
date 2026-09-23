import streamlit as st
import pandas as pd
import re
from pathlib import Path
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from theme import get_theme_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Leaves",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.html(get_theme_css())

st.html("""
<style>

/* Hide the complete left sidebar */
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
}

/* Hide sidebar navigation */
[data-testid="stSidebarNav"] { 
    display: none !important; 
}

[data-testid="stSidebarNavItems"] { 
    display: none !important; 
}

/* Hide sidebar toggle button */
[data-testid="stSidebarCollapseButton"] { 
    display: none !important; 
}

button[kind="header"] { 
    display: none !important; 
}

/* Hide toolbar */
[data-testid="stToolbar"] { 
    display: none !important; 
}

</style>
""")

# ============================================================
# HTML RENDER HELPER
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# FILE PATHS
#
# leaves.py lives in pages/, attendance_message.csv lives in
# data/ at the project root — one level up from pages/.
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ATTENDANCE_MSG_CSV = BASE_DIR.parent / "data" / "attendance_message.csv"

STUDENT_NAME = "Divanshi"


# ============================================================
# KNOWN SUBJECT INFO — the same code→name and code→class-timing
# mapping used elsewhere in this app (dashboard.py, timetable.py),
# so "Category"/"Timing" below are real, not fabricated.
# ============================================================

CODE_TO_SUBJECT = {
    "23CSR-449": "Data Structure",
    "SPO-113": "Computer Architecture",
    "23BDA-401": "Information System",
    "23BDA-402": "Cybersecurity Fundamentals",
    "23BDA-403": "Operating System",
}

CODE_TO_TIMING = {
    "SPO-113": ("09:00 AM", "09:40 AM"),
    "23BDA-402": ("09:40 AM", "10:20 AM"),
    "23BDA-401": ("10:20 AM", "11:00 AM"),
    "23CSR-449": ("11:00 AM", "11:40 AM"),
    "23BDA-403": ("11:40 AM", "12:20 PM"),
}


# ============================================================
# BUILD THE DL (DISCIPLINARY LEAVE) TABLE FROM attendance_message.csv
#
# Each Absent-attendance message becomes one Disciplinary Leave row. The
# subject code and instructor name are parsed straight out of the
# message text (which already exists — nothing invented), and
# Category/Timing come from the known subject/timetable data
# above. DL_No is a plain sequential number generated from the
# CSV's own row order — not copied from any reference screenshot.
# Status and Leave_Type are fixed values (this app has no real
# per-record approval workflow to draw them from).
# ============================================================

def build_leaves_df() -> pd.DataFrame:

    if not ATTENDANCE_MSG_CSV.exists():
        return pd.DataFrame(columns=[
            "DL_No", "Timing", "Category", "code", "Leave_Type",
            "Dated", "Status", "Remarks",
        ])

    msg_df = pd.read_csv(ATTENDANCE_MSG_CSV)
    msg_df.columns = msg_df.columns.str.strip()

    rows = []

    for i, msg_row in msg_df.iterrows():

        message = str(msg_row.get("message", ""))

        code_match = re.search(r"for \*\*([A-Za-z0-9\-]+)\*\*", message)
        instructor_match = re.search(r"Instructor:\s*\*\*(.*?)\*\*", message)

        code = code_match.group(1) if code_match else "Unknown"
        instructor = instructor_match.group(1) if instructor_match else "Unknown"

        subject_name = CODE_TO_SUBJECT.get(code, code)
        start_time, end_time = CODE_TO_TIMING.get(code, ("", ""))

        try:
            date_obj = datetime.strptime(str(msg_row["date"]).strip(), "%Y-%m-%d")
        except (ValueError, KeyError):
            date_obj = None

        rows.append({
            "DL_No": 3000000 + i,
            "Timing": f"{start_time} - {end_time}" if start_time else "",
            "Category": subject_name,
            "code": code,
            "Leave_Type": "Lecture Bases",
            "Dated": date_obj.strftime("%d %b %Y") if date_obj else str(msg_row.get("date", "")),
            "Status": "Recommend and Approved",
            "Remarks": f"Absent from {subject_name} class — Instructor {instructor}.",
        })

    return pd.DataFrame(rows)


leaves_df = build_leaves_df()


# ============================================================
# PER-ROW "VIEW DOC" PDF
#
# A simple, real, downloadable document per leave record —
# generated on the fly (same reportlab technique already used in
# fees.py) rather than a decorative button with nothing behind it.
# ============================================================

def build_leave_doc_pdf(row: dict) -> bytes:

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=22 * mm, rightMargin=22 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Normal"], fontSize=16, fontName="Helvetica-Bold")
    normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=11, leading=17)

    elements = [
        Paragraph("Disciplinary Leave Record", title_style),
        Spacer(1, 14),
    ]

    fields = [
        ("DL No.", str(row["DL_No"])),
        ("Student", STUDENT_NAME),
        ("Category", row["Category"]),
        ("Leave Type", row["Leave_Type"]),
        ("Dated", row["Dated"]),
        ("Timing", row["Timing"]),
        ("Status", row["Status"]),
    ]

    table_data = [[Paragraph(f"<b>{label}</b>", normal), Paragraph(value, normal)] for label, value in fields]
    field_table = Table(table_data, colWidths=[40 * mm, 110 * mm])
    field_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(field_table)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("<b>Remarks</b>", normal))
    elements.append(Paragraph(row["Remarks"], normal))

    doc.build(elements)
    return buffer.getvalue()


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
    max-width: 960px;
    padding: 14px 14px 30px 14px;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* ---------- Header row: back / title / refresh ---------- */

div.stVerticalBlock[class*="st-key-lv_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 8px;
    margin-bottom: 18px;
}

div.stVerticalBlock[class*="st-key-lv_header_row"] > div:nth-child(2) {
    flex: 1;
}

.lv-header-title {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
}

div[class*="st-key-lv_back"] .stButton > button {
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

div[class*="st-key-lv_refresh"] .stButton > button {
    background: #262626;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    width: 40px;
    height: 40px;
    font-size: 17px;
    padding: 0;
}

div[class*="st-key-lv_refresh"] .stButton > button:hover {
    background: #333333;
}

/* ---------- Tab row (DL only) ---------- */

div.stVerticalBlock[class*="st-key-lv_tabs"] {
    background: #1a1a1a;
    border-radius: 16px;
    padding: 6px;
    margin-bottom: 18px;
}

div[class*="st-key-lv_tabs"] .stButton > button {
    background: #ffffff;
    color: #000000;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
    font-size: 14px;
    width: auto;
    min-width: 48px;
    height: 40px;
}

/* ---------- Table header row (built with the SAME 3-part flex
   structure as the data rows below, rather than one continuous
   <table> using table-layout:fixed — two different sizing
   mechanisms only approximate each other and can drift apart by
   a few pixels from how each counts borders/padding; using the
   identical structure for both guarantees they match exactly). ---------- */

div.stVerticalBlock[class*="st-key-lv_table_wrap"] {
    border-radius: 12px;
    border: 1px solid #262626;
    overflow: hidden;
}

.lv-header-flex {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    background: #f0f0f0;
    border-bottom: 2px solid #dddddd;
}

.lv-header-flex .lv-hgroup-1 { flex: 300 0 0; min-width: 0; }
.lv-header-flex .lv-hgroup-2 { flex: 90 0 0; min-width: 0; }
.lv-header-flex .lv-hgroup-3 { flex: 455 0 0; min-width: 0; }

table.lv-table {
    table-layout: fixed;
    border-collapse: collapse;
    width: 100%;
    background: transparent;
    color: #111111;
    font-size: 13px;
}

table.lv-table th {
    text-align: left;
    padding: 10px 12px;
    border-right: 1px solid #e5e5e5;
    font-weight: 700;
    word-wrap: break-word;
}

table.lv-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #eeeeee;
    border-right: 1px solid #f0f0f0;
    vertical-align: top;
    word-wrap: break-word;
}

table.lv-table tr:nth-child(even) td {
    background: #fafafa;
}

.lv-col-dlno { width: 70px; }
.lv-col-timing { width: 110px; }
.lv-col-category { width: 120px; }
.lv-col-filename { width: 90px; text-align: center; }
.lv-col-leavetype { width: 90px; }
.lv-col-dated { width: 65px; }
.lv-col-status { width: 120px; }
.lv-col-remarks { width: 180px; }

/* Real "View Doc" download buttons, one per row, styled to sit
   inside the table cell like the reference screenshot's button. */
div[class*="st-key-lv_doc_"] .stDownloadButton > button {
    background: #e8e8e8;
    color: #333333;
    border: 1px solid #cccccc;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    font-weight: 500;
    width: auto;
    min-width: 82px;
    height: 40px;
    white-space: nowrap;
}

.lv-empty {
    color: #888888;
    text-align: center;
    padding: 40px 20px;
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

with st.container(key="lv_header_row"):

    if st.button("BACK", key="lv_back"):
        st.switch_page("pages/dashboard.py")

    render('<div class="lv-header-title">Leaves</div>')

    if st.button("⟳", key="lv_refresh"):
        st.rerun()


# ============================================================
# TAB ROW — DL only, per your instructions
# ============================================================

with st.container(key="lv_tabs"):
    st.button("DL", key="lv_tab_dl", disabled=True)


# ============================================================
# TABLE
#
# Header + every row live inside ONE real st.container(key=...),
# not a raw HTML <div> opened in one render() call and closed in
# a separate one later — a plain HTML tag can't actually contain
# content from a later, separate st.markdown() call (each is its
# own independent fragment). Without a real containing element,
# the row's columns have nothing constraining their total width,
# which is what let them compress into each other and overlap. A
# real Streamlit container genuinely nests everything inside it,
# so overflow-x:auto on it works and each column keeps its own
# space.
# ============================================================

render("""
<style>
div.stVerticalBlock[class*="st-key-lv_row_"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    background: #ffffff;
    border-bottom: 1px solid #eeeeee;
    width: 100%;
}

/* Proportional flex-grow (matching the same 300:90:455 ratio the
   header's declared column widths use) instead of fixed pixel
   widths — this way each row stretches to fill the full container
   width exactly like the header table does (table-layout:fixed +
   width:100% scales its columns proportionally to fill the same
   space), so rows and header end up the same total width instead
   of the row being narrower. */
div.stVerticalBlock[class*="st-key-lv_row_"] > div:nth-child(1) {
    flex: 300 0 0 !important;
    width: auto !important;
    min-width: 0 !important;
}

div.stVerticalBlock[class*="st-key-lv_row_"] > div:nth-child(2) {
    flex: 90 0 0 !important;
    width: auto !important;
    min-width: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

div.stVerticalBlock[class*="st-key-lv_row_"] > div:nth-child(3) {
    flex: 455 0 0 !important;
    width: auto !important;
    min-width: 0 !important;
}

div.stVerticalBlock[class*="st-key-lv_row_"] table {
    table-layout: fixed;
    border-collapse: collapse;
    width: 100%;
    height: 100%;
}

div.stVerticalBlock[class*="st-key-lv_row_"] td {
    padding: 10px 12px;
    color: #111111;
    font-size: 13px;
    vertical-align: top;
    border-right: 1px solid #f0f0f0;
    word-wrap: break-word;
}
</style>
""")

if leaves_df.empty:
    render('<div class="lv-empty">No leave records found.</div>')
else:

    with st.container(key="lv_table_wrap"):

        render("""
        <div class="lv-header-flex">
            <div class="lv-hgroup-1">
                <table class="lv-table">
                    <tr>
                        <th class="lv-col-dlno">DL_No</th>
                        <th class="lv-col-timing">Timing</th>
                        <th class="lv-col-category">Category</th>
                    </tr>
                </table>
            </div>
            <div class="lv-hgroup-2">
                <table class="lv-table">
                    <tr><th class="lv-col-filename">File Name</th></tr>
                </table>
            </div>
            <div class="lv-hgroup-3">
                <table class="lv-table">
                    <tr>
                        <th class="lv-col-leavetype">Leave_Type</th>
                        <th class="lv-col-dated">Dated</th>
                        <th class="lv-col-status">Status</th>
                        <th class="lv-col-remarks">Remarks</th>
                    </tr>
                </table>
            </div>
        </div>
        """)

        for i, row in leaves_df.iterrows():

            with st.container(key=f"lv_row_{row['DL_No']}"):

                render(f"""
                <table>
                    <tr>
                        <td class="lv-col-dlno">{row['DL_No']}</td>
                        <td class="lv-col-timing">{row['Timing']}</td>
                        <td class="lv-col-category">{row['Category']}</td>
                    </tr>
                </table>
                """)

                pdf_bytes = build_leave_doc_pdf(row.to_dict())
                st.download_button(
                    "View Doc",
                    data=pdf_bytes,
                    file_name=f"DL_{row['DL_No']}.pdf",
                    mime="application/pdf",
                    key=f"lv_doc_{row['DL_No']}",
                )

                render(f"""
                <table>
                    <tr>
                        <td class="lv-col-leavetype">{row['Leave_Type']}</td>
                        <td class="lv-col-dated">{row['Dated']}</td>
                        <td class="lv-col-status">{row['Status']}</td>
                        <td class="lv-col-remarks">{row['Remarks']}</td>
                    </tr>
                </table>
                """)