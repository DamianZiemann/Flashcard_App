Flashcard Learning Application

Beschreibung

Diese Flashcard-Anwendung ist ein einfaches Lernprogramm, das Benutzern ermöglicht, eigene Karteikarten zu erstellen, zu lernen und ihre Fortschritte zu verfolgen. Es ist in Python mit der GUI-Bibliothek Tkinter entwickelt und verwendet SQLite für die Datenbankverwaltung.

Funktionen

	•	Benutzerregistrierung und -anmeldung: Sichere Anmeldung mit gehashtem Passwort.
	•	Dashboard: Übersicht über die persönlichen Lernstatistiken.
	•	Flashcards hinzufügen: Möglichkeit, neue Flashcards zu erstellen.
	•	Flashcards lernen: Interaktives Lernmodul mit Erfolgsmessung.
	•	Importieren und Exportieren: Flashcards im CSV-Format importieren und exportieren.
	•	Statistiken: Verfolgung von Gesamtzahl, gelernten und korrekt beantworteten Flashcards sowie Genauigkeit.

Anforderungen

	•	Python 3.x
	•	SQLite (in Python integriert)
	•	Betriebssystem: Plattformunabhängig (Windows, macOS, Linux)

Installation

	1.	Repository klonen oder herunterladen:
        git clone https://github.com/dein-benutzername/flashcard-app.git
        cd flashcard-app

	2.	Virtuelle Umgebung erstellen (optional, aber empfohlen):
        python -m venv venv
        source venv/bin/activate  # Auf Windows: venv\Scripts\activate

    3.	Benötigte Pakete installieren:
        Es werden keine externen Pakete benötigt, da Tkinter und SQLite standardmäßig mit Python installiert sind.

Verwendung

	1.	Anwendung starten:
        python main.py

    2.	Registrierung:
	    Wenn du die Anwendung zum ersten Mal verwendest, registriere dich mit einem Benutzernamen und Passwort.
	    Der Benutzername muss einzigartig sein.
        
	3.	Anmeldung:
	    Melde dich mit deinem Benutzernamen und Passwort an.

	4.	Dashboard:
	    Nach der Anmeldung gelangst du zum Dashboard, das dir deine Lernstatistiken anzeigt.

	5.	Flashcards hinzufügen:
	    Klicke auf “Neue Flashcard hinzufügen”, um eine neue Karteikarte zu erstellen.
	    Gib die Vorder- und Rückseite der Karte ein und speichere sie.

	6.	Flashcards lernen:
	    Klicke auf “Flashcards lernen”, um mit dem Lernen zu beginnen.
	    Die Anwendung zeigt die Vorderseite der Karte an; klicke auf “Rückseite anzeigen”, um die Antwort zu sehen.
	    Bewerte, ob du die Karte wusstest oder nicht, indem du auf “Kannte ich” oder “Kannte ich nicht” klickst.

	7.	Importieren und Exportieren:
	    Importieren: Klicke auf “Flashcards importieren (CSV)” und wähle eine CSV-Datei aus, die deine Flashcards enthält. Das Format sollte pro Zeile “Vorderseite, Rückseite” sein.
	    Exportieren: Klicke auf “Flashcards exportieren (CSV)”, um deine Flashcards in eine CSV-Datei zu exportieren.

Code-Struktur

	•	main.py: Startet die Anwendung, initialisiert die Datenbank und ruft die Anmeldemaske auf.
	•	db_utils.py: Enthält Funktionen zur Initialisierung und Verwaltung der SQLite-Datenbank.
	•	logger_config.py: Konfiguriert das Logging der Anwendung.
	•	login_module.py: Handhabt die Benutzerregistrierung und -anmeldung.
	•	dashboard_module.py: Zeigt das Dashboard und die Statistiken an.
	•	add_flashcard_module.py: Ermöglicht das Hinzufügen neuer Flashcards.
	•	learn_flashcards_module.py: Enthält das Lernmodul zum Durcharbeiten der Flashcards.
	•	csv_utils.py: Bietet Funktionen zum Importieren und Exportieren von Flashcards im CSV-Format.
	•	flashcards.db: SQLite-Datenbankdatei (wird automatisch erstellt).

Lizenz

MIT License
    MIT License

    Copyright (c) 2024 Barath Vijayasegaran, Damian Ziemann

    Hiermit wird unentgeltlich jeder Person, die eine Kopie der Software und der zugehörigen Dokumentationen (die "Software") erhält, die Erlaubnis erteilt, sie uneingeschränkt zu benutzen, einschließlich ohne Einschränkung des Rechts, sie zu verwenden, kopieren, verändern, zusammenführen, veröffentlichen, vertreiben, unterlizenzieren und/oder zu verkaufen, und Personen, denen diese Software überlassen wird, diese Rechte zu verschaffen, unter den folgenden Bedingungen:

    Der obige Urheberrechtshinweis und dieser Erlaubnishinweis müssen in allen Kopien oder Teilkopien der Software enthalten sein.

    DIE SOFTWARE WIRD OHNE JEDE AUSDRÜCKLICHE ODER IMPLIZIERTE GARANTIE BEREITGESTELLT, EINSCHLIESSLICH DER GARANTIE DER MARKTREIFE, DER EIGNUNG FÜR EINEN BESTIMMTEN ZWECK UND DER NICHTVERLETZUNG. IN KEINEM FALL SIND DIE AUTOREN ODER URHEBERRECHTSINHABER FÜR JEGLICHEN SCHADEN ODER SONSTIGE ANSPRÜCHE HAFTBAR ZU MACHEN, OB INFOLGE DER ERFÜLLUNG EINES VERTRAGES, EINES DELIKTS ODER ANDERS IM ZUSAMMENHANG MIT DER SOFTWARE ODER SONSTIGER VERWENDUNG DER SOFTWARE ENTSTANDEN.

Autoren

	•	Barath Vijayasegaran
	•	Damian Ziemann

Danksagungen

	•	Tkinter: Für die Bereitstellung einer einfachen Möglichkeit, GUI-Anwendungen in Python zu erstellen.
	•	SQLite: Für die leichte und effiziente Datenbankverwaltung.
	•	Python Community: Für umfangreiche Dokumentation und Unterstützung.

Unterstützung und Beiträge

Bei Fragen oder Problemen kannst du gerne ein Issue auf GitHub erstellen oder uns direkt kontaktieren.

Beiträge sind herzlich willkommen! Bitte erstelle einen Fork des Projekts und sende uns einen Pull Request mit deinen Änderungen.

Haftungsausschluss

Diese Anwendung wird “wie besehen” bereitgestellt, ohne jegliche ausdrückliche oder implizierte Garantie. Die Autoren haften nicht für Schäden oder Verluste, die aus der Nutzung dieser Software entstehen.

Weitere Informationen

Diese Anwendung wurde im Rahmen eines Projekts entwickelt, um die Verwendung von Python für GUI-Anwendungen und Datenbankmanagement zu demonstrieren. Sie eignet sich ideal für Lernzwecke und kann leicht erweitert oder angepasst werden, um zusätzliche Funktionen zu integrieren.

Viel Spaß beim Lernen mit deiner neuen Flashcard-Anwendung!