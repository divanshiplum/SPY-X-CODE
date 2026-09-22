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
# APPLY THEME
# ============================================================

st.html(get_theme_css())


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar("settings")


# ============================================================
# CUSTOM CSS
# ============================================================

st.html(
    """
    <style>

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
        margin-bottom: 20px;
    }

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

    .logout-box {
        background: var(--hc-surface);
        border: 1px solid var(--hc-border);
        border-radius: var(--hc-radius-lg);
        padding: 25px;
        margin-top: 15px;
        text-align: center;
    }

    .logout-icon {
        font-size: 40px;
    }

    .logout-title {
        color: var(--hc-text);
        font-size: 21px;
        font-weight: 800;
        margin-top: 8px;
    }

    .logout-text {
        color: var(--hc-text-soft);
        font-size: 14px;
        margin-top: 6px;
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

col1, col2 = st.columns([0.82, 0.18])

with col1:

    st.html(
        """
        <div class="settings-label">
            Dark Theme
        </div>

        <div class="settings-description">
            Enable dark mode for the dashboard
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

# Automatically apply dark theme
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


# ------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------

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
        value=False,
        key="logout_checkbox",
        label_visibility="collapsed"
    )


# ============================================================
# LOGOUT CONFIRMATION
# ============================================================

if logout_checked:

    st.html(
        """
        <div class="logout-box">

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

    col1, col2 = st.columns(2)

    with col1:

        confirm_logout = st.checkbox(
            "✓ Yes, Logout",
            key="confirm_logout_checkbox"
        )

    with col2:

        cancel_logout = st.checkbox(
            "✕ Cancel",
            key="cancel_logout_checkbox"
        )

    # --------------------------------------------------------
    # CONFIRM LOGOUT
    # --------------------------------------------------------

    if confirm_logout:

        st.session_state.logged_in = False
        st.session_state.logout_checkbox = False

        if "confirm_logout_checkbox" in st.session_state:
            st.session_state.confirm_logout_checkbox = False

        st.switch_page(
            "pages/login.py"
        )

    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    if cancel_logout:

        st.session_state.logout_checkbox = False

        if "cancel_logout_checkbox" in st.session_state:
            st.session_state.cancel_logout_checkbox = False

        st.rerun()


# ============================================================
# BACK TO DASHBOARD
# ============================================================

st.markdown("")

if st.button(
    "← Back to Dashboard",
    key="back_settings_btn"
):

    st.switch_page(
        "pages/dashboard.py"
    )