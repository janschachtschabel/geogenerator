import streamlit as st
import requests
import overpy
import json
import pandas as pd
from geopy.geocoders import Nominatim
from decimal import Decimal
import folium
from streamlit_folium import st_folium  # st_folium ersetzt folium_static

# Eine erweiterte Auswahl von Objektklassen.
# Für Museum, Galerie, Attraktion etc. soll später der Suchschlüssel "tourism" genutzt werden.
ENTITY_AMENITY_OPTIONS = {
    "Bar": "bar",
    "Biergarten": "biergarten",
    "Café": "cafe",
    "Fast Food": "fast_food",
    "Food Court": "food_court",
    "Eisdiele": "ice_cream",
    "Pub": "pub",
    "Restaurant": "restaurant",
    "Museum": "museum",       # Suchwert "museum" – im Code wird bei diesen Typen auf tourism umgestellt
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

# Hilfsfunktion: Liste der verfügbaren Objektklassen ausgeben
def list_amenity_options():
    st.write("Verfügbare Objektklassen (Key → Value):")
    for key, value in ENTITY_AMENITY_OPTIONS.items():
        st.write(f"{key} → {value}")

# Funktion zur Geokodierung mittels Nominatim
def get_area_geocode(area_name):
    geolocator = Nominatim(user_agent="ortsdaten_recherche")
    location = geolocator.geocode(f"{area_name}, Deutschland")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Funktion zur Ermittlung der OSM Area ID anhand eines Bundeslandnamens
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
        area_id = 3600000000 + relation_id
        return area_id
    except Exception as e:
        st.error(f"Fehler bei der Ermittlung der OSM Area ID: {e}")
        return None

# Funktion zur Abfrage von OSM Overpass
def query_osm_overpass(entity_label, area, timeout_sec):
    api = overpy.Overpass()
    # Sonderbehandlung: Für bestimmte tourism-Objekte (z.B. Museum, Galerie, Attraktion, etc.) wird 
    # der Schlüssel "tourism" verwendet, ansonsten "amenity".
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
    
    if area not in ["Deutschland", "Deutschland (Schleifen-Modus)"]:
        area_id = get_osm_area_id(area)
        if not area_id:
            st.error(f"Geografische Einschränkung für '{area}' konnte nicht gefunden werden.")
            return []
        area_filter = f"area({area_id})->.searchArea;"
    else:
        area_filter = f"area(3600000183)->.searchArea;"
    
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
    st.write("### Overpass-Abfrage (OpenStreetmap Overpass):")
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
        st.error(f"Fehler bei der Overpass-Abfrage: {e}")
        return []

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def osm_page():
    # Am Seitenanfang als Hilfestellung werden zwei Info-Links bereitgestellt.
    st.markdown(
        """
        **Weitere Informationen:**
        - [DE:Key:amenity](https://wiki.openstreetmap.org/wiki/DE:Key:amenity#Werte)
        - [Key:tourism](https://wiki.openstreetmap.org/wiki/Key:tourism)
        """
    )
    
    st.header("OpenStreetmap Overpass Abfrage")
    st.subheader("Suchparameter")
    
    # Amenity-/Objektklassen-Auswahl: Dropdown mit deutschen Labels; Standard: "Bar"
    entity_options = list(ENTITY_AMENITY_OPTIONS.keys())
    default_entity = "Bar" if "Bar" in entity_options else entity_options[0]
    default_entity_index = entity_options.index(default_entity)
    entity_label = st.selectbox("Objektklasse auswählen", entity_options, index=default_entity_index)
    
    # Geografischer Bereich: Auswahl zwischen "Deutschland", einzelnen Bundesländern und "Deutschland (Schleifen-Modus)"
    bundeslaender = [
        "Deutschland",
        "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg",
        "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
        "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
        "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen",
        "Deutschland (Schleifen-Modus)"
    ]
    default_area = "Thüringen" if "Thüringen" in bundeslaender else bundeslaender[0]
    default_area_index = bundeslaender.index(default_area)
    area = st.selectbox("Geografischer Bereich", bundeslaender, index=default_area_index)
    
    # Timeout-Eingabefeld (in Sekunden, Standard: 300)
    timeout_sec = st.number_input("Timeout (in Sekunden)", min_value=30, max_value=600, step=30, value=300)
    
    # Optionsfeld: Ergebnisvorschau anzeigen? (Standard: Ja)
    show_preview = st.checkbox("Ergebnisvorschau anzeigen", value=True)
    
    if st.button("Daten abfragen"):
        st.session_state["osm_results"] = []  # Ergebnisse initialisieren
        if area == "Deutschland (Schleifen-Modus)":
            bundeslaender_individuell = [
                "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg",
                "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
                "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen",
                "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
            ]
            st.info("Starte Schleifen-Abfrage für alle 16 Bundesländer...")
            for bl in bundeslaender_individuell:
                results = query_osm_overpass(entity_label, bl, timeout_sec)
                st.write(f"{bl}: {len(results)} Einträge")
                st.session_state["osm_results"].extend(results)
        else:
            st.info(f"Starte Abfrage für {area} ...")
            st.session_state["osm_results"] = query_osm_overpass(entity_label, area, timeout_sec)
        
        st.success(f"Abfrage abgeschlossen: {len(st.session_state['osm_results'])} Einträge gefunden.")
    
    if "osm_results" in st.session_state and st.session_state["osm_results"]:
        df = pd.DataFrame(st.session_state["osm_results"]).drop_duplicates(subset=["name"])
        if "geodaten" in df.columns:
            df["geodaten"] = df["geodaten"].apply(
                lambda x: x if isinstance(x, str) else json.dumps(x, default=decimal_to_float)
            )
        result_json = json.dumps(df.to_dict(orient='records'), ensure_ascii=False, indent=2)
        
        if show_preview:
            st.subheader("Ergebnisse (JSON)")
            st.text_area("JSON-Ergebnis", value=result_json, height=300)
            st.subheader("Ergebnisse (Tabelle)")
            st.dataframe(df)
        
        st.download_button(
            label="JSON herunterladen",
            data=result_json,
            file_name=f"{ENTITY_AMENITY_OPTIONS[entity_label]}_overpass_daten.json",
            mime="application/json"
        )
        
        if show_preview:
            try:
                if not df.empty:
                    lat_mean = df['geodaten'].apply(lambda x: json.loads(x)['lat']).mean()
                    lon_mean = df['geodaten'].apply(lambda x: json.loads(x)['lon']).mean()
                    m = folium.Map(location=[lat_mean, lon_mean], zoom_start=6)
                    for _, row in df.iterrows():
                        if row['geodaten']:
                            coords = json.loads(row['geodaten'])
                            folium.Marker([coords['lat'], coords['lon']], popup=row['name']).add_to(m)
                    st.subheader("Kartenansicht")
                    st_folium(m, width=700)
            except ImportError:
                st.warning("Für die Kartenvisualisierung bitte 'folium' und 'streamlit-folium' installieren.")
    
    st.subheader("Verfügbare Objektklassen (zur Kontrolle)")
    list_amenity_options()

def main():
    st.set_page_config(page_title="Ortsdaten-Recherche Tool", layout="wide")
    st.title("Ortsdaten-Recherche Tool")
    
    if "osm_results" not in st.session_state:
        st.session_state["osm_results"] = None
    
    st.sidebar.header("Navigation")
    osm_page()

if __name__ == "__main__":
    main()
