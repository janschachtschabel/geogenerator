# Adressdaten-Abfrage – OSM & Wikidata

Dieses Projekt ist ein Streamlit-Tool zur Abfrage von Adress- und Ortsdaten aus zwei Quellen:

- **OpenStreetMap Overpass API** – um OSM-Daten wie Objektinformationen (z. B. Bars, Cafés, Museen) abzurufen.
- **Wikidata SPARQL-Endpunkt** – um zusätzliche Informationen zu denselben Objekten über Wikidata zu erlangen.

Das Tool ermöglicht es, die Datenquellen einzeln oder kombiniert abzufragen. Bei der kombinierten Abfrage besteht zudem die Möglichkeit, Ergebnisse getrennt anzuzeigen oder mithilfe einer Dublettenbereinigung (basierend auf Name und Webseite) zusammenzuführen.

## Features

- **Flexibles Datenquellen-Management:** Wähle per Sidebar zwischen OSM, Wikidata oder beiden.
- **Objektklassen-Auswahl:** Bei kombinierter Abfrage wird die Schnittmenge der verfügbaren Objektklassen angezeigt.
- **Geografische Abfragen:** Wähle einen einzelnen geografischen Bereich (z. B. ein Bundesland) oder den Modus „Ganz Deutschland“. Im letzteren Fall werden alle Bundesländer einzeln abgefragt.
- **Dublettenbereinigung:** Option zur Zusammenführung von Ergebnissen mit Filterung doppelter Einträge (basierend auf Name und Webseite).
- **Konfigurierbare Parameter:** Stelle Timeout-Werte für die OSM-Abfrage sowie das LIMIT für die Wikidata-Abfrage ein.
- **Ergebnisvisualisierung:** Ergebnisse werden als JSON und in Tabellenform angezeigt, inklusive einer Kartenvisualisierung (sofern OSM-Koordinaten vorhanden sind).

## Installation

1. Klone das Repository oder lade die Projektdateien herunter.
2. Stelle sicher, dass [Python](https://www.python.org/) installiert ist.
3. Installiere die benötigten Pakete, indem du im Projektverzeichnis folgenden Befehl ausführst:

   ```bash
   pip install -r requirements.txt
   ```

##  Verwendung
Starte die Streamlit-App mit:

   ```bash
streamlit run app.py
   ```

Öffne deinen Browser (normalerweise unter http://localhost:8501) und nutze die Benutzeroberfläche:

- **Datenquelle wählen:** Wähle in der Sidebar die zu verwendende(n) Datenquelle(n): OSM Overpass, Wikidata oder beide.
- **Objektklasse auswählen:** Wähle die gewünschte Objektklasse aus dem Dropdown-Menü aus.
- **Geografischen Bereich wählen:** Wähle einen Bereich (z. B. „Thüringen“ oder „Ganz Deutschland“).
- **Hinweis:** Bei "Ganz Deutschland" werden alle Bundesländer der Reihe nach abgearbeitet.
- **Timeout und LIMIT:** Stelle den Timeout (für OSM) und das LIMIT (für Wikidata, Standard 1000) ein.
- **Ergebnisanzeige:** Entscheide über die Anzeige – getrennt oder gemeinsam (mit Dublettenbereinigung). Klicke auf „Abfrage starten“, um die Ergebnisse abzurufen. Die Ergebnisse werden in Form einer JSON-Ausgabe und als Tabelle angezeigt. Bei gemeinsamer Anzeige können die Daten zudem zusammengeführt werden, wobei Dubletten anhand des Namens oder der Webseite entfernt werden.

## Anpassungen
- **Erweiterung der Objektklassen:**
Die Mappings für OSM und Wikidata befinden sich im Quellcode. Füge bei Bedarf weitere Einträge hinzu.

## API-Parameter:
Passe Timeout-Werte, LIMIT oder andere Parameter an deine Bedürfnisse an.

## Contributing
Beiträge sind willkommen! Falls du Verbesserungsvorschläge, neue Features oder Bugfixes hast, erstelle bitte einen Pull Request oder öffne ein Issue.

## Lizenz
Apache 2.0
