import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Manage Students", 
    page_icon="👥", 
    layout="wide", 
    initial_sidebar_state="collapsed"
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
    
    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    
    .section-header {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border-left: 4px solid #B8D4B6;
        padding: 15px 20px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 600;
        margin: 20px 0 15px 0;
    }
    
    .stSelectbox select, .stTextInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label, .stTextInput label {
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
    
    .student-card {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border: 2px solid #6b6b80;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .student-name {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .student-detail {
        color: #b4a7c6;
        font-size: 13px;
        margin: 5px 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .status-active {
        background: #3a5a3a;
        color: #b3ffb3;
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

# ==================== BACK BUTTON ====================
if st.button("← Back to Dashboard", use_container_width=True, key="back_btn"):
    st.switch_page("pages/teacher_dashboard.py")

st.markdown("<div class='header-title'>👥 Manage Students</div>", unsafe_allow_html=True)

# ==================== INITIALIZE DATA ====================
STUDENTS_FILE = "data/students_info.csv"

if not os.path.exists("data"):
    os.makedirs("data")

def create_students_csv():
    if not os.path.exists(STUDENTS_FILE):
        students_data = {
            "Roll No": ["25267546", "25267547", "25267548", "25267549", "25267550", 
                       "25267551", "25267552", "25267553"],
            "Name": ["Divanshi Khosla", "Raj Kumar", "Priya Singh", "Aman Patel",
                    "Neha Sharma", "Vikram Singh", "Anjali Gupta", "Rohan Sharma"],
            "Email": ["divanshi@hinducollegamritsar.edu", "raj@hinducollegamritsar.edu",
                     "priya@hinducollegamritsar.edu", "aman@hinducollegamritsar.edu",
                     "neha@hinducollegamritsar.edu", "vikram@hinducollegamritsar.edu",
                     "anjali@hinducollegamritsar.edu", "rohan@hinducollegamritsar.edu"],
            "Phone": ["9876543210", "9876543211", "9876543212", "9876543213",
                     "9876543214", "9876543215", "9876543216", "9876543217"],
            "Status": ["Active", "Active", "Active", "Active", "Active", "Active", "Active", "Active"],
            "Enrollment Date": ["2022-09-15", "2022-09-15", "2022-09-15", "2022-09-15",
                               "2022-09-15", "2022-09-15", "2022-09-15", "2022-09-15"]
        }
        df = pd.DataFrame(students_data)
        df.to_csv(STUDENTS_FILE, index=False)
    
    return pd.read_csv(STUDENTS_FILE)

students_df = create_students_csv()

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["Student List", "Student Details", "Add Student"])

# ==================== TAB 1: STUDENT LIST ====================
with tab1:
    st.markdown("<div class='section-header'>📊 All Students</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("🔍 Search by Name or Roll No", placeholder="Enter name or roll number", key="search_input")
    
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "Suspended"], key="filter_status")
    
    # Apply filters
    filtered_df = students_df.copy()
    
    if search_term:
        filtered_df = filtered_df[
            (filtered_df["Roll No"].astype(str).str.contains(search_term, case=False)) |
            (filtered_df["Name"].str.contains(search_term, case=False))
        ]
    
    if filter_status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == filter_status]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        st.markdown("<div class='section-header'>📈 Statistics</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", len(filtered_df))
        
        with col2:
            active = len(filtered_df[filtered_df["Status"] == "Active"])
            st.metric("Active", active)
        
        with col3:
            inactive = len(filtered_df[filtered_df["Status"] == "Inactive"])
            st.metric("Inactive", inactive)
        
        with col4:
            suspended = len(filtered_df[filtered_df["Status"] == "Suspended"])
            st.metric("Suspended", suspended)
    else:
        st.info("📭 No students found matching the search criteria.")

# ==================== TAB 2: STUDENT DETAILS ====================
with tab2:
    st.markdown("<div class='section-header'>👤 Student Details</div>", unsafe_allow_html=True)
    
    selected_roll = st.selectbox("Select Student", students_df["Roll No"].tolist(), key="select_student")
    
    student = students_df[students_df["Roll No"] == selected_roll].iloc[0]
    
    st.markdown(f"""
    <div class='student-card'>
        <div class='student-name'>👤 {student['Name']}</div>
        <div class='student-detail'><strong>Roll No:</strong> {student['Roll No']}</div>
        <div class='student-detail'><strong>Email:</strong> {student['Email']}</div>
        <div class='student-detail'><strong>Phone:</strong> {student['Phone']}</div>
        <div class='student-detail'><strong>Status:</strong> {student['Status']}</div>
        <div class='student-detail'><strong>Enrollment Date:</strong> {student['Enrollment Date']}</div>
        <div class='status-badge status-active'>{student['Status']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📚 Academic Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        attendance_df = pd.read_csv("data/attendance_records.csv")
        student_attendance = attendance_df[attendance_df["Student Roll No"] == selected_roll]
        
        if not student_attendance.empty:
            total_classes = len(student_attendance)
            present = len(student_attendance[student_attendance["Status"] == "Present"])
            attendance_pct = (present / total_classes * 100) if total_classes > 0 else 0
            
            with col1:
                st.metric("Attendance %", f"{attendance_pct:.1f}%")
    except:
        pass
    
    try:
        marks_df = pd.read_csv("data/student-marks.csv")
        student_marks = marks_df[marks_df["Student Roll No"] == selected_roll]
        
        if not student_marks.empty:
            avg_marks = student_marks["Marks"].mean()
            
            with col2:
                st.metric("Avg Marks", f"{avg_marks:.1f}")
    except:
        pass
    
    st.markdown("---")
    st.markdown("<div class='section-header'>✏️ Edit Student Status</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_status = st.selectbox("Update Status", ["Active", "Inactive", "Suspended"], 
                                 key="update_status")
    
    with col2:
        if st.button("💾 Update Status", use_container_width=True, key="update_btn"):
            students_df.loc[students_df["Roll No"] == selected_roll, "Status"] = new_status
            students_df.to_csv(STUDENTS_FILE, index=False)
            st.success(f"✅ Student status updated to {new_status}")
            st.rerun()

# ==================== TAB 3: ADD STUDENT ====================
with tab3:
    st.markdown("<div class='section-header'>➕ Add New Student</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_roll = st.text_input("Roll No", placeholder="e.g., 25267554", key="new_roll_input")
        new_name = st.text_input("Student Name", placeholder="Full name", key="new_name_input")
        new_email = st.text_input("Email", placeholder="student@hinducollegamritsar.edu", key="new_email_input")
    
    with col2:
        new_phone = st.text_input("Phone", placeholder="10 digit number", key="new_phone_input")
        new_status = st.selectbox("Initial Status", ["Active", "Inactive"], key="new_status_select")
        new_enroll_date = st.date_input("Enrollment Date", key="new_enroll_date_input")
    
    if st.button("✅ Add Student", use_container_width=True, key="add_student_btn"):
        if new_roll and new_name and new_email and new_phone:
            if new_roll in students_df["Roll No"].values:
                st.error("❌ Roll number already exists!")
            else:
                new_student = {
                    "Roll No": new_roll,
                    "Name": new_name,
                    "Email": new_email,
                    "Phone": new_phone,
                    "Status": new_status,
                    "Enrollment Date": str(new_enroll_date)
                }
                
                new_row = pd.DataFrame([new_student])
                students_df = pd.concat([students_df, new_row], ignore_index=True)
                students_df.to_csv(STUDENTS_FILE, index=False)
                
                st.success(f"✅ Student {new_name} added successfully!")
        else:
            st.error("❌ Please fill in all fields")