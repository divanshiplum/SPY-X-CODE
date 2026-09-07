import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nav_bar import render_bottom_nav

# Page settings
st.set_page_config(
    page_title="Student Performance",
    page_icon="📊",
    layout="centered"
)

# ============================================================
# LOGIN GUARD
# ============================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("login.py")

# Leave room at the bottom so the fixed nav bar never covers content
st.markdown(
    "<style>.block-container { padding-bottom: 110px; }</style>",
    unsafe_allow_html=True
)

# Title
st.title("📊 Student Performance Analysis")

st.write("Enter each subject and its marks — one row per subject.")


# -------------------------
# DEFAULT DATA
# -------------------------

DEFAULT_SUBJECTS = [
    "Computer Architecture",
    "Cybersecurity",
    "Information System",
    "Data Structure",
    "Operating System",
]

DEFAULT_MARKS = [85, 72, 90, 65, 78]


# -------------------------
# TABLE-STYLE INPUT SECTION
#
# Each subject gets its own row, with a subject field and a marks
# field side by side — plain st.text_input fields (same kind used
# for a first/last name form), just laid out one row per subject
# instead of one big multi-line box.
#
# Each row is its own st.container(key=...) forced into a flex row
# via CSS (same technique used for the nav bar and day selector),
# rather than st.columns, so this stays a proper table layout even
# on a narrow screen instead of the subject/marks fields stacking
# on top of each other.
# -------------------------

st.markdown("""
<style>
div.stVerticalBlock[class*="st-key-marks_row_"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
    align-items: flex-end !important;
}

div.stVerticalBlock[class*="st-key-marks_row_"] > div:nth-child(1) {
    flex: 3 1 0px !important;
    min-width: 0 !important;
}

div.stVerticalBlock[class*="st-key-marks_row_"] > div:nth-child(2) {
    flex: 1 1 0px !important;
    min-width: 0 !important;
}
</style>
""", unsafe_allow_html=True)

subjects = []
marks_raw = []

for i in range(len(DEFAULT_SUBJECTS)):

    with st.container(key=f"marks_row_{i}"):

        subject_val = st.text_input(
            "Subject",
            value=DEFAULT_SUBJECTS[i],
            key=f"subject_{i}",
            label_visibility="visible" if i == 0 else "collapsed",
        )

        marks_val = st.text_input(
            "Marks",
            value=str(DEFAULT_MARKS[i]),
            key=f"marks_{i}",
            label_visibility="visible" if i == 0 else "collapsed",
        )

    subjects.append(subject_val)
    marks_raw.append(marks_val)


# -------------------------
# CLEAN UP SUBJECTS
# (skip any row left completely blank)
# -------------------------

rows = [
    (s.strip(), m.strip())
    for s, m in zip(subjects, marks_raw)
    if s.strip()
]

subjects = [s for s, m in rows]
marks_text = [m for s, m in rows]


# -------------------------
# CONVERT MARKS TO NUMBERS
# -------------------------

try:
    marks = [int(m) for m in marks_text]

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


# -------------------------
# BOTTOM NAVIGATION (shared component — see nav_bar.py)
# -------------------------

render_bottom_nav("marks")