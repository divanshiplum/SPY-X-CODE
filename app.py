import streamlit as st

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
    ],
    position="hidden",
)

pg.run()