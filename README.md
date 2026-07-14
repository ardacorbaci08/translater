# Ingilizce Kelime Çevirmen (English Word Lookup)

A lightweight Turkish-English word lookup tool. Enter an English word and get back:
- Turkish translation
- English definitions
- Up to 3 example sentences

## Usage

**CLI (Interactive)**
```bash
python3 translator.py
```

**CLI (Single word)**
```bash
python3 translator.py serendipity
```

**GUI (Desktop)**
```bash
python3 app.py
```

## Requirements

None — uses only Python standard library (urllib, json, tkinter).

## How it works

- Fetches Turkish translations via Google Translate or MyMemory API
- Gets definitions from the Free Dictionary API
- Supplements examples from Tatoeba if needed
- Gracefully degrades if any API is unavailable
