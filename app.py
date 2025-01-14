import streamlit as st
import requests
import overpy
import json
import pandas as pd
from geopy.geocoders import Nominatim
from decimal import Decimal
import folium
from streamlit_folium import st_folium

######################################
# Modul: OpenStreetMap Overpass-Abfrage
######################################

# Mapping von deutschen Objektklassen zu OSM-Werten
ENTITY_AMENITY_OPTIONS = {
    "Bar": "bar",
    "Biergarten": "biergarten",
    "Café": "cafe",
    "Fast Food": "fast_food",
    "Food Court": "food_court",
    "Eisdiele": "ice_cream",
    "Pub": "pub",
    "Restaurant": "restaurant",
    "Museum": "museum",       # Hier wird bei manchen Typen später "tourism" genutzt
    "Galerie": "gallery",
    "Attraktion": "attraction",
    "Camp Site": "camp_site",
    "Caravan Site": "caravan_site",
    "Chalet": "chalet",
    "Guest House": "guest_house",
    "Hostel": "hostel",
    "Hotel": "hotel",
    "Information": "information",
    "Motel": "motel",
    "Picnic Site": "picnic_site",
    "Theme Park": "theme_park",
    "Trail Riding Station": "trail_riding_station",
    "Viewpoint": "viewpoint",
    "Wilderness Hut": "wilderness_hut",
    "Zoo": "zoo",
    "College": "college",
    "Tanzschule": "dancing_school",
    "Fahrschule": "driving_school",
    "Erste-Hilfe-Schule": "first_aid_school",
    "Kindergarten": "kindergarten",
    "Sprachschule": "language_school",
    "Bibliothek": "library",
    "Surfschule": "surf_school",
    "Spielzeugbibliothek": "toy_library",
    "Forschungsinstitut": "research_institute",
    "Trainingsstätte": "training",
    "Musikschule": "music_school",
    "Schule": "school",
    "Verkehrsschule": "traffic_park",
    "Universität": "university",
    "Fahrradparkplatz": "bicycle_parking",
    "Fahrradreparaturstation": "bicycle_repair_station",
    "Fahrradverleih": "bicycle_rental",
    "Fahrradwaschanlage": "bicycle_wash",
    "Bootsverleih": "boat_rental",
    "Boots-Sharing": "boat_sharing",
    "Bushaltestelle": "bus_station",
    "Autoverleih": "car_rental",
    "Carsharing": "car_sharing",
    "Autowäsche": "car_wash",
    "Luftkompressor": "compressed_air",
    "Fahrzeuginspektion": "vehicle_inspection",
    "Ladestation": "charging_station",
    "Fahrsicherheitstraining": "driver_training",
    "Fährterminal": "ferry_terminal",
    "Tankstelle": "fuel",
    "Streugut-Container": "grit_bin",
    "Motorradparkplatz": "motorcycle_parking",
    "Parkplatz": "parking",
    "Parkplatzeingang": "parking_entrance",
    "Einzelner Parkplatz": "parking_space",
    "Taxistand": "taxi",
    "Waage": "weighbridge",
    "Geldautomat": "atm",
    "Zahlungsterminal": "payment_terminal",
    "Bank": "bank",
    "Wechselstube": "bureau_de_change",
    "Geldtransfer": "money_transfer",
    "Zahlungszentrum": "payment_centre",
    "Babyklappe": "baby_hatch",
    "Klinik": "clinic",
    "Zahnarzt": "dentist",
    "Arztpraxis": "doctors",
    "Krankenhaus": "hospital",
    "Pflegeheim": "nursing_home",
    "Apotheke": "pharmacy",
    "Sozialeinrichtung": "social_facility",
    "Tierarzt": "veterinary",
    "Kulturzentrum": "arts_centre",
    "Bordell": "brothel",
    "Casino": "casino",
    "Kino": "cinema",
    "Gemeinschaftszentrum": "community_centre",
    "Kongresszentrum": "conference_centre",
    "Veranstaltungsort": "events_venue",
    "Ausstellungszentrum": "exhibition_centre",
    "Springbrunnen": "fountain",
    "Glücksspiel": "gambling",
    "Liebeshotel": "love_hotel",
    "Musikveranstaltungsort": "music_venue",
    "Nachtclub": "nightclub",
    "Planetarium": "planetarium",
    "Öffentlicher Bücherschrank": "public_bookcase",
    "Soziales Zentrum": "social_centre",
    "Bühne": "stage",
    "Stripclub": "stripclub",
    "Studio": "studio",
    "Swingerclub": "swingerclub",
    "Theater": "theatre",
    "Gericht": "courthouse",
    "Feuerwache": "fire_station",
    "Polizeistation": "police",
    "Briefkasten": "post_box",
    "Postdepot": "post_depot",
    "Postamt": "post_office",
    "Gefängnis": "prison",
    "Besucherzentrum": "ranger_station",
    "Rathaus": "townhall",
    "Grillplatz": "bbq",
    "Bankbank": "bench",
    "Hundetoilette": "dog_toilet",
    "Umkleideraum": "dressing_room",
    "Trinkwasserstelle": "drinking_water",
    "Tauschecke": "give_box",
    "Lounge": "lounge",
    "Postraum": "mailroom",
    "Paketfach": "parcel_locker",
    "Unterstand": "shelter",
    "Duscheinrichtung": "shower",
    "Öffentliche Telefonzelle": "telephone",
    "Öffentliche Toilette": "toilets",
    "Wasserzapfstelle": "water_point",
    "Wassertrog": "watering_place",
    "Sanitäre Entsorgungsstation": "sanitary_dump_station",
    "Recyclingstation": "recycling",
    "Mülleimer": "waste_basket",
    "Abfallentsorgung": "waste_disposal",
    "Abfallumladestation": "waste_transfer_station",
    "Tierpension": "animal_boarding",
    "Tierzucht": "animal_breeding",
    "Tierheim": "animal_shelter",
    "Tiertraining": "animal_training",
    "Backofen": "baking_oven",
    "Öffentliche Uhr": "clock",
    "Krematorium": "crematorium",
    "Tauchbasis": "dive_centre",
    "Trauerhalle": "funeral_hall",
    "Friedhof": "grave_yard",
    "Hochsitz": "hunting_stand",
    "Internetcafé": "internet_cafe",
    "Öffentliche Küche": "kitchen",
    "Kneipp-Wassertreten": "kneipp_water_cure",
    "Liege": "lounger",
    "Marktplatz": "marketplace",
    "Kloster": "monastery",
    "Leichenschauhaus": "mortuary",
    "Fotoautomat": "photo_booth",
    "Trauerraum": "place_of_mourning",
    "Andachtsstätte": "place_of_worship",
    "Öffentliches Bad": "public_bath",
    "Öffentliches Gebäude": "public_building",
    "Flüchtlingssiedlung": "refugee_site",
    "Verkaufsautomat": "vending_machine",
    "Benutzerdefiniert": "user_defined"
}

# Hilfsfunktion zum Anzeigen der OSM-Objektklassen (zur Kontrolle)
def list_amenity_options():
    st.write("Verfügbare OSM Objektklassen (Key → Value):")
    for key, value in ENTITY_AMENITY_OPTIONS.items():
        st.write(f"{key} → {value}")

# Ermittlung der OSM Area ID (z. B. anhand eines Bundeslandnamens)
def get_osm_area_id(area_name):
    api = overpy.Overpass()
    query = f"""
    [out:json][timeout:25];
    relation["admin_level"="4"]["name"="{area_name}"]["boundary"="administrative"];
    out ids;
    """
    try:
        result = api.query(query)
        if not result.relations:
            return None
        relation_id = result.relations[0].id
        return 3600000000 + relation_id
    except Exception as e:
        st.error(f"Fehler bei der Ermittlung der OSM Area ID: {e}")
        return None

# Abfrage von OSM Overpass
def query_osm_overpass(entity_label, area, timeout_sec):
    api = overpy.Overpass()
    if entity_label in ["Museum", "Galerie", "Attraktion", "Camp Site", "Caravan Site", "Chalet",
                        "Guest House", "Hostel", "Hotel", "Information", "Motel", "Picnic Site",
                        "Theme Park", "Trail Riding Station", "Viewpoint", "Wilderness Hut", "Zoo"]:
        search_key = "tourism"
    else:
        search_key = "amenity"
    search_value = ENTITY_AMENITY_OPTIONS.get(entity_label)
    if not search_value:
        st.error(f"Für die Objektklasse '{entity_label}' wurde kein Wert definiert.")
        return []
    
    if area not in ["Ganz Deutschland", "Deutschland (Schleifen-Modus)"]:
        area_id = get_osm_area_id(area)
        if not area_id:
            st.error(f"Geografische Einschränkung für '{area}' konnte nicht gefunden werden.")
            return []
        area_filter = f"area({area_id})->.searchArea;"
    else:
        # Standard OSM Area ID für Deutschland
        area_filter = "area(3600000183)->.searchArea;"
    
    query = f"""
    [out:json][timeout:{timeout_sec}];
    {area_filter}
    (
      node["{search_key}"="{search_value}"]["name"~".*"](area.searchArea);
      way["{search_key}"="{search_value}"]["name"~".*"](area.searchArea);
      relation["{search_key}"="{search_value}"]["name"~".*"](area.searchArea);
    );
    out center;
    """
    st.write("### Overpass-Abfrage (OSM):")
    st.code(query, language='xml')
    
    try:
        result = api.query(query)
        items = []
        for element in result.nodes + result.ways + result.relations:
            if isinstance(element, overpy.Node):
                lat, lon = element.lat, element.lon
            elif hasattr(element, 'center_lat') and hasattr(element, 'center_lon'):
                lat, lon = element.center_lat, element.center_lon
            else:
                lat, lon = None, None
            item = {
                "name": element.tags.get("name", ""),
                "beschreibung": element.tags.get("description", ""),
                "website": element.tags.get("website", ""),
                "telefon": element.tags.get("phone", ""),
                "fax": element.tags.get("fax", ""),
                "email": element.tags.get("email", ""),
                "straße": element.tags.get("addr:street", ""),
                "plz": element.tags.get("addr:postcode", ""),
                "ort": element.tags.get("addr:city", ""),
                "geodaten": {"lat": float(lat), "lon": float(lon)} if lat and lon else ""
            }
            # Nur Datensätze mit Name und Adressinformationen aufnehmen
            if item["name"] and item["straße"] and item["plz"] and item["ort"]:
                items.append(item)
        return items
    except overpy.exception.OverpassTooManyRequests:
        st.error("Zu viele Anfragen an die Overpass API. Bitte versuche es später erneut.")
        return []
    except overpy.exception.OverpassGatewayTimeout:
        st.error("Die Overpass API hat die Anfrage nicht rechtzeitig bearbeitet. Bitte versuche es später erneut.")
        return []
    except Exception as e:
        st.error(f"Fehler bei der OSM-Abfrage: {e}")
        return []

######################################
# Modul: Wikidata-Abfrage
######################################

# Mapping von Entitätsklassen zu ihren Wikidata-IDs
ENTITY_CLASSES_WIKIDATA = {
    "Bar": "Q570116",
    "Biergarten": "Q25387",
    "Café": "Q213684",
    "Fast Food": "Q18534542",
    "Food Court": "Q14752696",
    "Eisdiele": "Q2101909",
    "Pub": "Q133492",
    "Restaurant": "Q11707",
    "Museum": "Q33506",
    "Galerie": "Q207694",
    "Attraktion": "Q570116",
    "Campingplatz": "Q16917",
    "Wohnmobilstellplatz": "Q16917",
    "Chalet": "Q3947",
    "Gästehaus": "Q3947",
    "Hostel": "Q27686",
    "Hotel": "Q27686",
    "Informationsstelle": "Q11032",
    "Motel": "Q27686",
    "Picknickplatz": "Q570116",
    "Freizeitpark": "Q570116",
    "Reitstation": "Q570116",
    "Aussichtspunkt": "Q570116",
    "Schutzhütte": "Q570116",
    "Zoo": "Q43501",
    "Hochschule": "Q3918",
    "Tanzschule": "Q3918",
    "Fahrschule": "Q3918",
    "Erste-Hilfe-Schule": "Q3918",
    "Kindergarten": "Q3914",
    "Sprachschule": "Q3918",
    "Bibliothek": "Q7075",
    "Surfschule": "Q3918",
    "Spielzeugbibliothek": "Q7075",
    "Forschungsinstitut": "Q31855",
    "Trainingsstätte": "Q3918",
    "Musikschule": "Q3918",
    "Schule": "Q3914",
    "Verkehrsschule": "Q3918",
    "Universität": "Q3918",
    "Fahrradparkplatz": "Q570116",
    "Fahrradreparaturstation": "Q570116",
    "Fahrradverleih": "Q570116",
    "Fahrradwaschanlage": "Q570116",
    "Bootsverleih": "Q570116",
    "Boots-Sharing": "Q570116",
    "Bushaltestelle": "Q570116",
    "Autoverleih": "Q570116",
    "Carsharing": "Q570116",
    "Autowäsche": "Q570116",
    "Luftkompressor": "Q570116",
    "Fahrzeuginspektion": "Q570116",
    "Ladestation": "Q570116",
    "Fahrsicherheitstraining": "Q3918",
    "Fährterminal": "Q570116",
    "Tankstelle": "Q570116",
    "Streugut-Container": "Q570116",
    "Motorradparkplatz": "Q570116",
    "Parkplatz": "Q570116",
    "Parkplatzeingang": "Q570116",
    "Einzelner Parkplatz": "Q570116",
    "Taxistand": "Q570116",
    "Waage": "Q570116",
    "Geldautomat": "Q570116",
    "Zahlungsterminal": "Q570116",
    "Bank": "Q570116",
    "Wechselstube": "Q570116",
    "Geldtransfer": "Q570116",
    "Zahlungszentrum": "Q570116",
    "Babyklappe": "Q570116",
    "Klinik": "Q16917",
    "Zahnarzt": "Q570116",
    "Arztpraxis": "Q570116",
    "Krankenhaus": "Q16917",
    "Pflegeheim": "Q570116",
    "Apotheke": "Q570116",
    "Sozialeinrichtung": "Q570116",
    "Tierarzt": "Q570116",
    "Kulturzentrum": "Q570116",
    "Bordell": "Q570116",
    "Casino": "Q570116",
    "Kino": "Q570116",
    "Gemeinschaftszentrum": "Q570116",
    "Kongresszentrum": "Q570116",
    "Veranstaltungsort": "Q570116",
    "Ausstellungszentrum": "Q570116",
    "Museen": "Q33506",
    "Schulen": "Q3914",
    "Theater": "Q11641",
    "Bibliotheken": "Q7075",
    "Krankenhäuser": "Q16917",
    "Universitäten": "Q3918"
}

# Mapping von Bundesländern zu ihren Wikidata-IDs (für Wikidata)
BUNDESLAENDER_WIKIDATA = {
    "Ganz Deutschland": "Q183",
    "Baden-Württemberg": "Q980",
    "Bayern": "Q980",
    "Berlin": "Q64",
    "Brandenburg": "Q1202",
    "Bremen": "Q2481",
    "Hamburg": "Q1055",
    "Hessen": "Q1198",
    "Mecklenburg-Vorpommern": "Q1199",
    "Niedersachsen": "Q1197",
    "Nordrhein-Westfalen": "Q1199",
    "Rheinland-Pfalz": "Q1200",
    "Saarland": "Q1201",
    "Sachsen": "Q1202",
    "Sachsen-Anhalt": "Q1203",
    "Schleswig-Holstein": "Q1199",
    "Thüringen": "Q1205"
}

# Funktion zum Erstellen der SPARQL-Abfrage für Wikidata (mit dynamischem LIMIT)
def create_sparql_query_wikidata(entity_qid, region_qid, limit):
    region_filter = f"?item wdt:P131* wd:{region_qid} ." if region_qid else ""
    query = f"""
    SELECT ?item ?itemLabel ?description ?website ?phone ?fax ?email ?streetAddress ?postalCode ?cityLabel ?coordinate
    WHERE {{
      ?item wdt:P31 wd:{entity_qid} .
      {region_filter}
      OPTIONAL {{ ?item wdt:P856 ?website. }}
      OPTIONAL {{ ?item wdt:P1329 ?phone. }}
      OPTIONAL {{ ?item wdt:P2900 ?fax. }}
      OPTIONAL {{ ?item wdt:P968 ?email. }}
      OPTIONAL {{ ?item wdt:P6375 ?streetAddress. }}
      OPTIONAL {{ ?item wdt:P281 ?postalCode. }}
      OPTIONAL {{ ?item wdt:P131 ?city. }}
      OPTIONAL {{ ?item wdt:P625 ?coordinate. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }}
    }}
    LIMIT {limit}
    """
    return query

# Funktion zum Ausführen der SPARQL-Abfrage für Wikidata
def execute_sparql_query_wikidata(query):
    url = 'https://query.wikidata.org/sparql'
    headers = {'Accept': 'application/sparql-results+json'}
    response = requests.get(url, params={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Fehler bei der Abfrage von Wikidata.")
        return None

######################################
# Hilfsfunktion zur Dublettenbereinigung
######################################
def deduplicate_results(entries):
    deduped = []
    seen_names = set()
    seen_websites = set()
    for entry in entries:
        # Falls Website vorhanden ist, prüfen wir darauf; ansonsten Name
        name = entry.get("name", "").strip().lower()
        website = entry.get("website", "").strip().lower()
        if (name and name in seen_names) or (website and website in seen_websites):
            continue
        deduped.append(entry)
        if name:
            seen_names.add(name)
        if website:
            seen_websites.add(website)
    return deduped

######################################
# Hauptbereich: Benutzeroberfläche
######################################

st.title("Adressdaten-Abfrage – OSM & Wikidata")

# Auswahl der Datenquelle(n)
data_sources = st.sidebar.multiselect(
    "Wähle die Datenquelle(n):",
    options=["OpenStreetMap Overpass", "Wikidata"],
    default=["OpenStreetMap Overpass"]
)

# Bei mehreren Quellen: Option, ob getrennte oder gemeinsame Ergebnisse (mit Dublettenbereinigung) angezeigt werden sollen
if len(data_sources) > 1:
    merge_option = st.sidebar.radio("Ergebnisanzeige:", options=["Getrennt anzeigen", "Gemeinsam (Dubletten bereinigen)"])
else:
    merge_option = "Getrennt anzeigen"

# Gemeinsame Auswahl der Objektklasse:
# Wenn beide Quellen ausgewählt sind, wird die Schnittmenge der Klassen angezeigt.
if "OpenStreetMap Overpass" in data_sources and "Wikidata" in data_sources:
    common_classes = sorted(set(ENTITY_AMENITY_OPTIONS.keys()) & set(ENTITY_CLASSES_WIKIDATA.keys()))
    selected_class = st.selectbox("Wähle die Objektklasse (für beide Quellen):", common_classes)
elif "OpenStreetMap Overpass" in data_sources:
    osm_classes = list(ENTITY_AMENITY_OPTIONS.keys())
    selected_class = st.selectbox("OSM: Wähle die Objektklasse:", osm_classes, index=osm_classes.index("Bar") if "Bar" in osm_classes else 0)
elif "Wikidata" in data_sources:
    wd_classes = list(ENTITY_CLASSES_WIKIDATA.keys())
    selected_class = st.selectbox("Wikidata: Wähle die Objektklasse:", wd_classes, index=wd_classes.index("Bar") if "Bar" in wd_classes else 0)
else:
    selected_class = None

# Auswahl des geografischen Bereichs
bundeslaender = [
    "Ganz Deutschland",
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg",
    "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
    "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
    "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
]
default_area = "Thüringen" if "Thüringen" in bundeslaender else bundeslaender[0]
selected_area = st.selectbox("Wähle den geografischen Bereich:", bundeslaender, index=bundeslaender.index(default_area))

timeout_sec = st.number_input("Timeout für OSM-Abfrage (in Sekunden):", min_value=30, max_value=600, step=30, value=300)

# Eingabefeld für Wikidata LIMIT (Standard: 1000)
wikidata_limit = st.number_input("Limit für Wikidata-Abfrage:", min_value=10, max_value=10000, step=10, value=1000)

######################################
# Variante: Falls "Ganz Deutschland" gewählt, alle Bundesländer in Schleife abarbeiten
######################################
def query_all_bundeslaender(source, query_func, selected_entity, timeout_sec_val=None, limit_val=None):
    # Liste aller Bundesländer (ohne "Ganz Deutschland")
    alle_bundeslaender = [
        "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg",
        "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
        "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
        "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
    ]
    all_results = []
    for bl in alle_bundeslaender:
        st.write(f"Abfrage für {bl}...")
        if source == "OpenStreetMap Overpass":
            res = query_func(selected_entity, bl, timeout_sec_val)
        elif source == "Wikidata":
            # Für Wikidata nutzen wir die spezifischen Mappings und den LIMIT-Wert
            wd_qid = ENTITY_CLASSES_WIKIDATA.get(selected_entity)
            bl_qid = BUNDESLAENDER_WIKIDATA.get(bl)
            if wd_qid and bl_qid:
                query_wd = create_sparql_query_wikidata(wd_qid, bl_qid, limit_val)
                st.code(query_wd, language='sparql')
                data = execute_sparql_query_wikidata(query_wd)
                res = []
                if data:
                    for item in data['results']['bindings']:
                        res.append({
                            'name': item.get('itemLabel', {}).get('value', ''),
                            'beschreibung': item.get('description', {}).get('value', ''),
                            'website': item.get('website', {}).get('value', ''),
                            'telefon': item.get('phone', {}).get('value', ''),
                            'fax': item.get('fax', {}).get('value', ''),
                            'email': item.get('email', {}).get('value', ''),
                            'straße': item.get('streetAddress', {}).get('value', ''),
                            'plz': item.get('postalCode', {}).get('value', ''),
                            'ort': item.get('cityLabel', {}).get('value', ''),
                            'geodaten': item.get('coordinate', {}).get('value', '')
                        })
            else:
                res = []
        st.write(f"{bl}: {len(res)} Einträge")
        all_results.extend(res)
    return all_results

######################################
# Abfrage starten
######################################
if st.button("Abfrage starten"):
    results_dict = {}  # Ergebnisse je Quelle
    # Variante: Wenn "Ganz Deutschland" gewählt, Schleife über Bundesländer
    if selected_area == "Ganz Deutschland":
        # OSM
        if "OpenStreetMap Overpass" in data_sources:
            st.info("Starte OSM-Abfrage für ganz Deutschland (alle Bundesländer in Schleife)...")
            osm_results = query_all_bundeslaender("OpenStreetMap Overpass", query_osm_overpass, selected_class, timeout_sec, None)
            st.success(f"OSM: Insgesamt {len(osm_results)} Einträge gefunden.")
            results_dict["OSM"] = osm_results
        # Wikidata
        if "Wikidata" in data_sources:
            st.info("Starte Wikidata-Abfrage für ganz Deutschland (alle Bundesländer in Schleife)...")
            wd_results = query_all_bundeslaender("Wikidata", None, selected_class, None, wikidata_limit)
            st.success(f"Wikidata: Insgesamt {len(wd_results)} Einträge gefunden.")
            results_dict["Wikidata"] = wd_results
    else:
        # Standard: Nur einen Bereich abfragen
        if "OpenStreetMap Overpass" in data_sources:
            st.info(f"Starte OSM-Abfrage für {selected_area} ...")
            osm_results = query_osm_overpass(selected_class, selected_area, timeout_sec)
            st.success(f"OSM: {len(osm_results)} Einträge gefunden.")
            results_dict["OSM"] = osm_results
        if "Wikidata" in data_sources:
            st.info(f"Starte Wikidata-Abfrage für {selected_area} ...")
            wd_entity_qid = ENTITY_CLASSES_WIKIDATA.get(selected_class)
            wd_region_qid = BUNDESLAENDER_WIKIDATA.get(selected_area, None)
            if not wd_entity_qid:
                st.error(f"Für Wikidata ist für {selected_class} keine ID definiert.")
                results_dict["Wikidata"] = []
            elif not wd_region_qid:
                st.error(f"Für den Bereich {selected_area} ist keine Wikidata-ID definiert.")
                results_dict["Wikidata"] = []
            else:
                wd_query = create_sparql_query_wikidata(wd_entity_qid, wd_region_qid, wikidata_limit)
                st.code(wd_query, language='sparql')
                wd_data = execute_sparql_query_wikidata(wd_query)
                wd_results = []
                if wd_data:
                    for item in wd_data['results']['bindings']:
                        wd_results.append({
                            'name': item.get('itemLabel', {}).get('value', ''),
                            'beschreibung': item.get('description', {}).get('value', ''),
                            'website': item.get('website', {}).get('value', ''),
                            'telefon': item.get('phone', {}).get('value', ''),
                            'fax': item.get('fax', {}).get('value', ''),
                            'email': item.get('email', {}).get('value', ''),
                            'straße': item.get('streetAddress', {}).get('value', ''),
                            'plz': item.get('postalCode', {}).get('value', ''),
                            'ort': item.get('cityLabel', {}).get('value', ''),
                            'geodaten': item.get('coordinate', {}).get('value', '')
                        })
                st.success(f"Wikidata: {len(wd_results)} Einträge gefunden.")
                results_dict["Wikidata"] = wd_results

    ######################################
    # Anzeige der Ergebnisse
    ######################################
    st.header("Ergebnisübersicht")
    if merge_option == "Gemeinsam (Dubletten bereinigen)":
        all_entries = []
        for entries in results_dict.values():
            all_entries.extend(entries)
        combined = deduplicate_results(all_entries)
        if combined:
            df = pd.DataFrame(combined)
            result_json = json.dumps(df.to_dict(orient='records'), ensure_ascii=False, indent=2)
            st.subheader("Gemeinsam zusammengeführte Ergebnisse (Dubletten entfernt):")
            st.text_area("JSON-Ergebnis:", value=result_json, height=300)
            st.dataframe(df)
        else:
            st.info("Keine Ergebnisse gefunden.")
    else:
        for source, entries in results_dict.items():
            st.subheader(f"{source} Ergebnisse:")
            if entries:
                df = pd.DataFrame(entries).drop_duplicates(subset=["name"])
                result_json = json.dumps(df.to_dict(orient='records'), ensure_ascii=False, indent=2)
                st.text_area(f"{source} - JSON-Ergebnis:", value=result_json, height=300)
                st.dataframe(df)
            else:
                st.info(f"Für {source} wurden keine Ergebnisse gefunden.")

######################################
# Zur Kontrolle: Anzeige der OSM-Objektklassen
######################################
st.sidebar.subheader("Verfügbare OSM Objektklassen (zur Kontrolle)")
list_amenity_options()
