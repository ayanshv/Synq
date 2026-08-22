"""Synq visual design system.

This module owns the CSS that defines Synq's look and feel.

Design language (GENERE NEO-BRUTALIST):
    - Loud, high-contrast brutalism: #0f0f0f (black), #ffffff (white), #f3f3f3 (surface)
    - A striking, aggressive red accent (#ff3333)
    - Massive uppercase display headings (Oswald) over a structural sans body (Inter)
    - Sharp corners, harsh shadows, thick borders, and kinetic hover states.
    - MAXIMUM PERSONALITY.
"""

from nicegui import ui

_THEME_CSS = """
<style>
:root {
    /* Color palette - Unapologetic High-Contrast */
    --synq-bg: #f4f4f5;            /* industrial light gray */
    --synq-surface: #ffffff;       /* stark white surface */
    --synq-surface-2: #e4e4e7;     /* secondary surface for hover */
    --synq-border: #d4d4d8;        /* subtle structural border */
    --synq-border-strong: #0f0f0f; /* harsh, chunky black border */
    --synq-ink: #0f0f0f;           /* absolute primary black text */
    --synq-ink-2: #3f3f46;         /* heavy gray text */
    --synq-ink-3: #71717a;         /* tertiary / metadata text */
    --synq-accent: #ff3333;        /* striking red brand accent */
    --synq-accent-soft: #ffe5e5;   /* stark light red tint */
    --synq-accent-grad: linear-gradient(135deg, #18181b 0%, #000000 100%);
    --synq-success: #059669;
    --synq-warning: #d97706;
    --synq-error: #dc2626;
    
    /* Shadows & Radii - Neo-brutalist hard edges */
    --synq-shadow: 6px 6px 0px 0px var(--synq-ink);
    --synq-shadow-sm: 3px 3px 0px 0px var(--synq-ink);
    --synq-shadow-hover: 2px 2px 0px 0px var(--synq-ink);
    --synq-radius: 0px;            /* No rounded corners allowed. */
    --synq-radius-sm: 0px;
    --synq-radius-pill: 0px;       /* Blocks only. */
}

/* Page background + base typography. */
.synq-page {
    background-color: var(--synq-bg);
    color: var(--synq-ink);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
}

/* ---- Typography helpers ---- */
.synq-display {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: clamp(3.5rem, 8vw, 7rem);
    line-height: 0.9;
    letter-spacing: -0.03em;
    text-transform: uppercase;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h1 {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 0.95;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: var(--synq-ink);
    margin: 0;
}
.synq-h2 {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    line-height: 1.05;
    letter-spacing: -0.01em;
    text-transform: uppercase;
    color: var(--synq-ink);
    margin: 0;
}
.synq-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--synq-accent);
    margin: 0;
}
.synq-body {
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 400;
    line-height: 1.6;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-body-lg {
    font-family: 'Inter', sans-serif;
    font-size: 1.25rem;
    font-weight: 400;
    line-height: 1.6;
    color: var(--synq-ink-2);
    margin: 0;
}
.synq-muted {
    font-size: 0.9rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--synq-ink-3);
    margin: 0;
}
.synq-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--synq-ink);
    margin: 0;
}

/* ---- Navigation bar ---- */
.synq-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 24px 0;
    background: var(--synq-surface);
    border-bottom: 4px solid var(--synq-border-strong);
}
.synq-nav-brand {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: var(--synq-ink);
    text-decoration: none;
}
.synq-nav-brand .synq-nav-dot {
    display: inline-block;
    color: var(--synq-accent);
    background: transparent;
    width: auto;
    height: auto;
    margin-left: 2px;
}
.synq-nav-brand .synq-nav-dot::after {
    content: ".";
}
.synq-nav-links {
    display: flex;
    align-items: center;
    gap: 32px; /* Fixed spacing from screenshot 1 */
    flex-wrap: wrap;
}
.synq-nav-pill {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--synq-ink);
    text-decoration: none;
    border: 2px solid transparent;
    transition: all 0.15s ease-out;
}
.synq-nav-pill:hover {
    color: var(--synq-surface);
    background: var(--synq-ink);
}
.synq-nav-pill.synq-active {
    color: var(--synq-accent);
    border: 2px solid var(--synq-accent);
    background: var(--synq-surface);
    box-shadow: 4px 4px 0px 0px var(--synq-accent);
    transform: translate(-2px, -2px);
}
.synq-user-menu { margin-left: 16px; border-left: 3px solid var(--synq-border-strong); padding-left: 24px; }
.synq-avatar {
    width: 44px; height: 44px; min-height: 44px;
    padding: 0; 
    background: var(--synq-ink); color: var(--synq-surface);
    font-family: 'Oswald', sans-serif;
    font-size: 1.2rem; font-weight: 700;
}
.synq-avatar-small {
    width: 40px; height: 40px; min-height: 40px;
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0; background: var(--synq-accent-soft); color: var(--synq-accent);
    border: 2px solid var(--synq-accent);
}

/* ---- Section heading block ---- */
.synq-section-head { 
    margin: 0 0 32px 0; 
    border-bottom: 4px solid var(--synq-border-strong); 
    padding-bottom: 12px; 
}
.synq-section-head .synq-section-sub {
    margin: 12px 0 0 0;
    font-size: 1.1rem;
    color: var(--synq-ink-2);
}

/* ---- Layout & Grid Fixes ---- */
.synq-dashboard-intro { display: flex; flex-direction: column; gap: 16px; padding: 48px 0 32px; }
.synq-dashboard-section { display: flex; flex-direction: column; gap: 24px; }

/* Fixed the right-hand column squish from Screenshot 3 */
.synq-dashboard-grid { 
    display: grid; 
    grid-template-columns: minmax(0, 2fr) minmax(380px, 1fr); 
    gap: 64px; 
    align-items: start; 
}

/* Brutalist Stat Grid - fixing Screenshot 1 */
.synq-stat-grid { 
    display: grid; 
    grid-template-columns: repeat(4, 1fr); 
    gap: 0; 
    border: 3px solid var(--synq-border-strong); 
    box-shadow: var(--synq-shadow); 
    background: var(--synq-surface);
}
.synq-dashboard-main, .synq-dashboard-side { display: flex; flex-direction: column; gap: 48px; min-width: 0; }

/* Updates & Activity Lists */
.synq-goal-list, .synq-update-list { display: flex; flex-direction: column; gap: 24px; }
.synq-goal-list { padding: 0; }
.synq-goal-row { display: flex; flex-direction: column; gap: 16px; padding: 24px; border: 2px solid var(--synq-border-strong); background: var(--synq-surface); box-shadow: var(--synq-shadow-sm); }
.synq-goal-heading, .synq-update-topline, .synq-meeting-title-row, .synq-timeline-heading {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 24px;
}
.synq-goal-title { font-family: 'Oswald', sans-serif; font-size: 1.5rem; font-weight: 700; text-transform: uppercase; color: var(--synq-ink); }
.synq-goal-meta { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
.synq-goal-percent { font-family: 'Oswald', sans-serif; font-size: 2rem; font-weight: 700; color: var(--synq-accent); }
.synq-update-card { display: flex; flex-direction: column; gap: 20px; padding: 24px; border: 2px solid var(--synq-border-strong); background: var(--synq-surface); box-shadow: var(--synq-shadow-sm); }
.synq-person { display: flex; align-items: center; gap: 16px; }
.synq-update-name, .synq-timeline-person { font-weight: 800; color: var(--synq-ink); text-transform: uppercase; font-size: 1rem; letter-spacing: 0.1em; }
.synq-update-detail { display: flex; flex-direction: column; gap: 8px; padding-top: 16px; border-top: 2px solid var(--synq-border); }
.synq-detail-label { font-size: 0.75rem; font-weight: 800; letter-spacing: 0.2em; text-transform: uppercase; color: var(--synq-ink-3); }
.synq-detail-text { font-size: 1.05rem; line-height: 1.6; color: var(--synq-ink-2); font-weight: 400; }
.synq-update-detail.synq-blocker { border-top-color: var(--synq-accent); border-top-width: 3px; }
.synq-update-detail.synq-blocker .synq-detail-label { color: var(--synq-accent); }

/* Timeline fix for Screenshot 3 */
.synq-timeline { display: flex; flex-direction: column; gap: 0; padding: 0 0 0 32px; border-left: 4px solid var(--synq-border-strong); margin-left: 8px; }
.synq-timeline-item { 
    display: grid; 
    grid-template-columns: auto 1fr; 
    gap: 24px; 
    padding: 24px 0; 
    border-bottom: 2px solid var(--synq-border); 
    position: relative; 
}
.synq-timeline-item:last-child { border-bottom: 0; }
.synq-timeline-dot { 
    width: 16px; 
    height: 16px; 
    margin-top: 6px; 
    background: var(--synq-accent); 
    border: 3px solid var(--synq-border-strong);
    position: absolute; 
    left: -42px; 
}
.synq-timeline-copy { display: flex; flex-direction: column; gap: 8px; word-break: break-word; }
.synq-timeline-copy .synq-body { font-size: 1rem; line-height: 1.5; }

/* ---- Cards / panels ---- */
/* ---- Cards / panels ---- */
.synq-card {
    background: var(--synq-surface);
    border: 3px solid var(--synq-border-strong);
    padding: 32px;
    box-shadow: var(--synq-shadow);
    transition: transform 0.1s ease, box-shadow 0.1s ease;
}
.synq-card:hover {
    transform: translate(2px, 2px);
    box-shadow: var(--synq-shadow-hover);
}
.synq-panel {
    background: var(--synq-surface);
    border: 3px solid var(--synq-border-strong);
    padding: 40px;
    box-shadow: var(--synq-shadow);
}

/* Accent Panel Fixes (Targets 18394.png issues) */
.synq-panel-accent {
    background: var(--synq-ink);
    color: var(--synq-surface);
    border: 3px solid var(--synq-border-strong);
    padding: 40px;
    box-shadow: var(--synq-shadow);
}
/* Force text inside the dark panel to flip to light colors */
.synq-panel-accent .synq-body, 
.synq-panel-accent .synq-body-lg,
.synq-panel-accent p {
    color: var(--synq-surface) !important;
}
.synq-panel-accent .synq-muted {
    color: #a1a1aa !important; /* Lighter gray to contrast against black */
}
/* Nuke the default Quasar blue and enforce brutalist buttons inside the dark panel */
.synq-panel-accent .q-btn,
.synq-panel-accent .synq-btn {
    background-color: var(--synq-accent) !important;
    color: var(--synq-surface) !important;
    border: 3px solid var(--synq-surface) !important;
    box-shadow: 4px 4px 0px 0px var(--synq-surface) !important;
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    transition: all 0.1s ease-out;
}
.synq-panel-accent .q-btn:hover,
.synq-panel-accent .synq-btn:hover {
    background-color: var(--synq-surface) !important;
    color: var(--synq-accent) !important;
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0px 0px var(--synq-surface) !important;
}

/* ---- Stat card (From Screenshot 1) ---- */
.synq-stat {
    background: var(--synq-surface);
    border-right: 2px solid var(--synq-border-strong);
    padding: 32px 24px;
    transition: background 0.15s ease, transform 0.15s ease;
}
.synq-stat:last-child { border-right: none; }
.synq-stat:hover {
    background: var(--synq-accent-soft);
}
.synq-stat-value {
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 4rem;
    line-height: 1;
    color: var(--synq-ink);
    margin: 16px 0 0 0;
}
.synq-stat-label {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--synq-ink-3);
    margin: 0;
}

/* Progress bars fix for Screenshot 2 */
.synq-goal-progress-track { 
    height: 12px; 
    background: var(--synq-surface-2); 
    border: 2px solid var(--synq-border-strong);
    overflow: hidden; 
    margin-top: 12px;
}
.synq-goal-progress-fill { 
    height: 100%; 
    background: var(--synq-accent); 
    border-right: 2px solid var(--synq-border-strong);
}

/* ---- Badge / pill ---- */
.synq-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-size: 0.8rem;
    font-weight: 800;
    border: 2px solid var(--synq-border-strong);
    box-shadow: 2px 2px 0px 0px var(--synq-border-strong);
}
.synq-badge-neutral { background: var(--synq-surface-2); color: var(--synq-ink); }
.synq-badge-accent { background: var(--synq-accent); color: var(--synq-surface); }
.synq-badge-success { background: var(--synq-success); color: var(--synq-surface); }
.synq-badge-warning { background: var(--synq-warning); color: var(--synq-surface); }

/* ---- Buttons ---- */
.synq-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 16px 32px;
    border: 3px solid var(--synq-border-strong);
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    cursor: pointer;
    transition: all 0.1s ease-out;
    text-decoration: none;
    box-shadow: var(--synq-shadow) !important;
}
.synq-btn:active {
    transform: translate(4px, 4px) !important;
    box-shadow: var(--synq-shadow-hover) !important;
}
.synq-btn-primary {
    background-color: var(--synq-accent) !important;
    color: var(--synq-surface) !important;
}
.synq-btn-primary:hover {
    background-color: var(--synq-ink) !important;
    color: var(--synq-surface) !important;
}
.synq-btn-secondary {
    background-color: var(--synq-surface) !important;
    color: var(--synq-ink) !important;
}
.synq-btn-secondary:hover {
    background-color: var(--synq-surface-2) !important;
}

/* ---- Responsive ---- */
.synq-container {
    width: 100%;
    max-width: 1300px; /* Widened for structural integrity */
    margin: 0 auto;
    padding: 0 40px;
    box-sizing: border-box;
}
.synq-content {
    display: flex;
    flex-direction: column;
    gap: 64px;
    padding: 64px 0 96px 0;
}
@media (max-width: 1024px) {
    .synq-dashboard-grid { grid-template-columns: 1fr; gap: 48px; }
    .synq-stat-grid { grid-template-columns: repeat(2, 1fr); }
    .synq-stat:nth-child(2) { border-right: none; }
    .synq-stat:nth-child(1), .synq-stat:nth-child(2) { border-bottom: 2px solid var(--synq-border-strong); }
}
@media (max-width: 640px) {
    .synq-nav { padding: 16px 0; flex-direction: column; gap: 16px; align-items: flex-start; }
    .synq-container { padding: 0 24px; }
    .synq-content { gap: 48px; padding: 32px 0 64px 0; }
    .synq-stat-grid { grid-template-columns: 1fr; }
    .synq-stat { border-right: none; border-bottom: 2px solid var(--synq-border-strong); }
    .synq-stat:last-child { border-bottom: none; }
    .synq-nav-links { gap: 16px; }
}
</style>
"""

def apply_theme() -> None:
    ui.add_head_html(_THEME_CSS)
    ui.add_head_html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Oswald:wght@500;700&display=swap" rel="stylesheet">'
    )