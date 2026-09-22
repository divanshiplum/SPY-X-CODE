import streamlit as st


def get_theme_css():

    dark = st.session_state.get("dark_theme", False)

    if dark:
        return """
        <style>

        :root {
            --hc-bg: #242033;
            --hc-surface: #302a42;
            --hc-surface-2: #39324d;
            --hc-border: #4b4260;

            --hc-text: #f5efff;
            --hc-text-soft: #c9bfd8;

            --hc-purple: #b8a0ff;
            --hc-pink: #f3a6d5;
            --hc-blue: #9ec5ff;
            --hc-green: #a8dfc0;
            --hc-yellow: #f5d98b;
            --hc-orange: #f5b48c;
            --hc-red: #f2a5a5;
            --hc-teal: #9edbd5;

            --hc-radius: 14px;
            --hc-radius-lg: 18px;

            --hc-shadow:
                0 8px 25px rgba(0, 0, 0, 0.20);
        }

        .stApp {
            background: var(--hc-bg) !important;
            color: var(--hc-text) !important;
        }

        html, body, [class*="css"] {
            font-family: "Segoe UI", Arial, Helvetica, sans-serif;
            color: var(--hc-text);
        }

        [data-testid="stSidebar"] {
            background: var(--hc-surface) !important;
            border-right: 1px solid var(--hc-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--hc-text) !important;
        }

        .hc-card {
            background: var(--hc-surface);
            border: 1px solid var(--hc-border);
            border-radius: var(--hc-radius-lg);
            padding: 20px;
            box-shadow: var(--hc-shadow);
        }

        .settings-section {
            background: var(--hc-surface);
            border: 1px solid var(--hc-border);
        }

        input,
        textarea,
        [data-baseweb="select"] > div {
            background-color: var(--hc-surface-2) !important;
            color: var(--hc-text) !important;
            border-color: var(--hc-border) !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            color: var(--hc-text) !important;
        }

        .stMarkdown,
        .stText,
        label {
            color: var(--hc-text) !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        footer {
            visibility: hidden;
        }

        </style>
        """

    else:
        return """
        <style>

        :root {
            --hc-bg: #ede9f7;
            --hc-surface: #ffffff;
            --hc-surface-2: #f8f6fc;
            --hc-border: #ececf5;

            --hc-text: #302b3d;
            --hc-text-soft: #777185;

            --hc-purple: #8e7cc3;
            --hc-pink: #d99ac5;
            --hc-blue: #8bb8d9;
            --hc-green: #91c7aa;
            --hc-yellow: #e8c97d;
            --hc-orange: #e5aa82;
            --hc-red: #d98f8f;
            --hc-teal: #8dc8c1;

            --hc-radius: 14px;
            --hc-radius-lg: 18px;

            --hc-shadow:
                0 8px 25px rgba(80, 65, 110, 0.08);
        }

        .stApp {
            background: var(--hc-bg) !important;
            color: var(--hc-text) !important;
        }

        html, body, [class*="css"] {
            font-family: "Segoe UI", Arial, Helvetica, sans-serif;
            color: var(--hc-text);
        }

        [data-testid="stSidebar"] {
            background: var(--hc-surface) !important;
            border-right: 1px solid var(--hc-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--hc-text) !important;
        }

        .hc-card {
            background: var(--hc-surface);
            border: 1px solid var(--hc-border);
            border-radius: var(--hc-radius-lg);
            padding: 20px;
            box-shadow: var(--hc-shadow);
        }

        input,
        textarea,
        [data-baseweb="select"] > div {
            background-color: var(--hc-surface) !important;
            color: var(--hc-text) !important;
            border-color: var(--hc-border) !important;
        }

        .stTextInput input,
        .stTextArea textarea {
            color: var(--hc-text) !important;
        }

        .stMarkdown,
        .stText,
        label {
            color: var(--hc-text) !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        footer {
            visibility: hidden;
        }

        </style>
        """


# Backward compatibility
THEME_CSS = get_theme_css()