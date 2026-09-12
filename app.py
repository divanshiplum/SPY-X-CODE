import streamlit as st

# ============================================================
# APP ROUTER
#
# login.py is the default page — it's shown first when you run
# `streamlit run app.py`.
#
# position="hidden" turns off Streamlit's own sidebar page list,
# since dashboard.py / marks.py / timetable.py / performance.py
# render their own navigation.
# ============================================================

pg = st.navigation(
    [
        st.Page("login.py", title="Login", default=True),
        st.Page("dashboard.py", title="Home"),
        st.Page("marks.py", title="Marks"),
        st.Page("timetable.py", title="TimeTable"),
        st.Page("performance.py", title="Performance"),
        st.Page("datesheet.py", title="Date Sheet"),

        # NEW: Messages page
        st.Page("messages.py", title="Messages"),
    ],
    position="hidden",
)

pg.run()