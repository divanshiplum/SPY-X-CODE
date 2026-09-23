import streamlit as st


# ============================================================
# THEME CSS
# ============================================================

def get_theme_css():

    dark = st.session_state.get("dark_theme", False)


    # ========================================================
    # DARK PASTEL THEME
    # ========================================================

    if dark:

        return """
        <style>

        :root {

            /* ------------------------------------------------
               MAIN COLORS
            ------------------------------------------------ */

            --hc-bg: #242033;
            --hc-surface: #302a42;
            --hc-surface-2: #39324d;

            --hc-border: #4b4260;

            --hc-text: #f5efff;
            --hc-text-soft: #c9bfd8;


            /* ------------------------------------------------
               MAIN ACCENT COLORS
            ------------------------------------------------ */

            --hc-purple: #b8a0ff;
            --hc-pink: #f3a6d5;
            --hc-blue: #9ec5ff;
            --hc-green: #a8dfc0;
            --hc-yellow: #f5d98b;
            --hc-orange: #f5b48c;
            --hc-red: #f2a5a5;
            --hc-teal: #9edbd5;


            /* ------------------------------------------------
               COURSE CARD PASTEL COLORS
            ------------------------------------------------ */

            --hc-blue-soft: #30445a;
            --hc-blue-hover: #405b77;

            --hc-orange-soft: #594438;
            --hc-orange-hover: #765843;

            --hc-green-soft: #304b3d;
            --hc-green-hover: #3d624f;

            --hc-purple-soft: #453b5e;
            --hc-purple-hover: #594b78;

            --hc-yellow-soft: #5a5133;
            --hc-yellow-hover: #74683e;

            --hc-teal-soft: #304f4d;
            --hc-teal-hover: #3d6865;

            --hc-red-soft: #553638;


            /* ------------------------------------------------
               EXTRA COLORS
            ------------------------------------------------ */

            --hc-purple-text: #c7b5ff;

            --hc-ring-empty: #454052;


            /* ------------------------------------------------
               RADIUS
            ------------------------------------------------ */

            --hc-radius-sm: 8px;
            --hc-radius-md: 12px;
            --hc-radius-lg: 18px;


            /* ------------------------------------------------
               SHADOW
            ------------------------------------------------ */

            --hc-shadow:
                0 8px 24px rgba(0, 0, 0, 0.20);

        }


        /* ====================================================
           MAIN STREAMLIT APP
        ==================================================== */

        .stApp {

            background:
                var(--hc-bg) !important;

            color:
                var(--hc-text) !important;
        }


        .main {

            background:
                var(--hc-bg) !important;
        }


        .block-container {

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           TEXT
        ==================================================== */

        html,
        body,
        [class*="css"] {

            font-family:
                "Segoe UI",
                Arial,
                Helvetica,
                sans-serif;
        }


        p,
        span,
        label,
        div {

            color:
                inherit;
        }


        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           HEADER
        ==================================================== */

        header[data-testid="stHeader"] {

            background:
                var(--hc-bg) !important;
        }


        [data-testid="stHeader"] {

            background:
                var(--hc-bg) !important;
        }


        /* ====================================================
           SIDEBAR
        ==================================================== */

        section[data-testid="stSidebar"] {

            background:
                var(--hc-surface) !important;

            border-right:
                1px solid var(--hc-border);
        }


        section[data-testid="stSidebar"] * {

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           CARDS
        ==================================================== */

        .hc-card {

            background:
                var(--hc-surface);

            border:
                1px solid var(--hc-border);

            border-radius:
                var(--hc-radius-lg);

            box-shadow:
                var(--hc-shadow);
        }


        /* ====================================================
           STREAMLIT BUTTONS
        ==================================================== */

        .stButton > button {

            background:
                var(--hc-surface) !important;

            color:
                var(--hc-text) !important;

            border:
                1px solid var(--hc-border) !important;

            border-radius:
                var(--hc-radius-md) !important;
        }


        .stButton > button:hover {

            background:
                var(--hc-surface-2) !important;

            border-color:
                var(--hc-purple) !important;

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           INPUTS
        ==================================================== */

        input,
        textarea,
        select {

            background:
                var(--hc-surface) !important;

            color:
                var(--hc-text) !important;

            border-color:
                var(--hc-border) !important;
        }


        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] {

            background:
                var(--hc-surface) !important;

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           SELECTBOX
        ==================================================== */

        [data-baseweb="select"] > div {

            background:
                var(--hc-surface) !important;

            border-color:
                var(--hc-border) !important;

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           CHECKBOX
        ==================================================== */

        [data-testid="stCheckbox"] label {

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           EXPANDER
        ==================================================== */

        [data-testid="stExpander"] {

            background:
                var(--hc-surface) !important;

            border:
                1px solid var(--hc-border) !important;

            border-radius:
                var(--hc-radius-md) !important;
        }


        /* ====================================================
           TABS
        ==================================================== */

        button[data-baseweb="tab"] {

            color:
                var(--hc-text-soft) !important;
        }


        button[data-baseweb="tab"][aria-selected="true"] {

            color:
                var(--hc-purple) !important;
        }


        /* ====================================================
           DATAFRAME
        ==================================================== */

        [data-testid="stDataFrame"] {

            border:
                1px solid var(--hc-border);

            border-radius:
                var(--hc-radius-md);
        }


        /* ====================================================
           ALERTS
        ==================================================== */

        [data-testid="stAlert"] {

            background:
                var(--hc-surface-2) !important;

            border:
                1px solid var(--hc-border) !important;

            color:
                var(--hc-text) !important;
        }


        /* ====================================================
           SCROLLBAR
        ==================================================== */

        ::-webkit-scrollbar {

            width: 8px;

            height: 8px;
        }


        ::-webkit-scrollbar-track {

            background:
                var(--hc-bg);
        }


        ::-webkit-scrollbar-thumb {

            background:
                var(--hc-border);

            border-radius:
                10px;
        }


        ::-webkit-scrollbar-thumb:hover {

            background:
                var(--hc-purple);
        }


        /* ====================================================
           HIDE STREAMLIT DEFAULT UI
        ==================================================== */

        #MainMenu {

            visibility: hidden;
        }


        footer {

            visibility: hidden;
        }


        </style>
        """


    # ========================================================
    # LIGHT PASTEL THEME
    # ========================================================

    return """

    <style>

    :root {

        /* ----------------------------------------------------
           MAIN COLORS
        ---------------------------------------------------- */

        --hc-bg: #ede9f7;

        --hc-surface: #ffffff;

        --hc-surface-2: #f8f6fc;

        --hc-border: #ececf5;

        --hc-text: #302b3d;

        --hc-text-soft: #777185;


        /* ----------------------------------------------------
           MAIN ACCENT COLORS
        ---------------------------------------------------- */

        --hc-purple: #8e7cc3;

        --hc-pink: #d99ac5;

        --hc-blue: #8bb8d9;

        --hc-green: #91c7aa;

        --hc-yellow: #e8c97d;

        --hc-orange: #e5aa82;

        --hc-red: #d98f8f;

        --hc-teal: #8dc8c1;


        /* ----------------------------------------------------
           COURSE CARD PASTEL COLORS
        ---------------------------------------------------- */

        --hc-blue-soft: #e8f3ff;

        --hc-blue-hover: #cfe6ff;


        --hc-orange-soft: #fff0e4;

        --hc-orange-hover: #ffd8bd;


        --hc-green-soft: #e7f7ee;

        --hc-green-hover: #c9ecd8;


        --hc-purple-soft: #f0eaff;

        --hc-purple-hover: #ddd0ff;


        --hc-yellow-soft: #fff8dc;

        --hc-yellow-hover: #ffedaa;


        --hc-teal-soft: #e4f7f5;

        --hc-teal-hover: #c5ebe7;


        --hc-red-soft: #fdeaea;


        /* ----------------------------------------------------
           EXTRA COLORS
        ---------------------------------------------------- */

        --hc-purple-text: #725caf;

        --hc-ring-empty: #ececf5;


        /* ----------------------------------------------------
           RADIUS
        ---------------------------------------------------- */

        --hc-radius-sm: 8px;

        --hc-radius-md: 12px;

        --hc-radius-lg: 18px;


        /* ----------------------------------------------------
           SHADOW
        ---------------------------------------------------- */

        --hc-shadow:
            0 8px 24px rgba(60, 45, 90, 0.08);

    }


    /* ========================================================
       MAIN STREAMLIT APP
    ======================================================== */

    .stApp {

        background:
            var(--hc-bg) !important;

        color:
            var(--hc-text) !important;
    }


    .main {

        background:
            var(--hc-bg) !important;
    }


    .block-container {

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       FONT
    ======================================================== */

    html,
    body,
    [class*="css"] {

        font-family:
            "Segoe UI",
            Arial,
            Helvetica,
            sans-serif;
    }


    /* ========================================================
       HEADINGS
    ======================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       HEADER
    ======================================================== */

    header[data-testid="stHeader"] {

        background:
            var(--hc-bg) !important;
    }


    [data-testid="stHeader"] {

        background:
            var(--hc-bg) !important;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            var(--hc-surface) !important;

        border-right:
            1px solid var(--hc-border);
    }


    section[data-testid="stSidebar"] * {

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       CARDS
    ======================================================== */

    .hc-card {

        background:
            var(--hc-surface);

        border:
            1px solid var(--hc-border);

        border-radius:
            var(--hc-radius-lg);

        box-shadow:
            var(--hc-shadow);
    }


    /* ========================================================
       DEFAULT BUTTON
    ======================================================== */

    .stButton > button {

        background:
            var(--hc-surface) !important;

        color:
            var(--hc-text) !important;

        border:
            1px solid var(--hc-border) !important;

        border-radius:
            var(--hc-radius-md) !important;

        transition:
            all 0.2s ease !important;
    }


    .stButton > button:hover {

        background:
            var(--hc-surface-2) !important;

        border-color:
            var(--hc-purple) !important;

        color:
            var(--hc-purple) !important;
    }


    /* ========================================================
       INPUTS
    ======================================================== */

    input,
    textarea,
    select {

        background:
            var(--hc-surface) !important;

        color:
            var(--hc-text) !important;

        border-color:
            var(--hc-border) !important;
    }


    [data-baseweb="input"],
    [data-baseweb="textarea"],
    [data-baseweb="select"] {

        background:
            var(--hc-surface) !important;

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    [data-baseweb="select"] > div {

        background:
            var(--hc-surface) !important;

        border-color:
            var(--hc-border) !important;

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       CHECKBOX
    ======================================================== */

    [data-testid="stCheckbox"] label {

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       EXPANDER
    ======================================================== */

    [data-testid="stExpander"] {

        background:
            var(--hc-surface) !important;

        border:
            1px solid var(--hc-border) !important;

        border-radius:
            var(--hc-radius-md) !important;
    }


    /* ========================================================
       TABS
    ======================================================== */

    button[data-baseweb="tab"] {

        color:
            var(--hc-text-soft) !important;
    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            var(--hc-purple) !important;
    }


    /* ========================================================
       DATAFRAME
    ======================================================== */

    [data-testid="stDataFrame"] {

        border:
            1px solid var(--hc-border);

        border-radius:
            var(--hc-radius-md);
    }


    /* ========================================================
       ALERTS
    ======================================================== */

    [data-testid="stAlert"] {

        background:
            var(--hc-surface-2) !important;

        border:
            1px solid var(--hc-border) !important;

        color:
            var(--hc-text) !important;
    }


    /* ========================================================
       SCROLLBAR
    ======================================================== */

    ::-webkit-scrollbar {

        width: 8px;

        height: 8px;
    }


    ::-webkit-scrollbar-track {

        background:
            var(--hc-bg);
    }


    ::-webkit-scrollbar-thumb {

        background:
            var(--hc-border);

        border-radius:
            10px;
    }


    ::-webkit-scrollbar-thumb:hover {

        background:
            var(--hc-purple);
    }


    /* ========================================================
       HIDE DEFAULT STREAMLIT UI
    ======================================================== */

    #MainMenu {

        visibility: hidden;
    }


    footer {

        visibility: hidden;
    }


    </style>

    """


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================
#
# Agar kisi purani file me:
#
# from theme import THEME_CSS
#
# use ho raha hai, to error nahi aayega.
#

THEME_CSS = get_theme_css()