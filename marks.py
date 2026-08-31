import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(
    page_title="Student Performance",
    page_icon="📊",
    layout="centered"
)

# Title
st.title("📊 Student Performance Analysis")

st.write("Enter subjects and their marks.")


# -------------------------
# INPUT SECTION
# -------------------------

# Two columns
col1, col2 = st.columns(2)

# Left side - Subjects
with col1:
    st.subheader("Subjects")

    subjects_input = st.text_area(
        "Enter Subjects (one per line)",
        value="""Computer Architecture
Cybersecurity
Information System
Data Structure
Operating System""",
        height=180
    )


# Right side - Marks
with col2:
    st.subheader("Marks")

    marks_input = st.text_area(
        "Enter Marks (one per line)",
        value="""85
72
90
65
78""",
        height=180
    )


# -------------------------
# CONVERT SUBJECTS TO LIST
# -------------------------

subjects = [
    x.strip()
    for x in subjects_input.split("\n")
    if x.strip()
]


# -------------------------
# CONVERT MARKS TO LIST
# -------------------------

try:
    marks = [
        int(x.strip())
        for x in marks_input.split("\n")
        if x.strip()
    ]

except ValueError:
    st.error("⚠️ Please enter marks only in numbers.")
    st.stop()


# -------------------------
# VALIDATE SUBJECTS AND MARKS
# -------------------------

if len(subjects) != len(marks):

    st.error(
        f"⚠️ Number of subjects ({len(subjects)}) and marks ({len(marks)}) must be equal."
    )
    st.stop()


# -------------------------
# VALIDATE MARKS RANGE
# -------------------------

if any(mark < 0 or mark > 100 for mark in marks):

    st.error(
        "⚠️ Marks should be between 0 and 100."
    )
    st.stop()


# -------------------------
# CREATE DATAFRAME
# -------------------------

df = pd.DataFrame({
    "Subject": subjects,
    "Marks": marks
})


# -------------------------
# PERFORMANCE FUNCTION
# -------------------------

def get_performance(mark):

    if mark >= 90:
        return "Excellent"

    elif mark >= 75:
        return "Good"

    elif mark >= 50:
        return "Average"

    else:
        return "Needs Improvement"


# Add Performance column
df["Performance"] = df["Marks"].apply(
    get_performance
)


# -------------------------
# MARKS OVERVIEW
# -------------------------

st.subheader("📋 Marks Overview")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# -------------------------
# PERFORMANCE ANALYSIS
# -------------------------

st.subheader("📈 Performance Analysis")

# Create chart
fig, ax = plt.subplots(figsize=(10, 5))

# Line chart
ax.plot(
    subjects,
    marks,
    marker="o",
    linewidth=2
)

# Chart title
ax.set_title(
    "Student Performance Analysis"
)

# Labels
ax.set_xlabel("Subjects")
ax.set_ylabel("Marks")

# Marks range
ax.set_ylim(0, 100)

# Rotate subject names
plt.xticks(rotation=20)

# Grid
ax.grid(True)


# Display marks above points
for i, mark in enumerate(marks):

    ax.text(
        i,
        mark + 3,
        str(mark),
        ha="center"
    )


# Adjust chart layout
plt.tight_layout()

# Show chart
st.pyplot(fig)


# -------------------------
# SUMMARY
# -------------------------

st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Marks",
        round(df["Marks"].mean(), 2)
    )

with col2:
    st.metric(
        "Highest Marks",
        df["Marks"].max()
    )

with col3:
    st.metric(
        "Lowest Marks",
        df["Marks"].min()
    )