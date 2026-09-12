import streamlit as st

# ============================================================
# APP ROUTER
#
# login.py is the default page — it's shown first when you run
# `streamlit run app.py`. Each of the other pages checks
# st.session_state.logged_in at the top and bounces back to
# login.py if it isn't set, so they can't be reached directly
# (e.g. by URL) without logging in first.
#
# datesheet.py is reached only via the "Date Sheet" tile on
# dashboard.py (and its own back arrow returns there) — it's
# still listed here because st.switch_page requires the target
# to be one of the registered pages.
#
# position="hidden" turns off Streamlit's own sidebar page list,
# since dashboard.py / marks.py / timetable.py / performance.py
# render their own bottom navigation bar instead (see nav_bar.py).
# ============================================================

pg = st.navigation(
    [
        st.Page("login.py", title="Login", default=True),
        st.Page("dashboard.py", title="Home"),
        st.Page("marks.py", title="Marks"),
        st.Page("timetable.py", title="TimeTable"),
        st.Page("performance.py", title="Performance"),
        st.Page("datesheet.py", title="Date Sheet"),
    ],
    position="hidden",
)

pg.run()