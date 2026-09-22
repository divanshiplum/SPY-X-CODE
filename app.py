import streamlit as st

# Set page config
st.set_page_config(
    page_title="HC IMS - Hindu College Information Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pastel Dark Theme CSS
LANDING_CSS = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    /* Header Section */
    .header-container {
        text-align: center;
        padding: 30px 20px 20px 20px;
    }
    
    .logo-title {
        font-size: 48px;
        font-weight: 700;
        margin: 10px 0 10px 0;
        color: #ffffff;
        letter-spacing: 2px;
    }
    
    .subtitle {
        font-size: 18px;
        color: #d4a5a5;
        margin-bottom: 50px;
        font-weight: 300;
    }
    
    /* Cards Container */
    .cards-wrapper {
        display: flex;
        justify-content: center;
        gap: 100px;
        padding: 40px 20px 0px 20px;
        flex-wrap: wrap;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Login Card Styling */
    .login-card {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border: 2px solid #6b6b80;
        border-radius: 20px;
        padding: 50px 40px 35px 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        text-align: center;
        width: 350px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 500px;
    }
    
    .login-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
        border-color: #9B8BA8;
    }
    
    .card-icon {
        font-size: 60px;
        margin-bottom: 25px;
    }
    
    .card-title {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 20px;
    }
    
    .card-description {
        font-size: 14px;
        color: #b4a7c6;
        line-height: 1.8;
        margin-bottom: 0px;
        flex-grow: 1;
    }
    
    /* Button styling */
    .stButton {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #9B8BA8 0%, #B4A7C6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 12px 40px !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        width: auto !important;
        min-width: 200px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(155, 139, 168, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: scale(0.98) !important;
    }
    
    /* Hide Streamlit elements */
    header {
        display: none !important;
    }
    
    .stApp > header {
        display: none !important;
    }
    
    footer {
        display: none !important;
    }
    
    .viewerBadge_container__r5tak {
        display: none !important;
    }
    
    /* Hide top navigation bar */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* Make content full width */
    .main .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    /* Hide entire sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide sidebar container */
    .st-emotion-cache-1wbqy5l {
        display: none !important;
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
    
    /* Hide sidebar toggle button */
    button[kind="header"] {
        display: none !important;
    }
    
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    /* Hide hamburger menu icon */
    [data-testid="baseButton-header"] {
        display: none !important;
    }
    
    /* Hide the sidebar toggle completely */
    .st-emotion-cache-18ni7ap {
        display: none !important;
    }
</style>
"""

st.html(LANDING_CSS)

# Header
st.html("<div class='header-container'><div class='logo-title'>🎓 HCIMS</div><div class='subtitle'>Hindu College Information Management System</div></div>")

# Cards
st.html("""
<div class='cards-wrapper'>
    <!-- Student Card -->
    <div class='login-card'>
        <div>
            <div class='card-icon'>👨‍🎓</div>
            <div class='card-title'>Student Login</div>
            <div class='card-description'>
                Login with your Roll Number and Password to access your academic information, attendance, marks, and college announcements.
            </div>
        </div>
    </div>
    
    <!-- Teacher Card -->
    <div class='login-card'>
        <div>
            <div class='card-icon'>👨‍🏫</div>
            <div class='card-title'>Teacher Login</div>
            <div class='card-description'>
                Login with your Employee Code and Password to manage student data, add marks, attendance, fees, and college announcements.
            </div>
        </div>
    </div>
</div>
""")

# Space before buttons
st.markdown("<br>", unsafe_allow_html=True)

# Buttons with proper navigation - Center aligned
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col2:
    if st.button("🔓 Login Now", key="student_login_btn", use_container_width=True):
        st.switch_page("pages/login.py")

with col4:
    if st.button("🔓 Login Now", key="teacher_login_btn", use_container_width=True):
        st.switch_page("pages/teacher_login.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #9B8BA8; font-size: 12px; padding: 20px;'>
    <p>Hindu College, Amritsar | Affiliated to Guru Nanak Dev University</p>
    <p style='margin-top: 10px;'>© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)