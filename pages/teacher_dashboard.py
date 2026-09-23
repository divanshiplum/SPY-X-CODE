import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Teacher Dashboard", 
    page_icon="👨‍🏫", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ==================== THEME CSS ====================
THEME_CSS = """
<style>
    body {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .header-section {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border-bottom: 2px solid #6b6b80;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    
    .teacher-info {
        color: #ffffff;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .teacher-detail {
        color: #b4a7c6;
        font-size: 14px;
        margin: 5px 0;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border: 2px solid #6b6b80;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        border-color: #9B8BA8;
        box-shadow: 0 10px 30px rgba(155, 139, 168, 0.2);
    }
    
    .card-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 10px;
    }
    
    .card-description {
        font-size: 13px;
        color: #b4a7c6;
        line-height: 1.5;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #9B8BA8 0%, #B4A7C6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
    }
    
    .logout-button > button {
        background: linear-gradient(135deg, #D4A5A5 0%, #C9888A 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    .logout-button > button:hover {
        transform: scale(1.02) !important;
    }
    
    .stSelectbox, .stMultiSelect {
        background: #3d3d52 !important;
    }
    
    .stSelectbox label, .stMultiSelect label {
        color: #b4a7c6 !important;
    }
    
    /* Hide entire sidebar and all sidebar elements */
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
    }
    
    /* Hide Streamlit's automatic page navigation in sidebar */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }
    
    /* Hide sidebar toggle buttons */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    button[kind="header"] {
        display: none !important;
    }
    /* Hide navigation section */
    ul[role="menuitem"] {
        display: none !important;
    }
    
    /* Hide all navigation links */
    .css-1v3fvcr {
        display: none !important;
    }
    
    /* Hide top navigation toolbar */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Hide header elements */
    header {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
</style>
"""

st.html(THEME_CSS)

# ==================== TOP RIGHT LOGOUT BUTTON ====================
col1, col2, col3 = st.columns([4, 1, 0.5])

with col3:
    st.markdown("<div class='logout-button'>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, key="logout_top_btn"):
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_emp_code = None
        st.session_state.teacher_name = None
        st.session_state.teacher_subject = None
        st.session_state.teacher_email = None
        st.switch_page("app.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 👨‍🏫 Teacher Portal")
    
    teacher_name = st.session_state.get("teacher_name", "Teacher")
    st.write(f"**Logged in as:**  \n{teacher_name}")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.teacher_logged_in = False
        st.session_state.teacher_emp_code = None
        st.session_state.teacher_name = None
        st.session_state.teacher_subject = None
        st.session_state.teacher_email = None
        st.switch_page("app.py")

# ==================== HEADER ====================
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f"""
    <div class='header-section'>
        <div class='teacher-info'>👨‍🏫 Welcome, {st.session_state.get('teacher_name', 'Teacher')}!</div>
        <div class='teacher-detail'>📚 Subject: {st.session_state.get('teacher_subject', 'N/A')}</div>
        <div class='teacher-detail'>✉️ Email: {st.session_state.get('teacher_email', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
st.markdown("### 📊 Teacher Management Dashboard")
st.markdown("---")

# Dashboard Cards in 3x2 Grid
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>📋</div>
        <div class='card-title'>Add Attendance</div>
        <div class='card-description'>Record student attendance for your classes and manage attendance records.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="attendance_btn", use_container_width=True):
        st.switch_page("pages/teacher_add_attendance.py")

with col2:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>📊</div>
        <div class='card-title'>Add Marks</div>
        <div class='card-description'>Enter and manage student marks for assignments, tests, and exams.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="marks_btn", use_container_width=True):
        st.switch_page("pages/teacher_add_marks.py")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>💰</div>
        <div class='card-title'>Add Fees</div>
        <div class='card-description'>Manage student fee records and generate receipts for payments.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="fees_btn", use_container_width=True):
        st.switch_page("pages/teacher_add_fees.py")

with col4:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>📣</div>
        <div class='card-title'>Add Notices</div>
        <div class='card-description'>Create and publish announcements and notices for students.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="notices_btn", use_container_width=True):
        st.switch_page("pages/teacher_add_notices.py")

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>⏰</div>
        <div class='card-title'>Manage Timetable</div>
        <div class='card-description'>Create and update class schedule and timetable information.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="timetable_btn", use_container_width=True):
        st.switch_page("pages/teacher_manage_timetable.py")

with col6:
    st.markdown("""
    <div class='dashboard-card'>
        <div class='card-icon'>👥</div>
        <div class='card-title'>Manage Students</div>
        <div class='card-description'>View and manage student information and enrollment details.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔓 Open", key="students_btn", use_container_width=True):
        st.switch_page("pages/teacher_manage_students.py")

# ==================== STATISTICS SECTION ====================
st.markdown("---")
st.markdown("### 📈 Quick Statistics")

col1, col2, col3, col4 = st.columns(4)

from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with col1:
    st.metric("Total Students", "150", "↑ 5 this month")

with col2:
    try:
        attendance_df = pd.read_csv(DATA_DIR / "attendance_records.csv")
        total_records = len(attendance_df)
        st.metric("Attendance Records", total_records, "✓ Updated")
    except:
        st.metric("Attendance Records", "0", "No data yet")

with col3:
    try:
        marks_df = pd.read_csv(DATA_DIR / "student-marks.csv")
        total_marks = len(marks_df)
        st.metric("Marks Entered", total_marks, "✓ Updated")
    except:
        st.metric("Marks Entered", "0", "No data yet")

with col4:
    try:
        fees_df = pd.read_csv(DATA_DIR / "fees.csv")
        total_fees = len(fees_df)
        st.metric("Fee Records", total_fees, "✓ Recorded")
    except:
        st.metric("Fee Records", "0", "No data yet")