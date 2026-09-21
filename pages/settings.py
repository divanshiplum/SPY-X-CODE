import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
toggle_defaults = {
    "dark_theme": True,
    "hide_cgpa": False,
    "marks_privacy": False,
    "hide_mess": False,
    "simple_timetable": False,
    "force_result": False,
    "force_course": False,
    "biometric_lock": False,
}

for key, value in toggle_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #000000;
    color: white;
}

/* Main container */
.block-container {
    max-width: 1000px;
    padding-top: 20px;
}

/* Header */
.header {
    background-color: #181818;
    height: 90px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 25px;
    border-bottom: 1px solid #333;
    margin-bottom: 15px;
}

.header-title {
    font-size: 36px;
    font-weight: 500;
}

.header-icon {
    font-size: 38px;
}

/* Section title */
.section-title {
    color: #9b9b9b;
    font-size: 22px;
    margin: 28px 0 10px 20px;
}

/* Settings box */
.settings-box {
    background-color: #1d1d1f;
    border-radius: 25px;
    padding: 5px 25px;
    margin-bottom: 20px;
}

/* Setting row */
.setting-row {
    min-height: 75px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #303030;
}

.setting-row:last-child {
    border-bottom: none;
}

.icon-box {
    width: 55px;
    height: 55px;
    background-color: #29292b;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    margin-right: 18px;
}

.setting-name {
    font-size: 23px;
    color: #f5f5f5;
    flex: 1;
}

.description {
    color: #9b9b9b;
    font-size: 19px;
    margin: 5px 0 25px 20px;
}

/* Streamlit buttons */
div.stButton > button {
    border-radius: 18px;
    border: none;
    background-color: #29292b;
    color: white;
    font-size: 20px;
    padding: 12px 20px;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #353537;
    border: none;
}

/* Toggle area */
.toggle-label {
    color: #aaa;
    font-size: 18px;
}

/* Danger buttons */
.danger button {
    color: #ff3b30 !important;
}

/* Success message */
.success-box {
    background-color: #183b25;
    color: #5cff8d;
    padding: 12px 18px;
    border-radius: 12px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="header">
    <div class="header-icon">◀</div>
    <div class="header-title">🦉 Settings</div>
    <div class="header-icon">⚙️</div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# TOGGLE FUNCTION
# --------------------------------------------------
def setting_toggle(icon, title, key):

    col1, col2 = st.columns([4.8, 1.2])

    with col1:
        st.markdown(
            f"""
            <div class="setting-row">
                <div class="icon-box">{icon}</div>
                <div class="setting-name">{title}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.toggle(
            "",
            key=key,
            label_visibility="collapsed"
        )


# --------------------------------------------------
# APPEARANCE
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Appearance</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

setting_toggle("🌙", "Dark Theme", "dark_theme")
setting_toggle("🙈", "Hide CGPA", "hide_cgpa")
setting_toggle("🔒", "Marks & Result Privacy", "marks_privacy")
setting_toggle("📚", "Hide Mess Menu", "hide_mess")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# MEAL DESCRIPTION
# --------------------------------------------------
st.markdown(
    '<div class="description">Only show next meal session on home screen</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# TIMETABLE
# --------------------------------------------------
st.markdown('<div class="settings-box">', unsafe_allow_html=True)

setting_toggle("🗓️", "Simple Timetable", "simple_timetable")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="description">Use a simple list view instead of calendar view</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# DATA & SYNC
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Data & Sync</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

setting_toggle("🔄", "Force Result Refresh", "force_result")
setting_toggle("📄", "Force Course Plan Refresh", "force_course")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# SUBJECT MANAGEMENT
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Subject Management</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

# Attendance Goals
col1, col2 = st.columns([4.5, 1.5])

with col1:
    st.markdown(
        """
        <div class="setting-row">
            <div class="icon-box">%</div>
            <div class="setting-name">Attendance<br>Goals</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    if st.button("Per-subject %  ›", key="attendance_goals"):
        st.session_state["attendance_clicked"] = True

# Manage Subjects
col1, col2 = st.columns([4.5, 1.5])

with col1:
    st.markdown(
        """
        <div class="setting-row">
            <div class="icon-box">☷</div>
            <div class="setting-name">Manage<br>Subjects</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    if st.button("Show/Hide  ›", key="manage_subjects"):
        st.session_state["subjects_clicked"] = True

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# ATTENDANCE GOALS PAGE/ACTION
# --------------------------------------------------
if st.session_state.get("attendance_clicked", False):

    st.subheader("🎯 Attendance Goals")

    attendance_goal = st.slider(
        "Set Attendance Goal",
        min_value=50,
        max_value=100,
        value=75,
        step=1
    )

    st.success(
        f"Attendance goal set to {attendance_goal}%"
    )


# --------------------------------------------------
# MANAGE SUBJECTS ACTION
# --------------------------------------------------
if st.session_state.get("subjects_clicked", False):

    st.subheader("📚 Manage Subjects")

    subjects = [
        "Computer Architecture",
        "Cybersecurity",
        "Information System",
        "Data Structure",
        "Operating System"
    ]

    for subject in subjects:
        st.checkbox(
            subject,
            value=True,
            key=f"subject_{subject}"
        )


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Security</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

# Biometric Lock
setting_toggle("🔒", "Biometric Lock", "biometric_lock")

# Logout
col1, col2 = st.columns([4.8, 1.2])

with col1:
    st.markdown(
        """
        <div class="setting-row">
            <div class="icon-box">↪</div>
            <div class="setting-name" style="color:#ff453a;">
                Logout - Clear app data
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    if st.button("›", key="logout_button"):
        st.warning("You have been logged out.")


# Delete Account
col1, col2 = st.columns([4.8, 1.2])

with col1:
    st.markdown(
        """
        <div class="setting-row">
            <div class="icon-box">🗑️</div>
            <div class="setting-name" style="color:#ff453a;">
                Delete Account
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    if st.button("›", key="delete_button"):
        st.error("Delete Account option selected.")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# CURRENT SETTINGS
# --------------------------------------------------
with st.expander("⚙️ Current Settings"):

    st.write("Dark Theme:", st.session_state.dark_theme)
    st.write("Hide CGPA:", st.session_state.hide_cgpa)
    st.write("Marks & Result Privacy:", st.session_state.marks_privacy)
    st.write("Hide Mess Menu:", st.session_state.hide_mess)
    st.write("Simple Timetable:", st.session_state.simple_timetable)
    st.write("Force Result Refresh:", st.session_state.force_result)
    st.write("Force Course Plan Refresh:", st.session_state.force_course)
    st.write("Biometric Lock:", st.session_state.biometric_lock)