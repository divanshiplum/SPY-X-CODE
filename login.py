import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b0b0b, #202020);
}

.title {
    text-align: center;
    color: #d4af37;
    font-size: 30px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 18px;
    margin-bottom: 25px;
}

.stButton > button {
    width: 100%;
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
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================================
# LOGIN PAGE
# =========================================================

if st.session_state.page == "login":

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
            st.session_state.page = "dashboard"

            st.success("Login Successful! 🎉")
            st.rerun()

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

        st.session_state.page = "register"
        st.rerun()


# =========================================================
# REGISTRATION PAGE
# =========================================================

elif st.session_state.page == "register":

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

        st.session_state.page = "login"
        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

elif st.session_state.page == "dashboard":

    st.markdown(
        '<div class="title">🎓 STUDENT DASHBOARD</div>',
        unsafe_allow_html=True
    )

    st.success("Welcome to Student Management System! 🎉")

    st.write("### Student Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Students", "50")
    col2.metric("Attendance", "85%")
    col3.metric("Subjects", "6")

    # -----------------------------
    # PERFORMANCE CHART
    # -----------------------------

    st.write("### Performance")

    data = pd.DataFrame({
        "Subject": [
            "Python",
            "C",
            "Data Structures",
            "DBMS",
            "Maths"
        ],
        "Marks": [
            78,
            85,
            72,
            88,
            80
        ]
    })

    fig, ax = plt.subplots()

    ax.bar(
        data["Subject"],
        data["Marks"]
    )

    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_title("Student Performance")

    plt.xticks(rotation=20)

    st.pyplot(fig)

    # -----------------------------
    # LOGOUT
    # -----------------------------

    if st.button("LOGOUT"):

        st.session_state.logged_in = False
        st.session_state.page = "login"

        st.rerun()