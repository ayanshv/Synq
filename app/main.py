"""Entry point for the Synq app.

Starts the NiceGUI server and registers each page route. Pages live in the
`ui` package; this file wires them to URLs so NiceGUI knows what to render.
"""

from nicegui import ui

from app.database import init_db
from app.seed import run_seed
from app.ui import landing, dashboard, review, goals, settings as settings_page


def init_pages() -> None:
    """Register each page's content function with its URL route.

    Each ui module exposes a `render` function that builds the page content.
    We wrap them in lambdas so NiceGUI calls them when the route is visited.
    """
    ui.page("/")(landing.render)
    ui.page("/dashboard")(dashboard.render)
    ui.page("/review")(review.render)
    ui.page("/goals")(goals.render)
    ui.page("/settings")(settings_page.render)


def main() -> None:
    """Initialize the database, register pages, and start the server."""
    init_db()
    run_seed()
    init_pages()
    ui.run(title="Synq", port=8080)


if __name__ in {"__main__", "__mp_main__"}:
    main()
