import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nav_bar import render_bottom_nav


def render(content: str):
    """Strips leading whitespace from every line before handing it
    to st.markdown — Markdown treats 4+ spaces of indentation as a
    code block, which would otherwise show raw HTML as literal text."""
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Student Performance",
    page_icon="🎓",
    layout="wide"
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
#
# This used to be two independent Streamlit columns/containers —
# one looping over subjects, one looping over grades — relying on
# each row rendering at exactly the same height in both to stay
# aligned. Small rendering differences (e.g. the two ### headers)
# threw that off, shifting the grades one row out of sync with
# their subjects. Rendering it as ONE html grid instead means
# each row's subject and grade are literally the same row in the
# same element, so there's no way for them to drift apart.
# -----------------------------
st.divider()

st.subheader("📚 Subject Performance")

row_html = "".join(
    f"""
    <div class="perf-row">
        <div class="perf-subject">
            {subject} <span class="perf-type">({subject_type})</span>
        </div>
        <div class="perf-grade">{grade}</div>
    </div>
    """
    for subject, subject_type, grade in zip(df["Subject"], df["Type"], df["Grade"])
)

render(f"""
<style>
.perf-header {{
    display: flex;
    font-weight: 800;
    font-size: 22px;
    margin-bottom: 14px;
}}
.perf-header .perf-subject-h {{ flex: 3; }}
.perf-header .perf-grade-h {{ flex: 1; }}

.perf-row {{
    display: flex;
    align-items: baseline;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.perf-subject {{
    flex: 3;
    font-weight: 700;
}}
.perf-type {{ font-weight: 400; opacity: 0.85; }}
.perf-grade {{
    flex: 1;
    font-weight: 700;
}}
</style>

<div class="perf-header">
    <div class="perf-subject-h">📖 Subject Name</div>
    <div class="perf-grade-h">🏆 Grade</div>
</div>

{row_html}
""")


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


# -----------------------------
# BOTTOM NAVIGATION (shared component — see nav_bar.py)
# -----------------------------

render_bottom_nav("performance")