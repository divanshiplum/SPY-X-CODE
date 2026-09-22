import streamlit as st
import pandas as pd
from datetime import date
import os
import json
from pathlib import Path
import base64

st.set_page_config(
    page_title="Add Notices", 
    page_icon="📣", 
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
    
    .stSelectbox select, .stTextInput input, .stNumberInput input, .stDateInput input, .stTextArea textarea {
        background: #3d3d52 !important;
        border: 2px solid #6b6b80 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stTextArea label {
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
    
    .notice-card {
        background: linear-gradient(135deg, #4a4a5e 0%, #3d3d52 100%);
        border: 2px solid #6b6b80;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .notice-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .notice-content {
        color: #b4a7c6;
        font-size: 14px;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    
    .notice-meta {
        color: #9B8BA8;
        font-size: 12px;
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

st.markdown("<div class='header-title'>📣 Add & Manage Notices</div>", unsafe_allow_html=True)

# ==================== INITIALIZE DATA ====================
NOTICES_FILE = "data/notices.json"

os.makedirs("data", exist_ok=True)

def load_notices():
    """Load all notices from JSON"""
    if os.path.exists(NOTICES_FILE):
        try:
            with open(NOTICES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_notices(notices):
    """Save notices to JSON"""
    try:
        with open(NOTICES_FILE, 'w') as f:
            json.dump(notices, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving notices: {str(e)}")
        return False

def get_attachment_count(attachments):
    """Safely get attachment count - handles both old and new formats"""
    if isinstance(attachments, list):
        return len(attachments)
    elif isinstance(attachments, int):
        return attachments
    else:
        return 0

# ==================== CONFIGURATION ====================
NOTICE_CATEGORIES = ["Academic", "Announcement", "Event", "Holiday", "Urgent", "General"]

# ==================== TABS ====================
tab1, tab2 = st.tabs(["Add Notice", "View All Notices"])

# ==================== TAB 1: ADD NOTICE ====================
with tab1:
    st.markdown("<div class='section-header'>📝 Create New Notice</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        notice_title = st.text_input("Notice Title", placeholder="Enter notice title", key="notice_title")
    
    with col2:
        category = st.selectbox("Category", NOTICE_CATEGORIES, key="category")
    
    notice_content = st.text_area("Notice Content", placeholder="Enter detailed notice content", height=150, key="notice_content")
    
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    
    with col1:
        notice_date = st.date_input("Date", value=date.today(), key="notice_date")
    
    with col2:
        st.write("")
        st.write("")
        is_pinned = st.checkbox("Pin to Top", value=False, key="is_pinned")
    
    with col3:
        st.write("")
        st.write("")
        is_urgent = st.checkbox("Mark as Urgent", value=False, key="is_urgent")
    
    st.markdown("<div class='section-header'>📎 Attachments</div>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload attachments (PDF, Images, Documents, etc.)",
        accept_multiple_files=True,
        key="attachments"
    )
    
    if uploaded_files:
        st.info(f"✅ {len(uploaded_files)} file(s) ready to upload: {', '.join([f.name for f in uploaded_files])}")
    
    if st.button("📤 Publish Notice", use_container_width=True, key="publish_btn"):
        if notice_title and notice_content:
            notices = load_notices()
            
            # Convert uploaded files to base64
            attachments_data = []
            try:
                for uploaded_file in uploaded_files:
                    file_bytes = uploaded_file.getbuffer()
                    file_base64 = base64.b64encode(file_bytes).decode('utf-8')
                    
                    attachments_data.append({
                        "filename": uploaded_file.name,
                        "file_type": uploaded_file.type,
                        "data": file_base64
                    })
            except Exception as e:
                st.error(f"Error processing files: {str(e)}")
                attachments_data = []
            
            # Create new notice record
            new_notice = {
                "id": len(notices) + 1,
                "title": notice_title,
                "content": notice_content,
                "category": category,
                "date": str(notice_date),
                "author": st.session_state.get("teacher_name", "Anonymous"),
                "pinned": is_pinned,
                "urgent": is_urgent,
                "attachments": attachments_data if attachments_data else []
            }
            
            notices.insert(0, new_notice)
            
            # Save notices
            if save_notices(notices):
                # Success message
                if attachments_data:
                    st.success(f"✅ Notice published successfully with {len(attachments_data)} attachment(s)!")
                else:
                    st.success("✅ Notice published successfully!")
                
                # Clear form
                st.session_state.pop("notice_title", None)
                st.session_state.pop("notice_content", None)
                st.session_state.pop("category", None)
                st.session_state.pop("notice_date", None)
                st.session_state.pop("is_pinned", None)
                st.session_state.pop("is_urgent", None)
                st.session_state.pop("attachments", None)
                st.rerun()
        else:
            st.error("❌ Please fill in title and content")

# ==================== TAB 2: VIEW NOTICES ====================
with tab2:
    st.markdown("<div class='section-header'>📊 All Notices</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + NOTICE_CATEGORIES, key="filter_category")
    
    with col2:
        filter_urgent = st.checkbox("Show Urgent Only", value=False, key="filter_urgent")
    
    notices = load_notices()
    
    if not notices:
        st.info("📭 No notices published yet.")
    else:
        for notice in notices:
            if filter_category != "All" and notice.get("category") != filter_category:
                continue
            
            if filter_urgent and not notice.get("urgent", False):
                continue
            
            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
            
            with col1:
                # Get attachment count safely
                attachments = notice.get('attachments', [])
                attachment_count = get_attachment_count(attachments)
                attachment_info = f" | Attachments: {attachment_count}" if attachment_count > 0 else ""
                
                st.markdown(f"""
                <div class='notice-card'>
                    <div class='notice-title'>
                        {'🚨 ' if notice.get('urgent') else ''}{'📌 ' if notice.get('pinned') else ''}{notice['title']}
                    </div>
                    <div class='notice-content'>{notice['content']}</div>
                    <div class='notice-meta'>
                        Category: {notice['category']} | Date: {notice['date']} | By: {notice['author']}{attachment_info}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display attachment list
                if attachment_count > 0 and isinstance(attachments, list):
                    st.caption("📎 Attached Files:")
                    for attachment in attachments:
                        if isinstance(attachment, dict):
                            st.caption(f"  ✅ {attachment.get('filename', 'Unknown')}")
            
            with col2:
                if st.button("✏️", key=f"edit_{notice['id']}", help="Edit"):
                    st.info("✅ Edit functionality coming soon")
            
            with col3:
                if st.button("🗑️", key=f"delete_{notice['id']}", help="Delete"):
                    # Remove notice from JSON
                    notices = [n for n in notices if n['id'] != notice['id']]
                    if save_notices(notices):
                        st.success("✅ Notice deleted")
                        st.rerun()

# ==================== STATISTICS ====================
st.markdown("---")
st.markdown("<div class='section-header'>📈 Statistics</div>", unsafe_allow_html=True)

notices = load_notices()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Notices", len(notices))

with col2:
    pinned = len([n for n in notices if n.get('pinned', False)])
    st.metric("Pinned Notices", pinned)

with col3:
    urgent = len([n for n in notices if n.get('urgent', False)])
    st.metric("Urgent Notices", urgent)

with col4:
    if notices:
        academic = len([n for n in notices if n.get('category') == 'Academic'])
        st.metric("Academic Notices", academic)
