# Synq

Synq helps small software teams reduce unnecessary meetings.

Each team member clicks **Finish Work** at the end of their work period.
Synq builds an activity snapshot, the user confirms, AI drafts a summary,
the user reviews and edits it, and only after clicking **Publish** does the
update become visible to the team. The team dashboard aggregates published
updates and uses progress toward goals to flag whether a meeting is needed.

The product is designed to feel like an assistant the employee controls,
not surveillance software.

## Tech stack

- Python
- NiceGUI for the UI
- FastAPI for backend/API structure
- SQLModel for database models
- SQLite for development
- Pydantic where useful
- httpx for future integrations

## Project structure

```
app/
  main.py            Entry point. Starts the NiceGUI app and registers pages.
  config.py          Loads environment variables and exposes settings.
  database.py        Creates the SQLite engine and session helper.
  models/            SQLModel data models (User, Team, WorkUpdate, Goal).
  services/          Business logic (AI, updates, goals, meetings).
  ui/                NiceGUI pages and shared layout.
  utils/             Small shared helpers.
tests/               Tests.
```

## Getting started

```bash
pip install -r requirements.txt
python -m app.main
```

Then open the printed local URL in your browser.

## Status

This is the initial foundation only. Authentication, real OAuth integrations,
and real AI analysis are intentionally not implemented yet.
