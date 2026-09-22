import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from nav_sidebar import render_sidebar
from theme import get_theme_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "logged_in": True,
    "dark_theme": False,
    "force_result": False,
    "force_course": False,
    "biometric_lock": False,
    "logout_checked": False,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# APPLY GLOBAL THEME
# ============================================================

st.html(get_theme_css())

st.html("""
<style>

/* Hide the complete left sidebar */
section[data-testid="stSidebar"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
}

/* Hide sidebar navigation */
[data-testid="stSidebarNav"] { 
    display: none !important; 
}

[data-testid="stSidebarNavItems"] { 
    display: none !important; 
}

/* Hide sidebar toggle button */
[data-testid="stSidebarCollapseButton"] { 
    display: none !important; 
}

button[kind="header"] { 
    display: none !important; 
}

/* Hide toolbar */
[data-testid="stToolbar"] { 
    display: none !important; 
}

</style>
""")


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar("settings")


# ============================================================
# SETTINGS CSS
# ============================================================

st.html(
    """
    <style>

    /* ======================================================
       PAGE HEADER
       ====================================================== */

    .settings-title {
        color: var(--hc-text);
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .settings-subtitle {
        color: var(--hc-text-soft);
        font-size: 14px;
        margin-bottom: 28px;
    }


    /* ======================================================
       SECTION
       ====================================================== */

    .settings-section {
        background: var(--hc-surface);
        border: 1px solid var(--hc-border);
        border-radius: var(--hc-radius-lg);
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--hc-shadow);
    }

    .settings-section-title {
        color: var(--hc-text);
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 5px;
    }


    /* ======================================================
       SETTINGS LABEL
       ====================================================== */

    .settings-label {
        color: var(--hc-text);
        font-size: 15px;
        font-weight: 700;
    }

    .settings-description {
        color: var(--hc-text-soft);
        font-size: 13px;
        margin-top: 5px;
    }


    /* ======================================================
       LOGOUT DIALOG
       ====================================================== */

    .logout-dialog {
        text-align: center;
        padding: 5px 5px 10px 5px;
    }

    .logout-icon {
        font-size: 50px;
        margin-bottom: 10px;
    }

    .logout-title {
        color: var(--hc-text);
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .logout-text {
        color: var(--hc-text-soft);
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 10px;
    }


    /* ======================================================
       CHECKBOX
       ====================================================== */

    [data-testid="stCheckbox"] label {
        color: var(--hc-text) !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid var(--hc-border);
        background: var(--hc-surface);
        color: var(--hc-text);
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: var(--hc-purple);
        color: var(--hc-purple);
    }

    </style>
    """
)


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="settings-title">
        ⚙️ Settings
    </div>

    <div class="settings-subtitle">
        Manage your preferences and account settings.
    </div>
    """
)


# ============================================================
# APPEARANCE
# ============================================================

st.html(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🎨 Appearance
        </div>

    </div>
    """
)


# ------------------------------------------------------------
# DARK THEME
# ------------------------------------------------------------

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Dark Theme
        </div>

        <div class="settings-description">
            Enable dark pastel mode for the entire application
        </div>
        """
    )

with col2:

    dark_theme = st.checkbox(
        "Dark Theme",
        value=st.session_state.dark_theme,
        key="dark_theme_checkbox",
        label_visibility="collapsed"
    )


# ------------------------------------------------------------
# APPLY DARK THEME
# ------------------------------------------------------------

if dark_theme != st.session_state.dark_theme:

    st.session_state.dark_theme = dark_theme

    st.rerun()


# ============================================================
# DATA & SYNC
# ============================================================

st.html(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            📊 Data & Sync
        </div>

    </div>
    """
)


# ------------------------------------------------------------
# FORCE RESULT
# ------------------------------------------------------------

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Force Result
        </div>

        <div class="settings-description">
            Show experimental features
        </div>
        """
    )

with col2:

    st.session_state.force_result = st.checkbox(
        "Force Result",
        value=st.session_state.force_result,
        key="force_result_checkbox",
        label_visibility="collapsed"
    )


# ------------------------------------------------------------
# FORCE COURSE
# ------------------------------------------------------------

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Force Course
        </div>

        <div class="settings-description">
            Override course restrictions
        </div>
        """
    )

with col2:

    st.session_state.force_course = st.checkbox(
        "Force Course",
        value=st.session_state.force_course,
        key="force_course_checkbox",
        label_visibility="collapsed"
    )


# ============================================================
# SECURITY
# ============================================================

st.html(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🔒 Security
        </div>

    </div>
    """
)


# ------------------------------------------------------------
# BIOMETRIC LOCK
# ------------------------------------------------------------

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Biometric Lock
        </div>

        <div class="settings-description">
            Enable fingerprint/face authentication
        </div>
        """
    )

with col2:

    st.session_state.biometric_lock = st.checkbox(
        "Biometric Lock",
        value=st.session_state.biometric_lock,
        key="biometric_checkbox",
        label_visibility="collapsed"
    )


# ============================================================
# ACCOUNT
# ============================================================

st.html(
    """
    <div class="settings-section">

        <div class="settings-section-title">
            🚪 Account
        </div>

    </div>
    """
)


# ============================================================
# LOGOUT DIALOG
# ============================================================

@st.dialog("⚠️ Logout Confirmation")
def logout_dialog():

    st.html(
        """
        <div class="logout-dialog">

            <div class="logout-icon">
                ⚠️
            </div>

            <div class="logout-title">
                Logout?
            </div>

            <div class="logout-text">
                Are you sure you want to logout from your account?
            </div>

        </div>
        """
    )

    st.write("")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # YES LOGOUT
    # --------------------------------------------------------

    with col1:

        if st.button(
            "✓ Yes, Logout",
            use_container_width=True,
            key="confirm_logout"
        ):

            st.session_state.logged_in = False
            st.session_state.logout_checked = False

            if "logout_checkbox" in st.session_state:
                st.session_state.logout_checkbox = False

            st.switch_page(
                "pages/login.py"
            )

    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    with col2:

        if st.button(
            "✕ Cancel",
            use_container_width=True,
            key="cancel_logout"
        ):

            st.session_state.logout_checked = False

            if "logout_checkbox" in st.session_state:
                st.session_state.logout_checkbox = False

            st.rerun()


# ============================================================
# SIGN OUT
# ============================================================

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Sign Out
        </div>

        <div class="settings-description">
            End your current session
        </div>
        """
    )

with col2:

    logout_checked = st.checkbox(
        "Logout",
        value=st.session_state.logout_checked,
        key="logout_checkbox",
        label_visibility="collapsed"
    )


# ============================================================
# OPEN LOGOUT POPUP
# ============================================================

if logout_checked:

    st.session_state.logout_checked = True

    logout_dialog()


# ============================================================
# BACK TO DASHBOARD
# ============================================================

st.write("")

if st.button(
    "← Back to Dashboard",
    key="back_settings_btn",
    use_container_width=False
):

    st.switch_page(
        "pages/dashboard.py"
    )