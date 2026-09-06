import streamlit as st

# ============================================================
# APP ROUTER
#
# position="hidden" turns off Streamlit's own sidebar page list,
# since each page renders its own bottom navigation bar instead
# (see nav_bar.py). Run this file with:
#     streamlit run app.py
# ============================================================

pg = st.navigation(
    [
        st.Page("marks.py", title="Marks"),
        st.Page("dashboard.py", title="Home", default=True),
        st.Page("timetable.py", title="TimeTable"),
        st.Page("performance.py", title="Performance"),
    ],
    position="hidden",
)

pg.run()