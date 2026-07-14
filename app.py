#!/usr/bin/env python3
"""Ingilizce Kelime Cevirmen - masaustu uygulama (Tkinter).

Core API mantigini translator.py modulunden yeniden kullanir;
aramayi arka plan thread'inde yapar, sonucu pencerede gosterir.
"""

import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

from api import (
    get_turkish_meaning,
    get_word_data,
    get_tatoeba_sentences,
)


BG = "#1e1e1e"
PANEL = "#252526"
ENTRY_BG = "#2d2d30"
Fg = "#d4d4d4"
FG_DIM = "#9e9e9e"
ACCENT = "#0e639c"
ACCENT_HOVER = "#1177bb"

WORD_COLOR = "#4ec9b0"
HDR_TR = "#dcdcaa"
HDR_EN = "#6a9955"
HDR_EX = "#569cd6"
BODY = "#d4d4d4"
STATUS = "#808080"
ERR = "#f48771"


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Ingilizce Kelime Cevirmen")
        root.geometry("760x680")
        root.minsize(580, 480)
        root.configure(bg=BG)

        self.font_body = ("Menlo", 12)
        self.font_word = ("Menlo", 20, "bold")
        self.font_header = ("Menlo", 13, "bold")
        self.font_sect = ("Menlo", 12, "italic")

        self._build_ui()

    def _build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        bar = tk.Frame(self.root, bg=BG)
        bar.grid(row=0, column=0, sticky="ew", padx=14, pady=(14, 8))
        bar.grid_columnconfigure(1, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            bar, textvariable=self.entry_var, font=("Menlo", 14),
            bg=ENTRY_BG, fg=Fg, insertbackground=Fg,
            relief="flat", bd=0, highlightthickness=2,
            highlightbackground="#3c3c3c", highlightcolor=ACCENT,
        )
        self.entry.grid(row=0, column=1, ipady=8, sticky="ew")

        self.search_btn = tk.Button(
            bar, text="Ara", font=("Menlo", 13, "bold"),
            bg=ACCENT, fg="#ffffff", activebackground=ACCENT_HOVER,
            activeforeground="#ffffff", relief="flat", bd=0,
            padx=22, pady=8, cursor="hand2", command=self._on_search,
        )
        self.search_btn.grid(row=0, column=2, padx=(10, 0))

        self.entry.bind("<Return>", lambda e: self._on_search())

        yazi = tk.Frame(self.root, bg=PANEL)
        yazi.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        yazi.grid_columnconfigure(0, weight=1)
        yazi.grid_rowconfigure(0, weight=1)

        self.output = scrolledtext.ScrolledText(
            yazi, wrap="word", font=self.font_body,
            bg=PANEL, fg=BODY, insertbackground=Fg,
            relief="flat", bd=10, padx=14, pady=14,
            spacing1=2, spacing3=4,
        )
        self.output.grid(row=0, column=0, sticky="nsew")
        self.output.configure(state="disabled")

        self.output.tag_configure("word", font=self.font_word, foreground=WORD_COLOR, spacing3=10)
        self.output.tag_configure("hdr_tr", font=self.font_header, foreground=HDR_TR, spacing1=6)
        self.output.tag_configure("hdr_en", font=self.font_header, foreground=HDR_EN, spacing1=6)
        self.output.tag_configure("hdr_ex", font=self.font_header, foreground=HDR_EX, spacing1=6)
        self.output.tag_configure("body", font=self.font_body, foreground=BODY)
        self.output.tag_configure("bullet", font=self.font_body, foreground=BODY, lmargin1=18, lmargin2=18)
        self.output.tag_configure("num", font=self.font_body, foreground=HDR_EX, lmargin1=18, lmargin2=30)
        self.output.tag_configure("status", font=self.font_sect, foreground=STATUS)
        self.output.tag_configure("error", font=self.font_sect, foreground=ERR)

    def _set_status(self, text, tag="status"):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text + "\n", tag)
        self.output.configure(state="disabled")

    def _append(self, text, tag):
        self.output.insert("end", text + "\n", tag)

    def _on_search(self):
        word = self.entry_var.get().strip()
        if not word:
            return
        self.search_btn.configure(state="disabled", text="Araniyor...")
        self._set_status(f"Araniyor: {word} ...")

        t = threading.Thread(target=self._do_search, args=(word,), daemon=True)
        t.start()

    def _do_search(self, word):
        errors = []
        try:
            tr = get_turkish_meaning(word) or ""
        except Exception as e:
            tr = ""
            errors.append(f"Turkce anlam: {e}")

        definitions, examples = [], []
        try:
            definitions, dct_examples = get_word_data(word)
            examples = list(dct_examples)
        except Exception as e:
            errors.append(f"Sozluk: {e}")

        if len(examples) < 3:
            try:
                for s in get_tatoeba_sentences(word):
                    if s not in examples:
                        examples.append(s)
                    if len(examples) >= 3:
                        break
            except Exception as e:
                errors.append(f"Tatoeba: {e}")

        self.root.after(0, lambda: self._render(word, tr, definitions, examples[:3], errors))

    def _render(self, word, tr, definitions, examples, errors):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")

        self._append(word, "word")

        self._append("TURKCE ANLAMI", "hdr_tr")
        if tr and tr.lower() != word.lower():
            self._append(tr, "body")
        else:
            self._append("(bulunamadi)", "status")

        self._append("INGILIZCE TANIMI", "hdr_en")
        if definitions:
            for d in definitions[:5]:
                self.output.insert("end", "  • ", "bullet")
                self.output.insert("end", d + "\n", "bullet")
        else:
            self._append("(tanim bulunamadi)", "status")

        self._append("ORNEK CUMLELER", "hdr_ex")
        if examples:
            for i, ex in enumerate(examples, 1):
                self.output.insert("end", f"  {i}. ", "num")
                self.output.insert("end", ex + "\n", "body")
            if len(examples) < 3:
                self._append(f"(yalnizca {len(examples)} ornek cumle bulundu)", "status")
        else:
            self._append("(ornek cumle bulunamadi)", "status")

        if errors:
            self._append("")
            for e in errors:
                self._append(e, "error")

        self.output.configure(state="disabled")
        self.search_btn.configure(state="normal", text="Ara")


def main():
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
