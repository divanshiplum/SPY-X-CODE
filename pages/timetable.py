import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
from datetime import datetime

from nav_sidebar import render_sidebar
from theme import get_theme_css


st.set_page_config(
    page_title="Student Timetable",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.html(get_theme_css())


def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


render_sidebar("timetable")


# ============================================================
# TIMETABLE DATA (unchanged)
# ============================================================

timetable = {
    "Monday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sharma", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Tuesday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sharma", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Wednesday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sharma", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Thursday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sethi", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Friday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sethi", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Saturday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur Dhaliwal", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sethi", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],
    "Sunday": [],
}


# ============================================================
# CSS — light theme, matching the mockup's day-tabs + card list
# ============================================================

render("""
<style>

.hc-tt-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 4px;
}

.hc-tt-subtitle {
    color: var(--hc-text-soft);
    font-size: 13px;
    margin-bottom: 18px;
}

/* Day tab row */
div.stVerticalBlock[class*="st-key-tt_day_selector"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 6px !important;
    background: var(--hc-surface);
    border-radius: var(--hc-radius-md);
    padding: 6px;
    margin-bottom: 20px;
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
}

div.stVerticalBlock[class*="st-key-tt_day_selector"] > div {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}

div[class*="st-key-tt_day_selector"] .stButton > button {
    width: 100%;
    background: transparent;
    color: var(--hc-text-soft);
    border: none;
    border-radius: var(--hc-radius-sm);
    font-weight: 700;
    font-size: 13px;
    padding: 10px 4px;
}

div[class*="st-key-tt_day_selector"] .stButton > button[kind="primary"] {
    background: var(--hc-purple-soft) !important;
    color: var(--hc-purple-text) !important;
}

/* Class cards — cycle through a small pastel palette per row
   (matching the reference's varied left-border colors), rather
   than a strict practical/lecture split. */
.hc-class-card {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    border-left: 5px solid var(--hc-purple);
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.hc-class-card.c-blue { border-left-color: var(--hc-blue); }
.hc-class-card.c-green { border-left-color: var(--hc-green); }
.hc-class-card.c-purple { border-left-color: var(--hc-purple); }
.hc-class-card.c-teal { border-left-color: var(--hc-teal); }
.hc-class-card.c-orange { border-left-color: var(--hc-orange); }

.hc-class-left { display: flex; align-items: center; gap: 14px; }

.hc-class-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: var(--hc-purple-soft);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.hc-class-card.c-blue .hc-class-icon { background: var(--hc-blue-soft); }
.hc-class-card.c-green .hc-class-icon { background: var(--hc-green-soft); }
.hc-class-card.c-purple .hc-class-icon { background: var(--hc-purple-soft); }
.hc-class-card.c-teal .hc-class-icon { background: var(--hc-teal-soft); }
.hc-class-card.c-orange .hc-class-icon { background: var(--hc-orange-soft); }

.hc-class-subject { font-weight: 700; color: var(--hc-text); font-size: 15px; }
.hc-class-meta { color: var(--hc-text-soft); font-size: 13px; margin-top: 3px; }

.hc-type-pill {
    background: var(--hc-purple-soft);
    color: var(--hc-purple-text);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
}

.hc-empty-day {
    text-align: center;
    padding: 60px 20px;
    color: var(--hc-text-soft);
}

.hc-empty-day-icon { font-size: 48px; margin-bottom: 14px; }

</style>
""")


def format_time(time_string):
    return datetime.strptime(time_string, "%H:%M").strftime("%I:%M %p").lstrip("0")


days = list(timetable.keys())

if "tt_selected_day" not in st.session_state:
    today = datetime.now().strftime("%A")
    st.session_state.tt_selected_day = today if today in days else "Monday"

render(f"""
<div class="hc-tt-title"><span>📅</span> Timetable</div>
""")

with st.container(key="tt_day_selector"):
    for day in days:
        if st.button(
            day[:3].upper(),
            key=f"tt_day_{day}",
            type="primary" if st.session_state.tt_selected_day == day else "secondary",
        ):
            st.session_state.tt_selected_day = day
            st.rerun()

selected_day = st.session_state.tt_selected_day
lectures = timetable[selected_day]

CARD_COLORS = ["c-blue", "c-green", "c-purple", "c-teal", "c-orange"]

if not lectures:
    render(f"""
    <div class="hc-empty-day">
        <div class="hc-empty-day-icon">🏖️</div>
        <div style="font-size:20px; font-weight:700; color:var(--hc-text);">Free Day</div>
        <div>No classes scheduled for {selected_day}</div>
    </div>
    """)
else:
    render(f'<div class="hc-tt-subtitle">{selected_day} &bull; {len(lectures)} classes scheduled</div>')

    for i, lecture in enumerate(lectures):
        is_practical = lecture["type"] == "Practical"
        color_class = CARD_COLORS[i % len(CARD_COLORS)]
        icon = "🧪" if is_practical else "📖"

        render(f"""
        <div class="hc-class-card {color_class}">
            <div class="hc-class-left">
                <div class="hc-class-icon">{icon}</div>
                <div>
                    <div class="hc-class-subject">{lecture['subject']}</div>
                    <div class="hc-class-meta">
                        👤 {lecture['teacher']} &nbsp;&bull;&nbsp;
                        🕐 {format_time(lecture['start'])} - {format_time(lecture['end'])} &nbsp;&bull;&nbsp;
                        📍 {lecture['room']}
                    </div>
                </div>
            </div>
            <div class="hc-type-pill">{lecture['type']}</div>
        </div>
        """)