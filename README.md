# Event Ticket Portal

A simple Flask-based event ticketing portal for demonstrations and local development.

## Quick setup (Windows, PowerShell)

1. Clone or open the repository and change to the project root:

```powershell
Set-Location -LiteralPath 'D:\Event management system'
```

2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
& '.\.venv\Scripts\Activate.ps1'
```

3. Install dependencies using the `requirements.txt` in the `event_ticket_portal` folder:

```powershell
# Use the venv python explicitly and an absolute path to the requirements file
& 'D:\Event management system\.venv\Scripts\python.exe' -m pip install -r 'D:\Event management system\event_ticket_portal\requirements.txt'
```

4. Start the app (creates DB tables automatically):

```powershell
# From project root
$env:PYTHONPATH = 'D:\Event management system'
& 'D:\Event management system\.venv\Scripts\python.exe' 'D:\Event management system\run.py'
```

Open http://127.0.0.1:5000 in your browser.

## Files changed during setup
- `event_ticket_portal/requirements.txt`
  - Replaced `Flask-Login==0.7.0` with `Flask-Login==0.6.3` (0.7.0 not on PyPI)
  - Added `Werkzeug==2.3.6` to maintain compatibility with Flask-WTF
- `event_ticket_portal/app.py`
  - Removed use of `@app.before_first_request` and now rely on creating tables explicitly at startup
- `run.py` (new)
  - Adds a small runner that creates DB tables and starts the Flask dev server

## Troubleshooting
- "Could not open requirements file": ensure you're running pip from the folder containing the file or use the absolute path and quote paths with spaces.
- Import errors like `ModuleNotFoundError: No module named 'event_ticket_portal'`: set `PYTHONPATH` to the project root before running or run using `run.py` from the project root.
- Werkzeug/Flask-WTF compatibility errors: we pinned `Werkzeug==2.3.6` in `requirements.txt`.

## Next steps / suggestions
- Add a `Makefile` or PowerShell script to automate venv creation, install and start.
- Add tests and a health-check endpoint for automated smoke testing.
- For production, use a WSGI server (Gunicorn, Waitress) and do not enable debug mode.

---
If you want, I can:
- Add a PowerShell script to automate the steps above.
- Run a smoke test (GET /) and save the response HTML.
