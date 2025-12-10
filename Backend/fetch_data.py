import requests
from Backend.database import get_connection

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def insert_earthquakes():

    params = {
        "format": "geojson",
        #"limit": 200
    }

    response = requests.get(USGS_API_URL, params=params)
    data = response.json()

    conn = get_connection()
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    for feature in data.get("features", []):
        earthquake_id = feature["properties"]["ids"]
        props = feature["properties"]
        geom = feature["geometry"]

        cursor.execute("""
            INSERT INTO locations (earthquake_id, latitude, longitude)
            VALUES (?, ?, ?)
        """, (
            earthquake_id,
            geom["coordinates"][0],
            geom["coordinates"][1],
        ))

        location_id = cursor.lastrowid 

        cursor.execute("""
            INSERT INTO properties (earthquake_id, properties)
            VALUES (?, ?)
        """, (
            earthquake_id,
            props.get("detail")
        ))

        property_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO earthquakes (earthquake_id, magnitude, time_unix, place, location_id, property_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            earthquake_id,
            props.get("mag"),
            props.get("time"),
            props.get("place"),
            location_id,
            property_id
        ))

    conn.commit()
    conn.close()
    print("Inserted earthquakes into database")