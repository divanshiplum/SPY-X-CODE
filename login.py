import streamlit as st
import pandas as pd
import os

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="centered"
)

# -----------------------------
# CSS
#
# The whole form lives inside Streamlit's own .block-container.
# Capping its max-width and giving it auto margins keeps it a
# fixed, comfortable size AND perfectly centered on any window
# size — on a small window it just shrinks to fit (max-width is
# a ceiling, not a fixed width), so this is responsive on its
# own without needing st.columns to fake centering.
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b0b0b, #202020);
}

.block-container {
    max-width: clamp(360px, 55vw, 650px);
    margin: 0 auto;
    padding-top: 60px;
}

.title {
    text-align: center;
    color: #d4af37;
    font-size: 26px;
    font-weight: bold;
    line-height: 1.3;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 18px;
    margin-bottom: 25px;
}

/* The direct parent Streamlit gives a button is set to
   width: fit-content (it shrink-wraps tightly around the
   button itself), so centering .stButton inside it has no
   room to work with. We force that specific wrapper — the
   stElementContainer that directly holds a .stButton — to
   take the full available width instead, THEN center the
   button within that now-full-width space. */
div[data-testid="stElementContainer"]:has(> div.stButton) {
    width: 100% !important;
}

.stButton {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

.stButton > button {
    width: auto;
    min-width: 200px;
    background-color: #d4af37;
    color: black;
    border-radius: 10px;
    font-weight: bold;
    height: 45px;
}

.stButton > button:hover {
    background-color: #f0c94d;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# CSV FILE
# -----------------------------
FILE = "students.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(
        columns=["Roll No", "Password"]
    )
    df.to_csv(FILE, index=False)


# -----------------------------
# SESSION STATE
#
# "auth_view" only toggles between the Login form and the
# Register form on this page. Once login succeeds, we redirect
# straight to dashboard.py with st.switch_page() rather than
# tracking "dashboard" as a state here.
# -----------------------------
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "roll_no" not in st.session_state:
    st.session_state.roll_no = None


# If somebody is already logged in and lands back on this page
# (e.g. via browser back button), send them straight through.
if st.session_state.logged_in:
    st.switch_page("dashboard.py")


# =========================================================
# LOGIN VIEW
# =========================================================

if st.session_state.auth_view == "login":

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="title">🎓 STUDENT MANAGEMENT SYSTEM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">LOGIN</div>',
        unsafe_allow_html=True
    )

    # Roll Number
    roll_no = st.text_input(
        "Roll No",
        placeholder="Enter your Roll Number"
    )

    # Password
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your Password"
    )

    st.write("")

    # LOGIN BUTTON
    if st.button("LOGIN"):

        students = pd.read_csv(FILE)

        user = students[
            (students["Roll No"].astype(str) == roll_no) &
            (students["Password"].astype(str) == password)
        ]

        if not user.empty:

            st.session_state.logged_in = True
            st.session_state.roll_no = roll_no

            st.success("Login Successful! 🎉")
            st.switch_page("dashboard.py")

        else:

            st.error(
                "Account not found or incorrect Roll No/Password."
            )

    st.write("")

    # REGISTER OPTION
    st.markdown(
        "<p style='text-align:center;color:white;'>"
        "Don't have an account?"
        "</p>",
        unsafe_allow_html=True
    )

    if st.button("REGISTER HERE"):

        st.session_state.auth_view = "register"
        st.rerun()


# =========================================================
# REGISTRATION VIEW
# =========================================================

elif st.session_state.auth_view == "register":

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="title">🎓 STUDENT MANAGEMENT SYSTEM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">CREATE NEW ACCOUNT</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # REGISTRATION FIELDS
    # -----------------------------

    roll_no = st.text_input(
        "Roll No",
        placeholder="Enter your Roll Number"
    )

    password = st.text_input(
        "Create Password",
        type="password",
        placeholder="Create your Password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your Password"
    )

    st.write("")

    # -----------------------------
    # CREATE ACCOUNT
    # -----------------------------

    if st.button("CREATE ACCOUNT"):

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

            # Check Roll No
            if roll_no in students["Roll No"].astype(str).values:

                st.error(
                    "This Roll No is already registered."
                )

            else:

                # Create new account
                new_student = pd.DataFrame({
                    "Roll No": [roll_no],
                    "Password": [password]
                })

                # Save account in CSV
                new_student.to_csv(
                    FILE,
                    mode="a",
                    header=False,
                    index=False
                )

                st.success(
                    "Account created successfully! 🎉"
                )

                st.info(
                    "Now go back to Login and enter your Roll No and Password."
                )

    st.write("")

    # -----------------------------
    # BACK TO LOGIN
    # -----------------------------

    if st.button("← BACK TO LOGIN"):

        st.session_state.auth_view = "login"
        st.rerun()