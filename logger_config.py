# logger_config.py

"""
Modul: logger_config

Ersteller: Barath Vijayasegaran, Damian Ziemann
Datum: 07.10.2024
Version: 3.0
Lizenz: MIT
Kurzbeschreibung:
Dieses Modul konfiguriert das Logging für die Anwendung.
"""

import logging

def setup_logging():
    """
    Konfiguriert das Logging der Anwendung.
    """
    logging.basicConfig(
        filename='app.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )