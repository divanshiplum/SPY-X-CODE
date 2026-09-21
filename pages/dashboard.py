import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import math
import base64

from nav_sidebar import render_sidebar

# ============================================================
# AUTH CHECK (सिर्फ check करो, initialize नहीं)
# ============================================================
if not st.session_state.logged_in:
    st.switch_page("pages/login.py")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# SIDEBAR (also injects the shared theme CSS)
# ============================================================

render_sidebar("dashboard")


# ============================================================
# STUDENT DATA
# ============================================================

STUDENT_NAME = "Divanshi"
COURSE = "Bachelor's in Computer Application"
SEMESTER = 3
CGPA = 7.45

STUDENT_IMAGE = "student.jpg"
ATTENDANCE_CSV = "data/attendance_records.csv"


# ============================================================
# SUBJECT DATA
# ============================================================

subjects = pd.DataFrame({
    "subject": [
        "Data Structure",
        "Computer Architecture",
        "Information System",
        "Cybersecurity Fundamentals",
        "Operating System",
    ],
    "code": ["23CSR-449", "SPO-113", "23BDA-401", "23BDA-402", "23BDA-403"],
    "credits": ["3 Credits", "4 Credits", "4 Credits", "4 Credits", "3 Credits"],
    "attended": [0, 3, 18, 15, 20],
    "total": [0, 6, 24, 20, 25],
})

attended = np.array(subjects["attended"])
total = np.array(subjects["total"])
subjects["attendance"] = np.divide(
    attended * 100, total,
    out=np.zeros_like(attended, dtype=float),
    where=total != 0,
)

if os.path.exists(ATTENDANCE_CSV):
    attendance_log = pd.read_csv(ATTENDANCE_CSV, parse_dates=["date"])
else:
    attendance_log = pd.DataFrame(
        columns=["code", "date", "day", "start_time", "end_time", "room", "instructor", "status"]
    )

# Subject info
SUBJECT_INFO = {
    "23CSR-449": {"name": "Data Structure", "icon": "✉️"},
    "SPO-113": {"name": "Computer Architecture", "icon": "📈"},
    "23BDA-401": {"name": "Information System", "icon": "💡"},
    "23BDA-402": {"name": "Cybersecurity Fundamentals", "icon": "🛡️"},
    "23BDA-403": {"name": "Operating System", "icon": "🖥️"},
}


# ============================================================
# CSS — light theme, matching the HC NEXUS mockup
# ============================================================

render("""
<style>

/* ---------- Greeting card ---------- */

.hc-greeting-card {
    background: linear-gradient(135deg, var(--hc-purple-soft) 0%, var(--hc-blue-soft) 100%);
    padding: 20px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.hc-greeting-left { display: flex; align-items: center; gap: 14px; }

.hc-greeting-avatar {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: var(--hc-purple-soft);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.hc-greeting-text-sub { color: var(--hc-text-soft); font-size: 13px; }
.hc-greeting-text-name { color: var(--hc-text); font-size: 18px; font-weight: 800; }

.hc-greeting-icons { display: flex; gap: 16px; color: var(--hc-text-soft); font-size: 17px; }

/* ---------- Course card ---------- */

.hc-course-top {
    padding: 22px 22px 18px 22px;
}

.hc-course-card-bg {
    background: linear-gradient(135deg, var(--hc-purple-soft) 0%, var(--hc-blue-soft) 100%);
}

.hc-course-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
}

.hc-course-name {
    font-size: 17px;
    font-weight: 700;
    color: var(--hc-text);
    line-height: 1.4;
}

.hc-cgpa-box { text-align: right; }
.hc-cgpa-label { color: var(--hc-text-soft); font-size: 12px; margin-bottom: 2px; }
.hc-cgpa-value { color: var(--hc-text); font-size: 24px; font-weight: 800; }

.hc-divider { height: 1px; background: var(--hc-border); margin: 18px 0 0 0; }

div.stVerticalBlock[class*="st-key-hc_quick_row_1"],
div.stVerticalBlock[class*="st-key-hc_quick_row_2"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
    padding: 14px 22px;
}

div.stVerticalBlock[class*="st-key-hc_quick_row_2"] {
    padding-bottom: 22px;
}

div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div,
div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-hc_quick_"] .stButton > button {
    width: 100%;
    background: var(--hc-bg);
    border: none;
    border-radius: var(--hc-radius-md);
    color: var(--hc-text);
    font-weight: 600;
    font-size: 13px;
    padding: 14px 10px;
    text-align: left;
    white-space: pre-line;
    line-height: 1.5;
    transition: background-color 0.15s ease;
}

div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(1) .stButton > button { background: var(--hc-blue-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(1) .stButton > button:hover { background: var(--hc-blue-hover); }

div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(2) .stButton > button { background: var(--hc-orange-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(2) .stButton > button:hover { background: var(--hc-orange-hover); }

div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(3) .stButton > button { background: var(--hc-green-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_1"] > div:nth-child(3) .stButton > button:hover { background: var(--hc-green-hover); }

div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(1) .stButton > button { background: var(--hc-purple-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(1) .stButton > button:hover { background: var(--hc-purple-hover); }

div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(2) .stButton > button { background: var(--hc-yellow-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(2) .stButton > button:hover { background: var(--hc-yellow-hover); }

div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(3) .stButton > button { background: var(--hc-teal-soft); }
div.stVerticalBlock[class*="st-key-hc_quick_row_2"] > div:nth-child(3) .stButton > button:hover { background: var(--hc-teal-hover); }

/* ---------- Subjects header ---------- */

.hc-subjects-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 26px 2px 4px 2px;
}

.hc-subjects-title { font-size: 20px; font-weight: 800; color: var(--hc-text); }
.hc-subjects-count { color: var(--hc-text-soft); font-size: 13px; margin: 2px 2px 16px 2px; }
.hc-filter { color: var(--hc-text-soft); font-size: 13px; }

/* ---------- Subject card container (NO MARGIN!) ---------- */

.hc-subject-card-container {
    margin-bottom: 14px;
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    overflow: hidden;
}

.hc-subject-card {
    position: relative;
    background: var(--hc-surface);
    border-left: 5px solid transparent;
    padding: 18px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.hc-subject-card.red { border-left-color: var(--hc-red); }
.hc-subject-card.purple { border-left-color: var(--hc-purple); }
.hc-subject-card.green { border-left-color: var(--hc-green); }

.hc-subject-left { display: flex; align-items: flex-start; gap: 14px; }

.hc-subject-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.hc-subject-card.red .hc-subject-icon { background: var(--hc-red-soft); }
.hc-subject-card.purple .hc-subject-icon { background: var(--hc-purple-soft); }
.hc-subject-card.green .hc-subject-icon { background: var(--hc-green-soft); }

.hc-subject-name { font-size: 16px; font-weight: 700; color: var(--hc-text); }
.hc-subject-code { color: var(--hc-text-soft); font-size: 13px; margin-top: 4px; }

.hc-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    border-radius: 20px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 12px;
}

.hc-status-pill.bad { background: var(--hc-red-soft); color: var(--hc-red); }
.hc-status-pill.good { background: var(--hc-green-soft); color: var(--hc-green); }

.hc-ring-wrap { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }

.hc-ring {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-shrink: 0;
}

.hc-ring::before {
    content: "";
    position: absolute;
    width: 44px;
    height: 44px;
    background: var(--hc-surface);
    border-radius: 50%;
}

.hc-ring-value {
    position: relative;
    font-size: 13px;
    font-weight: 800;
    color: var(--hc-text);
}

.hc-ring-fraction { color: var(--hc-text-soft); font-size: 12px; min-width: 32px; }

.hc-subject-dots {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.hc-subject-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

/* ---------- View Attendance Button (ATTACHED TO BOTTOM) ---------- */

div[class*="st-key-attendance_"] {
    margin: 0 !important;
}

div[class*="st-key-attendance_"] .stButton {
    width: 100%;
    margin: 0 !important;
}

div[class*="st-key-attendance_"] .stButton > button {
    width: 100% !important;
    background: var(--hc-purple-soft) !important;
    border: none !important;
    border-radius: 0 !important;
    color: var(--hc-purple) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 12px 22px !important;
    text-align: center !important;
    transition: all 0.2s ease !important;
    border-top: 1px solid var(--hc-border) !important;
    margin: 0 !important;
    height: auto !important;
}

div[class*="st-key-attendance_"] .stButton > button:hover {
    background: var(--hc-purple-hover) !important;
    color: var(--hc-purple-text) !important;
}

div[class*="st-key-attendance_"] .stButton > button:active {
    opacity: 0.9 !important;
}

/* ---------- ATTENDANCE VIEW STYLES ---------- */

.attendance-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--hc-border);
}

.attendance-header-title {
    font-size: 24px;
    font-weight: 700;
    color: var(--hc-text);
}

.attendance-icon {
    font-size: 28px;
}

.attendance-stat-card {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    padding: 16px;
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 140px;
}

.stat-label {
    color: var(--hc-text-soft);
    font-size: 13px;
    margin-bottom: 8px;
}

.stat-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 4px;
}

.stat-percentage {
    font-size: 12px;
    color: var(--hc-text-soft);
}

.timeline-container {
    position: relative;
    padding-left: 40px;
}

.timeline-line {
    position: absolute;
    left: 16px;
    top: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, var(--hc-green) 0%, var(--hc-red) 100%);
}

.timeline-item {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
    position: relative;
}

.timeline-dot {
    position: absolute;
    left: -28px;
    top: 8px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border: 3px solid var(--hc-surface);
    z-index: 2;
}

.timeline-dot.present {
    background-color: var(--hc-green);
}

.timeline-dot.absent {
    background-color: var(--hc-red);
}

.timeline-content {
    flex: 1;
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    padding: 16px;
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    border-left: 4px solid transparent;
}

.timeline-content.present {
    border-left-color: var(--hc-green);
}

.timeline-content.absent {
    border-left-color: var(--hc-red);
}

.timeline-date {
    font-size: 16px;
    font-weight: 700;
    color: var(--hc-text);
    margin-bottom: 6px;
}

.timeline-time {
    font-size: 13px;
    color: var(--hc-text-soft);
    margin-bottom: 8px;
}

.timeline-instructor {
    font-size: 13px;
    color: var(--hc-text-soft);
    margin-bottom: 8px;
}

.timeline-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 16px;
    font-size: 13px;
    font-weight: 700;
}

.timeline-status.present {
    background: var(--hc-green-soft);
    color: var(--hc-green);
}

.timeline-status.absent {
    background: var(--hc-red-soft);
    color: var(--hc-red);
}

/* ---------- BACK BUTTON ---------- */

div[class*="st-key-back_btn_"] .stButton > button {
    background: var(--hc-purple-soft) !important;
    border: 1px solid var(--hc-border) !important;
    border-radius: var(--hc-radius-md) !important;
    color: var(--hc-purple) !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
}

div[class*="st-key-back_btn_"] .stButton > button:hover {
    background: var(--hc-purple-hover) !important;
    border-color: var(--hc-purple) !important;
}

@media (max-width: 900px) {
    .block-container { padding-left: 24px !important; }
}

</style>
""")


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "show_attendance" not in st.session_state:
    st.session_state.show_attendance = False
    st.session_state.attendance_subject_code = None


# ============================================================
# ATTENDANCE VIEW
# ============================================================

if st.session_state.show_attendance and st.session_state.attendance_subject_code:
    
    subject_code = st.session_state.attendance_subject_code
    subject_name = SUBJECT_INFO[subject_code]["name"]
    subject_icon = SUBJECT_INFO[subject_code]["icon"]
    
    # Back button
    if st.button("← Back", key="back_btn_attendance"):
        st.session_state.show_attendance = False
        st.rerun()
    
    # Header
    render(f"""
    <div class="attendance-header">
        <div class="attendance-icon">{subject_icon}</div>
        <div>
            <div class="attendance-header-title">{subject_name}</div>
            <div style="color: var(--hc-text-soft); font-size: 13px; margin-top: 2px;">{subject_code}</div>
        </div>
    </div>
    """)
    
    # Filter attendance by subject
    subject_attendance = attendance_log[attendance_log["code"] == subject_code].copy()
    
    if len(subject_attendance) > 0:
        # Sort by date descending
        subject_attendance = subject_attendance.sort_values("date", ascending=False)
        
        # Stats
        total_classes = len(subject_attendance)
        present_count = len(subject_attendance[subject_attendance["status"] == "Present"])
        absent_count = len(subject_attendance[subject_attendance["status"] == "Absent"])
        present_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        # Display stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render(f"""
            <div class="attendance-stat-card">
                <div class="stat-label">Total Classes</div>
                <div class="stat-value">{total_classes}</div>
            </div>
            """)
        
        with col2:
            render(f"""
            <div class="attendance-stat-card" style="background: linear-gradient(135deg, var(--hc-green-soft) 0%, var(--hc-surface) 100%);">
                <div class="stat-label">Present</div>
                <div class="stat-value">{present_count}</div>
                <div class="stat-percentage">{present_percentage:.1f}%</div>
            </div>
            """)
        
        with col3:
            render(f"""
            <div class="attendance-stat-card" style="background: linear-gradient(135deg, var(--hc-red-soft) 0%, var(--hc-surface) 100%);">
                <div class="stat-label">Absent</div>
                <div class="stat-value">{absent_count}</div>
                <div class="stat-percentage">{(absent_count/total_classes*100):.1f}%</div>
            </div>
            """)
        
        st.markdown("---")
        
        # Timeline
        st.subheader("📅 Attendance Timeline")
        
        timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
        
        for _, row in subject_attendance.iterrows():
            status = row["status"]
            date_str = pd.to_datetime(row["date"]).strftime("%A, %d %b %Y")
            time_str = f"{row['start_time']} - {row['end_time']}"
            instructor = row["instructor"] if pd.notna(row["instructor"]) else "N/A"
            
            status_class = "present" if status == "Present" else "absent"
            status_icon = "✓" if status == "Present" else "✕"
            status_text = "Present" if status == "Present" else "Absent"
            
            timeline_html += f"""
            <div class="timeline-item">
                <div class="timeline-dot {status_class}"></div>
                <div class="timeline-content {status_class}">
                    <div class="timeline-date">{date_str}</div>
                    <div class="timeline-time">⏱️ {time_str}</div>
                    <div class="timeline-instructor">👨‍🏫 {instructor}</div>
                    <div class="timeline-status {status_class}">{status_icon} {status_text}</div>
                </div>
            </div>
            """
        
        timeline_html += '</div>'
        render(timeline_html)
    
    else:
        st.info(f"No attendance records found for {subject_name}")


# ============================================================
# DASHBOARD VIEW
# ============================================================

else:
    
    # ============================================================
    # GREETING CARD
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

    render(f"""
    <div class="hc-card hc-greeting-card">
        <div class="hc-greeting-left">
            <div class="hc-greeting-avatar">🧑‍🎓</div>
            <div>
                <div class="hc-greeting-text-sub">{greeting},</div>
                <div class="hc-greeting-text-name">{STUDENT_NAME}</div>
            </div>
        </div>
        <div class="hc-greeting-icons">
            <span>+</span>
        </div>
    </div>
    """)


    # ============================================================
    # COURSE CARD
    # ============================================================

    QUICK_ITEMS = [
        ("✉️", "Messages", "pages/messages.py"),
        ("📅", "Date Sheet", "pages/datesheet.py"),
        ("🧑‍🏫", "Leaves", "pages/leaves.py"),
        ("🔊", "Notices", "pages/notices.py"),
        ("💲", "Fees", "pages/fees.py"),
        ("🎫", "ID Card", "pages/id-card.py"),
    ]

    with st.container(key="hc_course_card"):

        render(f"""
        <div class="hc-card hc-course-card-bg">
            <div class="hc-course-top">
                <div class="hc-course-row">
                    <div class="hc-course-name">
                        📖 &nbsp; {COURSE}<br>(Sem-{SEMESTER})
                    </div>
                    <div class="hc-cgpa-box">
                        <div class="hc-cgpa-label">CGPA</div>
                        <div class="hc-cgpa-value">{CGPA}</div>
                    </div>
                </div>
                <div class="hc-divider"></div>
            </div>
        </div>
        """)

        rows = [QUICK_ITEMS[0:3], QUICK_ITEMS[3:6]]
        for row_index, row_items in enumerate(rows, start=1):
            with st.container(key=f"hc_quick_row_{row_index}"):
                for icon, label, target_page in row_items:
                    if st.button(f"{icon}\n{label}", key=f"hc_quick_{label}"):
                        if target_page:
                            st.switch_page(target_page)


    # ============================================================
    # SUBJECT LIST
    # ============================================================

    render(f"""
    <div class="hc-subjects-header">
        <div class="hc-subjects-title">Your Subjects</div>
        <div class="hc-filter">☰ &nbsp; Filter</div>
    </div>
    <div class="hc-subjects-count">{len(subjects)} subjects</div>
    """)


    def classes_to_recover(attended_count, total_count):
        if total_count == 0 or attended_count / total_count >= 0.75:
            return 0
        return max(0, math.ceil((0.75 * total_count - attended_count) / 0.25))


    def safe_to_miss(attended_count, total_count):
        if total_count == 0 or attended_count / total_count < 0.75:
            return 0
        return max(0, math.floor(attended_count / 0.75 - total_count))


    SUBJECT_ICONS = {
        "Data Structure": "✉️",
        "Computer Architecture": "📈",
        "Information System": "💡",
        "Cybersecurity Fundamentals": "🛡️",
        "Operating System": "🖥️",
    }

    for _, row in subjects.iterrows():

        percentage = int(row["attendance"])

        if percentage < 75:
            border_class = "red"
            pill_class = "bad"
            needed = classes_to_recover(int(row["attended"]), int(row["total"]))
            pill_text = f"❌ Attend {needed} to recover"
            ring_color = "var(--hc-red)"
            dot_colors = ["var(--hc-red)", "var(--hc-red)", "var(--hc-orange)", "var(--hc-green)", "var(--hc-green)"]
        elif percentage < 90:
            border_class = "purple"
            pill_class = "good"
            safe = safe_to_miss(int(row["attended"]), int(row["total"]))
            pill_text = f"✓ Safe to miss {safe} classes"
            ring_color = "var(--hc-purple)"
            dot_colors = ["var(--hc-red)", "var(--hc-orange)", "var(--hc-purple)", "var(--hc-green)", "var(--hc-green)"]
        else:
            border_class = "green"
            pill_class = "good"
            safe = safe_to_miss(int(row["attended"]), int(row["total"]))
            pill_text = f"✓ Safe to miss {safe} classes"
            ring_color = "var(--hc-green)"
            dot_colors = ["var(--hc-orange)", "var(--hc-green)", "var(--hc-green)", "var(--hc-green)", "var(--hc-green)"]

        degree = percentage * 3.6
        ring_bg = (
            f"background: conic-gradient({ring_color} 0deg {degree}deg, #ececf5 {degree}deg 360deg);"
            if percentage > 0 else "background: #ececf5;"
        )

        dots_html = "".join(
            f'<span class="hc-subject-dot" style="background:{c};"></span>' for c in dot_colors
        )

        icon = SUBJECT_ICONS.get(row["subject"], "📘")
        subject_code = row["code"]

        # Render card container with button inside
        render(f"""
        <div class="hc-subject-card-container">
            <div class="hc-subject-card {border_class}">
                <div class="hc-subject-left">
                    <div class="hc-subject-icon">{icon}</div>
                    <div>
                        <div class="hc-subject-name">{row['subject']}</div>
                        <div class="hc-subject-code">{row['code']} &bull; {row['credits']}</div>
                        <div class="hc-status-pill {pill_class}">{pill_text}</div>
                    </div>
                </div>
                <div class="hc-ring-wrap">
                    <div class="hc-ring" style="{ring_bg}">
                        <div class="hc-ring-value">{percentage}</div>
                    </div>
                    <div class="hc-ring-fraction">{row['attended']}/{row['total']}</div>
                    <div class="hc-subject-dots">{dots_html}</div>
                </div>
            </div>
        """)
        
        # Button directly in the container
        if st.button(
            "View Attendance Timeline",
            key=f"attendance_{subject_code}",
            use_container_width=True
        ):
            st.session_state.show_attendance = True
            st.session_state.attendance_subject_code = subject_code
            st.rerun()
        
        render("""</div>""")