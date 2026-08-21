"""Synq visual design system.

This module owns the CSS that defines Synq's look and feel. Keeping all
styling in one place means a designer can tweak the brand without hunting
through every page module. `layout.py` exposes reusable Python helpers that
apply these classes, so page code stays clean and declarative.

Design language:
    - warm off-white backgrounds, near-black text, muted gray for secondary text
    - a single soft blue accent, used sparingly
    - large editorial serif headings (Fraunces) over a clean sans body (Inter)
    - generous whitespace, subtle borders, restrained shadows, rounded cards
    - calm rather than flashy
"""

from nicegui import ui

# All custom classes are prefixed with `synq-` to avoid colliding with the
# Tailwind and Quasar classes that NiceGUI ships with.
_THEME_CSS = """
<style>
:root {
    /* Color palette - intentionally limited. */
    --synq-bg: #f7f6f3;            /* warm off-white page background */
    --synq-surface: #fffefb;       /* card / panel surface */
    --synq-surface-2: #f1efea;     /* subtle raised surface */
    --synq-border: #e7e4dd;        /* subtle warm border */
    --synq-border-strong: #d8d4cb;
    --synq-ink: #1c1c1e;           /* near-black primary text */
    --synq-ink-2: #5c5c63;          /* muted gray secondary text */
    --synq-ink-3: #9a9aa1;          /* tertiary / placeholder text */
    --synq-accent: #4a6fa5;         /* soft blue accent */
    --synq-accent-soft: #eaf1f9;    /* very light blue tint */
    --synq-accent-grad: linear-gradient(135deg, #eef4fb 0%, #f7f6f3 70%);
    --synq-success: #5b8c6a;
    --synq-warning: #c08a3e;
    --synq-error: #b05c4a;
    --synq-shadow: 0 1px 2px rgba(28, 28, 30, 0.04), 0 4px 16px rgba(28, 28, 30, 0.04);
    --synq-shadow-sm: 0 1px 2px rgba(28, 28, 30, 0.05);
    --synq-radius: 16px;
    --synq-radius-sm: 10px;
    --synq-radius-pill: 999px;
}

/* Page background + base typography. */
.synq-page {
    background-color: var(--synq-bg);
    background-image: radial-gradient(circle at 18% -10%, rgba(74, 111, 165, 0.06), transparent 45%);
    color: var(--synq-ink);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
}

/* ---- Typography helpers ---- */
.synq-display {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    line-height: 1.08;
    letter-spacing: -0.02em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(1.9rem, 3.5vw, 2.6rem);
    line-height: 1.12;
    letter-spacing: -0.015em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h2 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 1.5rem;
    line-height: 1.2;
    letter-spacing: -0.01em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--synq-accent);
    margin: 0;
}
.synq-body {
    font-size: 1.0625rem;
    line-height: 1.6;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-body-lg {
    font-size: 1.2rem;
    line-height: 1.55;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-muted {
    font-size: 0.95rem;
    line-height: 1.55;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-label {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: var(--synq-ink-2);
    margin: 0;
}

/* ---- Navigation bar ---- */
.synq-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 18px 0;
    background: transparent;
    border: none;
}
.synq-nav-brand {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 600;
    font-size: 1.35rem;
    letter-spacing: -0.01em;
    color: var(--synq-ink);
    text-decoration: none;
}
.synq-nav-brand .synq-nav-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--synq-accent);
    margin-left: 3px;
    vertical-align: middle;
}
.synq-nav-links {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
}
.synq-nav-pill {
    display: inline-flex;
    align-items: center;
    padding: 7px 15px;
    border-radius: var(--synq-radius-pill);
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--synq-ink-2);
    text-decoration: none;
    border: 1px solid transparent;
    transition: all 0.18s ease;
}
.synq-nav-pill:hover {
    color: var(--synq-ink);
    background: var(--synq-surface-2);
}
.synq-nav-pill.synq-active {
    color: var(--synq-accent);
    background: var(--synq-accent-soft);
    border-color: rgba(74, 111, 165, 0.16);
}
.synq-user-menu { margin-left: 10px; }
.synq-avatar {
    width: 34px; height: 34px; min-height: 34px;
    padding: 0; border-radius: 50%;
    background: var(--synq-ink); color: #fffdfb;
    font-size: 0.72rem; font-weight: 700;
}
.synq-avatar-small {
    width: 38px; height: 38px; min-height: 38px;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0; background: var(--synq-accent-soft); color: var(--synq-accent);
}
.synq-dashboard-intro { display: flex; flex-direction: column; gap: 10px; padding: 18px 0 10px; }
.synq-dashboard-section { display: flex; flex-direction: column; gap: 16px; }
.synq-stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.synq-dashboard-grid { display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.8fr); gap: 42px; align-items: start; }
.synq-dashboard-main, .synq-dashboard-side { display: flex; flex-direction: column; gap: 34px; min-width: 0; }
.synq-goal-list, .synq-update-list { display: flex; flex-direction: column; gap: 24px; }
.synq-goal-list { padding: 4px 24px; }
.synq-goal-row { display: flex; flex-direction: column; gap: 11px; padding: 20px 0; border-bottom: 1px solid var(--synq-border); }
.synq-goal-row:last-child { border-bottom: 0; }
.synq-goal-heading, .synq-update-topline, .synq-meeting-title-row, .synq-timeline-heading {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;
}
.synq-goal-title { font-size: 1.04rem; font-weight: 600; color: var(--synq-ink); }
.synq-goal-meta { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.synq-goal-percent { font-family: 'Fraunces', Georgia, serif; font-size: 1.15rem; color: var(--synq-ink); }
.synq-update-card { display: flex; flex-direction: column; gap: 16px; }
.synq-person { display: flex; align-items: center; gap: 12px; }
.synq-update-name, .synq-timeline-person { font-weight: 600; color: var(--synq-ink); }
.synq-update-detail { display: flex; flex-direction: column; gap: 4px; padding-top: 13px; border-top: 1px solid var(--synq-border); }
.synq-detail-label { font-size: 0.74rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--synq-ink-3); }
.synq-detail-text { font-size: 0.96rem; line-height: 1.5; color: var(--synq-ink-2); }
.synq-update-detail.synq-blocker { border-top-color: rgba(192, 138, 62, 0.35); }
.synq-update-detail.synq-blocker .synq-detail-label { color: var(--synq-warning); }
.synq-meeting-card { display: flex; flex-direction: column; gap: 15px; padding: 24px; border: 1px solid rgba(91, 140, 106, 0.25); border-radius: var(--synq-radius); background: rgba(91, 140, 106, 0.07); }
.synq-meeting-card.synq-meeting-alert { border-color: rgba(192, 138, 62, 0.3); background: rgba(192, 138, 62, 0.08); }
.synq-meeting-title { font-family: 'Fraunces', Georgia, serif; font-size: 1.45rem; line-height: 1.15; color: var(--synq-ink); }
.synq-timeline { display: flex; flex-direction: column; gap: 0; padding: 8px 22px; }
.synq-timeline-item { display: grid; grid-template-columns: 14px 1fr; gap: 14px; padding: 18px 0; border-bottom: 1px solid var(--synq-border); }
.synq-timeline-item:last-child { border-bottom: 0; }
.synq-timeline-dot { width: 8px; height: 8px; margin-top: 7px; border: 2px solid var(--synq-accent); border-radius: 50%; background: var(--synq-surface); }
.synq-timeline-copy { display: flex; flex-direction: column; gap: 6px; }
.synq-timeline-copy .synq-body { font-size: 0.94rem; }
.synq-work-flow { max-width: 760px; }
.synq-work-status { display: flex; flex-direction: column; gap: 16px; }
.synq-private-card { display: flex; flex-direction: column; gap: 16px; }
.synq-private-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.synq-activity-list { gap: 0; }
.synq-activity-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 17px 0; border-bottom: 1px solid var(--synq-border); }
.synq-activity-row:last-child { border-bottom: 0; }
.synq-activity-copy { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.synq-activity-title { color: var(--synq-ink); font-size: 1rem; line-height: 1.45; }
.synq-remove-button { color: var(--synq-ink-3); }
.synq-remove-button:hover { color: var(--synq-error); }
.synq-work-consent { display: flex; flex-direction: column; gap: 15px; padding: 8px 0; }
.synq-review-notice { display: flex; flex-direction: column; gap: 5px; padding: 18px 20px; border-left: 3px solid var(--synq-accent); background: var(--synq-accent-soft); }
.synq-review-notice-title { color: var(--synq-ink); font-weight: 600; }
.synq-editor-card { display: flex; flex-direction: column; gap: 14px; }
.synq-editor-field { width: 100%; }
.synq-include-grid { display: flex; gap: 22px; flex-wrap: wrap; padding: 8px 0; border-top: 1px solid var(--synq-border); border-bottom: 1px solid var(--synq-border); }
.synq-editor-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.synq-goals-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.synq-goal-card { display: flex; flex-direction: column; gap: 24px; }
.synq-goal-card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; }
.synq-goal-card-copy { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.synq-goal-card-title { font-family: 'Fraunces', Georgia, serif; font-size: 1.5rem; line-height: 1.18; color: var(--synq-ink); }
.synq-goal-card-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.synq-goal-edit { color: var(--synq-ink-3); }
.synq-goal-progress-block { display: flex; flex-direction: column; gap: 10px; }
.synq-goal-progress-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }
.synq-goal-progress-value { font-family: 'Fraunces', Georgia, serif; font-size: 2.4rem; line-height: 1; color: var(--synq-ink); }
.synq-goal-progress-track { height: 9px; border-radius: 999px; overflow: hidden; }
.synq-goal-details { display: flex; gap: 18px; flex-wrap: wrap; padding-top: 15px; border-top: 1px solid var(--synq-border); }
.synq-goal-form { display: flex; flex-direction: column; gap: 14px; max-width: 720px; }
.synq-goal-dialog { width: min(560px, calc(100vw - 32px)); display: flex; flex-direction: column; gap: 14px; padding: 28px; }

/* ---- Buttons ---- */
.synq-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 22px;
    border-radius: var(--synq-radius-pill);
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.18s ease;
    text-decoration: none;
    line-height: 1;
}
.synq-btn-primary {
    background: var(--synq-ink);
    color: #fffdfb;
}
.synq-btn-primary:hover {
    background: #2a2a2e;
    box-shadow: var(--synq-shadow-sm);
}
.synq-btn-secondary {
    background: transparent;
    color: var(--synq-ink);
    border-color: var(--synq-border-strong);
}
.synq-btn-secondary:hover {
    background: var(--synq-surface-2);
    border-color: var(--synq-ink-3);
}
.synq-btn-accent {
    background: var(--synq-accent);
    color: #fff;
}
.synq-btn-accent:hover {
    background: #3d5e8c;
    box-shadow: var(--synq-shadow-sm);
}

/* ---- Cards / panels ---- */
.synq-card {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    box-shadow: var(--synq-shadow);
    padding: 24px;
}
.synq-panel {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    padding: 28px;
}
.synq-panel-accent {
    background: var(--synq-accent-grad);
    border: 1px solid rgba(74, 111, 165, 0.14);
    border-radius: var(--synq-radius);
    padding: 28px;
}

/* ---- Stat card ---- */
.synq-stat {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    padding: 22px 24px;
    box-shadow: var(--synq-shadow-sm);
}
.synq-stat-value {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 2.1rem;
    line-height: 1;
    color: var(--synq-ink);
    margin: 6px 0 0 0;
}
.synq-stat-label {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-stat-hint {
    font-size: 0.85rem;
    color: var(--synq-ink-3);
    margin: 8px 0 0 0;
}

/* ---- Badge / pill ---- */
.synq-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: var(--synq-radius-pill);
    font-size: 0.8rem;
    font-weight: 600;
    line-height: 1.4;
}
.synq-badge-neutral { background: var(--synq-surface-2); color: var(--synq-ink-2); }
.synq-badge-accent { background: var(--synq-accent-soft); color: var(--synq-accent); }
.synq-badge-success { background: rgba(91, 140, 106, 0.12); color: var(--synq-success); }
.synq-badge-warning { background: rgba(192, 138, 62, 0.14); color: var(--synq-warning); }

/* ---- Divider ---- */
.synq-divider {
    height: 1px;
    background: var(--synq-border);
    border: none;
    margin: 0;
    width: 100%;
}

/* ---- Empty state ---- */
.synq-empty {
    text-align: center;
    padding: 48px 24px;
    border: 1px dashed var(--synq-border-strong);
    border-radius: var(--synq-radius);
    background: var(--synq-surface);
}
.synq-empty-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.25rem;
    color: var(--synq-ink);
    margin: 0 0 6px 0;
}
.synq-empty-msg {
    font-size: 0.98rem;
    color: var(--synq-ink-3);
    margin: 0;
}

/* ---- Section heading block ---- */
.synq-section-head { margin: 0; }
.synq-section-head .synq-section-sub {
    margin: 8px 0 0 0;
}

/* ---- Hero ---- */
.synq-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 24px;
    padding: 56px 0 40px 0;
}
.synq-hero .synq-display {
    font-size: clamp(2.8rem, 7vw, 5.2rem);
    line-height: 1.02;
    letter-spacing: -0.03em;
    max-width: 16ch;
}
.synq-hero .synq-body-lg {
    max-width: 46ch;
    font-size: 1.22rem;
    line-height: 1.5;
}
.synq-hero-cta {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 4px;
}

/* ---- Product preview ---- */
.synq-preview {
    margin: 16px 0 0 0;
    padding: 14px;
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: 20px;
    box-shadow: 0 1px 2px rgba(28,28,30,0.04), 0 12px 40px rgba(28,28,30,0.07);
}
.synq-preview-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px 12px 10px;
}
.synq-preview-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--synq-border-strong);
}
.synq-preview-body {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 14px;
}
.synq-preview-col {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.synq-preview-card {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.synq-preview-card-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 500;
    color: var(--synq-ink);
    margin: 0;
}
.synq-preview-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}
.synq-preview-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    background: var(--synq-accent-soft);
    color: var(--synq-accent);
    font-size: 0.72rem; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.synq-progress-track {
    height: 6px; border-radius: 999px;
    background: var(--synq-surface-2);
    overflow: hidden;
}
.synq-progress-fill {
    height: 100%; border-radius: 999px;
    background: var(--synq-accent);
}
.synq-preview-meeting {
    background: var(--synq-accent-grad);
    border: 1px solid rgba(74,111,165,0.16);
    border-radius: 14px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ---- Responsive ---- */
.synq-container {
    width: 100%;
    max-width: 1080px;
    margin: 0 auto;
    padding: 0 24px;
    box-sizing: border-box;
}
.synq-content {
    display: flex;
    flex-direction: column;
    gap: 28px;
    padding: 32px 0 64px 0;
}
@media (max-width: 860px) {
    .synq-preview-body { grid-template-columns: 1fr; }
    .synq-dashboard-grid { grid-template-columns: 1fr; gap: 34px; }
}
@media (max-width: 640px) {
    .synq-nav { padding: 14px 0; }
    .synq-container { padding: 0 16px; }
    .synq-content { gap: 22px; padding: 24px 0 48px 0; }
    .synq-card, .synq-panel, .synq-panel-accent { padding: 18px; }
    .synq-nav-pill { padding: 6px 11px; font-size: 0.84rem; }
    .synq-hero { padding: 32px 0 24px 0; gap: 18px; }
    .synq-preview { padding: 10px; }
    .synq-preview-card { padding: 14px; }
    .synq-stat-grid { grid-template-columns: repeat(2, 1fr); }
    .synq-goal-heading, .synq-update-topline, .synq-meeting-title-row { flex-direction: column; }
    .synq-nav-links { justify-content: flex-end; }
    .synq-user-menu { margin-left: 0; }
    .synq-goals-list { grid-template-columns: 1fr; }
    .synq-goal-card-top { flex-direction: column; }
}
</style>
"""


def apply_theme() -> None:
    """Inject the design-system CSS into the current page.

    Called once per page by `page_frame`. Using `add_head_html` keeps the
    styles in the document head so they load before the page renders.
    """
    ui.add_head_html(_THEME_CSS)
    # Load the editorial serif (Fraunces) and clean sans (Inter) from Google Fonts.
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
