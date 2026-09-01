import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Student Performance",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------
# LOAD CSV FILE
# -----------------------------
df = pd.read_csv("student-marks.csv")


# -----------------------------
# CALCULATE GPA
# Marks are converted to GPA out of 10
# -----------------------------
df["GPA"] = (df["Marks"] / 10).round(2)


# -----------------------------
# FUNCTION TO CALCULATE GRADE
# -----------------------------
def get_grade(marks):

    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B+"
    elif marks >= 60:
        return "B"
    elif marks >= 50:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


# Apply grade function
df["Grade"] = df["Marks"].apply(get_grade)


# -----------------------------
# CALCULATE OVERALL CGPA
# -----------------------------
cgpa = df["GPA"].mean().round(2)


# -----------------------------
# TITLE
# -----------------------------
st.title("🎓 Student Performance Dashboard")

st.write("### Academic Performance Overview")


# -----------------------------
# OVERALL CGPA
# -----------------------------
st.metric(
    "Overall CGPA",
    f"{cgpa} / 10"
)


# -----------------------------
# CGPA LINE CHART
# -----------------------------
st.subheader("📈 CGPA Performance")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    df["Subject"],
    df["GPA"],
    marker="o",
    linewidth=2
)

# Y-axis fixed from 0 to 10
ax.set_ylim(0, 10)

# Labels
ax.set_xlabel("Subjects")
ax.set_ylabel("GPA (Out of 10)")

# Chart title
ax.set_title("Subject-wise CGPA Performance")

# Rotate subject names
plt.xticks(
    rotation=35,
    ha="right"
)

# Grid
ax.grid(True)

# Adjust layout
plt.tight_layout()

# Show chart in Streamlit
st.pyplot(fig)


# -----------------------------
# SUBJECT PERFORMANCE
# -----------------------------
st.divider()

st.subheader("📚 Subject Performance")


# Create two columns
col1, col2 = st.columns(2)


# -----------------------------
# LEFT SIDE - SUBJECT NAMES
# -----------------------------
with col1:

    st.markdown("### 📖 Subject Name")

    for subject, subject_type in zip(
        df["Subject"],
        df["Type"]
    ):

        st.write(
            f"**{subject}** ({subject_type})"
        )


# -----------------------------
# RIGHT SIDE - GRADES
# -----------------------------
with col2:

    st.markdown("### 🏆 Grade")

    for grade in df["Grade"]:

        st.write(
            f"**{grade}**"
        )


# -----------------------------
# MARKS OVERVIEW
# -----------------------------
st.divider()

st.subheader("📊 Marks Overview")

st.dataframe(
    df[
        [
            "Subject",
            "Type",
            "Marks",
            "GPA",
            "Grade"
        ]
    ],
    use_container_width=True,
    hide_index=True
)