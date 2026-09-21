import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
toggle_defaults = {
    "dark_theme": False,
    "force_result": False,
    "force_course": False,
    "biometric_lock": False,
}

for key, value in toggle_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# HC NEXUS PASTEL THEME CSS
# --------------------------------------------------
st.markdown("""
<style>

:root {
    --hc-bg: #f4f2fb;
    --hc-surface: #ffffff;
    --hc-border: #ececf5;
    --hc-shadow: 0 2px 14px rgba(80, 70, 160, 0.06);

    --hc-purple: #7c6ff0;
    --hc-purple-soft: #eeecfd;
    --hc-purple-text: #6a5cd6;
    --hc-purple-hover: #ddd8fb;

    --hc-text: #1f2130;
    --hc-text-soft: #8b8a9a;
    --hc-text-faint: #b3b2c0;

    --hc-red: #ff5b6e;
    --hc-red-soft: #ffe7ea;
    --hc-green: #2ec793;
    --hc-green-soft: #e2f9f0;
    --hc-green-hover: #c8f3e3;
    --hc-blue: #4f8ef7;
    --hc-blue-soft: #e6f0fe;
    --hc-blue-hover: #d0e4fd;
    --hc-orange: #ff9f43;
    --hc-orange-soft: #fff1e2;
    --hc-orange-hover: #ffe0c2;
    --hc-yellow: #f6c445;
    --hc-yellow-soft: #fef6e0;
    --hc-yellow-hover: #fbe9b8;
    --hc-teal: #2bb3a3;
    --hc-teal-soft: #e2f7f4;
    --hc-teal-hover: #c8efe9;

    --hc-radius-lg: 20px;
    --hc-radius-md: 14px;
    --hc-radius-sm: 10px;
}

.stApp {
    background: var(--hc-bg);
}

html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* Main container */
.block-container {
    max-width: 1000px;
    padding-top: 20px;
}

/* Header styling with columns */
.stColumns > div:first-child {
    background-color: var(--hc-purple-soft);
    border-radius: var(--hc-radius-md);
    border: 1px solid var(--hc-border);
}

.header-title {
    font-size: 36px;
    font-weight: 600;
    color: var(--hc-text);
    flex: 1;
    text-align: center;
}

.header-icon {
    font-size: 38px;
    cursor: pointer;
    color: var(--hc-text);
}

.header-icon:hover {
    opacity: 0.7;
    transition: 0.2s;
}

/* Section title */
.section-title {
    color: var(--hc-text-soft);
    font-size: 22px;
    margin: 28px 0 10px 20px;
    font-weight: 600;
}

/* Settings box */
.settings-box {
    background-color: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    padding: 0;
    margin-bottom: 20px;
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    overflow: hidden;
}

/* Setting row */
.setting-row {
    min-height: 75px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 25px;
    border-bottom: 1px solid var(--hc-border);
}

.setting-row:last-child {
    border-bottom: none;
}

.setting-content {
    display: flex;
    align-items: center;
    gap: 18px;
    flex: 1;
}

.icon-box {
    width: 55px;
    height: 55px;
    background-color: var(--hc-purple-soft);
    border-radius: var(--hc-radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    flex-shrink: 0;
}

.setting-name {
    font-size: 19px;
    color: var(--hc-text);
    font-weight: 500;
}

.setting-toggle-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    min-width: 60px;
}

.description {
    color: var(--hc-text-soft);
    font-size: 19px;
    margin: 5px 0 25px 20px;
}

/* Streamlit buttons */
div.stButton > button {
    border-radius: var(--hc-radius-md);
    border: 1px solid var(--hc-border);
    background-color: var(--hc-surface);
    color: var(--hc-text);
    font-size: 18px;
    padding: 12px 20px;
    width: 100%;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: var(--hc-purple-soft);
    border: 1px solid var(--hc-border);
}

/* Back button styling */
[data-testid="baseButton-secondary"] {
    background-color: var(--hc-purple-soft) !important;
    color: var(--hc-text) !important;
    border: 1px solid var(--hc-border) !important;
    border-radius: var(--hc-radius-md) !important;
    font-size: 24px !important;
    padding: 12px 16px !important;
}

[data-testid="baseButton-secondary"]:hover {
    background-color: var(--hc-purple-hover) !important;
}

/* Toggle styling - DARK THEME */
.stToggle {
    margin: 0 !important;
}

/* Make toggle MUCH darker and visible */
[data-testid="baseButton-secondary"] > svg {
    fill: #5a4a8f !important;
}

/* Toggle track (background) - make it very dark */
div[role="switch"] {
    background-color: #4a3f6b !important;
    border: 1px solid #3a2f5b !important;
}

/* Toggle thumb when OFF - darker color */
div[role="switch"]::before {
    background-color: #3a2f5b !important;
}

/* Toggle when ON - purple */
div[role="switch"][aria-checked="true"] {
    background-color: #6a5cd6 !important;
    border: 1px solid #5a4cd6 !important;
}

/* Toggle thumb when ON */
div[role="switch"][aria-checked="true"]::before {
    background-color: #ffffff !important;
}

/* Extra dark styling for all toggle elements */
.stToggle [role="switch"],
[data-baseweb="toggle"] {
    background-color: #4a3f6b !important !important;
}

.stToggle [role="switch"][aria-checked="true"],
[data-baseweb="toggle"][aria-checked="true"] {
    background-color: #6a5cd6 !important !important;
}

/* Ensure max contrast and visibility */
.streamlit-expanderContent .stToggle [role="switch"],
.stToggle > * [role="switch"] {
    background-color: #3d3257 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25) !important;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER WITH BACK NAVIGATION
# --------------------------------------------------
col1, col2, col3 = st.columns([0.8, 10, 0.8])

with col1:
    if st.button("‹", key="back_button", help="Go back to Dashboard"):
        st.switch_page("pages/dashboard.py")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="font-size: 36px; font-weight: 600; color: var(--hc-text);">Settings</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; font-size: 36px;">⚙️</div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# TOGGLE FUNCTION WITH PROPER LAYOUT
# --------------------------------------------------
def setting_toggle(icon, title, key):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 18px; padding: 15px 0;">
                <div style="width: 55px; height: 55px; background-color: var(--hc-purple-soft); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 27px; flex-shrink: 0;">
                    {icon}
                </div>
                <div style="font-size: 19px; color: var(--hc-text); font-weight: 500;">
                    {title}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.toggle("", key=key, label_visibility="collapsed")


# --------------------------------------------------
# APPEARANCE
# --------------------------------------------------
st.markdown('<div class="section-title">Appearance</div>', unsafe_allow_html=True)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

setting_toggle("🌙", "Dark Theme", "dark_theme")
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# DATA & SYNC
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Data & Sync</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

setting_toggle("🔄", "Force Result Refresh", "force_result")
setting_toggle("📄", "Force Course Plan Refresh", "force_course")

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# SECURITY
# --------------------------------------------------
st.markdown(
    '<div class="section-title">Security</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="settings-box">', unsafe_allow_html=True)

# Biometric Lock
setting_toggle("🔒", "Biometric Lock", "biometric_lock")

# Logout
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 18px; padding: 15px 0;">
            <div style="width: 55px; height: 55px; background-color: var(--hc-red-soft); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 27px; flex-shrink: 0;">
                ↪
            </div>
            <div style="font-size: 19px; color: var(--hc-red); font-weight: 500;">
                Logout
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("›", key="logout_button"):
        st.warning("You have been logged out.")


# Delete Account
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 18px; padding: 15px 0;">
            <div style="width: 55px; height: 55px; background-color: var(--hc-red-soft); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 27px; flex-shrink: 0;">
                🗑️
            </div>
            <div style="font-size: 19px; color: var(--hc-red); font-weight: 500;">
                Delete Account
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("›", key="delete_button"):
        st.error("Delete Account option selected.")

st.markdown('</div>', unsafe_allow_html=True)