"""
Shared design tokens for the light "HC NEXUS" theme.

THEME_CSS is injected once per page (via render_sidebar(), which every
page already calls) rather than duplicated inline in each page file.
Keeping colors/radius/shadow here means changing the palette later is
a one-file edit instead of hunting through every page.
"""

THEME_CSS = """
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
    background: var(--hc-bg);
}

html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
}

header { visibility: hidden; height: 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

.hc-card {
    background: var(--hc-surface);
    border-radius: var(--hc-radius-lg);
    box-shadow: var(--hc-shadow);
    border: 1px solid var(--hc-border);
}

</style>
"""