import streamlit as st
from datetime import datetime
import time

# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Student Timetable",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>

body {
    background-color: #f5f6fa;
}

.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 25px;
}

/* Day circles */

.day-button {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    border: 2px solid #222;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    font-weight: bold;
}

/* Lecture card */

.lecture-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

/* Active lecture */

.active-card {
    background-color: #ffffff;
    border: 2px solid #111827;
    border-radius: 12px;
    padding: 0px 18px 18px 18px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

/* Horizontal LIVE bar */

.live-bar {
    height: 7px;
    background-color: #111827;
    border-radius: 12px 12px 0px 0px;
    margin-bottom: 12px;
}

.live-text {
    font-size: 12px;
    font-weight: bold;
    margin-bottom: 8px;
}

.subject {
    font-size: 19px;
    font-weight: bold;
}

.teacher {
    color: #666;
    margin-top: 7px;
}

.time {
    font-weight: bold;
    color: #555;
    padding-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# TIMETABLE DATA
# -----------------------------

timetable = {

    "Monday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Computer Architecture",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Cyber Security",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "11:00",
            "end": "12:00",
            "subject": "Information System",
            "teacher": "Neha Sharma"
        },
        {
            "start": "12:00",
            "end": "01:00",
            "subject": "Data Structure",
            "teacher": "Anshuman Sharma"
        },
        {
            "start": "01:00",
            "end": "02:00",
            "subject": "Operating System",
            "teacher": "Anshuman Sharma"
        }
    ],

    "Tuesday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Cyber Security",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Information System",
            "teacher": "Neha Sharma"
        },
        {
            "start": "11:00",
            "end": "12:00",
            "subject": "Data Structure",
            "teacher": "Anshuman Sharma"
        },
        {
            "start": "12:00",
            "end": "01:00",
            "subject": "Computer Architecture",
            "teacher": "Manpreet Kaur"
        }
    ],

    "Wednesday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Computer Architecture",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Cyber Security",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "11:00",
            "end": "12:00",
            "subject": "Information System",
            "teacher": "Neha Sharma"
        }
    ],

    "Thursday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Data Structure",
            "teacher": "Anshuman Sharma"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Operating System",
            "teacher": "Anshuman Sharma"
        },
        {
            "start": "11:00",
            "end": "12:00",
            "subject": "Computer Architecture",
            "teacher": "Manpreet Kaur"
        }
    ],

    "Friday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Operating System",
            "teacher": "Anshuman Sharma"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Cyber Security",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "11:00",
            "end": "12:00",
            "subject": "Data Structure",
            "teacher": "Anshuman Sharma"
        }
    ],

    "Saturday": [
        {
            "start": "09:00",
            "end": "10:00",
            "subject": "Computer Architecture",
            "teacher": "Manpreet Kaur"
        },
        {
            "start": "10:00",
            "end": "11:00",
            "subject": "Operating System",
            "teacher": "Anshuman Sharma"
        }
    ]
}

# -----------------------------
# TIME FUNCTIONS
# -----------------------------

def convert_minutes(time_string):

    hour, minute = map(int, time_string.split(":"))

    return hour * 60 + minute


def format_time(time_string):

    time = datetime.strptime(time_string, "%H:%M")

    return time.strftime("%I:%M %p")


# -----------------------------
# CHECK ACTIVE LECTURE
# -----------------------------

def is_active(lecture):

    now = datetime.now()

    current_minutes = now.hour * 60 + now.minute

    start = convert_minutes(lecture["start"])
    end = convert_minutes(lecture["end"])

    return start <= current_minutes < end


# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    '<div class="main-title">📚 My Timetable</div>',
    unsafe_allow_html=True
)


# -----------------------------
# CURRENT TIME
# -----------------------------

now = datetime.now()

st.markdown(
    f"<p style='text-align:right;'>Current Time: "
    f"<b>{now.strftime('%I:%M:%S %p')}</b></p>",
    unsafe_allow_html=True
)


# -----------------------------
# DAY SELECTION
# -----------------------------

days = list(timetable.keys())

if "selected_day" not in st.session_state:

    today = datetime.now().strftime("%A")

    if today in days:
        st.session_state.selected_day = today
    else:
        st.session_state.selected_day = "Monday"


cols = st.columns(6)

for i, day in enumerate(days):

    with cols[i]:

        if st.button(
            day[:3].upper(),
            key=day,
            use_container_width=True
        ):

            st.session_state.selected_day = day


selected_day = st.session_state.selected_day


st.markdown("---")


# -----------------------------
# SHOW SELECTED DAY
# -----------------------------

st.subheader(f"📅 {selected_day}")


lectures = timetable[selected_day]


# -----------------------------
# LECTURE DISPLAY
# -----------------------------

# -----------------------------
# LECTURE DISPLAY
# -----------------------------

for lecture in lectures:

    col1, col2 = st.columns([1, 4])

    # TIME - LEFT SIDE
    with col1:

        st.markdown(
            f"""
            <div style="
                font-weight: bold;
                color: #555;
                text-align: right;
                padding: 25px 10px;
                font-size: 15px;
            ">
                {format_time(lecture["start"])}
                <br>
                ↓
                <br>
                {format_time(lecture["end"])}
            </div>
            """,
            unsafe_allow_html=True
        )

    # LECTURE - RIGHT SIDE
    with col2:

        if is_active(lecture):

            st.markdown(
                f"""
                <div style="
                    background: white;
                    border: 2px solid #111827;
                    border-radius: 15px;
                    padding: 0 20px 20px 20px;
                    margin-bottom: 18px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
                ">

                    <div style="
                        height: 7px;
                        background: #111827;
                        border-radius: 15px 15px 0 0;
                        margin: 0 -20px 15px -20px;
                    ">
                    </div>

                    <div style="
                        font-size: 12px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    ">
                        🔴 LECTURE IN PROGRESS
                    </div>

                    <div style="
                        font-size: 20px;
                        font-weight: bold;
                        color: #111827;
                    ">
                        {lecture["subject"]}
                    </div>

                    <div style="
                        font-size: 15px;
                        color: #666;
                        margin-top: 8px;
                    ">
                        👨‍🏫 Teacher: {lecture["teacher"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    background: white;
                    border: 1px solid #ddd;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 18px;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                ">

                    <div style="
                        font-size: 20px;
                        font-weight: bold;
                        color: #111827;
                    ">
                        {lecture["subject"]}
                    </div>

                    <div style="
                        font-size: 15px;
                        color: #666;
                        margin-top: 8px;
                    ">
                        👨‍🏫 Teacher: {lecture["teacher"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------
# AUTO REFRESH
# -----------------------------

time.sleep(1)

st.rerun()