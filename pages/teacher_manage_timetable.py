import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(
    page_title="Manage Timetable", 
    page_icon="⏰", 
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
        border-left: 4px solid #A5C7A4;
        padding: 15px 20px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 600;
        margin: 20px 0 15px 0;
    }
    
    .stSelectbox select, .stTextInput input, .stTimeInput input, .stDateInput input, .stNumberInput input {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label, .stTextInput label, .stTimeInput label, .stDateInput label, .stNumberInput label {
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
    
    .timetable-cell {
        background: #3d3d52;
        border: 1px solid #6b6b80;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        color: #b4a7c6;
        font-weight: 600;
    }
    
    .timetable-class {
        background: linear-gradient(135deg, #4a5a5a 0%, #3d4a4a 100%);
        border: 2px solid #9B8BA8;
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

st.markdown("<div class='header-title'>⏰ Manage Timetable</div>", unsafe_allow_html=True)

# ==================== INITIALIZE DATA ====================
TIMETABLE_FILE = "data/timetable.json"

if not os.path.exists("data"):
    os.makedirs("data")

def load_timetable():
    if os.path.exists(TIMETABLE_FILE):
        with open(TIMETABLE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_timetable(timetable):
    with open(TIMETABLE_FILE, 'w') as f:
        json.dump(timetable, f, indent=2)

# ==================== CONFIGURATION ====================
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = ["09:00 - 09:40", "09:40 - 10:20", "10:20 - 11:00", "11:00 - 11:40", "11:40 - 12:20"]
SUBJECTS = [
    "23CSR-449 (Data Structure)",
    "SPO-113 (Computer Architecture)",
    "23BDA-401 (Information System)",
    "23BDA-402 (Cybersecurity Fundamentals)",
    "23BDA-403 (Operating System)"
]
CLASS_TYPES = ["Lecture", "Practical"]

# ==================== TABS ====================
tab1, tab2 = st.tabs(["Edit Timetable", "View Timetable"])

# ==================== TAB 1: EDIT TIMETABLE ====================
with tab1:
    st.markdown("<div class='section-header'>📝 Add/Edit Class Schedule</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        day = st.selectbox("Day", DAYS, key="select_day")
    
    with col2:
        time_slot = st.selectbox("Time Slot", TIME_SLOTS, key="select_time_slot")
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox("Subject", SUBJECTS, key="select_subject")
    
    with col2:
        class_type = st.selectbox("Class Type", CLASS_TYPES, key="select_class_type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        room_no = st.text_input("Room No.", placeholder="e.g., 101", key="room_no_input")
    
    with col2:
        instructor = st.text_input(
            "Instructor Name", 
            value=st.session_state.get("teacher_name", ""),
            key="instructor_input"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        capacity = st.number_input(
            "Class Capacity", 
            min_value=10, 
            value=60, 
            step=10, 
            key="capacity_input"
        )
    
    if st.button("➕ Add to Schedule", use_container_width=True, key="add_schedule_btn"):
        if not room_no or not instructor:
            st.error("❌ Please fill in all fields (Room No. and Instructor Name are required)")
        else:
            timetable = load_timetable()
            
            if day not in timetable:
                timetable[day] = {}
            
            class_info = {
                "time_slot": time_slot,
                "subject": subject,
                "type": class_type,
                "room": room_no,
                "instructor": instructor,
                "capacity": capacity
            }
            
            timetable[day][time_slot] = class_info
            save_timetable(timetable)
            
            st.success(f"✅ Class added for {day} at {time_slot}!")
            st.rerun()

# ==================== TAB 2: VIEW TIMETABLE ====================
with tab2:
    st.markdown("<div class='section-header'>📅 Weekly Timetable</div>", unsafe_allow_html=True)
    
    timetable = load_timetable()
    
    if not timetable:
        st.info("📭 No timetable scheduled yet. Add classes from the Edit Timetable tab.")
    else:
        selected_day = st.selectbox("View Schedule for:", DAYS, key="view_day_select")
        
        if selected_day in timetable and timetable[selected_day]:
            st.markdown(f"### {selected_day} Schedule")
            
            day_schedule = timetable[selected_day]
            
            for time_slot in TIME_SLOTS:
                if time_slot in day_schedule:
                    class_info = day_schedule[time_slot]
                    
                    st.markdown(f"""
                    <div class='timetable-cell timetable-class'>
                        <strong>⏰ {time_slot}</strong><br>
                        📚 {class_info['subject']}<br>
                        🎓 {class_info['type']}<br>
                        👨‍🏫 {class_info['instructor']}<br>
                        🏫 Room {class_info['room']} | 👥 Capacity: {class_info['capacity']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
                    
                    with col2:
                        if st.button("✏️", key=f"edit_{selected_day}_{time_slot}", help="Edit"):
                            st.info("Edit functionality coming soon")
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{selected_day}_{time_slot}", help="Delete"):
                            del timetable[selected_day][time_slot]
                            if not timetable[selected_day]:
                                del timetable[selected_day]
                            save_timetable(timetable)
                            st.success("✅ Class removed from schedule")
                            st.rerun()
                else:
                    st.markdown(f"""
                    <div class='timetable-cell'>
                        ⏰ {time_slot}<br>
                        <em style='color: #6b6b80;'>No class scheduled</em>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"📭 No classes scheduled for {selected_day}")
        
        st.markdown("---")
        st.markdown("### 📅 Full Week Overview")
        
        week_data = []
        for day in DAYS:
            slot_count = len(timetable.get(day, {}))
            week_data.append({"Day": day, "Classes": slot_count})
        
        week_df = pd.DataFrame(week_data)
        st.dataframe(week_df, use_container_width=True, hide_index=True)