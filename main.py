# main.py

"""
Modul: main

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 2.0
Lizenz: MIT
Kurzbeschreibung:
Dies ist die Hauptdatei der Flashcard-Anwendung. Sie initialisiert die Datenbank und startet die Anmeldemaske.
"""

from db_utils import init_db
from login_module import login_screen
from logger_config import setup_logging

if __name__ == "__main__":
    setup_logging()
    init_db()
    login_screen()