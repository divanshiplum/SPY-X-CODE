import streamlit as st

# ============================================================
# GLOBAL SESSION STATE INITIALIZATION
# (सिर्फ एक जगह - यहीं करो, कहीं और नहीं)
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "roll_no" not in st.session_state:
    st.session_state.roll_no = None

if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

if "logout_confirmed" not in st.session_state:
    st.session_state.logout_confirmed = False

if "show_attendance" not in st.session_state:
    st.session_state.show_attendance = False
    st.session_state.attendance_subject_code = None

# ============================================================
# APP ROUTER
#
# All page modules now live under pages/, including nav_bar.py
# and login.py — so every st.Page() call below needs the
# "pages/" prefix. nav_bar.py is a shared helper, not a page
# itself, so it's intentionally NOT listed here even though it
# physically sits in the pages/ folder — st.navigation() takes
# full manual control of what's registered, so Streamlit's own
# automatic "every .py in pages/ is a page" discovery never
# kicks in.
# ============================================================

pg = st.navigation(
    [
        st.Page("pages/login.py", title="Login", default=True),
        st.Page("pages/dashboard.py", title="Home"),
        st.Page("pages/marks.py", title="Marks"),
        st.Page("pages/timetable.py", title="TimeTable"),
        st.Page("pages/performance.py", title="Performance"),
        st.Page("pages/datesheet.py", title="Date Sheet"),
        st.Page("pages/notices.py", title="Notices"),
        st.Page("pages/messages.py", title="Messages"),
        st.Page("pages/id-card.py", title="ID Card"),
        st.Page("pages/fees.py", title="Fees"),
        st.Page("pages/leaves.py", title="Leaves"),
        st.Page("pages/settings.py", title="Settings")
    ],
    position="hidden",
)

pg.run()