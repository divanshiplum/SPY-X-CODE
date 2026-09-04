import streamlit as st
from datetime import datetime


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Student Timetable",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HTML RENDER HELPER
# (Strips leading whitespace from every line before handing it
# to st.markdown. Markdown treats 4+ spaces of indentation as a
# code block, which is why raw "<div style=..." text was showing
# up literally on screen instead of rendering as HTML.)
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# TIMETABLE DATA
#
# type   -> "Lecture" or "Practical" (drives the card color + pill)
# room   -> shown as a location pill
# group  -> shown as a group pill (e.g. "GP-All", "GP-B")
# ============================================================

timetable = {

    "Monday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sharma", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],

    "Tuesday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-006", "group": "GP-All"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sharma", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-114", "group": "GP-All"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],

    "Wednesday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-006", "group": "GP-All"},
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
         "teacher": "Manpreet Kaur", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "10:20", "end": "11:00", "subject": "Information System",
         "teacher": "Neha Sethi", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "11:00", "end": "11:40", "subject": "Data Structure",
         "teacher": "Anshuman Sharma", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
        {"start": "11:40", "end": "12:20", "subject": "Operating System",
         "teacher": "Anshuman Sharma", "type": "Lecture", "room": "R-116", "group": "GP-All"},
    ],

    "Saturday": [
        {"start": "09:00", "end": "09:40", "subject": "Computer Architecture",
         "teacher": "Manpreet Kaur", "type": "Lecture", "room": "R-115", "group": "GP-All"},
        {"start": "09:40", "end": "10:20", "subject": "Cybersecurity Fundamentals",
         "teacher": "Manpreet Kaur", "type": "Practical", "room": "R-LA3", "group": "GP-B"},
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
# CSS
# ============================================================

render("""
<style>

.stApp {
    background: #0e0e10;
    color: #ffffff;
}

.block-container {
    max-width: 900px;
    padding-top: 18px;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

.main-title {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-bottom: 2px;
}

.main-title-icon { font-size: 24px; }

.main-title-text {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
}

.subtitle {
    color: #8a8a8f;
    font-size: 15px;
    margin-bottom: 18px;
}

/* Day chip buttons */
.stButton > button {
    background: #1c1c20;
    color: #d6d6da;
    border: 1px solid #2a2a30;
    border-radius: 16px;
    font-weight: 700;
    padding: 10px 6px;
}

.stButton > button:hover {
    border-color: #4a4a52;
    color: #ffffff;
}

.stButton > button[kind="primary"] {
    background: #3b5bfd;
    border-color: #3b5bfd;
    color: #ffffff;
}

/* Timeline */

.timeline-wrap {
    position: relative;
    margin-top: 10px;
    margin-left: 4px;
}

.time-label {
    position: absolute;
    left: 0;
    width: 74px;
    color: #8a8a8f;
    font-size: 13px;
    font-weight: 600;
    transform: translateY(-50%);
}

.time-gridline {
    position: absolute;
    left: 84px;
    right: 0;
    height: 1px;
    background: #232327;
}

.class-block {
    position: absolute;
    left: 90px;
    right: 6px;
    border-radius: 16px;
    padding: 14px 16px;
    box-sizing: border-box;
    overflow: hidden;
    box-shadow: 0 6px 16px rgba(0,0,0,0.35);
}

.class-block-lecture {
    background: linear-gradient(135deg, #5b6cf5, #4739c9);
}

.class-block-practical {
    background: linear-gradient(135deg, #33c481, #1f8f5b);
}

.class-block.is-live {
    box-shadow: 0 0 0 3px #ffffff55, 0 6px 16px rgba(0,0,0,0.4);
}

.class-top-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
}

.class-subject {
    font-size: 17px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
}

.type-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #ffffff;
    color: #222222;
    border-radius: 20px;
    padding: 4px 11px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
}

.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #ff3b3b;
    color: #ffffff;
    border-radius: 20px;
    padding: 4px 11px;
    font-size: 11px;
    font-weight: 800;
    margin-left: 6px;
}

.class-teacher {
    color: #e8e8ff;
    font-size: 13px;
    margin-top: 6px;
}

.meta-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 12px;
}

.meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.18);
    color: #ffffff;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
    white-space: nowrap;
}

/* Free day / empty schedule state */

.empty-state {
    text-align: center;
    padding: 70px 20px 40px;
}

.empty-icon {
    font-size: 64px;
    margin-bottom: 22px;
    opacity: 0.85;
}

.empty-title {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}

.empty-subtitle {
    color: #8a8a8f;
    font-size: 15px;
}

@media (max-width: 700px) {
    .time-label { width: 58px; font-size: 11px; }
    .time-gridline { left: 66px; }
    .class-block { left: 72px; }
    .class-subject { font-size: 15px; }
}

</style>
""")


# ============================================================
# TIME HELPERS
# ============================================================

def to_minutes(time_string):
    hour, minute = map(int, time_string.split(":"))
    return hour * 60 + minute


def format_time(time_string):
    return datetime.strptime(time_string, "%H:%M").strftime("%I:%M %p").lstrip("0")


def is_active(lecture):
    now = datetime.now()
    current_minutes = now.hour * 60 + now.minute
    return to_minutes(lecture["start"]) <= current_minutes < to_minutes(lecture["end"])


# ============================================================
# SCHEDULE RENDERING (Free Day message OR the timeline — never
# both. Written as a function with an early return so there is
# no way for both branches to run at once, even if this gets
# re-pasted with different indentation.)
# ============================================================

def render_schedule(day_name, day_lectures):

    if not day_lectures:
        render(f"""
        <div class="empty-state">
            <div class="empty-icon">🏖️</div>
            <div class="empty-title">Free Day</div>
            <div class="empty-subtitle">No classes scheduled for {day_name}</div>
        </div>
        """)
        return

    PIXELS_PER_MIN = 2.6
    TOP_PADDING = 10

    day_start = min(to_minutes(l["start"]) for l in day_lectures)
    day_end = max(to_minutes(l["end"]) for l in day_lectures)

    tick_minutes = list(range(day_start, day_end + 1, 30))
    if tick_minutes[-1] != day_end:
        tick_minutes.append(day_end)

    timeline_height = (day_end - day_start) * PIXELS_PER_MIN + TOP_PADDING * 2

    pieces = [f'<div class="timeline-wrap" style="height:{timeline_height}px;">']

    for minute in tick_minutes:
        y = (minute - day_start) * PIXELS_PER_MIN + TOP_PADDING
        label = datetime.strptime(f"{minute // 60:02d}:{minute % 60:02d}", "%H:%M").strftime("%I:%M %p").lstrip("0")
        pieces.append(f'<div class="time-label" style="top:{y}px;">{label}</div>')
        pieces.append(f'<div class="time-gridline" style="top:{y}px;"></div>')

    for lecture in day_lectures:
        start = to_minutes(lecture["start"])
        end = to_minutes(lecture["end"])
        top = (start - day_start) * PIXELS_PER_MIN + TOP_PADDING
        height = (end - start) * PIXELS_PER_MIN

        is_practical = lecture["type"] == "Practical"
        color_class = "class-block-practical" if is_practical else "class-block-lecture"
        type_icon = "🧪" if is_practical else "📖"
        live_class = " is-live" if is_active(lecture) else ""
        live_pill = '<span class="live-pill">🔴 Live</span>' if is_active(lecture) else ""

        start_label = format_time(lecture["start"])
        end_label = format_time(lecture["end"])

        pieces.append(f"""
        <div class="class-block {color_class}{live_class}" style="top:{top}px; height:{height}px;">
            <div class="class-top-row">
                <div class="class-subject">{lecture["subject"]}</div>
                <div>
                    <span class="type-pill">{type_icon} {lecture["type"]}</span>
                    {live_pill}
                </div>
            </div>
            <div class="class-teacher">👤 &nbsp;{lecture["teacher"]}</div>
            <div class="meta-row">
                <span class="meta-pill">🕐 &nbsp;{start_label} - {end_label}</span>
                <span class="meta-pill">📍 &nbsp;{lecture["room"]}</span>
            </div>
        </div>
        """)

    pieces.append("</div>")

    render("".join(pieces))

# ============================================================
# DAY SELECTION
# ============================================================

days = list(timetable.keys())

if "selected_day" not in st.session_state:
    today = datetime.now().strftime("%A")
    st.session_state.selected_day = today if today in days else "Monday"

today_name = datetime.now().strftime("%A")

cols = st.columns(len(days))

for i, day in enumerate(days):
    with cols[i]:
        is_selected = day == st.session_state.selected_day
        label = day[:3].upper()
        if day == today_name:
            label += " •"

        if st.button(
            label,
            key=f"day_{day}",
            use_container_width=True,
            type="primary" if is_selected else "secondary",
        ):
            st.session_state.selected_day = day
            st.rerun()

selected_day = st.session_state.selected_day
lectures = timetable[selected_day]


# ============================================================
# SELECTED DAY TITLE + SCHEDULE (also in a fragment so the
# "Live" badge on any current class stays up to date every 30s
# without a full blocking page rerun)
# ============================================================

@st.fragment(run_every=30)
def show_day(day_name, day_lectures):
    render(f"""
    <div class="main-title">
        <span class="main-title-icon">📅</span>
        <span class="main-title-text">{day_name}</span>
    </div>
    """)

    if day_lectures:
        render(f'<div class="subtitle">{len(day_lectures)} classes scheduled</div>')

    render_schedule(day_name, day_lectures)


show_day(selected_day, lectures)