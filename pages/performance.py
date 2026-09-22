import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nav_sidebar import render_sidebar
from theme import get_theme_css


def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


st.set_page_config(
    page_title="Student Performance",
    page_icon="🎓",
    layout="wide",
)

st.html(get_theme_css())

render_sidebar("performance")


# -----------------------------
# LOAD CSV FILE
# -----------------------------
df = pd.read_csv("data/student-marks.csv")

df["GPA"] = (df["Marks"] / 10).round(2)


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


df["Grade"] = df["Marks"].apply(get_grade)

cgpa = df["GPA"].mean().round(2)


# -----------------------------
# CSS
# -----------------------------

render("""
<style>

.hc-perf-title {
    font-size: 22px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 4px;
}

.hc-perf-subtitle {
    color: var(--hc-text-soft);
    font-size: 13px;
    margin-bottom: 18px;
}

.hc-cgpa-card {
    background: linear-gradient(135deg, var(--hc-purple-soft) 0%, var(--hc-blue-soft) 100%);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    padding: 20px 24px;
    margin-bottom: 22px;
}

.hc-cgpa-card-label { color: var(--hc-text-soft); font-size: 13px; margin-bottom: 6px; }
.hc-cgpa-card-value { font-size: 32px; font-weight: 800; color: var(--hc-text); }

.hc-chart-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 700;
    color: var(--hc-text);
    margin-bottom: 14px;
}

.hc-chart-title-icon {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: var(--hc-purple-soft);
    color: var(--hc-purple-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

div.stVerticalBlock[class*="st-key-hc_perf_chart_card"],
div.stVerticalBlock[class*="st-key-hc_perf_table_card"],
div.stVerticalBlock[class*="st-key-hc_perf_marks_card"] {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    padding: 20px 24px;
    margin-bottom: 22px;
}

.hc-perf-row {
    display: flex;
    align-items: baseline;
    padding: 12px 0;
    border-bottom: 1px solid var(--hc-border);
}
.hc-perf-subject { flex: 3; font-weight: 700; color: var(--hc-text); }
.hc-perf-type { font-weight: 400; color: var(--hc-text-soft); }
.hc-perf-grade { flex: 1; font-weight: 700; color: var(--hc-purple-text); }

.hc-perf-header-row {
    display: flex;
    font-weight: 800;
    font-size: 13px;
    color: var(--hc-text-soft);
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--hc-border);
}
.hc-perf-header-row .hc-perf-subject-h { flex: 3; }
.hc-perf-header-row .hc-perf-grade-h { flex: 1; }

</style>
""")


# -----------------------------
# TITLE + CGPA
# -----------------------------

render('<div class="hc-chart-title"><span class="hc-chart-title-icon">📈</span> Student Performance</div>')
render('<div class="hc-perf-subtitle">Academic Performance Overview</div>')

with st.container(key="hc_perf_cgpa_card"):
    render(f"""
    <div class="hc-cgpa-card">
        <div class="hc-cgpa-card-label">Overall CGPA</div>
        <div class="hc-cgpa-card-value">{cgpa} / 10</div>
    </div>
    """)


# -----------------------------
# CGPA LINE CHART
# -----------------------------

with st.container(key="hc_perf_chart_card"):

    render('<div class="hc-chart-title"><span class="hc-chart-title-icon">📈</span> CGPA Performance</div>')

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["Subject"], df["GPA"], marker="o", linewidth=2, color="#7c6ff0")
    ax.set_ylim(0, 10)
    ax.set_xlabel("Subjects")
    ax.set_ylabel("GPA (Out of 10)")
    plt.xticks(rotation=35, ha="right")
    ax.grid(True, color="#ececf5")
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    st.pyplot(fig)


# -----------------------------
# SUBJECT PERFORMANCE
# -----------------------------

row_html = "".join(
    f"""
    <div class="hc-perf-row">
        <div class="hc-perf-subject">
            {subject} <span class="hc-perf-type">({subject_type})</span>
        </div>
        <div class="hc-perf-grade">{grade}</div>
    </div>
    """
    for subject, subject_type, grade in zip(df["Subject"], df["Type"], df["Grade"])
)

with st.container(key="hc_perf_table_card"):
    render(f"""
    <div class="hc-chart-title"><span class="hc-chart-title-icon">📖</span> Subject Performance</div>
    <div class="hc-perf-header-row">
        <div class="hc-perf-subject-h">📖 Subject Name</div>
        <div class="hc-perf-grade-h">🏆 Grade</div>
    </div>
    {row_html}
    """)


# -----------------------------
# MARKS OVERVIEW
# -----------------------------

with st.container(key="hc_perf_marks_card"):
    render('<div class="hc-chart-title"><span class="hc-chart-title-icon">📊</span> Marks Overview</div>')
    st.dataframe(
        df[["Subject", "Type", "Marks", "GPA", "Grade"]],
        use_container_width=True,
        hide_index=True,
    )