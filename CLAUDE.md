# 🧠 Project Core & Synchronization Protocol

## [CRITICAL RULES - READ BEFORE EXECUTING ANY COMMAND]

1. **Strict Isolation:**
   - If your current task is related to the interface/frontend, ONLY modify files within the `/frontend` directory.
   - If your current task is related to the server/backend logic, ONLY modify files within the `/backend` directory.
   - DO NOT cross boundaries under any circumstances.

2. **Permission First:**
   - Never install global dependencies or execute destructive commands (like dropping a database or deleting folders) without explicit user confirmation.
   - Always ask before pushing to `main` branch; use `tolga` or feature branches by default.

3. **Run & Test:**
   - Do not commit or declare a task "done" without running a local test to verify the code compiles and functions.
   - Test both CLI and GUI for backend changes; verify layout and responsiveness for frontend changes.

---

## 🏗️ Architecture Layout

### Backend (`/backend`)
**Technology:** Python 3 (stdlib only: urllib, json, tkinter)
- `api.py` — Core API interactions with external services (translation, dictionary, examples)
- `translator.py` — CLI interface with ANSI-colored terminal output
- `app.py` — Tkinter desktop GUI (imports shared logic from `api.py`)

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

## 🤝 The Handshake Ledger (Sync Log)

*INSTRUCTION FOR CLAUDE: After completing a significant feature or refactoring, read this section to understand project history. The ledger is auto-updated via git hooks. This keeps both team members in sync.*

### Backend State
- [2026-07-14] Modified: .claude/settings.json, CLAUDE.md, api.py, app.py, translator.py, .claude/hooks/, .gitignore, backend/, frontend/
- [2026-07-14] Modified: .claude/settings.json, CLAUDE.md, api.py, app.py, translator.py, .claude/hooks/, .gitignore, backend/
- [2026-07-14] Modified: .claude/settings.json, CLAUDE.md, api.py, app.py, translator.py, .claude/hooks/, __pycache__/, backend/
- [2026-07-14] Refactored: API logic extracted to dedicated `api.py` module with type hints and docstrings. CLI and GUI both import from shared API module for consistency.
- [2026-07-14] Initial: Created project structure with CLI (translator.py) and Tkinter GUI (app.py) using three translation/definition APIs.

### Frontend State
- [2026-07-14] Modified: .claude/settings.json, CLAUDE.md, api.py, app.py, translator.py, .claude/hooks/, .gitignore, backend/, frontend/
- [2026-07-14] Initialized: `/frontend` directory ready for implementation. Brother will build web interface here.

---

## 📋 Development Workflow

### For Backend Changes (Python)
1. Work only in `/backend`
2. Test with: `python3 backend/translator.py serendipity` (CLI) and `python3 backend/app.py` (GUI)
3. Commit to `tolga` branch
4. Once tested, open a PR to `main`
5. The `update-ledger.js` hook will auto-log your changes to this file

### For Frontend Changes (HTML/CSS/JS)
1. Work only in `/frontend`
2. Test locally with a browser
3. Commit to `tolga` branch (or your own feature branch)
4. Once tested, open a PR to `main`
5. The `update-ledger.js` hook will auto-log your changes to this file

### Pushing to Main
- Only push to `main` after both team members agree
- Use `tolga` or feature branches for parallel work
- Use PR reviews before merging to `main`

---

## 🔗 API Dependencies

All requests use public APIs with no authentication:
- **Google Translate** (unofficial endpoint)
- **MyMemory Translation API** (fallback)
- **Free Dictionary API** (definitions)
- **Tatoeba** (example sentences)

No API keys required. Graceful degradation if any service is down.

---

## 🚀 Running the Application

### Backend (CLI)
```bash
# Interactive mode
python3 backend/translator.py

# Single word lookup
python3 backend/translator.py serendipity
```

### Backend (GUI)
```bash
python3 backend/app.py
```

### Frontend
```bash
# Open frontend/index.html in a browser (coming soon)
```

---

## 📝 Notes

- **No dependencies:** Backend uses only Python standard library
- **Cross-platform:** Works on macOS, Windows, Linux
- **Error handling:** Each API fails independently; app degrades gracefully
- **Async:** Frontend will eventually make async calls to a backend API server
