import streamlit as st
import pandas as pd
import numpy as np
from PyPDF2 import PdfReader
from datetime import datetime
import os
import math
import base64


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# HTML RENDER HELPER
# (Strips leading whitespace from every line before handing it
# to st.markdown, so Markdown never mistakes indented HTML for a
# code block.)
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# STUDENT DATA
# ============================================================

STUDENT_NAME = "Divanshi"
COURSE = "Bachelor's in Computer Application"
SEMESTER = 3
CGPA = 7.45

SECTION = ""  # optional line under the name, leave blank to hide

STUDENT_IMAGE = "student.jpg"
ATTENDANCE_CSV = "attendance_records.csv"


# ============================================================
# SUBJECT DATA (unchanged)
# ============================================================

subjects = pd.DataFrame({

    "subject": [
        "Data Structure",
        "Computer Architecture",
        "Information System",
        "Cybersecurity Fundamentals",
        "Operating System"
    ],

    "code": [
        "23CSR-449",
        "SPO-113",
        "23BDA-401",
        "23BDA-402",
        "23BDA-403"
    ],

    "credits": [
        "3 Credits",
        "4 Credits",
        "4 Credits",
        "4 Credits",
        "3 Credits"
    ],

    "attended": [
        0,
        3,
        18,
        15,
        20
    ],

    "total": [
        0,
        6,
        24,
        20,
        25
    ]
})


# ============================================================
# NUMPY ATTENDANCE CALCULATION
# ============================================================

attended = np.array(subjects["attended"])
total = np.array(subjects["total"])

attendance_percentage = np.divide(
    attended * 100,
    total,
    out=np.zeros_like(attended, dtype=float),
    where=total != 0
)

subjects["attendance"] = attendance_percentage


# ============================================================
# LOAD ATTENDANCE RECORD LOG (separate CSV file)
#
# Expected columns: code,date,day,start_time,end_time,instructor,status
# "status" is either "Present" or "Absent". One row per class held.
# ============================================================

if os.path.exists(ATTENDANCE_CSV):
    attendance_log = pd.read_csv(ATTENDANCE_CSV, parse_dates=["date"])
else:
    attendance_log = pd.DataFrame(
        columns=["code", "date", "day", "start_time", "end_time", "room", "instructor", "status"]
    )


# ============================================================
# TIME BASED GREETING
# ============================================================

hour = datetime.now().hour

if 5 <= hour < 12:
    greeting = "Good Morning"
elif 12 <= hour < 17:
    greeting = "Good Afternoon"
elif 17 <= hour < 21:
    greeting = "Good Evening"
else:
    greeting = "Good Night"


# ============================================================
# SESSION STATE
# ============================================================

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "detail_tab" not in st.session_state:
    st.session_state.detail_tab = "Timeline"


# ============================================================
# CUSTOM CSS
# ============================================================

render("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background: #121212;
    color: #ffffff;
}

.block-container {
    max-width: 720px;
    padding-top: 18px;
    padding-bottom: 105px;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* Reskin every Streamlit button to fit the dark theme */
.stButton > button {
    background: #1d1d1d;
    color: #eeeeee;
    border: 1px solid #2c2c2c;
    border-radius: 14px;
    font-weight: 600;
    padding: 8px 14px;
}
.stButton > button:hover {
    border-color: #4a4a4a;
    color: #ffffff;
}
.stButton > button:focus:not(:active) {
    color: #ffffff;
    border-color: #4a4a4a;
}

/* TOP HEADER */

.top-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.profile-area {
    display: flex;
    align-items: center;
    gap: 14px;
    min-width: 0;
}

.profile-image {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #2d2d2d;
    flex-shrink: 0;
}

.profile-placeholder {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: #292929;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 35px;
    flex-shrink: 0;
}

.profile-text { min-width: 0; }

.greeting {
    color: #999999;
    font-size: 16px;
    margin-bottom: 3px;
}

.student-name {
    color: #ffffff;
    font-size: 29px;
    font-weight: 700;
    line-height: 1.15;
}

.student-section {
    color: #888888;
    font-size: 14px;
    margin-top: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
}

.top-actions {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-shrink: 0;
}

.top-icon {
    color: #eeeeee;
    font-size: 27px;
    line-height: 1;
}

/* COURSE CARD */

.course-card {
    width: 100%;
    box-sizing: border-box;
    background: #1d1d1d;
    border-radius: 27px;
    padding: 25px 20px 15px 20px;
    margin-bottom: 24px;
    border: 1px solid #252525;
}

.course-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 15px;
}

.course-left { flex: 1; min-width: 0; }

.course-name {
    color: #ffffff;
    font-size: 21px;
    font-weight: 600;
    line-height: 1.35;
}

.cgpa-box { text-align: right; min-width: 80px; }

.cgpa-title {
    color: #999999;
    font-size: 16px;
    margin-bottom: 5px;
}

.cgpa-value {
    color: #ffffff;
    font-size: 40px;
    font-weight: 400;
}

.divider {
    height: 1px;
    background: #303030;
    margin: 20px 0 0 0;
}

/* QUICK MENU: 3 columns x 2 rows, compact sizing */

.quick-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    width: 100%;
    row-gap: 14px;
    padding-top: 14px;
}

.quick-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.icon-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
}

.quick-icon { font-size: 21px; line-height: 1; }

.quick-title {
    color: #eeeeee;
    font-size: 12px;
    font-weight: 600;
}

/* SUBJECT HEADER */

.subjects-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 25px 5px 3px 5px;
}

.subjects-title {
    color: #ffffff;
    font-size: 27px;
    font-weight: 700;
}

.filter { color: #999999; font-size: 16px; }

.subject-count {
    color: #777777;
    font-size: 17px;
    margin: 3px 5px 16px 5px;
}

/* SUBJECT CARD */

.subject-card {
    position: relative;
    width: 100%;
    min-height: 172px;
    box-sizing: border-box;
    background: #1b1b1b;
    border: 1px solid #2c2c2c;
    border-radius: 24px 24px 0 0;
    padding: 25px 46px 22px 25px;
    overflow: hidden;
}

.subject-card-standalone {
    border-radius: 24px;
    margin-bottom: 16px;
}

.subject-card-red { border-left: 6px solid #ff3b3b; }
.subject-card-green { border-left: 6px solid #29d65c; }

.subject-name {
    color: #ffffff;
    font-size: 21px;
    font-weight: 700;
    line-height: 1.25;
    padding-right: 110px;
}

.subject-code {
    color: #999999;
    font-size: 15px;
    margin-top: 12px;
    padding-right: 105px;
}

.recover {
    display: inline-block;
    background: #4c2523;
    border: 1px solid #71302c;
    color: #ff5252;
    border-radius: 22px;
    padding: 8px 13px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 15px;
}

.good-attendance {
    display: inline-block;
    background: #183d25;
    border: 1px solid #216b38;
    color: #3ee873;
    border-radius: 22px;
    padding: 8px 13px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 15px;
}

.card-menu {
    position: absolute;
    top: 18px;
    right: 18px;
    color: #777777;
    font-size: 19px;
    letter-spacing: 1px;
}

.card-chevron {
    position: absolute;
    top: 50%;
    right: 8px;
    transform: translateY(-50%);
    color: #5a5a5a;
    font-size: 22px;
    font-weight: 700;
}

/* Button that opens the attendance detail view — visually
   attached to the bottom of the subject card above it */
div[data-testid="stButton"].view-attendance-btn > button,
.view-attendance-btn > button {
    width: 100%;
    border-radius: 0 0 24px 24px !important;
    border-top: none !important;
    background: #191919 !important;
    color: #9fa0a3 !important;
    font-size: 13px !important;
    text-align: left !important;
    margin-top: -1px;
    margin-bottom: 16px !important;
}

/* ATTENDANCE CIRCLE */

.attendance-wrapper {
    position: absolute;
    right: 40px;
    top: 28px;
    width: 90px;
    text-align: center;
}

.attendance-circle {
    width: 86px;
    height: 86px;
    margin: 0 auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.attendance-circle::before {
    content: "";
    position: absolute;
    width: 70px;
    height: 70px;
    background: #1b1b1b;
    border-radius: 50%;
}

.arc-marker {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
}

.arc-marker::after {
    content: "";
    position: absolute;
    top: 1px;
    left: 50%;
    transform: translateX(-50%);
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 0 2px #1b1b1b;
}

.attendance-number {
    position: relative;
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 3px;
}

.tick {
    color: #6a6a6a;
    font-size: 13px;
    font-weight: 400;
}

.attendance-fraction {
    color: #999999;
    font-size: 14px;
    margin-top: 7px;
}

.attendance-dots {
    position: absolute;
    right: -14px;
    top: 6px;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.attendance-dot {
    display: block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.dot-red { background: #ff3b3b; }
.dot-pink { background: #ff4f87; }
.dot-green { background: #32d65b; }

/* DETAIL VIEW: TABS */

.tab-row {
    display: flex;
    gap: 6px;
    background: #1b1b1b;
    border: 1px solid #2c2c2c;
    border-radius: 18px;
    padding: 6px;
    margin: 14px 0 18px 0;
}

/* DETAIL VIEW: LEGEND */

.legend-row {
    display: flex;
    gap: 22px;
    justify-content: center;
    margin: 4px 0 20px 0;
    color: #cccccc;
    font-size: 14px;
}

.legend-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 7px;
}

/* DETAIL VIEW: TIMELINE */

.timeline-row {
    display: flex;
    align-items: stretch;
    gap: 12px;
    position: relative;
}

.timeline-marker {
    width: 16px;
    flex-shrink: 0;
    position: relative;
    display: flex;
    justify-content: center;
}

.timeline-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-top: 24px;
    position: relative;
    z-index: 2;
    flex-shrink: 0;
}

.timeline-connector {
    position: absolute;
    top: 36px;
    bottom: -14px;
    width: 2px;
}

.timeline-card {
    flex: 1;
    background: #1b1b1b;
    border: 1px solid #2c2c2c;
    border-left: 4px solid transparent;
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}

.timeline-date {
    color: #ffffff;
    font-size: 16px;
    font-weight: 700;
}

.timeline-meta {
    color: #999999;
    font-size: 13px;
    margin-top: 6px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 10px;
}

.pill-present {
    background: #183d25;
    border: 1px solid #216b38;
    color: #3ee873;
}

.pill-absent {
    background: #4c2523;
    border: 1px solid #71302c;
    color: #ff5252;
}

.no-records {
    color: #888888;
    font-size: 14px;
    text-align: center;
    padding: 30px 0;
}

/* BOTTOM NAVIGATION */

.bottom-nav {
    position: fixed;
    left: 50%;
    bottom: 0;
    transform: translateX(-50%);
    width: min(720px, 100%);
    height: 76px;
    background: #171717;
    border-top: 1px solid #292929;
    display: flex;
    align-items: center;
    justify-content: space-around;
    z-index: 999999;
}

.nav-item {
    color: #eeeeee;
    text-align: center;
    font-size: 26px;
    min-width: 65px;
    line-height: 1;
}

.nav-text { display: block; font-size: 12px; margin-top: 5px; }

.nav-active {
    background: #454545;
    border-radius: 35px;
    padding: 10px 25px;
    font-weight: 700;
}

/* MOBILE */

@media (max-width: 600px) {

    .block-container {
        padding-left: 13px;
        padding-right: 13px;
        padding-top: 14px;
        padding-bottom: 100px;
    }

    .profile-image, .profile-placeholder { width: 65px; height: 65px; }
    .greeting { font-size: 14px; }
    .student-name { font-size: 25px; }
    .student-section { font-size: 13px; max-width: 170px; }
    .top-actions { gap: 9px; }
    .top-icon { font-size: 24px; }

    .course-card { padding: 22px 17px 12px 17px; border-radius: 24px; }
    .course-name { font-size: 18px; }
    .cgpa-title { font-size: 13px; }
    .cgpa-value { font-size: 34px; }

    .quick-icon { font-size: 19px; }
    .quick-title { font-size: 10px; }

    .subjects-title { font-size: 24px; }
    .filter { font-size: 14px; }

    .subject-card { min-height: 165px; padding: 23px 40px 20px 20px; }
    .subject-name { font-size: 18px; padding-right: 95px; }
    .subject-code { font-size: 13px; padding-right: 92px; }

    .attendance-wrapper { right: 32px; top: 28px; width: 80px; }
    .attendance-circle { width: 76px; height: 76px; }
    .attendance-circle::before { width: 62px; height: 62px; }
    .attendance-dots { right: -12px; }
    .attendance-dot { width: 9px; height: 9px; }
    .card-chevron { right: 4px; font-size: 20px; }
    .card-menu { top: 16px; right: 14px; font-size: 17px; }

}

</style>
""")


# ============================================================
# PROFILE IMAGE
# ============================================================

if os.path.exists(STUDENT_IMAGE):
    with open(STUDENT_IMAGE, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    image_html = f'<img src="data:image/jpeg;base64,{encoded}" class="profile-image">'
else:
    image_html = '<div class="profile-placeholder">👤</div>'


# ============================================================
# TOP HEADER
# ============================================================

section_html = f'<div class="student-section">{SECTION}</div>' if SECTION else ""

render(f"""
<div class="top-header">
    <div class="profile-area">
        {image_html}
        <div class="profile-text">
            <div class="greeting">{greeting}</div>
            <div class="student-name">{STUDENT_NAME}</div>
            {section_html}
        </div>
    </div>
    <div class="top-actions">
        <div class="top-icon">＋</div>
        <div class="top-icon">⚙</div>
        <div class="top-icon">☰</div>
    </div>
</div>
""")


# ============================================================
# COURSE CARD (only shown on the subject list, not the detail view)
# ============================================================

def render_course_card():
    render(f"""
    <div class="course-card">
        <div class="course-row">
            <div class="course-left">
                <div class="course-name">
                    📖 &nbsp; {COURSE}<br>
                    &nbsp;&nbsp;&nbsp;&nbsp; (Sem-{SEMESTER})
                </div>
            </div>
            <div class="cgpa-box">
                <div class="cgpa-title">CGPA</div>
                <div class="cgpa-value">{CGPA}</div>
            </div>
        </div>
        <div class="divider"></div>
        <div class="quick-grid">
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">✉️</div></div>
                <div class="quick-title">Messages</div>
            </div>
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">📅</div></div>
                <div class="quick-title">Date Sheet</div>
            </div>
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">🧑‍🏫</div></div>
                <div class="quick-title">Leaves</div>
            </div>
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">🔊</div></div>
                <div class="quick-title">Notices</div>
            </div>
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">💲</div></div>
                <div class="quick-title">Fees</div>
            </div>
            <div class="quick-item">
                <div class="icon-wrap"><div class="quick-icon">🪪</div></div>
                <div class="quick-title">ID Card</div>
            </div>
        </div>
    </div>
    """)


# ============================================================
# ATTENDANCE HELPERS
# ============================================================

def get_attendance_color(value):
    if value < 75:
        return "#ff4b4b"
    elif value < 85:
        return "#ffc107"
    else:
        return "#32d65b"


def classes_to_recover(attended_count, total_count):
    if total_count == 0:
        return 0
    if attended_count / total_count >= 0.75:
        return 0
    required = math.ceil((0.75 * total_count - attended_count) / 0.25)
    return max(0, required)


def safe_to_miss(attended_count, total_count):
    if total_count == 0:
        return 0
    current_percentage = attended_count / total_count
    if current_percentage < 0.75:
        return 0
    safe = math.floor(attended_count / 0.75 - total_count)
    return max(0, safe)


def subject_card_html(row, standalone=False):
    """Builds the HTML for one subject's card (circle, badge, etc.)."""

    percentage = int(row["attendance"])
    color = get_attendance_color(percentage)
    degree = percentage * 3.6

    if percentage == 0:
        circle_background = "background: conic-gradient(#353535 0deg, #353535 360deg);"
    else:
        circle_background = (
            f"background: conic-gradient({color} 0deg {degree}deg, "
            f"#353535 {degree}deg 360deg);"
        )

    if percentage < 75:
        card_class = "subject-card subject-card-red"
        required_classes = classes_to_recover(int(row["attended"]), int(row["total"]))
        status = f'<div class="recover">❌ &nbsp; Attend {required_classes} to recover</div>'
        dots = """
        <div class="attendance-dots">
            <span class="attendance-dot dot-red"></span>
            <span class="attendance-dot dot-pink"></span>
            <span class="attendance-dot dot-pink"></span>
            <span class="attendance-dot dot-green"></span>
            <span class="attendance-dot dot-green"></span>
        </div>
        """
    else:
        card_class = "subject-card subject-card-green"
        safe_classes = safe_to_miss(int(row["attended"]), int(row["total"]))
        status = f'<div class="good-attendance">✓ &nbsp; Safe to miss {safe_classes} classes</div>'
        dots = """
        <div class="attendance-dots">
            <span class="attendance-dot dot-pink"></span>
            <span class="attendance-dot dot-pink"></span>
            <span class="attendance-dot dot-green"></span>
            <span class="attendance-dot dot-green"></span>
            <span class="attendance-dot dot-green"></span>
        </div>
        """

    if standalone:
        card_class += " subject-card-standalone"
        corner_extras = f'<div class="card-menu">⋮</div>'
    else:
        corner_extras = f'<div class="card-menu">⋮</div>'

    return f"""
    <div class="{card_class}">
        {corner_extras}
        <div class="subject-name">{row["subject"]}</div>
        <div class="subject-code">{row["code"]} • {row["credits"]}</div>
        {status}
        <div class="attendance-wrapper">
            <div class="attendance-circle" style="{circle_background}">
                <div class="arc-marker" style="transform: rotate({degree}deg);"></div>
                <div class="attendance-number">
                    <span class="tick">–</span>{percentage}
                </div>
            </div>
            <div class="attendance-fraction">{row["attended"]}/{row["total"]}</div>
            {dots}
        </div>
    </div>
    """


# ============================================================
# SUBJECT LIST VIEW
# ============================================================

def render_subject_list():

    render_course_card()

    render(f"""
    <div class="subjects-header">
        <div class="subjects-title">Your Subjects</div>
        <div class="filter">☷ &nbsp; Filter</div>
    </div>
    <div class="subject-count">{len(subjects)} subjects</div>
    """)

    for _, row in subjects.iterrows():
        render(subject_card_html(row, standalone=False))

        clicked = st.button(
            "View attendance record  ›",
            key=f"view_{row['code']}",
            use_container_width=True,
        )

        if clicked:
            st.session_state.selected_subject = row["code"]
            st.session_state.detail_tab = "Timeline"
            st.rerun()


# ============================================================
# ATTENDANCE DETAIL VIEW
# ============================================================

def render_attendance_detail(subject_code):

    row = subjects[subjects["code"] == subject_code].iloc[0]

    if st.button("‹ Back to Subjects", key="back_btn"):
        st.session_state.selected_subject = None
        st.rerun()

    render(subject_card_html(row, standalone=True))

    tabs = ["Prediction", "Timeline", "Course Plan"]
    tab_icons = {"Prediction": "📊", "Timeline": "🕐", "Course Plan": "📄"}

    cols = st.columns(len(tabs))
    for col, tab_name in zip(cols, tabs):
        with col:
            if st.button(
                f"{tab_icons[tab_name]} {tab_name}",
                key=f"tab_{tab_name}",
                use_container_width=True,
            ):
                st.session_state.detail_tab = tab_name
                st.rerun()

    active_tab = st.session_state.detail_tab

    if active_tab != "Timeline":
        render(f'<div class="no-records">{active_tab} view is coming soon.</div>')
        return

    records = attendance_log[attendance_log["code"] == subject_code].copy()

    if records.empty:
        render('<div class="no-records">No classes have been recorded for this subject yet.</div>')
        return

    records = records.sort_values("date", ascending=False).reset_index(drop=True)

    present_count = int((records["status"] == "Present").sum())
    absent_count = int((records["status"] == "Absent").sum())

    render(f"""
    <div class="legend-row">
        <span><span class="legend-dot" style="background:#32d65b;"></span>Present ({present_count})</span>
        <span><span class="legend-dot" style="background:#ff3b3b;"></span>Absent ({absent_count})</span>
    </div>
    """)

    rows_html = ""
    total_rows = len(records)

    for i, rec in records.iterrows():
        is_present = rec["status"] == "Present"
        dot_color = "#32d65b" if is_present else "#ff3b3b"
        pill_class = "pill-present" if is_present else "pill-absent"
        pill_icon = "✓" if is_present else "✕"
        card_border = "#216b38" if is_present else "#71302c"

        date_str = rec["date"].strftime("%A, %d %b %Y")
        instructor = str(rec["instructor"])
        if len(instructor) > 22:
            instructor = instructor[:20] + "…"
        room = str(rec["room"]) if "room" in rec and pd.notna(rec.get("room")) else ""
        room_part = f"{room} &nbsp;•&nbsp; " if room else ""

        connector_html = ""
        if i < total_rows - 1:
            connector_html = f'<div class="timeline-connector" style="background:{dot_color};"></div>'

        rows_html += f"""
        <div class="timeline-row">
            <div class="timeline-marker">
                <span class="timeline-dot" style="background:{dot_color};"></span>
                {connector_html}
            </div>
            <div class="timeline-card" style="border-left-color:{card_border};">
                <div class="timeline-date">{date_str}</div>
                <div class="timeline-meta">🕐 &nbsp;{rec['start_time']} - {rec['end_time']} &nbsp;•&nbsp; {room_part}{instructor}</div>
                <div class="status-pill {pill_class}">{pill_icon} &nbsp;{rec['status']}</div>
            </div>
        </div>
        """

    render(rows_html)


# ============================================================
# MAIN PAGE ROUTING
# ============================================================

if st.session_state.selected_subject is None:
    render_subject_list()
else:
    render_attendance_detail(st.session_state.selected_subject)



# ============================================================
# BOTTOM NAVIGATION
# ============================================================

render("""
<div class="bottom-nav">
    <div class="nav-item">◎</div>
    <div class="nav-item nav-active">
        🏠
        <span class="nav-text">Home</span>
    </div>
    <div class="nav-item">📅</div>
    <div class="nav-item">📊</div>
</div>
""")