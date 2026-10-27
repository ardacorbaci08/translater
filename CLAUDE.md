# Project Core & Synchronization Protocol

## Working rules

1. **Stay on your side of the split.** Frontend tasks change only `/frontend`, and backend tasks change only `/backend`. The two halves are owned by different people, so a change that needs both sides gets raised first, not made.
2. **Branches.** Work on `tolga` or a feature branch. Ask before pushing to `main`.
3. **Test before done.** Backend changes: run both the CLI and the GUI. Frontend changes: check layout and responsiveness in a browser.

---

## Architecture Layout

### Backend (`/backend`)
**Technology:** Python 3 (stdlib only: urllib, json, tkinter)
- `api.py`: core API calls to the external services (translation, dictionary, examples)
- `translator.py`: CLI interface with ANSI-colored terminal output
- `app.py`: Tkinter desktop GUI, importing its shared logic from `api.py`

**Responsibilities:**
- Fetch Turkish translations via Google Translate / MyMemory API
- Fetch English definitions from Free Dictionary API
- Fetch example sentences from Tatoeba
- Handle all network requests and error fallbacks

### Frontend (`/frontend`)
**Technology:** HTML/CSS/JavaScript (to be implemented)
- Web interface for the word lookup tool
- Real-time search with backend integration
- Responsive design for desktop and mobile

**Responsibilities:**
- User interface and interactions
- Communication with backend API
- Display lookup results (translations, definitions, examples)

---

## The Handshake Ledger (Sync Log)

Project history, auto-updated by `.claude/hooks/update-ledger.js` (it keys on the two `### ... State` headings below, so keep them verbatim). Read it to see what the other side has done.

### Backend State
- [2026-07-14] Implemented: Team synchronization workflow with /backend and /frontend directory separation. Auto-ledger hook configured.
- [2026-07-14] Refactored: API logic extracted to dedicated `api.py` module with type hints and docstrings. CLI and GUI both import from shared API module for consistency.
- [2026-07-14] Initial: Created project structure with CLI (translator.py) and Tkinter GUI (app.py) using three translation/definition APIs.

### Frontend State
- [2026-07-14] Initialized: `/frontend` directory with HTML template ready for implementation. Brother can build web interface here.

---

## Development Workflow

1. Work only in your side's directory (`/backend` or `/frontend`).
2. Test (see Running the Application below).
3. Commit to `tolga` or your own feature branch. The ledger hook logs the change here.
4. Open a PR to `main`. Merge only after both team members agree.

---

## API Dependencies

All requests use public APIs with no authentication:
- **Google Translate** (unofficial endpoint)
- **MyMemory Translation API** (fallback)
- **Free Dictionary API** (definitions)
- **Tatoeba** (example sentences)

No API keys required. Each API fails independently and the app degrades gracefully.

---

## Running the Application

```bash
python3 backend/translator.py              # CLI, interactive
python3 backend/translator.py serendipity  # CLI, single word
python3 backend/app.py                     # GUI
```

Frontend: open `frontend/index.html` in a browser (not built yet).

---

## Notes

- **No dependencies:** Backend uses only the Python standard library.
- **Cross-platform:** Works on macOS, Windows, Linux.
- **Async:** Frontend will eventually make async calls to a backend API server.
