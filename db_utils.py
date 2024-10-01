# db_utils.py

"""
Modul: db_utils

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul enthält Funktionen zur Initialisierung und Verwaltung der SQLite-Datenbank
für die Flashcard-Anwendung.
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


def init_db():
    """
    Initialisiert die Datenbank und erstellt die notwendigen Tabellen.
    """
    try:
        conn = sqlite3.connect('flashcards.db')
        cursor = conn.cursor()

        # Tabelle für Benutzer erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')

        # Tabelle für Flashcards erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                correct INTEGER DEFAULT 0,
                last_review DATE,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        logger.info("Datenbank initialisiert und Tabellen erstellt.")
    except sqlite3.Error as e:
        logger.exception("Fehler bei der Initialisierung der Datenbank.")
    finally:
        conn.close()


def get_connection():
    """
    Stellt eine Verbindung zur Datenbank her.

    Returns:
        conn (sqlite3.Connection): Datenbankverbindung
    """
    try:
        conn = sqlite3.connect('flashcards.db')
        return conn
    except sqlite3.Error as e:
        logger.exception("Fehler bei der Verbindung zur Datenbank.")
        return None