import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Important Message",
    page_icon="📢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# HTML RENDER HELPER
# ============================================================

def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# CSS — dark header bar (back / title / refresh) on a plain
# white body, matching the reference screenshot. Same header
# pattern already used on datesheet.py.
# ============================================================

render("""
<style>

.stApp {
    background: #ffffff;
    color: #111111;
}

.block-container {
    max-width: 720px;
    padding: 0;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

.msg-header-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    flex: 1;
    text-align: center;
}

div.stVerticalBlock[class*="st-key-msg_header_row"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    background: #000000;
    padding: 12px 16px;
    gap: 8px;
}

div.stVerticalBlock[class*="st-key-msg_header_row"] > div:nth-child(2) {
    flex: 1;
}

div[class*="st-key-msg_back"] .stButton > button,
div[class*="st-key-msg_refresh"] .stButton > button {
    background: #1c1c1c;
    color: #ffffff;
    border: none;
    border-radius: 50%;
    width: 42px;
    height: 42px;
    font-size: 18px;
    padding: 0;
}

div[class*="st-key-msg_back"] .stButton > button:hover,
div[class*="st-key-msg_refresh"] .stButton > button:hover {
    background: #333333;
}

.msg-body {
    padding: 20px 16px;
}

.msg-body p {
    margin: 0 0 16px 0;
    line-height: 1.5;
}

</style>
""")


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

attendance_file = BASE_DIR / "attendance_records.csv"
attendance_messages_file = BASE_DIR / "attendance_messages.csv"
messages_file = BASE_DIR / "messages.csv"


# ============================================================
# HEADER (back arrow, title, refresh)
# ============================================================

with st.container(key="msg_header_row"):

    if st.button("‹", key="msg_back"):
        st.switch_page("dashboard.py")

    render('<div class="msg-header-title">Important Message</div>')

    if st.button("⟳", key="msg_refresh"):
        st.rerun()


# ============================================================
# CHECK ATTENDANCE FILE
# (used further down for House Test Eligibility)
# ============================================================

if not attendance_file.exists():

    render('<div class="msg-body">')
    st.error(
        "attendance_records.csv file not found. "
        "Please make sure it is present in the project folder."
    )
    render('</div>')

    st.stop()


# ============================================================
# READ ATTENDANCE CSV USING PANDAS
# ============================================================

attendance_df = pd.read_csv(attendance_file)

# Remove extra spaces from column names
attendance_df.columns = attendance_df.columns.str.strip()

# Remove completely empty rows
attendance_df = attendance_df.dropna(how="all")


# ============================================================
# CONVERT DATE
# ============================================================

attendance_df["date"] = pd.to_datetime(
    attendance_df["date"],
    errors="coerce"
)


# ============================================================
# READ ATTENDANCE MESSAGES FROM attendance_messages.csv
#
# These messages are pre-generated from attendance_records.csv
# (one row per Absent class) rather than recomputed here on every
# run — see generate_attendance_messages.py if you need to
# regenerate this file after attendance_records.csv changes.
# ============================================================

attendance_messages = []

if attendance_messages_file.exists():

    attendance_messages_df = pd.read_csv(attendance_messages_file)

    attendance_messages_df.columns = (
        attendance_messages_df.columns.str.strip()
    )

    attendance_messages_df["date"] = pd.to_datetime(
        attendance_messages_df["date"],
        errors="coerce"
    )

    attendance_messages_df = attendance_messages_df.sort_values(
        "date",
        ascending=False
    )

    for _, row in attendance_messages_df.iterrows():

        attendance_messages.append({

            "type": str(row.get("type", "Attendance")),

            "date": row["date"],

            "title": str(row.get("title", "Attendance Notice")),

            "message": str(row.get("message", ""))
        })


# ============================================================
# READ GENERAL MESSAGES FROM messages.csv
# ============================================================

general_messages = []


if messages_file.exists():

    messages_df = pd.read_csv(
        messages_file
    )

    messages_df.columns = (
        messages_df.columns.str.strip()
    )


    for _, row in messages_df.iterrows():

        general_messages.append({

            "type": str(
                row.get(
                    "message_type",
                    "General"
                )
            ),

            "date": pd.NaT,

            "title": str(
                row.get(
                    "title",
                    "Important Message"
                )
            ),

            "message": str(
                row.get(
                    "message",
                    ""
                )
            )
        })


# ============================================================
# COMBINE MESSAGES
# ============================================================

all_messages = (
    attendance_messages
    + general_messages
)


# ============================================================
# HOUSE TEST ELIGIBILITY
#
# Computed directly from attendance_records.csv — the same 75%
# threshold used on the dashboard's attendance cards ("Attend N
# more to recover" / "Safe to miss N classes"). No table, no
# chart — just a plain eligible/not-eligible line per subject,
# matching the flat message-list style of the rest of this page.
# ============================================================

ELIGIBILITY_THRESHOLD = 75

# Friendly subject names for the raw course codes in
# attendance_records.csv — falls back to the raw code for any
# code not listed here.
CODE_TO_SUBJECT = {
    "23CSR-449": "Data Structure",
    "SPO-113": "Computer Architecture",
    "23BDA-401": "Information System",
    "23BDA-402": "Cybersecurity Fundamentals",
    "23BDA-403": "Operating System",
}

eligibility_counts = (
    attendance_df
    .groupby("code")["status"]
    .value_counts()
    .unstack(fill_value=0)
)

if "Present" not in eligibility_counts.columns:
    eligibility_counts["Present"] = 0

if "Absent" not in eligibility_counts.columns:
    eligibility_counts["Absent"] = 0

eligibility_counts["Total"] = (
    eligibility_counts["Present"] + eligibility_counts["Absent"]
)

eligibility_rows = []

for code, row in eligibility_counts.iterrows():

    total = int(row["Total"])
    present = int(row["Present"])

    if total == 0:
        continue

    percentage = round(present / total * 100)
    is_eligible = percentage >= ELIGIBILITY_THRESHOLD
    subject_name = CODE_TO_SUBJECT.get(code, code)

    if is_eligible:
        message = (
            f"You are **eligible** for the House Test in "
            f"**{subject_name}** — attendance is **{percentage}%** "
            f"({present}/{total})."
        )
    else:
        message = (
            f"You are **NOT eligible** for the House Test in "
            f"**{subject_name}** — attendance is only **{percentage}%** "
            f"({present}/{total}), below the required "
            f"{ELIGIBILITY_THRESHOLD}%."
        )

    eligibility_rows.append({
        "title": "House Test Eligibility",
        "message": message,
    })


# ============================================================
# PAGE BODY
# ============================================================

render('<div class="msg-body">')

if len(all_messages) > 0:

    for item in all_messages:

        st.markdown(
            f"• **{item['title']}:** "
            f"{item['message']}"
        )

else:

    st.markdown(
        "• **Important Message:** "
        "No messages available."
    )


# ============================================================
# PENDING DOCUMENT MESSAGE
# ============================================================

st.markdown(
    """
- **1. Pending Documents:** The status of
Pending documents is as given below, you
are required to submit the same in
**Block-B1 (Room No. 208 - General category)**
and **Room No. 204 - Scholarship students.**

**Abbreviation:**
MIG: Migration,
CHAR/CHR: Character,
DIP: Diploma,
ORG: Original
"""
)


st.markdown(
    "**Document Remarks:** NO DOCUMENTS PENDING"
)

# ============================================================
# HOUSE TEST ELIGIBILITY
# ============================================================

for item in eligibility_rows:

    st.markdown(
        f"• **{item['title']}:** "
        f"{item['message']}"
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "📢 Please check this page regularly "
    "for important updates."
)

render('</div>')