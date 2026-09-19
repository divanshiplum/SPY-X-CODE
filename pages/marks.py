import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nav_sidebar import render_sidebar


def render(content: str):
    lines = content.strip("\n").split("\n")
    flat = "\n".join(line.strip() for line in lines)
    st.markdown(flat, unsafe_allow_html=True)


st.set_page_config(
    page_title="Student Marks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_sidebar("marks")


# ============================================================
# DATA
#
# The reference shows a plain read-only table (no editable input
# rows), so that's what this rebuild matches — the earlier
# editable-text-input version is dropped in favor of this static
# display, per the mockup.
# ============================================================

DEFAULT_SUBJECTS = [
    "Computer Architecture",
    "Cybersecurity",
    "Information System",
    "Data Structure",
    "Operating System",
]

DEFAULT_MARKS = [85, 72, 90, 65, 78]


def get_grade(marks):
    """Calibrated so 70+ reads as "A" (not split into A/A+) — this
    matches the exact grade shown per subject in the reference
    table (85→A, 72→A, 90→A, 65→B+, 78→A)."""
    if marks >= 70:
        return "A"
    elif marks >= 60:
        return "B+"
    elif marks >= 50:
        return "B"
    elif marks >= 40:
        return "C"
    else:
        return "F"


df = pd.DataFrame({"Subject": DEFAULT_SUBJECTS, "Marks": DEFAULT_MARKS})
df["Grade"] = df["Marks"].apply(get_grade)


# ============================================================
# CSS
# ============================================================

render("""
<style>

.hc-marks-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 800;
    color: var(--hc-text);
    margin-bottom: 18px;
}

.hc-marks-title-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: var(--hc-purple-soft);
    color: var(--hc-purple-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

table.hc-marks-table {
    width: 100%;
    border-collapse: collapse;
}

table.hc-marks-table th {
    text-align: left;
    color: var(--hc-text-soft);
    font-size: 13px;
    font-weight: 700;
    padding: 14px 18px;
    border-bottom: 2px solid var(--hc-border);
}

table.hc-marks-table td {
    padding: 14px 18px;
    color: var(--hc-text);
    font-size: 14px;
    font-weight: 600;
    border-bottom: 1px solid var(--hc-border);
}

table.hc-marks-table tr:last-child td { border-bottom: none; }

div.stVerticalBlock[class*="st-key-hc_marks_chart_card"] {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
    padding: 16px 20px;
}

</style>
""")


# ============================================================
# TITLE
# ============================================================

render('<div class="hc-marks-title"><span class="hc-marks-title-icon">📊</span> Student Marks Analysis</div>')


# ============================================================
# TABLE
# ============================================================

rows_html = "".join(
    f"""
    <tr>
        <td>{subject}</td>
        <td>{marks}</td>
        <td>{grade}</td>
    </tr>
    """
    for subject, marks, grade in zip(df["Subject"], df["Marks"], df["Grade"])
)

with st.container(key="hc_marks_table_card"):
    render(f"""
    <div class="hc-card" style="padding: 6px 0;">
        <table class="hc-marks-table">
            <tr>
                <th>Subject</th>
                <th>Marks</th>
                <th>Grade</th>
            </tr>
            {rows_html}
        </table>
    </div>
    """)


# ============================================================
# MARKS OVERVIEW (chart)
# ============================================================

st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

render('<div class="hc-marks-title"><span class="hc-marks-title-icon">📈</span> Marks Overview</div>')

with st.container(key="hc_marks_chart_card"):

    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(df["Subject"], df["Marks"], marker="o", linewidth=2, color="#7c6ff0")
    ax.set_ylim(0, 100)
    ax.set_xlabel("")
    ax.set_ylabel("Marks")
    plt.xticks(rotation=15)
    ax.grid(True, color="#ececf5")
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")

    for i, mark in enumerate(df["Marks"]):
        ax.text(i, mark + 3, str(mark), ha="center", fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)