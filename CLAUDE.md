# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small Turkish-language English-word lookup tool ("Ingilizce Kelime Cevirmen"). Given an English word, it fetches:
1. Turkish translation
2. English dictionary definition(s)
3. Up to 3 example sentences

There are two entry points sharing the same core logic:
- [translator.py](translator.py) — CLI (interactive REPL or single-word arg), with ANSI-colored terminal output.
- [app.py](app.py) — Tkinter desktop GUI that imports and reuses the functions from `translator.py`, doing lookups on a background thread to keep the UI responsive.

No build system, package manifest, or test suite exists — this is plain-stdlib Python (only `urllib`, `json`, `tkinter`).

## Running

```bash
# CLI, interactive mode
python3 translator.py

# CLI, single word
python3 translator.py serendipity

# GUI
python3 app.py
```

No dependencies to install — everything used is in the Python standard library.

## Architecture

All external API calls live in `translator.py` and are consumed by both entry points:

- `get_turkish_meaning(word)` — tries the unofficial Google Translate endpoint first (more consistent for single words), falls back to MyMemory API if that fails or returns nothing.
- `get_word_data(word)` — hits the Free Dictionary API (`api.dictionaryapi.dev`) for definitions and any example sentences bundled with them.
- `get_tatoeba_sentences(word)` — backfills example sentences from Tatoeba when the dictionary API provides fewer than 3.
- `fetch_json(url)` — shared helper wrapping `urllib.request` with a spoofed User-Agent and 15s timeout.

Each lookup function fails independently (each swallows/returns empty on error) so a single API being down doesn't break the whole lookup — both `translator.show_word()` and `app.py`'s `_do_search()` call all three and degrade gracefully, showing "(bulunamadi)"/"(tanim bulunamadi)" placeholders and collecting error messages to display rather than raising.

`app.py`'s GUI mirrors `translator.py`'s CLI flow exactly (same three lookups, same fallback-to-Tatoeba-if-<3-examples logic) but renders into a `tkinter.scrolledtext.ScrolledText` widget with custom text tags instead of ANSI codes, and runs the network calls in a `threading.Thread` to avoid blocking the Tk main loop.
