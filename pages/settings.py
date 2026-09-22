import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from nav_sidebar import render_sidebar
from theme import get_theme_css


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide",
)


# ============================================================
# AUTH CHECK
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.switch_page("pages/login.py")


# ============================================================
# SESSION STATE
# ============================================================
toggle_defaults = {
    "dark_theme": False,
    "force_result": False,
    "force_course": False,
    "biometric_lock": False,
    "show_logout_modal": False,
}

for key, default_value in toggle_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


# ============================================================
# APPLY CURRENT THEME
# ============================================================
st.markdown(
    get_theme_css(),
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================
render_sidebar("settings")


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>

    /* ========================================================
       SETTINGS SECTIONS
       ======================================================== */

    .settings-section {
        background: var(--hc-surface);

        border: 1px solid var(--hc-border);

        border-radius: var(--hc-radius-lg);

        padding: 22px;

        margin-bottom: 18px;

        box-shadow: var(--hc-shadow);

        transition:
            background-color 0.3s ease,
            border-color 0.3s ease;
    }


    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .settings-section-title {
        font-size: 16px;

        font-weight: 800;

        color: var(--hc-text);

        margin-bottom: 14px;

        display: flex;

        align-items: center;

        gap: 8px;
    }


    /* ========================================================
       SETTINGS LABEL
       ======================================================== */

    .settings-label {
        font-size: 14px;

        font-weight: 600;

        color: var(--hc-text);
    }


    /* ========================================================
       SETTINGS DESCRIPTION
       ======================================================== */

    .settings-description {
        font-size: 12px;

        color: var(--hc-text-soft);

        margin-top: 4px;
    }


    /* ========================================================
       LOGOUT MODAL OVERLAY
       ======================================================== */

    .logout-modal-overlay {
        position: fixed;

        top: 0;
        left: 0;

        width: 100%;
        height: 100%;

        background: rgba(31, 33, 48, 0.65);

        display: flex;

        align-items: center;

        justify-content: center;

        z-index: 9999;
    }


    /* ========================================================
       LOGOUT MODAL BOX
       ======================================================== */

    .logout-modal-box {
        background: var(--hc-surface);

        border-radius: var(--hc-radius-lg);

        border: 1px solid var(--hc-border);

        box-shadow:
            0 15px 50px rgba(0, 0, 0, 0.25);

        padding: 40px;

        max-width: 420px;

        text-align: center;

        animation: slideIn 0.3s ease-out;

        position: relative;

        color: var(--hc-text);
    }


    /* ========================================================
       MODAL ICON
       ======================================================== */

    .logout-modal-icon {
        font-size: 70px;

        margin-bottom: 20px;
    }


    /* ========================================================
       MODAL TITLE
       ======================================================== */

    .logout-modal-title {
        font-size: 26px;

        font-weight: 800;

        color: var(--hc-text);

        margin-bottom: 12px;
    }


    /* ========================================================
       MODAL MESSAGE
       ======================================================== */

    .logout-modal-message {
        font-size: 15px;

        color: var(--hc-text-soft);

        margin-bottom: 32px;

        line-height: 1.6;
    }


    /* ========================================================
       MODAL ANIMATION
       ======================================================== */

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


    /* ========================================================
       CONFIRM LOGOUT BUTTON
       ======================================================== */

    div[class*="st-key-confirm_logout"] {
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


    /* ========================================================
       CANCEL BUTTON
       ======================================================== */

    div[class*="st-key-cancel_logout"] {
        position: relative !important;

        z-index: 10000 !important;
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


    /* ========================================================
       BACK BUTTON
       ======================================================== */

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


    /* ========================================================
       LOGOUT BUTTON
       ======================================================== */

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


    /* ========================================================
       CHECKBOX
       ======================================================== */

    [data-testid="stCheckbox"] label {

        color: var(--hc-text) !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: var(--hc-border) !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================
st.markdown("## ⚙️ Settings")

st.markdown("---")


# ============================================================
# APPEARANCE SECTION
# ============================================================
st.markdown(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🎨 Appearance
        </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DARK THEME - ONLY ONE TOGGLE
# ============================================================
col1, col2 = st.columns([0.8, 0.2])


with col1:

    st.markdown(
        """
        <div class="settings-label">
            Dark Theme
        </div>

        <div class="settings-description">
            Enable dark mode for the dashboard
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    dark_theme = st.checkbox(
        "Dark Theme",
        value=st.session_state.dark_theme,
        label_visibility="collapsed",
        key="dark_theme_toggle"
    )

    # --------------------------------------------------------
    # Detect change and reload theme
    # --------------------------------------------------------

    if dark_theme != st.session_state.dark_theme:

        st.session_state.dark_theme = dark_theme

        st.rerun()


st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DATA & SYNC SECTION
# ============================================================
st.markdown(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            📊 Data & Sync
        </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FORCE RESULT
# ============================================================
col1, col2 = st.columns([0.8, 0.2])


with col1:

    st.markdown(
        """
        <div class="settings-label">
            Force Result
        </div>

        <div class="settings-description">
            Show experimental features
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.session_state.force_result = st.checkbox(
        "Force Result",
        value=st.session_state.force_result,
        label_visibility="collapsed",
        key="force_result_toggle"
    )


# ============================================================
# FORCE COURSE
# ============================================================
col1, col2 = st.columns([0.8, 0.2])


with col1:

    st.markdown(
        """
        <div class="settings-label">
            Force Course
        </div>

        <div class="settings-description">
            Override course restrictions
        </div>
        """,
        unsafe_allow_html=True
    )


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
st.markdown(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🔒 Security
        </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BIOMETRIC LOCK
# ============================================================
col1, col2 = st.columns([0.8, 0.2])


with col1:

    st.markdown(
        """
        <div class="settings-label">
            Biometric Lock
        </div>

        <div class="settings-description">
            Enable fingerprint/face authentication
        </div>
        """,
        unsafe_allow_html=True
    )


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
st.markdown(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🚪 Logout
        </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns([0.8, 0.2])


with col1:

    st.markdown(
        """
        <div class="settings-label">
            Sign Out
        </div>

        <div class="settings-description">
            End your current session
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    if st.button(
        "Logout",
        key="logout_btn",
        use_container_width=True
    ):

        st.session_state.show_logout_modal = True

        st.rerun()


st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# BACK TO DASHBOARD
# ============================================================
st.markdown("---")


if st.button(
    "← Back to Dashboard",
    key="back_settings_btn",
    use_container_width=False
):

    st.switch_page("pages/dashboard.py")


# ============================================================
# LOGOUT CONFIRMATION MODAL
# ============================================================
if st.session_state.show_logout_modal:

    # --------------------------------------------------------
    # MODAL
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="logout-modal-overlay">

            <div class="logout-modal-box">

                <div class="logout-modal-icon">
                    ⚠️
                </div>

                <div class="logout-modal-title">
                    Logout?
                </div>

                <div class="logout-modal-message">
                    Are you sure you want to logout from your account?
                </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MODAL BUTTONS
    # --------------------------------------------------------

    button_col1, button_col2 = st.columns(
        2,
        gap="small"
    )


    # ========================================================
    # YES, LOGOUT
    # ========================================================
    with button_col1:

        if st.button(
            "✓ Yes, Logout",
            key="confirm_logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.roll_no = None

            st.session_state.show_logout_modal = False

            st.switch_page("pages/login.py")


    # ========================================================
    # CANCEL
    # ========================================================
    with button_col2:

        if st.button(
            "✕ Cancel",
            key="cancel_logout",
            use_container_width=True
        ):

            st.session_state.show_logout_modal = False

            st.rerun()


    # --------------------------------------------------------
    # CLOSE MODAL
    # --------------------------------------------------------

    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )