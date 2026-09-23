import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import os

from theme import THEME_CSS
from theme import get_theme_css


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HC NEXUS",
    page_icon="🎓",
    layout="centered",
)


# ============================================================
# THEME
# ============================================================

st.html(get_theme_css())


def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


st.markdown(THEME_CSS, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "roll_no" not in st.session_state:
    st.session_state.roll_no = None

if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"


# ============================================================
# REDIRECT TO DASHBOARD IF ALREADY LOGGED IN
# ============================================================

if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")


# ============================================================
# CSS
# ============================================================

render("""
<style>

/* ============================================================
   HIDE STREAMLIT MULTIPAGE NAVIGATION
   ============================================================ */

/* Hide the complete left sidebar */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Hide collapsed sidebar control */
div[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

/* Hide sidebar/menu toggle button */
button[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}


/* ============================================================
   LOGIN PAGE BACKGROUND
   ============================================================ */

.stApp {
    background: #f6f4fc;
    overflow: hidden;
}


/* ============================================================
   PASTEL BLOBS
   ============================================================ */

.hc-blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(2px);
    z-index: 0;
    opacity: 0.55;
}

.hc-blob-1 {
    top: -120px;
    left: -120px;
    width: 340px;
    height: 340px;
    background: #d8cef8;
}

.hc-blob-2 {
    top: 40px;
    right: -100px;
    width: 260px;
    height: 260px;
    background: #cfe6fb;
}

.hc-blob-3 {
    bottom: -140px;
    left: 10%;
    width: 300px;
    height: 300px;
    background: #fbdce6;
}

.hc-blob-4 {
    bottom: -80px;
    right: -80px;
    width: 280px;
    height: 280px;
    background: #cfe6fb;
}


/* ============================================================
   MAIN CONTENT
   ============================================================ */

.block-container {
    max-width: 900px;
    padding-top: 60px;
    position: relative;
    z-index: 1;
}


/* ============================================================
   LOGIN CARD
   ============================================================ */

div.stVerticalBlock[class*="st-key-hc_login_card"] {
    max-width: 380px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: var(--hc-radius-lg);
    box-shadow: 0 10px 40px rgba(120, 100, 200, 0.12);
    padding: 34px 34px 26px 34px;
    position: relative;
    z-index: 2;
}


/* ============================================================
   LOGIN LOGO
   ============================================================ */

.hc-login-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 20px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 4px;
}


/* ============================================================
   LOGIN TAG
   ============================================================ */

.hc-login-tag {
    text-align: center;
    color: var(--hc-purple-text);
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 1.5px;
    margin-bottom: 22px;
}


/* ============================================================
   TEXT INPUTS
   ============================================================ */

div[data-testid="stTextInput"] input {
    background: var(--hc-bg) !important;
    border: 1px solid var(--hc-border) !important;
    border-radius: var(--hc-radius-md) !important;
    color: var(--hc-text) !important;
    padding: 10px 14px !important;
}

div[data-testid="stTextInput"] label {
    display: none;
}


/* ============================================================
   BUTTON CONTAINER
   ============================================================ */

div[data-testid="stElementContainer"]:has(> div.stButton) {
    width: 100% !important;
}

.stButton {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}


/* ============================================================
   MAIN BUTTON
   ============================================================ */

.stButton > button {
    width: 100%;
    background: var(--hc-purple);
    color: #ffffff;
    border: none;
    border-radius: var(--hc-radius-md);
    font-weight: 700;
    padding: 12px 0;
    margin-top: 6px;
}

.stButton > button:hover {
    background: var(--hc-purple-text);
}


/* ============================================================
   FOOTER TEXT
   ============================================================ */

.hc-login-footer {
    text-align: center;
    color: var(--hc-text-soft);
    font-size: 13px;
    margin: 14px 0 10px 0;
}


/* ============================================================
   REGISTER BUTTON
   ============================================================ */

div[class*="st-key-login_register_btn"] .stButton > button {
    background: transparent;
    color: var(--hc-purple-text);
    border: 1px solid var(--hc-purple);
}

div[class*="st-key-login_register_btn"] .stButton > button:hover {
    background: var(--hc-purple-soft);
}


/* ============================================================
   BACK HOME BUTTON
   ============================================================ */

div[class*="st-key-back_home_btn"] .stButton > button {
    background: transparent;
    color: var(--hc-text-soft);
    border: 1px solid var(--hc-border);
    margin-top: 20px;
}

div[class*="st-key-back_home_btn"] .stButton > button:hover {
    background: var(--hc-bg);
    border-color: var(--hc-text-soft);
}


/* ============================================================
   ILLUSTRATION
   ============================================================ */

.hc-illustration {
    position: fixed;
    bottom: 40px;
    right: 60px;
    font-size: 70px;
    z-index: 1;
    opacity: 0.9;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .hc-illustration {
        display: none;
    }

}

</style>


<!-- ============================================================
     BACKGROUND BLOBS
     ============================================================ -->

<div class="hc-blob hc-blob-1"></div>
<div class="hc-blob hc-blob-2"></div>
<div class="hc-blob hc-blob-3"></div>
<div class="hc-blob hc-blob-4"></div>

""")


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FILE = DATA_DIR / "students.csv"

if not FILE.exists():

    pd.DataFrame(
        columns=["Roll No", "Password"]
    ).to_csv(
        FILE,
        index=False
    )


# ============================================================
# LOGIN VIEW
# ============================================================

if st.session_state.auth_view == "login":

    with st.container(key="hc_login_card"):

        # --------------------------------------------------------
        # LOGO
        # --------------------------------------------------------

        render(
            '<div class="hc-login-logo">🎓 HC NEXUS</div>'
        )

        render(
            '<div class="hc-login-tag">LOGIN</div>'
        )


        # --------------------------------------------------------
        # LOGIN INPUTS
        # --------------------------------------------------------

        roll_no = st.text_input(
            "Roll No",
            placeholder="Enter your Roll Number"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your Password"
        )


        # --------------------------------------------------------
        # LOGIN BUTTON
        # --------------------------------------------------------

        if st.button("LOGIN", key="login_btn"):

            students = pd.read_csv(FILE)

            user = students[
                (students["Roll No"].astype(str) == roll_no)
                &
                (students["Password"].astype(str) == password)
            ]


            if not user.empty:

                # Set session state
                st.session_state.logged_in = True
                st.session_state.roll_no = roll_no
                st.session_state.auth_view = "login"

                st.rerun()

            else:

                st.error(
                    "Account not found or incorrect Roll No/Password."
                )


        # --------------------------------------------------------
        # REGISTER TEXT
        # --------------------------------------------------------

        render(
            '<div class="hc-login-footer">'
            "Don't have an account?"
            "</div>"
        )


        # --------------------------------------------------------
        # REGISTER BUTTON
        # --------------------------------------------------------

        if st.button(
            "REGISTER HERE",
            key="login_register_btn"
        ):

            st.session_state.auth_view = "register"

            st.rerun()


        # --------------------------------------------------------
        # BACK TO HOME
        # --------------------------------------------------------

        if st.button(
            "← Back to Home",
            key="back_home_btn"
        ):

            st.switch_page("app.py")


# ============================================================
# REGISTRATION VIEW
# ============================================================

elif st.session_state.auth_view == "register":

    with st.container(key="hc_login_card"):

        # --------------------------------------------------------
        # LOGO
        # --------------------------------------------------------

        render(
            '<div class="hc-login-logo">🎓 HC NEXUS</div>'
        )

        render(
            '<div class="hc-login-tag">'
            "CREATE NEW ACCOUNT"
            "</div>"
        )


        # --------------------------------------------------------
        # REGISTRATION INPUTS
        # --------------------------------------------------------

        roll_no = st.text_input(
            "Roll No",
            placeholder="Enter your Roll Number"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create your Password"
        )

        confirm_password = st.text_input(
            "Confirm",
            type="password",
            placeholder="Re-enter your Password"
        )


        # --------------------------------------------------------
        # CREATE ACCOUNT
        # --------------------------------------------------------

        if st.button(
            "CREATE ACCOUNT",
            key="register_btn"
        ):

            if not roll_no or not password or not confirm_password:

                st.warning(
                    "Please fill all the fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                students = pd.read_csv(FILE)

                if roll_no in students["Roll No"].astype(str).values:

                    st.error(
                        "This Roll No is already registered."
                    )

                else:

                    new_student = pd.DataFrame(
                        {
                            "Roll No": [roll_no],
                            "Password": [password]
                        }
                    )

                    new_student.to_csv(
                        FILE,
                        mode="a",
                        header=False,
                        index=False
                    )

                    st.success(
                        "Account created successfully! 🎉 "
                        "Go back to Login."
                    )


        # --------------------------------------------------------
        # BACK TO LOGIN
        # --------------------------------------------------------

        if st.button(
            "← BACK TO LOGIN",
            key="back_to_login_btn"
        ):

            st.session_state.auth_view = "login"

            st.rerun()


        # --------------------------------------------------------
        # BACK TO HOME
        # --------------------------------------------------------

        if st.button(
            "← Back to Home",
            key="back_home_btn_register"
        ):

            st.switch_page("app.py")