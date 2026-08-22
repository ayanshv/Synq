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

_THEME_CSS = """
<style>
:root {
    --synq-bg: #f7f6f3;
    --synq-surface: #fffefb;
    --synq-surface-2: #f1efea;
    --synq-border: #e7e4dd;
    --synq-border-strong: #d8d4cb;
    --synq-ink: #1a1a1c;
    --synq-ink-2: #56565e;
    --synq-ink-3: #9a9aa1;
    --synq-accent: #4a6fa5;
    --synq-accent-soft: #eaf1f9;
    --synq-accent-grad: linear-gradient(135deg, #eef4fb 0%, #f7f6f3 72%);
    --synq-success: #5b8c6a;
    --synq-warning: #c08a3e;
    --synq-error: #b05c4a;
    --synq-shadow: 0 1px 2px rgba(26,26,28,0.03), 0 6px 20px rgba(26,26,28,0.035);
    --synq-shadow-sm: 0 1px 2px rgba(26,26,28,0.04);
    --synq-shadow-hover: 0 2px 4px rgba(26,26,28,0.05), 0 10px 28px rgba(26,26,28,0.06);
    --synq-radius: 14px;
    --synq-radius-sm: 10px;
    --synq-radius-pill: 999px;
    --synq-ease: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

* { box-sizing: border-box; }

/* ---- Page background ---- */
.synq-page {
    background-color: var(--synq-bg);
    background-image: radial-gradient(circle at 15% -8%, rgba(74,111,165,0.045), transparent 42%);
    color: var(--synq-ink);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    min-height: 100vh;
}

/* ---- Typography ---- */
.synq-display {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(2.6rem, 6vw, 4.4rem);
    line-height: 1.04;
    letter-spacing: -0.025em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h1 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(2rem, 3.8vw, 2.75rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h2 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 1.4rem;
    line-height: 1.2;
    letter-spacing: -0.012em;
    color: var(--synq-ink);
    margin: 0;
}
.synq-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--synq-accent);
    margin: 0;
}
.synq-body {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-body-lg {
    font-size: 1.18rem;
    line-height: 1.55;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-muted {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-label {
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: var(--synq-ink-2);
    margin: 0;
}

/* ---- Navigation ---- */
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
    font-weight: 600;
    font-size: 1.3rem;
    letter-spacing: -0.012em;
    color: var(--synq-ink);
    text-decoration: none;
    display: inline-flex;
    align-items: baseline;
    gap: 2px;
}
.synq-nav-brand .synq-nav-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--synq-accent);
    margin-left: 2px;
    transform: translateY(-1px);
}
.synq-nav-links {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}
.synq-nav-pill {
    display: inline-flex;
    align-items: center;
    padding: 8px 16px;
    border-radius: var(--synq-radius-pill);
    font-size: 0.88rem;
    font-weight: 500;
    color: var(--synq-ink-2);
    text-decoration: none;
    border: 1px solid transparent;
    transition: all var(--synq-ease);
}
.synq-nav-pill:hover {
    color: var(--synq-ink);
    background: var(--synq-surface-2);
}
.synq-nav-pill.synq-active {
    color: var(--synq-accent);
    background: var(--synq-accent-soft);
    border-color: rgba(74,111,165,0.14);
}
.synq-user-menu { margin-left: 12px; }
.synq-avatar {
    width: 34px; height: 34px; min-height: 34px;
    padding: 0; border-radius: 50%;
    background: var(--synq-ink); color: #fffdfb;
    font-size: 0.72rem; font-weight: 700;
    transition: opacity var(--synq-ease);
}
.synq-avatar:hover { opacity: 0.85; }
.synq-avatar-small {
    width: 36px; height: 36px; min-height: 36px;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    background: var(--synq-accent-soft); color: var(--synq-accent);
    border-radius: 50%;
    font-size: 0.72rem; font-weight: 700;
}

/* ---- Buttons ---- */
.synq-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 22px;
    border-radius: var(--synq-radius-pill);
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all var(--synq-ease);
    text-decoration: none;
    line-height: 1;
    letter-spacing: -0.005em;
}
.synq-btn-primary {
    background: var(--synq-ink);
    color: #fffdfb;
}
.synq-btn-primary:hover {
    background: #2a2a2e;
    box-shadow: var(--synq-shadow-sm);
    transform: translateY(-1px);
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
    transform: translateY(-1px);
}

/* ---- Cards / panels ---- */
.synq-card {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    box-shadow: var(--synq-shadow);
    padding: 26px;
    transition: box-shadow var(--synq-ease);
}
.synq-card:hover {
    box-shadow: var(--synq-shadow-hover);
}
.synq-panel {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    padding: 30px;
}
.synq-panel-accent {
    background: var(--synq-accent-grad);
    border: 1px solid rgba(74,111,165,0.12);
    border-radius: var(--synq-radius);
    padding: 30px;
}

/* ---- Stat card ---- */
.synq-stat {
    background: var(--synq-surface);
    border: 1px solid var(--synq-border);
    border-radius: var(--synq-radius);
    padding: 22px 24px;
    box-shadow: var(--synq-shadow-sm);
    transition: box-shadow var(--synq-ease);
}
.synq-stat:hover { box-shadow: var(--synq-shadow-hover); }
.synq-stat-value {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 2rem;
    line-height: 1;
    color: var(--synq-ink);
    margin: 8px 0 0 0;
    letter-spacing: -0.02em;
}
.synq-stat-label {
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-stat-hint {
    font-size: 0.82rem;
    color: var(--synq-ink-3);
    margin: 10px 0 0 0;
}

/* ---- Badge / pill ---- */
.synq-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 11px;
    border-radius: var(--synq-radius-pill);
    font-size: 0.78rem;
    font-weight: 600;
    line-height: 1.4;
    white-space: nowrap;
}
.synq-badge-neutral { background: var(--synq-surface-2); color: var(--synq-ink-2); }
.synq-badge-accent { background: var(--synq-accent-soft); color: var(--synq-accent); }
.synq-badge-success { background: rgba(91,140,106,0.1); color: var(--synq-success); }
.synq-badge-warning { background: rgba(192,138,62,0.12); color: var(--synq-warning); }

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
    padding: 52px 24px;
    border: 1px dashed var(--synq-border-strong);
    border-radius: var(--synq-radius);
    background: var(--synq-surface);
}
.synq-empty-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--synq-ink);
    margin: 0 0 8px 0;
}
.synq-empty-msg {
    font-size: 0.92rem;
    color: var(--synq-ink-3);
    margin: 0;
    max-width: 36ch;
    margin-left: auto;
    margin-right: auto;
}

/* ---- Section heading ---- */
.synq-section-head { margin: 0; }
.synq-section-head .synq-section-sub {
    margin: 7px 0 0 0;
    font-size: 0.95rem;
}

/* ---- Hero ---- */
.synq-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 22px;
    padding: 64px 0 44px 0;
}
.synq-hero .synq-display {
    font-size: clamp(2.8rem, 7vw, 5rem);
    line-height: 1.02;
    letter-spacing: -0.03em;
    max-width: 15ch;
}
.synq-hero .synq-body-lg {
    max-width: 44ch;
    font-size: 1.22rem;
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
    border-radius: 18px;
    box-shadow: 0 1px 2px rgba(26,26,28,0.03), 0 16px 48px rgba(26,26,28,0.06);
}
.synq-preview-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 8px 14px 8px;
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
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
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
    height: 7px; border-radius: 999px;
    background: var(--synq-surface-2);
    overflow: hidden;
}
.synq-progress-fill {
    height: 100%; border-radius: 999px;
    background: var(--synq-accent);
}
.synq-preview-meeting {
    background: var(--synq-accent-grad);
    border: 1px solid rgba(74,111,165,0.14);
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* ---- Dashboard layout ---- */
.synq-dashboard-intro { display: flex; flex-direction: column; gap: 10px; padding: 20px 0 12px; }
.synq-dashboard-section { display: flex; flex-direction: column; gap: 18px; }
.synq-stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.synq-dashboard-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(300px, 0.8fr);
    gap: 44px;
    align-items: start;
}
.synq-dashboard-main, .synq-dashboard-side {
    display: flex; flex-direction: column; gap: 36px; min-width: 0;
}
.synq-goal-list, .synq-update-list { display: flex; flex-direction: column; gap: 22px; }
.synq-goal-list { padding: 4px 26px; }
.synq-goal-row {
    display: flex; flex-direction: column; gap: 12px;
    padding: 22px 0;
    border-bottom: 1px solid var(--synq-border);
}
.synq-goal-row:last-child { border-bottom: 0; padding-bottom: 4px; }
.synq-goal-row:first-child { padding-top: 4px; }
.synq-goal-heading, .synq-update-topline, .synq-meeting-title-row, .synq-timeline-heading {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;
}
.synq-goal-title { font-size: 1.02rem; font-weight: 600; color: var(--synq-ink); }
.synq-goal-meta { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.synq-goal-percent {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.15rem; color: var(--synq-ink); font-weight: 500;
}
.synq-update-card { display: flex; flex-direction: column; gap: 16px; }
.synq-person { display: flex; align-items: center; gap: 12px; }
.synq-update-name, .synq-timeline-person { font-weight: 600; color: var(--synq-ink); font-size: 0.95rem; }
.synq-update-detail {
    display: flex; flex-direction: column; gap: 5px;
    padding-top: 14px;
    border-top: 1px solid var(--synq-border);
}
.synq-detail-label {
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--synq-ink-3);
}
.synq-detail-text { font-size: 0.94rem; line-height: 1.5; color: var(--synq-ink-2); }
.synq-update-detail.synq-blocker { border-top-color: rgba(192,138,62,0.3); }
.synq-update-detail.synq-blocker .synq-detail-label { color: var(--synq-warning); }
.synq-meeting-card {
    display: flex; flex-direction: column; gap: 16px;
    padding: 26px;
    border: 1px solid rgba(91,140,106,0.22);
    border-radius: var(--synq-radius);
    background: rgba(91,140,106,0.05);
}
.synq-meeting-card.synq-meeting-alert {
    border-color: rgba(192,138,62,0.28);
    background: rgba(192,138,62,0.06);
}
.synq-meeting-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.4rem; line-height: 1.15;
    color: var(--synq-ink); font-weight: 500;
}
.synq-timeline { display: flex; flex-direction: column; gap: 0; padding: 8px 24px; }
.synq-timeline-item {
    display: grid; grid-template-columns: 14px 1fr; gap: 14px;
    padding: 18px 0;
    border-bottom: 1px solid var(--synq-border);
}
.synq-timeline-item:last-child { border-bottom: 0; padding-bottom: 4px; }
.synq-timeline-item:first-child { padding-top: 4px; }
.synq-timeline-dot {
    width: 8px; height: 8px; margin-top: 7px;
    border: 2px solid var(--synq-accent);
    border-radius: 50%; background: var(--synq-surface);
}
.synq-timeline-copy { display: flex; flex-direction: column; gap: 6px; }
.synq-timeline-copy .synq-body { font-size: 0.92rem; }

/* ---- My Work ---- */
.synq-work-flow { max-width: 760px; }
.synq-work-status { display: flex; flex-direction: column; gap: 18px; }
.synq-private-card { display: flex; flex-direction: column; gap: 18px; }
.synq-private-heading { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.synq-activity-list { gap: 0; }
.synq-activity-row {
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    padding: 18px 0;
    border-bottom: 1px solid var(--synq-border);
}
.synq-activity-row:last-child { border-bottom: 0; padding-bottom: 2px; }
.synq-activity-row:first-child { padding-top: 2px; }
.synq-activity-copy { display: flex; flex-direction: column; gap: 5px; min-width: 0; }
.synq-activity-title { color: var(--synq-ink); font-size: 0.98rem; line-height: 1.45; }
.synq-remove-button { color: var(--synq-ink-3); transition: color var(--synq-ease); }
.synq-remove-button:hover { color: var(--synq-error); }
.synq-work-consent { display: flex; flex-direction: column; gap: 16px; padding: 8px 0; }
.synq-review-notice {
    display: flex; flex-direction: column; gap: 6px;
    padding: 18px 22px;
    border-left: 3px solid var(--synq-accent);
    background: var(--synq-accent-soft);
    border-radius: 0 8px 8px 0;
}
.synq-review-notice-title { color: var(--synq-ink); font-weight: 600; font-size: 0.95rem; }
.synq-editor-card { display: flex; flex-direction: column; gap: 16px; }
.synq-editor-field { width: 100%; }
.synq-include-grid {
    display: flex; gap: 24px; flex-wrap: wrap;
    padding: 10px 0;
    border-top: 1px solid var(--synq-border);
    border-bottom: 1px solid var(--synq-border);
}
.synq-editor-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

/* ---- Goals ---- */
.synq-goals-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
.synq-goal-card { display: flex; flex-direction: column; gap: 26px; }
.synq-goal-card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; }
.synq-goal-card-copy { display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.synq-goal-card-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.45rem; line-height: 1.18; color: var(--synq-ink); font-weight: 500;
}
.synq-goal-card-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.synq-goal-edit { color: var(--synq-ink-3); transition: color var(--synq-ease); }
.synq-goal-edit:hover { color: var(--synq-accent); }
.synq-goal-progress-block { display: flex; flex-direction: column; gap: 12px; }
.synq-goal-progress-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; }
.synq-goal-progress-value {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 2.3rem; line-height: 1; color: var(--synq-ink); font-weight: 500;
    letter-spacing: -0.02em;
}
.synq-goal-progress-track { height: 8px; border-radius: 999px; overflow: hidden; }
.synq-goal-details {
    display: flex; gap: 20px; flex-wrap: wrap;
    padding-top: 16px;
    border-top: 1px solid var(--synq-border);
}
.synq-goal-form { display: flex; flex-direction: column; gap: 16px; max-width: 720px; }
.synq-goal-dialog {
    width: min(560px, calc(100vw - 32px));
    display: flex; flex-direction: column; gap: 16px;
    padding: 30px;
    border-radius: var(--synq-radius);
}

/* ---- Page transition ---- */
.synq-content {
    animation: synq-fade-in 0.35s ease;
}
@keyframes synq-fade-in {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---- Container ---- */
.synq-container {
    width: 100%;
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 28px;
    box-sizing: border-box;
}
.synq-content {
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding: 32px 0 72px 0;
}

/* ---- Responsive ---- */
@media (max-width: 860px) {
    .synq-preview-body { grid-template-columns: 1fr; }
    .synq-dashboard-grid { grid-template-columns: 1fr; gap: 36px; }
    .synq-stat-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
    .synq-nav { padding: 16px 0; }
    .synq-container { padding: 0 18px; }
    .synq-content { gap: 24px; padding: 24px 0 52px 0; }
    .synq-card, .synq-panel, .synq-panel-accent { padding: 20px; }
    .synq-nav-pill { padding: 7px 12px; font-size: 0.82rem; }
    .synq-hero { padding: 36px 0 28px 0; gap: 18px; }
    .synq-preview { padding: 12px; }
    .synq-preview-card { padding: 16px; }
    .synq-goal-heading, .synq-update-topline, .synq-meeting-title-row { flex-direction: column; }
    .synq-nav-links { justify-content: flex-end; }
    .synq-user-menu { margin-left: 0; }
    .synq-goals-list { grid-template-columns: 1fr; }
    .synq-goal-card-top { flex-direction: column; }
    .synq-stat-grid { grid-template-columns: 1fr; }
    .synq-meeting-card { padding: 20px; }
    .synq-goal-list { padding: 4px 18px; }
    .synq-timeline { padding: 8px 18px; }
}
</style>
"""


def apply_theme() -> None:
    """Inject the design-system CSS into the current page."""
    ui.add_head_html(_THEME_CSS)
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
    )
