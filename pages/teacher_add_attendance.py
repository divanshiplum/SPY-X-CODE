import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Add Attendance", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")

# Pastel Dark Theme CSS
THEME_CSS = """
<style>
    body {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #2a2a3e 0%, #3d3d52 100%);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .section-header {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border-left: 4px solid #9B8BA8;
        padding: 15px 20px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 600;
        margin: 20px 0 15px 0;
    }
    
    .stDateInput input, .stSelectbox select, .stTextInput input, .stNumberInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stDateInput label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #b4a7c6 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #9B8BA8 0%, #B4A7C6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02) !important;
    }
    
    .attendance-table {
        background: #3d3d52;
        border: 2px solid #6b6b80;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
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
</style>
"""

st.html(THEME_CSS)

# Back button
if st.button("← Back to Dashboard", use_container_width=True, key="back_btn"):
    st.switch_page("pages/teacher_dashboard.py")

st.markdown("<div class='header-title'>📋 Add & Manage Attendance</div>", unsafe_allow_html=True)

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Load or create attendance records
ATTENDANCE_FILE = "data/attendance_records.csv"
if not os.path.exists(ATTENDANCE_FILE):
    attendance_df = pd.DataFrame({
        "Date": [],
        "Student Roll No": [],
        "Subject": [],
        "Status": [],
        "Remarks": [],
        "Teacher": []
    })
    attendance_df.to_csv(ATTENDANCE_FILE, index=False)
else:
    attendance_df = pd.read_csv(ATTENDANCE_FILE)

# Subject options
SUBJECTS = [
    "Computer Architecture and Cybersecurity Fundamentals",
    "Information Systems",
    "Data Structure and Operating System"
]

# Tabs
tab1, tab2, tab3 = st.tabs(["Add Attendance", "View Records", "Bulk Upload"])

with tab1:
    st.markdown("<div class='section-header'>📝 Record Single Class Attendance</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        attendance_date = st.date_input("Date of Class", value=date.today(), label_visibility="collapsed")
    
    with col2:
        subject = st.selectbox("Subject", SUBJECTS, label_visibility="collapsed")
    
    st.markdown("<div class='section-header'>👥 Student Attendance</div>", unsafe_allow_html=True)
    
    students = [
        "25267546",
        "25267547",
        "25267548",
        "25267549",
        "25267550",
        "25267551",
        "25267552",
        "25267553"
    ]
    
    if "attendance_data" not in st.session_state:
        st.session_state.attendance_data = {student: {"status": "Present", "remarks": ""} for student in students}
    
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        st.markdown("**📋 Roll No**")
    with col2:
        st.markdown("**✅ Status**")
    with col3:
        st.markdown("**📝 Remarks**")
    
    st.markdown("---")
    
    for student in students:
        col1, col2, col3 = st.columns([2, 2, 3])
        
        with col1:
            st.write(f"Roll No: {student}")
        
        with col2:
            st.session_state.attendance_data[student]["status"] = st.radio(
                "Status", 
                ["Present", "Absent"], 
                key=f"status_{student}", 
                horizontal=True,
                label_visibility="collapsed",
                index=0 if st.session_state.attendance_data[student]["status"] == "Present" else 1
            )
        
        with col3:
            st.session_state.attendance_data[student]["remarks"] = st.text_input(
                "Remarks", 
                key=f"remarks_{student}", 
                label_visibility="collapsed",
                value=st.session_state.attendance_data[student]["remarks"]
            )
    
    if st.button("💾 Save Attendance Records", use_container_width=True):
        attendance_records = []
        teacher_name = st.session_state.get("teacher_name", "Unknown Teacher")
        
        for student in students:
            attendance_records.append({
                "Date": str(attendance_date),
                "Student Roll No": student,
                "Subject": subject,
                "Status": st.session_state.attendance_data[student]["status"],
                "Remarks": st.session_state.attendance_data[student]["remarks"],
                "Teacher": teacher_name
            })
        
        if os.path.exists(ATTENDANCE_FILE):
            existing_df = pd.read_csv(ATTENDANCE_FILE)
            new_df = pd.DataFrame(attendance_records)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = pd.DataFrame(attendance_records)
        
        combined_df.to_csv(ATTENDANCE_FILE, index=False)
        st.success("✅ Attendance records saved successfully!")
        
        st.session_state.attendance_data = {student: {"status": "Present", "remarks": ""} for student in students}

with tab2:
    st.markdown("<div class='section-header'>📊 View Attendance Records</div>", unsafe_allow_html=True)
    
    teacher_name = st.session_state.get("teacher_name", "Unknown Teacher")
    st.info(f"👨‍🏫 **Showing records for: {teacher_name}**")
    
    if os.path.exists(ATTENDANCE_FILE):
        attendance_df = pd.read_csv(ATTENDANCE_FILE)
    else:
        attendance_df = pd.DataFrame({
            "Date": [],
            "Student Roll No": [],
            "Subject": [],
            "Status": [],
            "Remarks": [],
            "Teacher": []
        })
    
    if "Teacher" in attendance_df.columns:
        teacher_attendance = attendance_df[attendance_df["Teacher"] == teacher_name].copy()
    else:
        teacher_attendance = attendance_df.copy()
    
    if teacher_attendance.empty:
        st.info("📭 No attendance records found. Start by adding attendance records in the 'Add Attendance' tab.")
    else:
        required_cols = ["Date", "Student Roll No", "Subject", "Status", "Remarks"]
        if not all(col in teacher_attendance.columns for col in required_cols):
            st.error("❌ Attendance data has missing columns. Please check the CSV file.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                filter_subject = st.selectbox("Filter by Subject", ["All"] + SUBJECTS, key="filter_subject")
            
            with col2:
                filter_status = st.selectbox("Filter by Status", ["All", "Present", "Absent"], key="filter_status")
            
            filtered_df = teacher_attendance.copy()
            
            if filter_subject != "All":
                filtered_df = filtered_df[filtered_df["Subject"] == filter_subject]
            
            if filter_status != "All":
                filtered_df = filtered_df[filtered_df["Status"] == filter_status]
            
            if not filtered_df.empty:
                display_cols = ["Date", "Student Roll No", "Subject", "Status", "Remarks"]
                available_cols = [col for col in display_cols if col in filtered_df.columns]
                
                if available_cols:
                    st.dataframe(filtered_df[available_cols], use_container_width=True)
                else:
                    st.dataframe(filtered_df, use_container_width=True)
                
                st.markdown("<div class='section-header'>📈 Statistics</div>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Records", len(filtered_df))
                
                with col2:
                    if "Status" in filtered_df.columns:
                        present_count = len(filtered_df[filtered_df["Status"] == "Present"])
                        st.metric("Present", present_count)
                    else:
                        st.metric("Present", "N/A")
                
                with col3:
                    if "Status" in filtered_df.columns:
                        absent_count = len(filtered_df[filtered_df["Status"] == "Absent"])
                        st.metric("Absent", absent_count)
                    else:
                        st.metric("Absent", "N/A")
                
                with col4:
                    if "Status" in filtered_df.columns and len(filtered_df) > 0:
                        present_count = len(filtered_df[filtered_df["Status"] == "Present"])
                        attendance_pct = (present_count / len(filtered_df)) * 100
                        st.metric("Attendance %", f"{attendance_pct:.1f}%")
                    else:
                        st.metric("Attendance %", "N/A")
            else:
                st.info("📭 No attendance records found with the selected filters.")

with tab3:
    st.markdown("<div class='section-header'>📤 Bulk Upload Attendance</div>", unsafe_allow_html=True)
    
    st.write("Upload a CSV file with attendance data. Format should include columns: Date, Student Roll No, Subject, Status, Remarks")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            new_attendance_df = pd.read_csv(uploaded_file)
            
            required_columns = ["Date", "Student Roll No", "Subject", "Status", "Remarks"]
            if all(col in new_attendance_df.columns for col in required_columns):
                
                st.write("Preview of uploaded data:")
                st.dataframe(new_attendance_df, use_container_width=True)
                
                if st.button("✅ Confirm & Upload", use_container_width=True):
                    teacher_name = st.session_state.get("teacher_name", "Unknown Teacher")
                    new_attendance_df["Teacher"] = teacher_name
                    
                    if os.path.exists(ATTENDANCE_FILE):
                        existing_df = pd.read_csv(ATTENDANCE_FILE)
                        combined_df = pd.concat([existing_df, new_attendance_df], ignore_index=True)
                    else:
                        combined_df = new_attendance_df
                    
                    combined_df.to_csv(ATTENDANCE_FILE, index=False)
                    st.success("✅ Bulk attendance upload completed!")
            else:
                st.error("❌ CSV file must contain columns: " + ", ".join(required_columns))
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")