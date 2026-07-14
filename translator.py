#!/usr/bin/env python3
"""İngilizce kelime girince: İngilizce tanim, Turkce anlami ve 3 ornek cumle gosteren program."""

import sys

from api import (
    get_turkish_meaning,
    get_word_data,
    get_tatoeba_sentences,
)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


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
    try:
        definitions, examples = get_word_data(word)
    except Exception as e:
        definitions, examples = [], []
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
