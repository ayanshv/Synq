"""Reusable UI helpers built on top of the Synq design system.

This module is the single entry point pages use to render consistent UI.
Every visual decision (colors, type, spacing, radius) lives in `theme.py`;
this file exposes small Python helpers that apply those classes so page
code stays declarative and readable.

Usage:
    with page_frame("Dashboard"):
        section_heading("Recent updates", "Published by your team")
        with rounded_card():
            ui.label("Hello")
        primary_button("Publish", on_click=publish)
"""

from __future__ import annotations

from typing import Callable, Optional

from nicegui import ui

from app.ui.theme import apply_theme

# Navigation items shared across every page. Keeping them here means a new
# page automatically gets the right nav without re-listing links.
_NAV_ITEMS = [
    ("Home", "/"),
    ("Dashboard", "/dashboard"),
    ("Review", "/review"),
    ("Goals", "/goals"),
    ("Settings", "/settings"),
]


def page_frame(title: str, active_path: Optional[str] = None):
    """Wrap page content in the shared page background, nav, and container.

    Returns a context manager; the caller fills it with page-specific
    content. `active_path` highlights the matching nav pill; when omitted
    it is inferred from the title for convenience.
    """
    apply_theme()
    ui.page_title(f"Synq - {title}")

    # Page background spans the full viewport.
    ui.add_body_html('<div class="synq-page">')

    with ui.element("div").classes("synq-page w-full"):
        with ui.element("div").classes("synq-container"):
            _render_nav(active_path)
            # Content column the caller fills.
            return ui.element("div").classes("synq-content")

    # Closing tag for the background wrapper is handled by NiceGUI's DOM.


def _render_nav(active_path: Optional[str]) -> None:
    """Render the top navigation bar with pill-shaped links."""
    with ui.element("nav").classes("synq-nav"):
        # Brand mark: "Synq" with a small accent dot.
        ui.html('<a class="synq-nav-brand" href="/">Synq<span class="synq-nav-dot"></span></a>')
        with ui.element("div").classes("synq-nav-links"):
            for label, path in _NAV_ITEMS:
                classes = "synq-nav-pill"
                if active_path == path:
                    classes += " synq-active"
                ui.link(label, path).classes(classes)


# ---- Typography helpers ----

def display_heading(text: str) -> ui.label:
    """Largest editorial heading, used for hero/landing moments."""
    return ui.label(text).classes("synq-display")


def h1(text: str) -> ui.label:
    """Primary page heading."""
    return ui.label(text).classes("synq-h1")


def h2(text: str) -> ui.label:
    """Section-level heading."""
    return ui.label(text).classes("synq-h2")


def eyebrow(text: str) -> ui.label:
    """Small uppercase accent label above headings."""
    return ui.label(text).classes("synq-eyebrow")


def body(text: str) -> ui.label:
    """Standard body copy."""
    return ui.label(text).classes("synq-body")


def body_large(text: str) -> ui.label:
    """Slightly larger lead paragraph."""
    return ui.label(text).classes("synq-body-lg")


def muted(text: str) -> ui.label:
    """Tertiary muted text for hints/footnotes."""
    return ui.label(text).classes("synq-muted")


def field_label(text: str) -> ui.label:
    """Label above a form field."""
    return ui.label(text).classes("synq-label")


# ---- Section heading block ----

def section_heading(title: str, subtitle: Optional[str] = None) -> ui.element:
    """A section heading with an optional muted subtitle beneath it.

    Returns the container element so callers can append more content inside
    if needed.
    """
    with ui.element("div").classes("synq-section-head") as container:
        h2(title)
        if subtitle:
            ui.label(subtitle).classes("synq-body synq-section-sub")
    return container


# ---- Buttons ----

def primary_button(text: str, on_click: Optional[Callable] = None) -> ui.button:
    """Solid near-black primary action button."""
    return ui.button(text, on_click=on_click).classes("synq-btn synq-btn-primary")


def secondary_button(text: str, on_click: Optional[Callable] = None) -> ui.button:
    """Outlined secondary action button."""
    return ui.button(text, on_click=on_click).classes("synq-btn synq-btn-secondary")


def accent_button(text: str, on_click: Optional[Callable] = None) -> ui.button:
    """Soft-blue accent button for the one promoted action per page."""
    return ui.button(text, on_click=on_click).classes("synq-btn synq-btn-accent")


# ---- Cards / panels ----

def rounded_card() -> ui.element:
    """Standard surface card with subtle border and shadow."""
    return ui.element("div").classes("synq-card")


def rounded_panel() -> ui.element:
    """Larger surface panel (more padding, no shadow) for grouped content."""
    return ui.element("div").classes("synq-panel")


def accent_panel() -> ui.element:
    """Panel with the soft blue gradient background."""
    return ui.element("div").classes("synq-panel-accent")


# ---- Stat card ----

def stat_card(value: str, label: str, hint: Optional[str] = None) -> ui.element:
    """A compact metric card: big value, small label, optional hint line."""
    with ui.element("div").classes("synq-stat") as card:
        ui.label(label).classes("synq-stat-label")
        ui.label(value).classes("synq-stat-value")
        if hint:
            ui.label(hint).classes("synq-stat-hint")
    return card


# ---- Badge / pill ----

def badge(text: str, variant: str = "neutral") -> ui.element:
    """Small pill-shaped badge. variant: neutral|accent|success|warning."""
    classes = f"synq-badge synq-badge-{variant}"
    return ui.element("span").classes(classes).text(text)


# ---- Divider ----

def divider() -> ui.element:
    """A full-width subtle horizontal divider."""
    return ui.element("hr").classes("synq-divider")


# ---- Empty state ----

def empty_state(title: str, message: str) -> ui.element:
    """Dashed-border empty placeholder with a title and muted message."""
    with ui.element("div").classes("synq-empty") as container:
        ui.label(title).classes("synq-empty-title")
        ui.label(message).classes("synq-empty-msg")
    return container
