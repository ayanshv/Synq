"""Synq visual design system.

This module owns the CSS that defines Synq's look and feel. Keeping all
styling in one place means a designer can tweak the brand without hunting
through every page module. `layout.py` exposes reusable Python helpers that
apply these classes, so page code stays clean and declarative.

Design language:
    - warm off-white backgrounds, near-black text, muted gray for secondary text
    - a single restrained slate-blue accent, used sparingly
    - large editorial serif headings (Fraunces) over a clean sans body (Inter)
    - generous whitespace, hairline borders, soft restrained shadows, rounded cards
    - calm, confident, and quietly expensive rather than flashy
"""

from nicegui import ui

# All custom classes are prefixed with `synq-` to avoid colliding with the
# Tailwind and Quasar classes that NiceGUI ships with.
_THEME_CSS = """
<style>
:root {
    /* Color palette - intentionally limited: bg + 2 surfaces + ink scale + 1 accent. */
    --synq-bg: #f6f5f1;            /* warm off-white page background */
    --synq-surface: #fffefb;       /* card / panel surface */
    --synq-surface-2: #efece5;     /* subtle raised / inset surface */
    --synq-border: #e9e5dd;        /* hairline warm border */
    --synq-border-strong: #dbd6cc;
    --synq-ink: #1a1a1c;           /* near-black primary text */
    --synq-ink-2: #57575e;         /* muted gray secondary text */
    --synq-ink-3: #97959c;         /* tertiary / placeholder text */
    --synq-accent: #43648f;        /* restrained slate-blue accent */
    --synq-accent-strong: #375580;
    --synq-accent-soft: #edf1f7;   /* very light blue tint */
    --synq-accent-line: rgba(67, 100, 143, 0.16);
    --synq-success: #557f64;
    --synq-warning: #b3823c;
    --synq-error: #a95645;
    /* Soft, low-contrast shadows keep the surface calm. */
    --synq-shadow: 0 1px 2px rgba(26, 26, 28, 0.03), 0 6px 20px rgba(26, 26, 28, 0.04);
    --synq-shadow-sm: 0 1px 2px rgba(26, 26, 28, 0.04);
    --synq-shadow-lift: 0 2px 4px rgba(26, 26, 28, 0.04), 0 14px 36px rgba(26, 26, 28, 0.07);
    --synq-radius: 18px;
    --synq-radius-lg: 22px;
    --synq-radius-sm: 11px;
    --synq-radius-pill: 999px;
    --synq-ease: cubic-bezier(0.22, 0.61, 0.36, 1);
}

/* Page background + base typography. */
.synq-page {
    background-color: var(--synq-bg);
    background-image: radial-gradient(120% 60% at 50% -12%, rgba(67, 100, 143, 0.05), transparent 60%);
    background-repeat: no-repeat;
    color: var(--synq-ink);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-feature-settings: 'cv11', 'ss01';
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    min-height: 100vh;
}

/* ---- Typography helpers ---- */
.synq-display {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-weight: 460;
    font-size: clamp(2.5rem, 5vw, 3.75rem);
    line-height: 1.05;
    letter-spacing: -0.025em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-weight: 480;
    font-size: clamp(1.95rem, 3.5vw, 2.7rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h2 {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-weight: 480;
    font-size: 1.55rem;
    line-height: 1.2;
    letter-spacing: -0.015em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--synq-accent);
    margin: 0;
}
.synq-body {
    font-size: 1.05rem;
    line-height: 1.62;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-body-lg {
    font-size: 1.2rem;
    line-height: 1.58;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-muted {
    font-size: 0.94rem;
    line-height: 1.55;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-label {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.005em;
    color: var(--synq-ink-2);
    margin: 0;
}

/* ---- Navigation bar ---- */
.synq-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 20px 0;
    background: transparent;
    border: none;
}
.synq-nav-brand {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-weight: 560;
    font-size: 1.4rem;
    letter-spacing: -0.02em;
    color: var(--synq-ink);
    text-decoration: none;
}
.synq-nav-brand .synq-nav-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--synq-accent);
    margin-left: 3px;
    vertical-align: middle;
}
.synq-nav-links {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
    background: rgba(255, 254, 251, 0.55);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius-pill);
    padding: 4px;
    backdrop-filter: blur(8px);
}
.synq-nav-pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    border-radius: var(--synq-radius-pill);
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--synq-ink-2);
    text-decoration: none;
    border: 1px solid transparent;
    transition: color 0.2s var(--synq-ease), background 0.2s var(--synq-ease);
}
.synq-nav-pill:hover {
    color: var(--synq-ink);
    background: var(--synq-surface-2);
}
.synq-nav-pill.synq-active {
    color: var(--synq-ink);
    background: var(--synq-surface);
    border-color: var(--synq-border);
    box-shadow: var(--synq-shadow-sm);
}
.synq-user-menu { margin-left: 12px; }
.synq-avatar {
    width: 36px; height: 36px; min-height: 36px;
    padding: 0; border-radius: 50%;
    background: var(--synq-ink); color: #fffdfb;
    font-size: 0.72rem; font-weight: 700;
    transition: transform 0.2s var(--synq-ease), box-shadow 0.2s var(--synq-ease);
}
.synq-avatar:hover { transform: translateY(-1px); box-shadow: var(--synq-shadow-sm); }
.synq-avatar-small {
    width: 38px; height: 38px; min-height: 38px;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0; background: var(--synq-accent-soft); color: var(--synq-accent);
}
.synq-dashboard-intro { display: flex; flex-direction: column; gap: 12px; padding: 20px 0 14px; }
.synq-dashboard-section { display: flex; flex-direction: column; gap: 18px; }
.synq-stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.synq-dashboard-grid { display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.8fr); gap: 48px; align-items: start; }
.synq-dashboard-main, .synq-dashboard-side { display: flex; flex-direction: column; gap: 38px; min-width: 0; }
.synq-goal-list, .synq-update-list { display: flex; flex-direction: column; gap: 24px; }
.synq-goal-list { padding: 4px 26px; }
.synq-goal-row { display: flex; flex-direction: column; gap: 12px; padding: 22px 0; border-bottom: 1px solid var(--synq-border); }
.synq-goal-row:last-child { border-bottom: 0; }
.synq-goal-heading, .synq-update-topline, .synq-meeting-title-row, .synq-timeline-heading {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;
}
.synq-goal-title { font-size: 1.05rem; font-weight: 600; color: var(--synq-ink); }
.synq-goal-meta { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.synq-goal-percent { font-family: 'Fraunces', Georgia, serif; font-optical-sizing: auto; font-size: 1.2rem; color: var(--synq-ink); }
.synq-update-card { display: flex; flex-direction: column; gap: 16px; }
.synq-person { display: flex; align-items: center; gap: 12px; }
.synq-update-name, .synq-timeline-person { font-weight: 600; color: var(--synq-ink); }
.synq-update-detail { display: flex; flex-direction: column; gap: 5px; padding-top: 14px; border-top: 1px solid var(--synq-border); }
.synq-detail-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--synq-ink-3); }
.synq-detail-text { font-size: 0.96rem; line-height: 1.55; color: var(--synq-ink-2); }
.synq-update-detail.synq-blocker { border-top-color: rgba(179, 130, 60, 0.35); }
.synq-update-detail.synq-blocker .synq-detail-label { color: var(--synq-warning); }
.synq-meeting-card { display: flex; flex-direction: column; gap: 15px; padding: 26px; border: 1px solid rgba(85, 127, 100, 0.22); border-radius: var(--synq-radius); background: rgba(85, 127, 100, 0.06); }
.synq-meeting-card.synq-meeting-alert { border-color: rgba(179, 130, 60, 0.28); background: rgba(179, 130, 60, 0.07); }
.synq-meeting-title { font-family: 'Fraunces', Georgia, serif; font-optical-sizing: auto; font-size: 1.5rem; line-height: 1.15; color: var(--synq-ink); }
.synq-timeline { display: flex; flex-direction: column; gap: 0; padding: 8px 24px; }
.synq-timeline-item { display: grid; grid-template-columns: 14px 1fr; gap: 16px; padding: 20px 0; border-bottom: 1px solid var(--synq-border); }
.synq-timeline-item:last-child { border-bottom: 0; }
.synq-timeline-dot { width: 9px; height: 9px; margin-top: 7px; border: 2px solid var(--synq-accent); border-radius: 50%; background: var(--synq-surface); box-shadow: 0 0 0 4px var(--synq-accent-soft); }
.synq-timeline-copy { display: flex; flex-direction: column; gap: 6px; }
.synq-timeline-copy .synq-body { font-size: 0.94rem; }
.synq-work-flow { max-width: 760px; }
.synq-work-status { display: flex; flex-direction: column; gap: 16px; }
.synq-private-card { display: flex; flex-direction: column; gap: 16px; }
.synq-private-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.synq-activity-list { gap: 0; }
.synq-activity-row { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 0; border-bottom: 1px solid var(--synq-border); transition: padding-left 0.2s var(--synq-ease); }
.synq-activity-row:last-child { border-bottom: 0; }
.synq-activity-row:hover { padding-left: 4px; }
.synq-activity-copy { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.synq-activity-title { color: var(--synq-ink); font-size: 1rem; line-height: 1.45; }
.synq-remove-button { color: var(--synq-ink-3); transition: color 0.18s var(--synq-ease); }
.synq-remove-button:hover { color: var(--synq-error); }
.synq-work-consent { display: flex; flex-direction: column; gap: 15px; padding: 8px 0; }
.synq-review-notice { display: flex; flex-direction: column; gap: 6px; padding: 20px 22px; border-left: 3px solid var(--synq-accent); border-radius: 0 var(--synq-radius-sm) var(--synq-radius-sm) 0; background: var(--synq-accent-soft); }
.synq-review-notice-title { color: var(--synq-ink); font-weight: 600; }
.synq-editor-card { display: flex; flex-direction: column; gap: 14px; }
.synq-editor-field { width: 100%; }
.synq-include-grid { display: flex; gap: 24px; flex-wrap: wrap; padding: 10px 0; border-top: 1px solid var(--synq-border); border-bottom: 1px solid var(--synq-border); }
.synq-editor-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.synq-goals-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
.synq-goal-card { display: flex; flex-direction: column; gap: 24px; }
.synq-goal-card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; }
.synq-goal-card-copy { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.synq-goal-card-title { font-family: 'Fraunces', Georgia, serif; font-optical-sizing: auto; font-size: 1.5rem; line-height: 1.18; color: var(--synq-ink); }
.synq-goal-card-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.synq-goal-edit { color: var(--synq-ink-3); transition: color 0.18s var(--synq-ease); }
.synq-goal-edit:hover { color: var(--synq-ink); }
.synq-goal-progress-block { display: flex; flex-direction: column; gap: 12px; }
.synq-goal-progress-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }
.synq-goal-progress-value { font-family: 'Fraunces', Georgia, serif; font-optical-sizing: auto; font-size: 2.5rem; line-height: 1; letter-spacing: -0.02em; color: var(--synq-ink); }
.synq-goal-progress-track { height: 8px; border-radius: 999px; overflow: hidden; }
.synq-goal-details { display: flex; gap: 20px; flex-wrap: wrap; padding-top: 16px; border-top: 1px solid var(--synq-border); }
.synq-goal-form { display: flex; flex-direction: column; gap: 14px; max-width: 720px; }
.synq-goal-dialog { width: min(560px, calc(100vw - 32px)); display: flex; flex-direction: column; gap: 14px; padding: 30px; }
.synq-settings-card { display: flex; flex-direction: column; gap: 0; }
.synq-settings-row { padding: 16px 0; border-bottom: 1px solid var(--synq-border); }
.synq-settings-row:first-child { padding-top: 0; }
.synq-settings-row:last-child { padding-bottom: 0; border-bottom: 0; }
.synq-settings-name { color: var(--synq-ink); font-size: 1rem; font-weight: 600; }
.synq-settings-toggle { padding: 14px 0; }
.synq-settings-toggle:first-child { padding-top: 0; }
.synq-settings-toggle + .synq-settings-toggle { border-top: 1px solid var(--synq-border); }
.synq-exclusion-list { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 28px; margin-top: 10px; }
.synq-settings-checkbox { grid-column: 1; }
.synq-settings-checkbox-help { grid-column: 2; align-self: center; }
.synq-review-settings { display: flex; flex-direction: column; gap: 24px; }
.synq-review-statement { padding: 22px; border-left: 3px solid var(--synq-success); border-radius: 0 var(--synq-radius-sm) var(--synq-radius-sm) 0; background: rgba(85, 127, 100, 0.07); }
.synq-review-statement-text { color: var(--synq-ink); font-family: 'Fraunces', Georgia, serif; font-optical-sizing: auto; font-size: 1.4rem; line-height: 1.3; }
.synq-visibility-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0; }
.synq-visibility-item { padding: 20px 24px; }
.synq-visibility-item:nth-child(odd) { border-right: 1px solid var(--synq-border); }
.synq-visibility-item:nth-child(-n+2) { border-bottom: 1px solid var(--synq-border); }

/* ---- Buttons ---- */
.synq-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 24px;
    border-radius: var(--synq-radius-pill);
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.005em;
    cursor: pointer;
    border: 1px solid transparent;
    transition: transform 0.18s var(--synq-ease), background 0.18s var(--synq-ease),
                box-shadow 0.18s var(--synq-ease), border-color 0.18s var(--synq-ease);
    text-decoration: none;
    line-height: 1;
}
.synq-btn:active { transform: translateY(0); }
.synq-btn-primary {
    background: var(--synq-ink);
    color: #fffdfb;
}
.synq-btn-primary:hover {
    background: #2c2c30;
    transform: translateY(-1px);
    box-shadow: var(--synq-shadow-sm);
}
.synq-btn-secondary {
    background: transparent;
    color: var(--synq-ink);
    border-color: var(--synq-border-strong);
}
.synq-btn-secondary:hover {
    background: var(--synq-surface);
    border-color: var(--synq-ink-3);
    transform: translateY(-1px);
}
.synq-btn-accent {
    background: var(--synq-accent);
    color: #fff;
}
.synq-btn-accent:hover {
    background: var(--synq-accent-strong);
    transform: translateY(-1px);
    box-shadow: var(--synq-shadow-sm);
}

/* Accessible focus ring for keyboard users. */
.synq-btn:focus-visible,
.synq-nav-pill:focus-visible {
    outline: 2px solid var(--synq-accent);
    outline-offset: 2px;
}

/* ---- Cards / panels ---- */
.synq-card {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    box-shadow: var(--synq-shadow);
    padding: 26px;
    transition: border-color 0.2s var(--synq-ease), box-shadow 0.2s var(--synq-ease);
}
.synq-panel {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius-lg);
    padding: 30px;
}
.synq-panel-accent {
    background: linear-gradient(165deg, var(--synq-accent-soft) 0%, var(--synq-surface) 72%);
    border: 1px solid var(--synq-accent-line);
    border-radius: var(--synq-radius-lg);
    padding: 30px;
}

/* ---- Stat card ---- */
.synq-stat {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    padding: 22px 24px;
    box-shadow: var(--synq-shadow-sm);
    transition: transform 0.2s var(--synq-ease), box-shadow 0.2s var(--synq-ease), border-color 0.2s var(--synq-ease);
}
.synq-stat:hover {
    transform: translateY(-2px);
    box-shadow: var(--synq-shadow);
    border-color: var(--synq-border-strong);
}
.synq-stat-value {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-weight: 460;
    font-size: 2.2rem;
    line-height: 1;
    letter-spacing: -0.02em;
    color: var(--synq-ink);
    margin: 8px 0 0 0;
}
.synq-stat-label {
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.1em;
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
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    line-height: 1.4;
}
.synq-badge-neutral { background: var(--synq-surface-2); color: var(--synq-ink-2); }
.synq-badge-accent { background: var(--synq-accent-soft); color: var(--synq-accent); }
.synq-badge-success { background: rgba(85, 127, 100, 0.12); color: var(--synq-success); }
.synq-badge-warning { background: rgba(179, 130, 60, 0.14); color: var(--synq-warning); }

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
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 6px;
    padding: 56px 28px;
    border: 1px dashed var(--synq-border-strong);
    border-radius: var(--synq-radius);
    background: linear-gradient(180deg, var(--synq-surface) 0%, rgba(255, 254, 251, 0.4) 100%);
}
.synq-empty-title {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-size: 1.3rem;
    color: var(--synq-ink);
    margin: 0 0 2px 0;
}
.synq-empty-msg {
    font-size: 0.98rem;
    line-height: 1.55;
    color: var(--synq-ink-3);
    margin: 0;
    max-width: 40ch;
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
    gap: 26px;
    padding: 64px 0 44px 0;
}
.synq-hero .synq-display {
    font-size: clamp(2.9rem, 7vw, 5.4rem);
    line-height: 1.0;
    letter-spacing: -0.035em;
    max-width: 16ch;
}
.synq-hero .synq-body-lg {
    max-width: 46ch;
    font-size: 1.24rem;
    line-height: 1.5;
}
.synq-hero-cta {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 6px;
}

/* ---- Product preview ---- */
.synq-preview {
    margin: 20px 0 0 0;
    padding: 16px;
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius-lg);
    box-shadow: var(--synq-shadow-lift);
}
.synq-preview-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px 14px 10px;
}
.synq-preview-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--synq-border-strong);
}
.synq-preview-body {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 16px;
}
.synq-preview-col {
    display: flex;
    flex-direction: column;
    gap: 16px;
}
.synq-preview-card {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius-sm);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.synq-preview-card-title {
    font-family: 'Fraunces', Georgia, serif;
    font-optical-sizing: auto;
    font-size: 1.05rem;
    font-weight: 480;
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
    transition: width 0.6s var(--synq-ease);
}
.synq-preview-meeting {
    background: linear-gradient(165deg, var(--synq-accent-soft) 0%, var(--synq-surface) 80%);
    border: 1px solid var(--synq-accent-line);
    border-radius: var(--synq-radius-sm);
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ---- Responsive ---- */
.synq-container {
    width: 100%;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
    box-sizing: border-box;
}
.synq-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 36px 0 72px 0;
    animation: synq-enter 0.5s var(--synq-ease) both;
}

/* Subtle page-enter transition (respects reduced-motion below). */
@keyframes synq-enter {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: none; }
}

@media (max-width: 860px) {
    .synq-preview-body { grid-template-columns: 1fr; }
    .synq-dashboard-grid { grid-template-columns: 1fr; gap: 38px; }
}
@media (max-width: 640px) {
    .synq-nav { padding: 16px 0; flex-wrap: wrap; gap: 12px; }
    .synq-container { padding: 0 16px; }
    .synq-content { gap: 24px; padding: 26px 0 52px 0; }
    .synq-card { padding: 20px; }
    .synq-panel, .synq-panel-accent { padding: 22px; }
    .synq-nav-pill { padding: 7px 13px; font-size: 0.84rem; }
    .synq-hero { padding: 36px 0 26px 0; gap: 20px; }
    .synq-preview { padding: 12px; }
    .synq-preview-card { padding: 16px; }
    .synq-stat-grid { grid-template-columns: repeat(2, 1fr); }
    .synq-goal-heading, .synq-update-topline, .synq-meeting-title-row { flex-direction: column; }
    .synq-nav-links { justify-content: flex-end; }
    .synq-user-menu { margin-left: 0; }
    .synq-goals-list { grid-template-columns: 1fr; }
    .synq-goal-card-top { flex-direction: column; }
    .synq-exclusion-list, .synq-visibility-grid { grid-template-columns: 1fr; }
    .synq-settings-checkbox-help { grid-column: 1; padding-left: 32px; margin-top: -7px; margin-bottom: 6px; }
    .synq-visibility-item:nth-child(odd) { border-right: 0; }
    .synq-visibility-item:nth-child(-n+3) { border-bottom: 1px solid var(--synq-border); }
}

/* Respect users who prefer reduced motion. */
@media (prefers-reduced-motion: reduce) {
    .synq-content { animation: none; }
    .synq-btn, .synq-stat, .synq-avatar, .synq-activity-row, .synq-progress-fill { transition: none; }
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
