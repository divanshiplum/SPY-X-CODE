import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from nav_sidebar import render_sidebar

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide",
)

# ============================================================
# SIDEBAR (injects theme CSS)
# ============================================================
render_sidebar("settings")

# ============================================================
# SESSION STATE - Modal control
# ============================================================
if "show_logout_modal" not in st.session_state:
    st.session_state.show_logout_modal = False

# ============================================================
# CSS STYLING
# ============================================================
st.markdown("""
<style>

/* Modal Overlay */
.logout-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(31, 33, 48, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

/* Modal Box */
.logout-modal-box {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    border: 1px solid var(--hc-border);
    box-shadow: 0 15px 50px rgba(80, 70, 160, 0.25);
    padding: 40px;
    max-width: 420px;
    text-align: center;
    animation: slideIn 0.3s ease-out;
    position: relative;
}

.logout-modal-icon {
    font-size: 70px;
    margin-bottom: 20px;
}

.logout-modal-title {
    font-size: 26px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 12px;
}

.logout-modal-message {
    font-size: 15px;
    color: var(--hc-text-soft);
    margin-bottom: 32px;
    line-height: 1.6;
}

.modal-buttons-wrapper {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 20px;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Position buttons inside modal */
div[class*="st-key-confirm_logout"],
div[class*="st-key-cancel_logout"] {
    position: relative !important;
    z-index: 10000 !important;
}

div[class*="st-key-confirm_logout"] .stButton > button {
    background: var(--hc-green) !important;
    color: white !important;
    border: none !important;
    padding: 11px 20px !important;
    border-radius: var(--hc-radius-md) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

div[class*="st-key-confirm_logout"] .stButton > button:hover {
    background: #1ba871 !important;
    transform: scale(1.02) !important;
}

div[class*="st-key-cancel_logout"] .stButton > button {
    background: var(--hc-purple-soft) !important;
    color: var(--hc-purple-text) !important;
    border: 1px solid var(--hc-border) !important;
    padding: 11px 20px !important;
    border-radius: var(--hc-radius-md) !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

div[class*="st-key-cancel_logout"] .stButton > button:hover {
    background: var(--hc-purple-hover) !important;
}

/* Settings Sections */
.settings-section {
    background: var(--hc-surface);
    border: 1px solid var(--hc-border);
    border-radius: var(--hc-radius-lg);
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: var(--hc-shadow);
}

.settings-section-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.settings-label {
    font-size: 14px;
    font-weight: 600;
    color: var(--hc-text);
}

.settings-description {
    font-size: 12px;
    color: var(--hc-text-soft);
}

/* Back Button */
div[class*="st-key-back_settings_btn"] .stButton > button {
    background: var(--hc-purple-soft) !important;
    color: var(--hc-purple-text) !important;
    border: 1px solid var(--hc-border) !important;
    padding: 10px 20px !important;
    border-radius: var(--hc-radius-md) !important;
    font-weight: 600 !important;
}

div[class*="st-key-back_settings_btn"] .stButton > button:hover {
    background: var(--hc-purple-hover) !important;
}

/* Logout Button */
div[class*="st-key-logout_btn"] .stButton > button {
    background: var(--hc-red) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: var(--hc-radius-md) !important;
    font-weight: 600 !important;
    width: 100% !important;
}

div[class*="st-key-logout_btn"] .stButton > button:hover {
    background: #ff3d50 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("## ⚙️ Settings")
st.markdown("---")

# ============================================================
# SESSION STATE - Toggles
# ============================================================
toggle_defaults = {
    "dark_theme": False,
    "force_result": False,
    "force_course": False,
    "biometric_lock": False,
}

for key, default_value in toggle_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# ============================================================
# APPEARANCE SECTION
# ============================================================
st.markdown("""
<div class="settings-section">
    <div class="settings-section-title">🎨 Appearance</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div class="settings-label">Dark Theme</div>
    <div class="settings-description">Enable dark mode for the dashboard</div>
    """, unsafe_allow_html=True)
with col2:
    st.session_state.dark_theme = st.checkbox(
        "Dark Theme",
        value=st.session_state.dark_theme,
        label_visibility="collapsed",
        key="dark_theme_toggle"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# DATA & SYNC SECTION
# ============================================================
st.markdown("""
<div class="settings-section">
    <div class="settings-section-title">📊 Data & Sync</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div class="settings-label">Force Result</div>
    <div class="settings-description">Show experimental features</div>
    """, unsafe_allow_html=True)
with col2:
    st.session_state.force_result = st.checkbox(
        "Force Result",
        value=st.session_state.force_result,
        label_visibility="collapsed",
        key="force_result_toggle"
    )

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div class="settings-label">Force Course</div>
    <div class="settings-description">Override course restrictions</div>
    """, unsafe_allow_html=True)
with col2:
    st.session_state.force_course = st.checkbox(
        "Force Course",
        value=st.session_state.force_course,
        label_visibility="collapsed",
        key="force_course_toggle"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SECURITY SECTION
# ============================================================
st.markdown("""
<div class="settings-section">
    <div class="settings-section-title">🔒 Security</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div class="settings-label">Biometric Lock</div>
    <div class="settings-description">Enable fingerprint/face authentication</div>
    """, unsafe_allow_html=True)
with col2:
    st.session_state.biometric_lock = st.checkbox(
        "Biometric Lock",
        value=st.session_state.biometric_lock,
        label_visibility="collapsed",
        key="biometric_toggle"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# LOGOUT SECTION
# ============================================================
st.markdown("""
<div class="settings-section">
    <div class="settings-section-title">🚪 Logout</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown("""
    <div class="settings-label">Sign Out</div>
    <div class="settings-description">End your current session</div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("Logout", key="logout_btn", use_container_width=True):
        st.session_state.show_logout_modal = True
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# BACK BUTTON
# ============================================================
st.markdown("---")
if st.button("← Back to Dashboard", key="back_settings_btn", use_container_width=False):
    st.switch_page("pages/dashboard.py")

# ============================================================
# LOGOUT CONFIRMATION MODAL - WITH BUTTONS INSIDE
# ============================================================
if st.session_state.show_logout_modal:
    # Render modal overlay and box
    st.markdown("""
    <div class="logout-modal-overlay">
        <div class="logout-modal-box">
            <div class="logout-modal-icon">⚠️</div>
            <div class="logout-modal-title">Logout?</div>
            <div class="logout-modal-message">
                Are you sure you want to logout from your account?
            </div>
    """, unsafe_allow_html=True)
    
    # Render buttons inside modal
    button_col1, button_col2 = st.columns(2, gap="small")
    
    with button_col1:
        if st.button("✓ Yes, Logout", key="confirm_logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.roll_no = None
            st.session_state.show_logout_modal = False
            st.switch_page("pages/login.py")
    
    with button_col2:
        if st.button("✕ Cancel", key="cancel_logout", use_container_width=True):
            st.session_state.show_logout_modal = False
            st.rerun()
    
    # Close modal box and overlay
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)