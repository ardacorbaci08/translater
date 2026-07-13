#!/usr/bin/env python3
"""İngilizce kelime girince: İngilizce tanim, Turkce anlami ve 3 ornek cumle gosteren program."""

import json
import urllib.parse
import urllib.request
import urllib.error
import sys


DIC_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
TR_URL = "https://api.mymemory.translated.net/get?q={word}&langpair=en|tr"
TR_URL_G = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=tr&dt=t&q={word}"
TAT_URL = "https://tatoeba.org/en/api_v0/search?query={word}&from=eng&to=none&trans_filter=limit&trans_to=none"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_word_data(word):
    """Free Dictionary API'den tanim ve ornek cumleleri ceker."""
    url = DIC_URL.format(word=urllib.parse.quote(word))
    data = fetch_json(url)
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


def get_tatoeba_sentences(word):
    """Tatoeba'dan kelimeyi iceren gercek cumleleri getirir."""
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


def get_turkish_meaning(word):
    """Kelimenin Turkce karsiligini getirir. Once Google Translate, o basarisizsa MyMemory."""
    # 1) Google Translate (unofficial endpoint) — tek kelime icin cok daha tutarli
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

    # 2) Yedek: MyMemory — eslesmeler arasindan en iyisini sec
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


def show_word(word):
    print(f"\n{BOLD}{CYAN}{'=' * 50}{RESET}")
    print(f"{BOLD}{BLUE}Kelime:{RESET} {word}")
    print(f"{BOLD}{CYAN}{'=' * 50}{RESET}")

    # 1) Turkce anlami
    try:
        tr = get_turkish_meaning(word)
    except Exception as e:
        tr = ""
        print(f"{RED}Turkce anlam alinamadi: {e}{RESET}")
    if tr and tr.lower() == word.lower():
        tr = ""
    print(f"\n{BOLD}{YELLOW}Turkce Anlami:{RESET}")
    print(f"  {tr if tr else '(bulunamadi)'}")

    # 2) Ingilizce tanimi
    definitions = []
    examples = []
    try:
        definitions, examples = get_word_data(word)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"\n{YELLOW}Not: '{word}' sozluk API'sinde bulunamadi.{RESET}")
        else:
            print(f"\n{RED}Sozluk hatasi: {e}{RESET}")
    except Exception as e:
        print(f"\n{RED}Sozluk hatasi: {e}{RESET}")

    print(f"\n{BOLD}{GREEN}Ingilizce Tanimi:{RESET}")
    if definitions:
        for d in definitions[:5]:
            print(f"  - {d}")
    else:
        print("  (tanim bulunamadi)")

    # 3) Ornek cumleler: sozlukten al, eksikse Tatoeba tamamla
    if len(examples) < 3:
        for s in get_tatoeba_sentences(word):
            if s not in examples:
                examples.append(s)
            if len(examples) >= 3:
                break

    print(f"\n{BOLD}{CYAN}Ornek Cumleler:{RESET}")
    if examples:
        for i, ex in enumerate(examples[:3], 1):
            print(f"  {i}. {ex}")
        if len(examples) < 3:
            print(f"  {YELLOW}(Yalnizca {len(examples)} ornek cumle bulundu){RESET}")
    else:
        print("  (ornek cumle bulunamadi)")


def main():
    if len(sys.argv) > 1:
        word = " ".join(sys.argv[1:]).strip()
        show_word(word)
        return

    print(f"{BOLD}Ingilizce Kelime Cevirmen{RESET}")
    print(f"Cikmak icin {BOLD}q{RESET} veya {BOLD}cikis{RESET} yazin.\n")
    while True:
        try:
            word = input(f"{BOLD}Kelime> {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not word:
            continue
        if word.lower() in ("q", "quit", "cikis", "exit"):
            break
        try:
            show_word(word)
        except Exception as e:
            print(f"{RED}Hata: {e}{RESET}")
        print()


if __name__ == "__main__":
    main()
