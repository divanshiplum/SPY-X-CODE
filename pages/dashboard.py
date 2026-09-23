import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import math

from nav_sidebar import render_sidebar
from theme import get_theme_css

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL THEME
# ============================================================

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

    flat = "\n".join(
        line.strip()
        for line in lines
    )

    st.html(flat)


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar("dashboard")


# ============================================================
# STUDENT DATA
# ============================================================

STUDENT_NAME = "Divanshi"

COURSE = "Bachelor's in Computer Application"

SEMESTER = 3

CGPA = 7.45

BASE_DIR = Path(__file__).resolve().parent.parent
ATTENDANCE_CSV = BASE_DIR / "data" / "attendance_records.csv"


# ============================================================
# SUBJECT DATA
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
# ATTENDANCE CALCULATION
# ============================================================

attended = np.array(subjects["attended"])

total = np.array(subjects["total"])

subjects["attendance"] = np.divide(
    attended * 100,
    total,
    out=np.zeros_like(attended, dtype=float),
    where=total != 0
)


# ============================================================
# ATTENDANCE CSV
# ============================================================

if os.path.exists(ATTENDANCE_CSV):

    attendance_log = pd.read_csv(
        ATTENDANCE_CSV,
        parse_dates=["date"]
    )

else:

    attendance_log = pd.DataFrame(
        columns=[
            "code",
            "date",
            "day",
            "start_time",
            "end_time",
            "room",
            "instructor",
            "status"
        ]
    )


# ============================================================
# SUBJECT INFO
# ============================================================

SUBJECT_INFO = {

    "23CSR-449": {
        "name": "Data Structure",
        "icon": "✉️"
    },

    "SPO-113": {
        "name": "Computer Architecture",
        "icon": "📈"
    },

    "23BDA-401": {
        "name": "Information System",
        "icon": "💡"
    },

    "23BDA-402": {
        "name": "Cybersecurity Fundamentals",
        "icon": "🛡️"
    },

    "23BDA-403": {
        "name": "Operating System",
        "icon": "🖥️"
    }
}


# ============================================================
# DASHBOARD CSS
# ============================================================

render(
    """
    <style>

    /* ======================================================
       GREETING CARD
       ====================================================== */

    .hc-greeting-card {

        background:
            linear-gradient(
                135deg,
                var(--hc-purple-soft) 0%,
                var(--hc-blue-soft) 100%
            );

        padding: 20px 24px;

        display: flex;

        align-items: center;

        justify-content: space-between;

        margin-bottom: 18px;
    }


    .hc-greeting-left {

        display: flex;

        align-items: center;

        gap: 14px;
    }


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


    .hc-greeting-text-sub {

        color: var(--hc-text-soft);

        font-size: 13px;
    }


    .hc-greeting-text-name {

        color: var(--hc-text);

        font-size: 18px;

        font-weight: 800;
    }


    .hc-greeting-icons {

        display: flex;

        gap: 16px;

        color: var(--hc-text-soft);

        font-size: 17px;
    }


    /* ======================================================
       COURSE CARD
       ====================================================== */

    .hc-course-top {

        padding: 22px 22px 18px 22px;
    }


    .hc-course-card-bg {

        background:
            linear-gradient(
                135deg,
                var(--hc-purple-soft) 0%,
                var(--hc-blue-soft) 100%
            );
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


    .hc-cgpa-box {

        text-align: right;
    }


    .hc-cgpa-label {

        color: var(--hc-text-soft);

        font-size: 12px;

        margin-bottom: 2px;
    }


    .hc-cgpa-value {

        color: var(--hc-text);

        font-size: 24px;

        font-weight: 800;
    }


    .hc-divider {

        height: 1px;

        background: var(--hc-border);

        margin: 18px 0 0 0;
    }


    /* ======================================================
       QUICK ACTION ROWS
       ====================================================== */

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


    /* ======================================================
       QUICK ACTION BASE
       ====================================================== */

    div[class*="st-key-hc_quick_"] .stButton > button {

        width: 100% !important;

        border: 1px solid transparent !important;

        border-radius: var(--hc-radius-md) !important;

        color: var(--hc-text) !important;

        font-weight: 600 !important;

        font-size: 13px !important;

        padding: 14px 10px !important;

        text-align: left !important;

        white-space: pre-line !important;

        line-height: 1.5 !important;

        cursor: pointer !important;

        transition:
            background-color 0.22s ease,
            border-color 0.22s ease,
            transform 0.22s ease,
            box-shadow 0.22s ease !important;
    }


    /* ======================================================
       1. MESSAGES — BLUE
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(1)
    .stButton > button {

        background: var(--hc-blue-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(1)
    .stButton > button:hover {

        background: var(--hc-blue-hover) !important;

        border-color: var(--hc-blue) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(139, 184, 217, 0.22) !important;
    }


    /* ======================================================
       2. DATE SHEET — ORANGE
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(2)
    .stButton > button {

        background: var(--hc-orange-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(2)
    .stButton > button:hover {

        background: var(--hc-orange-hover) !important;

        border-color: var(--hc-orange) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(229, 170, 130, 0.22) !important;
    }


    /* ======================================================
       3. LEAVES — GREEN
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(3)
    .stButton > button {

        background: var(--hc-green-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_1"]
    > div:nth-child(3)
    .stButton > button:hover {

        background: var(--hc-green-hover) !important;

        border-color: var(--hc-green) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(145, 199, 170, 0.22) !important;
    }


    /* ======================================================
       4. NOTICES — PURPLE
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(1)
    .stButton > button {

        background: var(--hc-purple-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(1)
    .stButton > button:hover {

        background: var(--hc-purple-hover) !important;

        border-color: var(--hc-purple) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(142, 124, 195, 0.22) !important;
    }


    /* ======================================================
       5. FEES — YELLOW
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(2)
    .stButton > button {

        background: var(--hc-yellow-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(2)
    .stButton > button:hover {

        background: var(--hc-yellow-hover) !important;

        border-color: var(--hc-yellow) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(232, 201, 125, 0.22) !important;
    }


    /* ======================================================
       6. ID CARD — TEAL
       ====================================================== */

    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(3)
    .stButton > button {

        background: var(--hc-teal-soft) !important;
    }


    div.stVerticalBlock[class*="st-key-hc_quick_row_2"]
    > div:nth-child(3)
    .stButton > button:hover {

        background: var(--hc-teal-hover) !important;

        border-color: var(--hc-teal) !important;

        transform:
            translateY(-3px)
            scale(1.02) !important;

        box-shadow:
            0 8px 18px
            rgba(141, 200, 193, 0.22) !important;
    }


    /* ======================================================
       SUBJECT HEADER
       ====================================================== */

    .hc-subjects-header {

        display: flex;

        justify-content: space-between;

        align-items: center;

        margin: 26px 2px 4px 2px;
    }


    .hc-subjects-title {

        font-size: 20px;

        font-weight: 800;

        color: var(--hc-text);
    }


    .hc-subjects-count {

        color: var(--hc-text-soft);

        font-size: 13px;

        margin: 2px 2px 16px 2px;
    }


    .hc-filter {

        color: var(--hc-text-soft);

        font-size: 13px;
    }


    /* ======================================================
       SUBJECT CARD
       ====================================================== */

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


    .hc-subject-card.red {

        border-left-color: var(--hc-red);
    }


    .hc-subject-card.purple {

        border-left-color: var(--hc-purple);
    }


    .hc-subject-card.green {

        border-left-color: var(--hc-green);
    }


    .hc-subject-left {

        display: flex;

        align-items: flex-start;

        gap: 14px;
    }


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


    .hc-subject-card.red
    .hc-subject-icon {

        background: var(--hc-red-soft);
    }


    .hc-subject-card.purple
    .hc-subject-icon {

        background: var(--hc-purple-soft);
    }


    .hc-subject-card.green
    .hc-subject-icon {

        background: var(--hc-green-soft);
    }


    .hc-subject-name {

        font-size: 16px;

        font-weight: 700;

        color: var(--hc-text);
    }


    .hc-subject-code {

        color: var(--hc-text-soft);

        font-size: 13px;

        margin-top: 4px;
    }


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


    .hc-status-pill.bad {

        background: var(--hc-red-soft);

        color: var(--hc-red);
    }


    .hc-status-pill.good {

        background: var(--hc-green-soft);

        color: var(--hc-green);
    }


    .hc-ring-wrap {

        display: flex;

        align-items: center;

        gap: 12px;

        flex-shrink: 0;
    }


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


    .hc-ring-fraction {

        color: var(--hc-text-soft);

        font-size: 12px;

        min-width: 32px;
    }


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


    /* ======================================================
       ATTENDANCE BUTTON
       ====================================================== */

    div[class*="st-key-attendance_"] {

        margin: 0 !important;
    }


    div[class*="st-key-attendance_"] .stButton {

        width: 100%;

        margin: 0 !important;
    }


    div[class*="st-key-attendance_"]
    .stButton > button {

        width: 100% !important;

        background:
            var(--hc-purple-soft) !important;

        border: none !important;

        border-radius: 0 !important;

        color:
            var(--hc-purple) !important;

        font-size: 14px !important;

        font-weight: 600 !important;

        padding: 12px 22px !important;

        text-align: center !important;

        transition: all 0.2s ease !important;

        border-top:
            1px solid var(--hc-border) !important;

        margin: 0 !important;

        height: auto !important;
    }


    div[class*="st-key-attendance_"]
    .stButton > button:hover {

        background:
            var(--hc-purple-hover) !important;

        color:
            var(--hc-purple-text) !important;
    }


    /* ======================================================
       ATTENDANCE VIEW
       ====================================================== */

    .attendance-header {

        display: flex;

        align-items: center;

        gap: 12px;

        margin-bottom: 24px;

        padding-bottom: 16px;

        border-bottom:
            1px solid var(--hc-border);
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

        background:
            linear-gradient(
                180deg,
                var(--hc-green) 0%,
                var(--hc-red) 100%
            );
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

        background:
            var(--hc-green-soft);

        color:
            var(--hc-green);
    }


    .timeline-status.absent {

        background:
            var(--hc-red-soft);

        color:
            var(--hc-red);
    }


    /* ======================================================
       BACK BUTTON
       ====================================================== */

    div[class*="st-key-back_btn_"]
    .stButton > button {

        background:
            var(--hc-purple-soft) !important;

        border:
            1px solid var(--hc-border) !important;

        border-radius:
            var(--hc-radius-md) !important;

        color:
            var(--hc-purple) !important;

        font-weight: 600 !important;

        padding:
            10px 20px !important;

        transition:
            all 0.2s ease !important;
    }


    div[class*="st-key-back_btn_"]
    .stButton > button:hover {

        background:
            var(--hc-purple-hover) !important;

        border-color:
            var(--hc-purple) !important;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left: 24px !important;

            padding-right: 24px !important;
        }

    }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "show_attendance" not in st.session_state:

    st.session_state.show_attendance = False

    st.session_state.attendance_subject_code = None


# ============================================================
# ATTENDANCE VIEW
# ============================================================

if (
    st.session_state.show_attendance
    and st.session_state.attendance_subject_code
):

    subject_code = (
        st.session_state.attendance_subject_code
    )

    subject_name = (
        SUBJECT_INFO[subject_code]["name"]
    )

    subject_icon = (
        SUBJECT_INFO[subject_code]["icon"]
    )


    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button(
        "← Back",
        key="back_btn_attendance"
    ):

        st.session_state.show_attendance = False

        st.rerun()


    # ========================================================
    # ATTENDANCE HEADER
    # ========================================================

    render(
        f"""
        <div class="attendance-header">

            <div class="attendance-icon">
                {subject_icon}
            </div>

            <div>

                <div class="attendance-header-title">
                    {subject_name}
                </div>

                <div style="
                    color: var(--hc-text-soft);
                    font-size: 13px;
                    margin-top: 2px;
                ">
                    {subject_code}
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # FILTER ATTENDANCE
    # ========================================================

    subject_attendance = (
        attendance_log[
            attendance_log["code"] == subject_code
        ].copy()
    )


    if len(subject_attendance) > 0:

        subject_attendance = (
            subject_attendance
            .sort_values(
                "date",
                ascending=False
            )
        )


        # ====================================================
        # STATS
        # ====================================================

        total_classes = len(subject_attendance)

        present_count = len(
            subject_attendance[
                subject_attendance["status"] == "Present"
            ]
        )

        absent_count = len(
            subject_attendance[
                subject_attendance["status"] == "Absent"
            ]
        )

        present_percentage = (
            present_count /
            total_classes *
            100
            if total_classes > 0
            else 0
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            render(
                f"""
                <div class="attendance-stat-card">

                    <div class="stat-label">
                        Total Classes
                    </div>

                    <div class="stat-value">
                        {total_classes}
                    </div>

                </div>
                """
            )


        with col2:

            render(
                f"""
                <div
                    class="attendance-stat-card"
                    style="
                        background:
                        linear-gradient(
                            135deg,
                            var(--hc-green-soft) 0%,
                            var(--hc-surface) 100%
                        );
                    "
                >

                    <div class="stat-label">
                        Present
                    </div>

                    <div class="stat-value">
                        {present_count}
                    </div>

                    <div class="stat-percentage">
                        {present_percentage:.1f}%
                    </div>

                </div>
                """
            )


        with col3:

            absent_percentage = (
                absent_count /
                total_classes *
                100
            )

            render(
                f"""
                <div
                    class="attendance-stat-card"
                    style="
                        background:
                        linear-gradient(
                            135deg,
                            var(--hc-red-soft) 0%,
                            var(--hc-surface) 100%
                        );
                    "
                >

                    <div class="stat-label">
                        Absent
                    </div>

                    <div class="stat-value">
                        {absent_count}
                    </div>

                    <div class="stat-percentage">
                        {absent_percentage:.1f}%
                    </div>

                </div>
                """
            )


        st.markdown("---")


        # ====================================================
        # TIMELINE
        # ====================================================

        st.subheader("📅 Attendance Timeline")


        timeline_html = (
            '<div class="timeline-container">'
            '<div class="timeline-line"></div>'
        )


        for _, row in subject_attendance.iterrows():

            status = row["status"]

            date_str = (
                pd.to_datetime(
                    row["date"]
                ).strftime(
                    "%A, %d %b %Y"
                )
            )

            time_str = (
                f"{row['start_time']} - "
                f"{row['end_time']}"
            )

            instructor = (
                row["instructor"]
                if pd.notna(row["instructor"])
                else "N/A"
            )


            status_class = (
                "present"
                if status == "Present"
                else "absent"
            )

            status_icon = (
                "✓"
                if status == "Present"
                else "✕"
            )

            status_text = (
                "Present"
                if status == "Present"
                else "Absent"
            )


            timeline_html += f"""
            <div class="timeline-item">

                <div
                    class="timeline-dot
                    {status_class}"
                ></div>

                <div
                    class="timeline-content
                    {status_class}"
                >

                    <div class="timeline-date">
                        {date_str}
                    </div>

                    <div class="timeline-time">
                        ⏱️ {time_str}
                    </div>

                    <div class="timeline-instructor">
                        👨‍🏫 {instructor}
                    </div>

                    <div
                        class="timeline-status
                        {status_class}"
                    >
                        {status_icon}
                        {status_text}
                    </div>

                </div>

            </div>
            """


        timeline_html += "</div>"


        render(timeline_html)


    else:

        st.info(
            f"No attendance records found "
            f"for {subject_name}"
        )


# ============================================================
# DASHBOARD VIEW
# ============================================================

else:

    # ========================================================
    # GREETING
    # ========================================================

    hour = datetime.now().hour


    if 5 <= hour < 12:

        greeting = "Good Morning"

    elif 12 <= hour < 17:

        greeting = "Good Afternoon"

    elif 17 <= hour < 21:

        greeting = "Good Evening"

    else:

        greeting = "Good Night"


    render(
        f"""
        <div class="hc-card hc-greeting-card">

            <div class="hc-greeting-left">

                <div class="hc-greeting-avatar">
                    🧑‍🎓
                </div>

                <div>

                    <div class="hc-greeting-text-sub">
                        {greeting},
                    </div>

                    <div class="hc-greeting-text-name">
                        {STUDENT_NAME}
                    </div>

                </div>

            </div>

            <div class="hc-greeting-icons">
                <span>+</span>
            </div>

        </div>
        """
    )


    # ========================================================
    # COURSE CARD
    # ========================================================

    QUICK_ITEMS = [

        (
            "✉️",
            "Messages",
            "pages/messages.py"
        ),

        (
            "📅",
            "Date Sheet",
            "pages/datesheet.py"
        ),

        (
            "🧑‍🏫",
            "Leaves",
            "pages/leaves.py"
        ),

        (
            "🔊",
            "Notices",
            "pages/notices.py"
        ),

        (
            "💲",
            "Fees",
            "pages/fees.py"
        ),

        (
            "🎫",
            "ID Card",
            "pages/id-card.py"
        )

    ]


    with st.container(
        key="hc_course_card"
    ):

        render(
            f"""
            <div class="hc-card hc-course-card-bg">

                <div class="hc-course-top">

                    <div class="hc-course-row">

                        <div class="hc-course-name">

                            📖 &nbsp;
                            {COURSE}

                            <br>

                            (Sem-{SEMESTER})

                        </div>


                        <div class="hc-cgpa-box">

                            <div class="hc-cgpa-label">
                                CGPA
                            </div>

                            <div class="hc-cgpa-value">
                                {CGPA}
                            </div>

                        </div>

                    </div>


                    <div class="hc-divider"></div>

                </div>

            </div>
            """
        )


        # ====================================================
        # QUICK ACTION BUTTONS
        # ====================================================

        rows = [
            QUICK_ITEMS[0:3],
            QUICK_ITEMS[3:6]
        ]


        for row_index, row_items in enumerate(
            rows,
            start=1
        ):

            with st.container(
                key=f"hc_quick_row_{row_index}"
            ):

                for icon, label, target_page in row_items:

                    if st.button(
                        f"{icon}\n{label}",
                        key=f"hc_quick_{label}"
                    ):

                        if target_page:

                            st.switch_page(
                                target_page
                            )


    # ========================================================
    # SUBJECT LIST HEADER
    # ========================================================

    render(
        f"""
        <div class="hc-subjects-header">

            <div class="hc-subjects-title">
                Your Subjects
            </div>

            <div class="hc-filter">
                ☰ &nbsp; Filter
            </div>

        </div>

        <div class="hc-subjects-count">
            {len(subjects)} subjects
        </div>
        """
    )


    # ========================================================
    # ATTENDANCE HELPERS
    # ========================================================

    def classes_to_recover(
        attended_count,
        total_count
    ):

        if (
            total_count == 0
            or attended_count / total_count >= 0.75
        ):

            return 0

        return max(
            0,
            math.ceil(
                (
                    0.75 * total_count
                    - attended_count
                )
                / 0.25
            )
        )


    def safe_to_miss(
        attended_count,
        total_count
    ):

        if (
            total_count == 0
            or attended_count / total_count < 0.75
        ):

            return 0

        return max(
            0,
            math.floor(
                attended_count / 0.75
                - total_count
            )
        )


    # ========================================================
    # SUBJECT ICONS
    # ========================================================

    SUBJECT_ICONS = {

        "Data Structure":
            "✉️",

        "Computer Architecture":
            "📈",

        "Information System":
            "💡",

        "Cybersecurity Fundamentals":
            "🛡️",

        "Operating System":
            "🖥️"

    }


    # ========================================================
    # SUBJECT CARDS
    # ========================================================

    for _, row in subjects.iterrows():

        percentage = int(
            row["attendance"]
        )


        # ----------------------------------------------------
        # ATTENDANCE STATUS
        # ----------------------------------------------------

        if percentage < 75:

            border_class = "red"

            pill_class = "bad"

            needed = classes_to_recover(
                int(row["attended"]),
                int(row["total"])
            )

            pill_text = (
                f"❌ Attend {needed} to recover"
            )

            ring_color = "var(--hc-red)"

            dot_colors = [

                "var(--hc-red)",
                "var(--hc-red)",
                "var(--hc-orange)",
                "var(--hc-green)",
                "var(--hc-green)"

            ]


        elif percentage < 90:

            border_class = "purple"

            pill_class = "good"

            safe = safe_to_miss(
                int(row["attended"]),
                int(row["total"])
            )

            pill_text = (
                f"✓ Safe to miss {safe} classes"
            )

            ring_color = "var(--hc-purple)"

            dot_colors = [

                "var(--hc-red)",
                "var(--hc-orange)",
                "var(--hc-purple)",
                "var(--hc-green)",
                "var(--hc-green)"

            ]


        else:

            border_class = "green"

            pill_class = "good"

            safe = safe_to_miss(
                int(row["attended"]),
                int(row["total"])
            )

            pill_text = (
                f"✓ Safe to miss {safe} classes"
            )

            ring_color = "var(--hc-green)"

            dot_colors = [

                "var(--hc-orange)",
                "var(--hc-green)",
                "var(--hc-green)",
                "var(--hc-green)",
                "var(--hc-green)"

            ]


        # ----------------------------------------------------
        # RING
        # ----------------------------------------------------

        degree = percentage * 3.6


        if percentage > 0:

            ring_bg = (
                "background: "
                f"conic-gradient("
                f"{ring_color} "
                f"0deg {degree}deg, "
                f"var(--hc-ring-empty) "
                f"{degree}deg 360deg);"
            )

        else:

            ring_bg = (
                "background: "
                "var(--hc-ring-empty);"
            )


        # ----------------------------------------------------
        # DOTS
        # ----------------------------------------------------

        dots_html = "".join(

            f"""
            <span
                class="hc-subject-dot"
                style="background:{c};"
            ></span>
            """

            for c in dot_colors

        )


        # ----------------------------------------------------
        # ICON
        # ----------------------------------------------------

        icon = SUBJECT_ICONS.get(
            row["subject"],
            "📘"
        )


        subject_code = row["code"]


        # ----------------------------------------------------
        # SUBJECT CARD
        # ----------------------------------------------------

        render(
            f"""
            <div class="hc-subject-card-container">

                <div
                    class="hc-subject-card
                    {border_class}"
                >

                    <div class="hc-subject-left">

                        <div
                            class="hc-subject-icon"
                        >
                            {icon}
                        </div>


                        <div>

                            <div class="hc-subject-name">
                                {row['subject']}
                            </div>

                            <div class="hc-subject-code">
                                {row['code']}
                                &bull;
                                {row['credits']}
                            </div>

                            <div
                                class="hc-status-pill
                                {pill_class}"
                            >
                                {pill_text}
                            </div>

                        </div>

                    </div>


                    <div class="hc-ring-wrap">

                        <div
                            class="hc-ring"
                            style="{ring_bg}"
                        >

                            <div class="hc-ring-value">
                                {percentage}
                            </div>

                        </div>


                        <div class="hc-ring-fraction">
                            {row['attended']}/{row['total']}
                        </div>


                        <div class="hc-subject-dots">
                            {dots_html}
                        </div>

                    </div>

                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # VIEW ATTENDANCE BUTTON
        # ----------------------------------------------------

        if st.button(
            "View Attendance Timeline",
            key=f"attendance_{subject_code}",
            use_container_width=True
        ):

            st.session_state.show_attendance = True

            st.session_state.attendance_subject_code = (
                subject_code
            )

            st.rerun()