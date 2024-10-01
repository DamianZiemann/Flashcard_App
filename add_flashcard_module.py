# add_flashcard_module.py

"""
Modul: add_flashcard_module

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul ermöglicht dem Benutzer, neue Flashcards hinzuzufügen.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import get_connection
import logging

logger = logging.getLogger(__name__)


def add_flashcard(user_id, update_dashboard_callback=None):
    """
    Ermöglicht dem Benutzer, eine neue Flashcard hinzuzufügen.

    Args:
        user_id (int): Die ID des angemeldeten Benutzers.
        update_dashboard_callback (function, optional): Funktion zum Aktualisieren des Dashboards.
    """
    add_win = tk.Toplevel()
    add_win.title("Neue Flashcard hinzufügen")
    add_win.geometry("500x200")
    add_win.resizable(False, False)

    style = ttk.Style(add_win)
    style.theme_use('clam')

    main_frame = ttk.Frame(add_win, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Spalten konfigurieren
    main_frame.columnconfigure(1, weight=1)

    # Labels und Eingabefelder
    ttk.Label(main_frame, text="Vorderseite:").grid(row=0, column=0, pady=5, sticky=tk.E)
    front_entry = ttk.Entry(main_frame)
    front_entry.grid(row=0, column=1, pady=5, sticky=tk.EW)

    ttk.Label(main_frame, text="Rückseite:").grid(row=1, column=0, pady=5, sticky=tk.E)
    back_entry = ttk.Entry(main_frame)
    back_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)

    def save_flashcard():
        """Speichert die neue Flashcard in der Datenbank."""
        front = front_entry.get().strip()
        back = back_entry.get().strip()

        if not front or not back:
            messagebox.showwarning("Warnung", "Bitte beide Felder ausfüllen.", parent=add_win)
            return

        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen.", parent=add_win)
                return
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO flashcards (user_id, front, back, last_review) VALUES (?, ?, ?, DATE('now'))",
                (user_id, front, back)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Flashcard hinzugefügt!", parent=add_win)
            logger.info(f"Neue Flashcard hinzugefügt für Benutzer-ID {user_id}.")
            if update_dashboard_callback:
                update_dashboard_callback()
            add_win.destroy()
        except Exception as e:
            logger.exception("Fehler beim Hinzufügen der Flashcard.")
            messagebox.showerror("Fehler", "Fehler beim Hinzufügen der Flashcard.", parent=add_win)

    save_button = ttk.Button(main_frame, text="Speichern", command=save_flashcard)
    save_button.grid(row=2, column=0, columnspan=2, pady=20)

    add_win.mainloop()