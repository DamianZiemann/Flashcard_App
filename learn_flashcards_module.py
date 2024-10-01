# learn_flashcards_module.py

"""
Modul: learn_flashcards_module

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul ermöglicht es dem Benutzer, Flashcards zu lernen und aktualisiert die
Statistiken basierend auf dem Kenntnisstand.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import get_connection
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def learn_flashcards(user_id, update_dashboard_callback=None):
    """
    Ermöglicht dem Benutzer, Flashcards zu lernen.

    Args:
        user_id (int): Die ID des angemeldeten Benutzers.
        update_dashboard_callback (function, optional): Funktion zum Aktualisieren des Dashboards.
    """
    learn_win = tk.Toplevel()
    learn_win.title("Flashcards lernen")
    learn_win.geometry("500x400")
    learn_win.resizable(False, False)

    style = ttk.Style(learn_win)
    style.theme_use('clam')

    main_frame = ttk.Frame(learn_win, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)

    try:
        conn = get_connection()
        if not conn:
            messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen.", parent=learn_win)
            learn_win.destroy()
            return
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flashcards WHERE user_id=?", (user_id,))
        flashcards = cursor.fetchall()
        conn.close()
    except Exception as e:
        logger.exception("Fehler beim Abrufen der Flashcards.")
        messagebox.showerror("Fehler", "Fehler beim Laden der Flashcards.", parent=learn_win)
        learn_win.destroy()
        return

    if not flashcards:
        messagebox.showinfo("Info", "Keine Flashcards vorhanden.", parent=learn_win)
        learn_win.destroy()
        return

    current_index = 0

    def show_card(index):
        if index < len(flashcards):
            card = flashcards[index]
            front_label.config(text=card[2])  # Vorderseite
            back_label.config(text="")
            stats_label.config(text=f"Aufrufe: {card[4]}, Richtig: {card[5]}")
        else:
            messagebox.showinfo("Info", "Du hast alle Flashcards durchlaufen.", parent=learn_win)
            if update_dashboard_callback:
                update_dashboard_callback()
            learn_win.destroy()

    def reveal_back():
        card = flashcards[current_index]
        back_label.config(text=card[3])  # Rückseite

    def knew_it():
        update_flashcard(flashcards[current_index][0], True)
        next_card()

    def didnt_know():
        update_flashcard(flashcards[current_index][0], False)
        next_card()

    def update_flashcard(card_id, correct):
        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen.", parent=learn_win)
                return
            cursor = conn.cursor()

            # Aktualisieren der Statistik
            if correct:
                cursor.execute("UPDATE flashcards SET correct = correct + 1 WHERE id=?", (card_id,))

            cursor.execute(
                "UPDATE flashcards SET views = views + 1, last_review = ? WHERE id = ?",
                (datetime.now().date(), card_id)
            )
            conn.commit()
            conn.close()
            logger.info(f"Flashcard-ID {card_id} aktualisiert.")
        except Exception as e:
            logger.exception("Fehler beim Aktualisieren der Flashcard.")

    def next_card():
        nonlocal current_index
        current_index += 1
        show_card(current_index)

    def on_close():
        if update_dashboard_callback:
            update_dashboard_callback()
        learn_win.destroy()

    # Widgets
    front_label = ttk.Label(main_frame, text="", font=('Helvetica', 16), wraplength=450, anchor="center")
    front_label.grid(row=0, column=0, pady=10, sticky="NSEW")

    back_label = ttk.Label(main_frame, text="", font=('Helvetica', 16), wraplength=450, foreground='blue', anchor="center")
    back_label.grid(row=1, column=0, pady=10, sticky="NSEW")

    stats_label = ttk.Label(main_frame, text="", font=('Helvetica', 12))
    stats_label.grid(row=2, column=0, pady=5)

    reveal_button = ttk.Button(main_frame, text="Rückseite anzeigen", command=reveal_back)
    reveal_button.grid(row=3, column=0, pady=10)

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, pady=10)

    knew_button = ttk.Button(button_frame, text="Kannte ich", command=knew_it)
    knew_button.grid(row=0, column=0, padx=10)

    didnt_know_button = ttk.Button(button_frame, text="Kannte ich nicht", command=didnt_know)
    didnt_know_button.grid(row=0, column=1, padx=10)

    learn_win.protocol("WM_DELETE_WINDOW", on_close)

    show_card(current_index)
    learn_win.mainloop()