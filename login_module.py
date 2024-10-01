# login_module.py

"""
Modul: login_module

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.1
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul enthält die Anmeldemaske und die Funktionen zur Registrierung und Anmeldung der Benutzer.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from db_utils import get_connection
import hashlib
import logging

logger = logging.getLogger(__name__)


def login_screen():
    """
    Erstellt die Anmeldemaske für das Programm.
    """
    login_win = tk.Tk()
    login_win.title("Anmeldung")
    login_win.geometry("400x250")
    login_win.resizable(False, False)

    style = ttk.Style(login_win)
    style.theme_use('clam')

    main_frame = ttk.Frame(login_win, padding="20 20 20 20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Benutzername
    ttk.Label(main_frame, text="Benutzername:").grid(row=0, column=0, pady=10, sticky=tk.W)
    username_entry = ttk.Entry(main_frame)
    username_entry.grid(row=0, column=1, pady=10, sticky=tk.EW)

    # Passwort
    ttk.Label(main_frame, text="Passwort:").grid(row=1, column=0, pady=10, sticky=tk.W)
    password_entry = ttk.Entry(main_frame, show="*")
    password_entry.grid(row=1, column=1, pady=10, sticky=tk.EW)

    # Grid-Konfiguration
    main_frame.columnconfigure(1, weight=1)

    def hash_password(password):
        """
        Hasht das Passwort mit SHA-256.

        Args:
            password (str): Das zu hashende Passwort.

        Returns:
            str: Der gehashte Passwort-Hash.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_input(username, password):
        """
        Validiert die Benutzereingaben.

        Returns:
            bool: True, wenn die Eingaben gültig sind, sonst False.
        """
        if not username or not password:
            messagebox.showwarning("Warnung", "Bitte alle Felder ausfüllen.", parent=login_win)
            return False
        if len(password) < 6:
            messagebox.showwarning("Warnung", "Das Passwort muss mindestens 6 Zeichen lang sein.", parent=login_win)
            return False
        return True

    def register():
        """Registriert einen neuen Benutzer."""
        username = username_entry.get().strip()
        password = password_entry.get()

        if not validate_input(username, password):
            return

        hashed_password = hash_password(password)

        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen.", parent=login_win)
                return
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Fehler", "Benutzername existiert bereits!", parent=login_win)
                logger.warning(f"Registrierungsversuch mit bestehendem Benutzernamen: {username}")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich!", parent=login_win)
                logger.info(f"Neuer Benutzer registriert: {username}")
        except Exception as e:
            logger.exception("Fehler bei der Registrierung.")
            messagebox.showerror("Fehler", "Registrierung fehlgeschlagen.", parent=login_win)
        finally:
            if conn:
                conn.close()

    def login():
        """Meldet einen bestehenden Benutzer an."""
        username = username_entry.get().strip()
        password = password_entry.get()

        if not validate_input(username, password):
            return

        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Fehler", "Datenbankverbindung fehlgeschlagen.", parent=login_win)
                return
            cursor = conn.cursor()

            cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            if user and hash_password(password) == user[1]:
                messagebox.showinfo("Erfolg", "Anmeldung erfolgreich!", parent=login_win)
                logger.info(f"Benutzer angemeldet: {username}")
                login_win.destroy()
                from dashboard_module import show_dashboard
                show_dashboard(user[0])
            else:
                messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort!", parent=login_win)
                logger.warning(f"Fehlgeschlagener Anmeldeversuch für Benutzer: {username}")
        except Exception as e:
            logger.exception("Fehler bei der Anmeldung.")
            messagebox.showerror("Fehler", "Anmeldung fehlgeschlagen.", parent=login_win)
        finally:
            if conn:
                conn.close()

    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=20)

    register_button = ttk.Button(button_frame, text="Registrieren", command=register)
    register_button.grid(row=0, column=0, padx=10)

    login_button = ttk.Button(button_frame, text="Anmelden", command=login)
    login_button.grid(row=0, column=1, padx=10)

    login_win.mainloop()