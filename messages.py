import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Important Message",
    page_icon="📢",
    layout="wide"
)

# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

attendance_file = BASE_DIR / "attendance_record.csv"
messages_file = BASE_DIR / "messages.csv"


# ============================================================
# CHECK ATTENDANCE FILE
# ============================================================

if not attendance_file.exists():

    st.error(
        "attendance_record.csv file nahi mili. "
        "Please make sure it is present in the project folder."
    )

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
# CREATE MESSAGES FROM ATTENDANCE RECORD
# ============================================================

absent_df = attendance_df[
    attendance_df["status"]
    .astype(str)
    .str.strip()
    .str.lower()
    == "absent"
].copy()


attendance_messages = []


for _, row in absent_df.sort_values(
    "date",
    ascending=False
).iterrows():

    course = str(row["code"]).strip()

    date = row["date"]

    instructor = str(
        row.get("instructor", "")
    ).strip()


    # Format date
    if pd.isna(date):

        date_text = "Unknown date"

    else:

        date_text = date.strftime(
            "%d %B %Y"
        )


    # Create attendance message
    message = (
        f"Attendance is marked **Absent** "
        f"for **{course}** "
        f"on **{date_text}**."
    )


    # Add instructor if available
    if instructor and instructor.lower() != "nan":

        message += (
            f" Instructor: **{instructor}**."
        )


    attendance_messages.append({

        "type": "Attendance",

        "date": date,

        "title": "Attendance Notice",

        "message": message
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
# PAGE TITLE
# ============================================================

st.title("Important Message")


st.write(
    "View important notices, attendance alerts "
    "and other messages."
)


# ============================================================
# DISPLAY MESSAGES AS A LIST
# Screenshot-like format
# ============================================================

st.subheader("📢 Messages")


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

st.markdown("---")

st.subheader("📄 Pending Documents")


st.markdown(
    """
• **1. Pending Documents:** The status of
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


st.markdown("• [Leave Message]")

st.markdown("• [Other Message]")


# ============================================================
# ATTENDANCE SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📊 Attendance Summary")


summary = (
    attendance_df
    .groupby("code")["status"]
    .value_counts()
    .unstack(fill_value=0)
)


# Make sure Present and Absent columns exist

if "Present" not in summary.columns:

    summary["Present"] = 0


if "Absent" not in summary.columns:

    summary["Absent"] = 0


# Total classes

summary["Total"] = (
    summary["Present"]
    + summary["Absent"]
)


# Attendance percentage

summary["Attendance %"] = (
    summary["Present"]
    / summary["Total"]
    * 100
).round(2)


# Display dataframe

st.dataframe(
    summary,
    use_container_width=True
)


# ============================================================
# MATPLOTLIB CHART
# ============================================================

st.subheader("📈 Attendance Overview")


if not summary.empty:

    fig, ax = plt.subplots()


    ax.bar(
        summary.index,
        summary["Attendance %"]
    )


    ax.set_title(
        "Subject-wise Attendance Percentage"
    )

    ax.set_xlabel(
        "Subject / Course Code"
    )

    ax.set_ylabel(
        "Attendance (%)"
    )


    ax.set_ylim(
        0,
        100
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    plt.tight_layout()


    st.pyplot(fig)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "📢 Please check this page regularly "
    "for important updates."
)