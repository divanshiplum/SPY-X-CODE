import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Teacher Login - HCIMS", page_icon="👨‍🏫", layout="centered")

# Pastel Dark Theme CSS
THEME_CSS = """
<style>
    body {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .login-container {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border: 2px solid #6b6b80;
        border-radius: 20px;
        padding: 50px 40px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        max-width: 400px;
        margin: 60px auto;
    }
    
    .login-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .login-subtitle {
        font-size: 14px;
        color: #b4a7c6;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .stTextInput, .stTextInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
    }
    
    .stTextInput label {
        color: #b4a7c6 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        padding: 8px 20px !important;
        font-size: 14px !important;
        width: auto !important;
        min-width: 120px !important;
        display: block !important;
        margin: 0 auto !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(155, 139, 168, 0.4) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #5a3a3a 0%, #4a3030 100%) !important;
        border: 1px solid #8a5a5a !important;
        color: #ffb3b3 !important;
        border-radius: 10px !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #3a5a3a 0%, #304a30 100%) !important;
        border: 1px solid #5a8a5a !important;
        color: #b3ffb3 !important;
        border-radius: 10px !important;
    }
    
    .back-link {
        text-align: center;
        margin-top: 30px;
    }
    
    .back-link a {
        border: 2px solid #9B8BA8;
        padding: 8px 16px;
        border-radius: 8px;
        display: inline-block;
        transition: all 0.3s ease;
    }

    .back-link a:hover {
        border-color: #B4A7C6;
        background: rgba(155, 139, 168, 0.1);
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
    
    /* Hide entire sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
    }
</style>
"""

st.html(THEME_CSS)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEACHERS_FILE = DATA_DIR / "teachers.csv"

def create_teachers_csv():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not TEACHERS_FILE.exists():
        # Create sample teacher data
        teachers_data = {
            "Employee Code": ["TC001", "TC002", "TC003"],
            "Name": ["Dr. Manpreet Kaur Dhaliwal", "Ms. Neha Sharma", "Mr. Anshuman Sharma"],
            "Subject": ["Data Structures", "Computer Architecture", "Information Systems"],
            "Department": ["Computer Science", "Computer Science", "Computer Science"],
            "Email": ["manpreet@hinducollegamritsar.edu", "neha@hinducollegamritsar.edu", "anshuman@hinducollegamritsar.edu"],
            "Password": ["teacher001", "teacher002", "teacher003"]
        }
        df = pd.DataFrame(teachers_data)
        df.to_csv(TEACHERS_FILE, index=False)

create_teachers_csv()

st.markdown("<div class='login-title'>👨‍🏫 Teacher Login</div>", unsafe_allow_html=True)
st.markdown("<div class='login-subtitle'>HCIMS - Teacher Portal</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

with col2:
    emp_code = st.text_input("Employee Code", placeholder="e.g., TC001", key="emp_code_input")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="password_input")
    
    if st.button("Login", use_container_width=True):
        if emp_code and password:
            try:
                teachers_df = pd.read_csv(TEACHERS_FILE)
                teacher = teachers_df[
                    (teachers_df["Employee Code"].astype(str) == emp_code) &
                    (teachers_df["Password"].astype(str) == password)
                ]
                
                if not teacher.empty:
                    st.session_state.teacher_logged_in = True
                    st.session_state.teacher_emp_code = emp_code
                    st.session_state.teacher_name = teacher.iloc[0]["Name"]
                    st.session_state.teacher_subject = teacher.iloc[0]["Subject"]
                    st.session_state.teacher_email = teacher.iloc[0]["Email"]
                    
                    st.success(f"Welcome, {teacher.iloc[0]['Name']}!")
                    st.switch_page("pages/teacher_dashboard.py")
                else:
                    st.error("❌ Invalid Employee Code or Password")
            except FileNotFoundError:
                st.error("❌ Teacher database not found. Please contact administrator.")
        else:
            st.error("❌ Please fill in all fields")

st.markdown("</div>", unsafe_allow_html=True)

# Back to home link
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("← Back to Home", use_container_width=True, key="back_home_btn"):
        st.switch_page("app.py")