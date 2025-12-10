import sqlite3
from fastapi import FastAPI
from Backend.database import get_connection
from Backend.fetch_data import insert_earthquakes
from fastapi.responses import JSONResponse

app = FastAPI()

DATABASE_PATH = "Database/earthquakes.db"


@app.get("/")
def read_root():
    return {"message": "Earthquake API is running"}

@app.post("/fetch")
def fetch_data():
    try:
        insert_earthquakes()
        return {"status": "success", "message": "Earthquake data fetched and inserted"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/earthquakes")
def list_earthquakes(min_mag : float = None, max_mag : float = None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM earthquakes "
    conditions = []
    params = []

    if min_mag is not None:
        conditions.append("magnitude >= ?")
        params.append(min_mag)

    if max_mag is not None:
        conditions.append("magnitude <= ?")
        params.append(max_mag)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return {"earthquakes": results}

@app.get("/reset-db")
def reset_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS earthquakes")
    cursor.execute("DROP TABLE IF EXISTS locations")
    cursor.execute("DROP TABLE IF EXISTS properties")

    # Recreate tables
    cursor.execute("""
    CREATE TABLE earthquakes (
	    earthquake_id TEXT,
	    magnitude REAL,
	    time_unix TEXT,
	    place TEXT,
	    location_id INTEGER NOT NULL,
        property_id INTEGER NOT NULL,
	    PRIMARY KEY(earthquake_id),
	    FOREIGN KEY(location_id) REFERENCES locations(location_id)
        FOREIGN KEY(property_id) REFERENCES properties(property_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        earthquake_id TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE properties (
        property_id INTEGER PRIMARY KEY AUTOINCREMENT,
        earthquake_id TEXT NOT NULL,
        properties TEXT
    )
    """)

    conn.commit()
    conn.close()

    return {"message": "Database has been reset and tables recreated"}