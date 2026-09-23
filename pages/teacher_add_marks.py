import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Add Marks", 
    page_icon="📊", 
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
        border-left: 4px solid #9B8BA8;
        padding: 15px 20px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 600;
        margin: 20px 0 15px 0;
    }
    
    .stSelectbox select, .stTextInput input, .stNumberInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {
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
    
    .mark-type-label {
        color: #B4A7C6 !important;
        font-weight: 600 !important;
        font-size: 14px;
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

st.markdown("<div class='header-title'>📊 Add & Manage Marks</div>", unsafe_allow_html=True)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MARKS_FILE = DATA_DIR / "student-marks.csv"

if not MARKS_FILE.exists():
    marks_df = pd.DataFrame({
        "Subject": [
            "Computer Architecture",
            "Computer Architecture (Lab)",
            "Cybersecurity Fundamentals",
            "Cybersecurity Fundamentals (Lab)",
            "Information System",
            "Data Structure",
            "Data Structure (Lab)",
            "Operating System"
        ],
        "Type": ["Theory", "Practical", "Theory", "Practical", "Theory", "Theory", "Practical", "Theory"],
        "Marks": [82, 88, 78, 84, 80, 76, 90, 85]
    })
    marks_df.to_csv(MARKS_FILE, index=False)
else:
    marks_df = pd.read_csv(MARKS_FILE)

# ==================== CONFIGURATION ====================
SUBJECTS = [
    "Computer Architecture",
    "Computer Architecture (Lab)",
    "Cybersecurity Fundamentals",
    "Cybersecurity Fundamentals (Lab)",
    "Information System",
    "Data Structure",
    "Data Structure (Lab)",
    "Operating System"
]

ASSESSMENT_TYPES = ["Theory", "Practical"]

STUDENTS = [
    "25267546",
    "25267547",
    "25267548",
    "25267549",
    "25267550",
    "25267551",
    "25267552",
    "25267553"
]

# ==================== TABS ====================
tab1, tab2, tab3 = st.tabs(["Add Marks", "View Records", "All Subjects"])

# ==================== TAB 1: ADD MARKS ====================
with tab1:
    st.markdown("<div class='section-header'>📝 Enter Marks</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox("Subject", SUBJECTS, label_visibility="collapsed", key="add_subject")
    
    with col2:
        mark_type = st.selectbox("Assessment Type", ASSESSMENT_TYPES, label_visibility="collapsed", key="add_assessment")
    
    st.markdown(f"<div class='section-header'>👥 {mark_type} Marks</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.write("**Roll No**")
    with col2:
        st.write(f"**{mark_type} Marks**")
    with col3:
        st.write("**Out of**")
    
    st.divider()
    
    marks_records = []
    
    for student in STUDENTS:
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.write(f"{student}")
        
        with col2:
            marks = st.number_input(
                f"Marks for {student}", 
                min_value=0, 
                max_value=100, 
                key=f"marks_{student}", 
                label_visibility="collapsed", 
                step=1
            )
        
        with col3:
            total_marks = st.number_input(
                f"Total for {student}", 
                min_value=1, 
                value=100, 
                key=f"total_{student}", 
                label_visibility="collapsed", 
                step=1
            )
        
        marks_records.append({
            "Roll No": student,
            "Subject": subject,
            "Type": mark_type,
            "Marks": marks,
            "Total Marks": total_marks,
            "Date": datetime.now().strftime("%Y-%m-%d")
        })
    
    if st.button("💾 Save Marks", use_container_width=True, key="save_marks_btn"):
        try:
            new_df = pd.DataFrame(marks_records)
            st.dataframe(new_df, use_container_width=True)
            
            student_roll_no = "25267546"
            divanshi_records = [record for record in marks_records if record["Roll No"] == student_roll_no]
            
            if divanshi_records:
                if os.path.exists(MARKS_FILE):
                    existing_marks = pd.read_csv(MARKS_FILE)
                    
                    for record in divanshi_records:
                        subject = record["Subject"]
                        mark_type = record["Type"]
                        new_marks = record["Marks"]
                        
                        mask = (existing_marks["Subject"] == subject) & (existing_marks["Type"] == mark_type)
                        if mask.any():
                            existing_marks.loc[mask, "Marks"] = new_marks
                    
                    existing_marks.to_csv(MARKS_FILE, index=False)
                    st.info(f"✅ Roll No {student_roll_no} (Divanshi) marks auto-saved to student-marks.csv!")
                else:
                    st.warning("❌ student-marks.csv not found!")
            
            st.success("✅ Marks saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving marks: {str(e)}")

# ==================== TAB 2: VIEW RECORDS ====================
with tab2:
    st.markdown("<div class='section-header'>📊 View Marks Records</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        filter_subject = st.selectbox("Filter by Subject", ["All"] + SUBJECTS, key="filter_subject")
    
    with col2:
        filter_type = st.selectbox("Filter by Type", ["All"] + ASSESSMENT_TYPES, key="filter_type")
    
    try:
        filtered_df = marks_df.copy()
        
        if filter_subject != "All" and "Subject" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Subject"] == filter_subject]
        
        if filter_type != "All" and "Type" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Type"] == filter_type]
        
        if not filtered_df.empty:
            if len(filtered_df) > 0:
                mark_type_display = filtered_df["Type"].iloc[0] if "Type" in filtered_df.columns else "Marks"
                st.markdown(f"<p class='mark-type-label'>📌 Showing {mark_type_display} Marks</p>", unsafe_allow_html=True)
            
            st.dataframe(filtered_df, use_container_width=True)
            
            st.markdown("<div class='section-header'>📈 Statistics</div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(filtered_df))
            
            with col2:
                if len(filtered_df) > 0 and "Marks" in filtered_df.columns:
                    avg_marks = pd.to_numeric(filtered_df["Marks"], errors='coerce').mean()
                    st.metric("Average Marks", f"{avg_marks:.1f}" if not pd.isna(avg_marks) else "N/A")
                else:
                    st.metric("Average Marks", "N/A")
            
            with col3:
                if len(filtered_df) > 0 and "Marks" in filtered_df.columns:
                    highest = pd.to_numeric(filtered_df["Marks"], errors='coerce').max()
                    st.metric("Highest Marks", int(highest) if not pd.isna(highest) else "N/A")
                else:
                    st.metric("Highest Marks", "N/A")
            
            with col4:
                if len(filtered_df) > 0 and "Marks" in filtered_df.columns:
                    lowest = pd.to_numeric(filtered_df["Marks"], errors='coerce').min()
                    st.metric("Lowest Marks", int(lowest) if not pd.isna(lowest) else "N/A")
                else:
                    st.metric("Lowest Marks", "N/A")
        else:
            st.info("📭 No marks records found with the selected filters.")
    
    except KeyError as e:
        st.error(f"❌ Error: Column not found - {str(e)}")
        st.info("💡 Please ensure your CSV has 'Subject' and 'Type' columns.")
    except Exception as e:
        st.error(f"❌ Error loading records: {str(e)}")

# ==================== TAB 3: SUBJECTS OVERVIEW ====================
with tab3:
    st.markdown("<div class='section-header'>📚 All Subjects & Marks Overview</div>", unsafe_allow_html=True)
    
    theory_subjects = marks_df[marks_df["Type"] == "Theory"].copy()
    practical_subjects = marks_df[marks_df["Type"] == "Practical"].copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📖 Theory Marks")
        if not theory_subjects.empty:
            st.dataframe(
                theory_subjects[["Subject", "Marks"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No theory marks found")
    
    with col2:
        st.markdown("### 💻 Practical Marks")
        if not practical_subjects.empty:
            st.dataframe(
                practical_subjects[["Subject", "Marks"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No practical marks found")
    
    st.markdown("<div class='section-header'>📊 Summary</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Subjects", len(marks_df))
    
    with col2:
        st.metric("Theory Subjects", len(theory_subjects))
    
    with col3:
        st.metric("Practical Subjects", len(practical_subjects))
    
    with col4:
        if len(marks_df) > 0:
            avg_all = pd.to_numeric(marks_df["Marks"], errors='coerce').mean()
            st.metric("Overall Average", f"{avg_all:.1f}")
        else:
            st.metric("Overall Average", "N/A")