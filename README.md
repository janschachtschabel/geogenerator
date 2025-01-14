# Ortsdaten-Recherche Tool
Dieses Tool ermöglicht es, OpenStreetMap-Daten über die Overpass API abzufragen – speziell zu interessanten Einrichtungen und Objekten. Das Tool bietet dabei folgende Funktionen:

# Objektklassenauswahl:
Eine umfangreiche Dropdown-Auswahl an OSM-Objektklassen (z. B. Bar, Biergarten, Café, Museum, Galerie, Attraktion, Restaurant etc.).
Für einige Objektklassen (wie Museum, Galerie oder Attraktion) wird bei der Abfrage der Schlüssel tourism genutzt (z. B. tourism=museum), während für den Großteil der übrigen Objektklassen amenity verwendet wird.

# Geografische Bereiche:
Auswahlmöglichkeiten für den geografischen Bereich:

# Deutschland (gesamt)
Einzelne Bundesländer (z. B. "Thüringen")
Deutschland (Schleifen-Modus): Hierbei werden alle 16 Bundesländer einzeln abgefragt, um Timeouts zu vermeiden und anschließend die Ergebnisse zusammengeführt.
Timeout-Eingabefeld:
Möglichkeit, das Timeout (in Sekunden) für die Overpass-Abfrage festzulegen (Standard: 300 Sekunden).

# Ergebnisvorschau:
Es kann optional eine Ergebnisvorschau angezeigt werden, inklusive JSON-Textfeld, Tabelle und einer breiten Kartenansicht via Folium (mittels st_folium).

# Hilfeseiten:
Zwei klickbare Links zu den OpenStreetMap-Wiki-Seiten für detaillierte Informationen:

DE:Key:amenity
Key:tourism
Voraussetzungen
Stelle sicher, dass Python (3.x) installiert ist.

# Installation
Klone dieses Repository oder lade den Code herunter.

Installiere die benötigten Pakete, indem du die Datei requirements.txt verwendest:

bash
Code kopieren
pip install -r requirements.txt
Beispiel für die requirements.txt:

txt
Code kopieren
streamlit
requests
overpy
pandas
geopy
folium
streamlit-folium
Nutzung
Starte die Anwendung mit dem folgenden Befehl:

bash
Code kopieren
streamlit run <dateiname.py>
(Beispiel: streamlit run app.py)

# Anwendung
Hilfeseiten:
Am Seitenanfang findest du zwei Links, die zu den OSM-Wiki-Seiten für amenity und tourism führen. Diese bieten detaillierte Informationen zu den verfügbaren Werten.

# Suchparameter einstellen:

Wähle im Dropdown-Menü die gewünschte Objektklasse aus.
Bestimme den geografischen Bereich (einzelnes Bundesland, Deutschland oder Deutschland (Schleifen-Modus)).
Lege das Timeout für die Overpass-Abfrage fest (Standard sind 300 Sekunden).
Wähle, ob die Ergebnisvorschau angezeigt werden soll.
Daten abfragen:
Klicke auf "Daten abfragen". Bei Auswahl des Schleifen-Modus werden die Daten für alle 16 Bundesländer einzeln abgefragt und anschließend zusammengeführt.

# Ergebnisvorschau und Download:
Nach erfolgreicher Abfrage werden (sofern aktiviert) das JSON-Ergebnis, eine Tabelle und eine Kartenansicht angezeigt. Alternativ kannst du die Ergebnisse als JSON herunterladen.

# Weiterentwicklung
Mögliche Erweiterungen und Verbesserungen:

Multi-Select für Objektklassen: Ermögliche die gleichzeitige Auswahl mehrerer Typen.
Erweiterte Detail-Popups: Zeige beim Klick auf einen Kartenmarker erweiterte Informationen und Bilder an.
Fortschrittsanzeige im Schleifen-Modus: Zeige einen Fortschrittsbalken an, um den aktuellen Status der Abfragen besser sichtbar zu machen.
Export in alternative Formate: Neben JSON auch GeoJSON, CSV oder Shapefile exportieren.
Lizenz
Dieses Projekt ist Open Source. Bitte beachte die jeweiligen Lizenzen der verwendeten Daten (z. B. ODbL für OSM-Daten).
