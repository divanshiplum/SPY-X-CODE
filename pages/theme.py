"""
Shared design tokens for HC NEXUS theme.
Supports Light and Dark mode.
"""

import streamlit as st


def get_theme_css():

    dark = st.session_state.get("dark_theme", False)

    if dark:
        return """
        <style>

        :root {
            --hc-bg: #0f1117;
            --hc-surface: #181b24;
            --hc-border: #2a2e3a;
            --hc-shadow: 0 2px 14px rgba(0, 0, 0, 0.30);

            --hc-purple: #8b7cf6;
            --hc-purple-soft: #292642;
            --hc-purple-text: #b5adff;
            --hc-purple-hover: #393258;

            --hc-text: #f2f2f7;
            --hc-text-soft: #a8a8b8;
            --hc-text-faint: #77798a;

            --hc-red: #ff5b6e;
            --hc-red-soft: #3a2026;

            --hc-green: #2ec793;
            --hc-green-soft: #183a31;
            --hc-green-hover: #215345;

            --hc-blue: #4f8ef7;
            --hc-blue-soft: #1d2d49;
            --hc-blue-hover: #263c60;

            --hc-orange: #ff9f43;
            --hc-orange-soft: #3d2d1d;
            --hc-orange-hover: #574023;

            --hc-yellow: #f6c445;
            --hc-yellow-soft: #3b321d;
            --hc-yellow-hover: #51451f;

            --hc-teal: #2bb3a3;
            --hc-teal-soft: #193b38;
            --hc-teal-hover: #24534e;

            --hc-radius-lg: 20px;
            --hc-radius-md: 14px;
            --hc-radius-sm: 10px;
        }

        .stApp {
            background: var(--hc-bg) !important;
        }

        html, body, [class*="css"] {
            font-family: "Segoe UI", Arial, Helvetica, sans-serif;
            color: var(--hc-text);
        }

        section[data-testid="stSidebar"] {
            background: var(--hc-surface) !important;
        }

        .hc-card {
            background: var(--hc-surface);
            border-radius: var(--hc-radius-lg);
            box-shadow: var(--hc-shadow);
            border: 1px solid var(--hc-border);
        }

        </style>
        """

    else:
        return """
        <style>

        :root {
            --hc-bg: #ede9f7;
            --hc-surface: #ffffff;
            --hc-border: #ececf5;
            --hc-shadow: 0 2px 14px rgba(80, 70, 160, 0.06);

            --hc-purple: #7c6ff0;
            --hc-purple-soft: #eeecfd;
            --hc-purple-text: #6a5cd6;
            --hc-purple-hover: #ddd8fb;

            --hc-text: #1f2130;
            --hc-text-soft: #8b8a9a;
            --hc-text-faint: #b3b2c0;

            --hc-red: #ff5b6e;
            --hc-red-soft: #ffe7ea;

            --hc-green: #2ec793;
            --hc-green-soft: #e2f9f0;
            --hc-green-hover: #c8f3e3;

            --hc-blue: #4f8ef7;
            --hc-blue-soft: #e6f0fe;
            --hc-blue-hover: #d0e4fd;

            --hc-orange: #ff9f43;
            --hc-orange-soft: #fff1e2;
            --hc-orange-hover: #ffe0c2;

            --hc-yellow: #f6c445;
            --hc-yellow-soft: #fef6e0;
            --hc-yellow-hover: #fbe9b8;

            --hc-teal: #2bb3a3;
            --hc-teal-soft: #e2f7f4;
            --hc-teal-hover: #c8efe9;

            --hc-radius-lg: 20px;
            --hc-radius-md: 14px;
            --hc-radius-sm: 10px;
        }

        .stApp {
            background: var(--hc-bg) !important;
        }

        html, body, [class*="css"] {
            font-family: "Segoe UI", Arial, Helvetica, sans-serif;
            color: var(--hc-text);
        }

        section[data-testid="stSidebar"] {
            background: var(--hc-surface) !important;
        }

        .hc-card {
            background: var(--hc-surface);
            border-radius: var(--hc-radius-lg);
            box-shadow: var(--hc-shadow);
            border: 1px solid var(--hc-border);
        }

        </style>
        """


THEME_CSS = get_theme_css()