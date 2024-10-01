# csv_utils.py

"""
Modul: csv_utils

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 2.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul bietet Funktionen zum Importieren und Exportieren von Flashcards im CSV-Format.
"""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from db_utils import get_connection
import logging

logger = logging.getLogger(__name__)


def import_flashcards_from_csv(user_id):
    """
    Importiert Flashcards aus einer CSV-Datei.

    Parameter:
        user_id (int): Die ID des angemeldeten Benutzers.

    Return:
        None
    """
    file_path = filedialog.askopenfilename(
        title="CSV-Datei auswählen",
        filetypes=(("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*"))
    )
    if not file_path:
        return

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            flashcards = [(user_id, row[0], row[1]) for row in reader if len(row) >= 2]

        if not flashcards:
            messagebox.showwarning("Warnung", "Die ausgewählte CSV-Datei enthält keine gültigen Flashcards.", parent=tk._get_temp_root())
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO flashcards (user_id, front, back, last_review) VALUES (?, ?, ?, DATE('now'))",
            flashcards
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Erfolg", "Flashcards erfolgreich importiert!", parent=tk._get_temp_root())
        logger.info(f"{len(flashcards)} Flashcards importiert für Benutzer-ID {user_id}.")
    except Exception as e:
        logger.error(f"Fehler beim Importieren der Flashcards: {e}")
        messagebox.showerror("Fehler", "Fehler beim Importieren der Flashcards.", parent=tk._get_temp_root())


def export_flashcards_to_csv(user_id):
    """
    Exportiert Flashcards in eine CSV-Datei.

    Parameter:
        user_id (int): Die ID des angemeldeten Benutzers.

    Return:
        None
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        title="CSV-Datei speichern",
        filetypes=(("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*"))
    )
    if not file_path:
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT front, back FROM flashcards WHERE user_id=?", (user_id,))
        flashcards = cursor.fetchall()
        conn.close()

        if not flashcards:
            messagebox.showwarning("Warnung", "Keine Flashcards zum Exportieren gefunden.", parent=tk._get_temp_root())
            return

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(flashcards)

        messagebox.showinfo("Erfolg", "Flashcards erfolgreich exportiert!", parent=tk._get_temp_root())
        logger.info(f"{len(flashcards)} Flashcards exportiert für Benutzer-ID {user_id}.")
    except Exception as e:
        logger.error(f"Fehler beim Exportieren der Flashcards: {e}")
        messagebox.showerror("Fehler", "Fehler beim Exportieren der Flashcards.", parent=tk._get_temp_root())