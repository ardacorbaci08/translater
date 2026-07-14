#!/usr/bin/env python3
"""API interactions for English word lookup."""

import json
import urllib.parse
import urllib.request
import urllib.error


# API endpoints
DIC_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
TR_URL = "https://api.mymemory.translated.net/get?q={word}&langpair=en|tr"
TR_URL_G = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=tr&dt=t&q={word}"
TAT_URL = "https://tatoeba.org/en/api_v0/search?query={word}&from=eng&to=none&trans_filter=limit&trans_to=none"

REQUEST_TIMEOUT = 15


def fetch_json(url: str) -> dict | list:
    """Fetch and parse JSON from URL with spoofed User-Agent.

    Args:
        url: URL to fetch from

    Returns:
        Parsed JSON response (dict or list)

    Raises:
        urllib.error.HTTPError: On HTTP errors
        urllib.error.URLError: On network errors
        json.JSONDecodeError: On invalid JSON
    """
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_word_data(word: str) -> tuple[list[str], list[str]]:
    """Fetch definitions and example sentences from Free Dictionary API.

    Args:
        word: English word to look up

    Returns:
        Tuple of (definitions list, examples list). Empty lists on error.
    """
    try:
        url = DIC_URL.format(word=urllib.parse.quote(word))
        data = fetch_json(url)
    except Exception:
        return [], []

    if not isinstance(data, list) or not data:
        return [], []

    definitions = []
    examples = []
    for entry in data:
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech", "")
            for d in meaning.get("definitions", []):
                def_text = d.get("definition", "").strip()
                if def_text:
                    tag = f"({pos}) " if pos else ""
                    definitions.append(f"{tag}{def_text}")
                ex = d.get("example", "").strip()
                if ex and ex not in examples:
                    examples.append(ex)
    return definitions, examples


def get_tatoeba_sentences(word: str) -> list[str]:
    """Fetch example sentences from Tatoeba.

    Args:
        word: English word to find in sentences

    Returns:
        List of example sentences. Empty list on error.
    """
    url = TAT_URL.format(word=urllib.parse.quote(word))
    try:
        data = fetch_json(url)
    except Exception:
        return []

    sentences = []
    for r in data.get("results", []) or []:
        if r.get("lang") != "eng":
            continue
        text = (r.get("text") or "").strip()
        if text and word.lower() in text.lower() and text not in sentences:
            sentences.append(text)
    return sentences


def get_turkish_meaning(word: str) -> str:
    """Fetch Turkish translation of English word.

    Tries Google Translate first (more reliable for single words),
    falls back to MyMemory API if that fails or returns nothing.

    Args:
        word: English word to translate

    Returns:
        Turkish translation string. Empty string on error.
    """
    # Try Google Translate (unofficial endpoint) — more reliable for single words
    try:
        url = TR_URL_G.format(word=urllib.parse.quote(word))
        data = fetch_json(url)
        if data and isinstance(data, list) and data[0]:
            translations = [seg[0] for seg in data[0] if seg and seg[0]]
            translated = "".join(translations).strip()
            if translated and translated.lower() != word.lower():
                return translated
    except Exception:
        pass

    # Fallback: MyMemory API — choose best match from results
    try:
        url = TR_URL.format(word=urllib.parse.quote(word))
        data = fetch_json(url)
        matches = data.get("matches", []) or []
        best = ""
        for m in matches:
            seg = (m.get("segment") or "").strip().lower()
            tr = (m.get("translation") or "").strip()
            if not tr:
                continue
            if seg == word.lower():
                best = tr
                break
            if not best:
                best = tr
        if not best:
            best = (data.get("responseData") or {}).get("translatedText", "")
        return best.strip()
    except Exception:
        return ""
