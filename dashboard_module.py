# dashboard_module.py

"""
Modul: dashboard_module

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul zeigt das Dashboard nach erfolgreicher Anmeldung an und bietet Funktionen
zum Hinzufügen, Lernen, Importieren und Exportieren von Flashcards.
"""

import tkinter as tk
from tkinter import ttk
from db_utils import get_connection
import logging

logger = logging.getLogger(__name__)


def show_dashboard(user_id):
    """
    Erstellt das Dashboard für den angemeldeten Benutzer.

    Args:
        user_id (int): Die ID des angemeldeten Benutzers.
    """
    dash_win = tk.Tk()
    dash_win.title("Dashboard")
    dash_win.geometry("500x450")
    dash_win.resizable(False, False)

    style = ttk.Style(dash_win)
    style.theme_use('clam')

    main_frame = ttk.Frame(dash_win, padding="20 20 20 20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Labels für die Statistiken speichern
    stats_labels = {}

    def get_flashcard_stats():
        """Gibt verschiedene Statistiken des Benutzers zurück."""
        try:
            conn = get_connection()
            if not conn:
                return {}
            cursor = conn.cursor()
            stats = {}

            # Gesamtzahl der Flashcards
            cursor.execute("SELECT COUNT(*) FROM flashcards WHERE user_id=?", (user_id,))
            stats['total'] = cursor.fetchone()[0]

            # Anzahl der gelernten Flashcards (views > 0)
            cursor.execute("SELECT COUNT(*) FROM flashcards WHERE user_id=? AND views > 0", (user_id,))
            stats['learned'] = cursor.fetchone()[0]

            # Anzahl der korrekt beantworteten Flashcards
            cursor.execute("SELECT SUM(correct) FROM flashcards WHERE user_id=?", (user_id,))
            correct = cursor.fetchone()[0]
            stats['correct'] = correct if correct else 0

            # Genauigkeit
            stats['accuracy'] = round((stats['correct'] / stats['learned'] * 100), 2) if stats['learned'] > 0 else 0

            conn.close()
            return stats
        except Exception as e:
            logger.exception("Fehler beim Abrufen der Flashcard-Statistiken.")
            return {}

    def update_stats():
        """Aktualisiert die angezeigten Statistiken."""
        stats = get_flashcard_stats()
        stats_labels['total'].config(text=str(stats.get('total', 0)))
        stats_labels['learned'].config(text=str(stats.get('learned', 0)))
        stats_labels['correct'].config(text=str(stats.get('correct', 0)))
        stats_labels['accuracy'].config(text=f"{stats.get('accuracy', 0)}%")

    # Anzeige der Statistiken
    stats_frame = ttk.Frame(main_frame)
    stats_frame.pack(pady=10)

    ttk.Label(stats_frame, text="Flashcard-Statistiken", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(stats_frame, text="Gesamtzahl der Flashcards:").grid(row=1, column=0, sticky=tk.W)
    stats_labels['total'] = ttk.Label(stats_frame, text="")
    stats_labels['total'].grid(row=1, column=1, sticky=tk.W)

    ttk.Label(stats_frame, text="Anzahl gelernter Flashcards:").grid(row=2, column=0, sticky=tk.W)
    stats_labels['learned'] = ttk.Label(stats_frame, text="")
    stats_labels['learned'].grid(row=2, column=1, sticky=tk.W)

    ttk.Label(stats_frame, text="Anzahl korrekt beantworteter Flashcards:").grid(row=3, column=0, sticky=tk.W)
    stats_labels['correct'] = ttk.Label(stats_frame, text="")
    stats_labels['correct'].grid(row=3, column=1, sticky=tk.W)

    ttk.Label(stats_frame, text="Genauigkeit:").grid(row=4, column=0, sticky=tk.W)
    stats_labels['accuracy'] = ttk.Label(stats_frame, text="")
    stats_labels['accuracy'].grid(row=4, column=1, sticky=tk.W)

    # Initiale Aktualisierung der Statistiken
    update_stats()

    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)

    def open_add_flashcard():
        from add_flashcard_module import add_flashcard
        add_flashcard(user_id, update_dashboard_callback=update_stats)

    def open_learn_flashcards():
        from learn_flashcards_module import learn_flashcards
        learn_flashcards(user_id, update_dashboard_callback=update_stats)

    def import_flashcards():
        from csv_utils import import_flashcards_from_csv
        import_flashcards_from_csv(user_id)
        update_stats()

    def export_flashcards():
        from csv_utils import export_flashcards_to_csv
        export_flashcards_to_csv(user_id)

    add_button = ttk.Button(button_frame, text="Neue Flashcard hinzufügen", command=open_add_flashcard)
    add_button.grid(row=0, column=0, padx=10, pady=5)

    learn_button = ttk.Button(button_frame, text="Flashcards lernen", command=open_learn_flashcards)
    learn_button.grid(row=0, column=1, padx=10, pady=5)

    import_button = ttk.Button(button_frame, text="Flashcards importieren (CSV)", command=import_flashcards)
    import_button.grid(row=1, column=0, padx=10, pady=5)

    export_button = ttk.Button(button_frame, text="Flashcards exportieren (CSV)", command=export_flashcards)
    export_button.grid(row=1, column=1, padx=10, pady=5)

    # Passe die Spaltenbreite an und zentriere die Buttons
    for child in button_frame.winfo_children():
        child.grid_configure(padx=10, pady=5)

    # Urheberrechtshinweis oder Fußzeile
    footer_label = ttk.Label(main_frame, text="© 2024 Barath Vijayasegaran, Damian Ziemann", font=("Arial", 8))
    footer_label.pack(side=tk.BOTTOM, pady=10)

    dash_win.mainloop()