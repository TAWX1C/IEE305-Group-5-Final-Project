import streamlit as st
import sqlite3

DATABASE_PATH = "Database/earthquakes.db"  # Adjust path if needed

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Streamlit UI ---
st.title("Earthquake Data Explorer")

# Filter options
min_mag = st.slider("Minimum Magnitude", 0.0, 10.0, 0.0, 0.1)
max_mag = st.slider("Maximum Magnitude", 0.0, 10.0, 10.0, 0.1)

# Connect to database and fetch data
conn = get_db_connection()
cursor = conn.cursor()
query = """
    SELECT e.earthquake_id, e.magnitude, e.time_unix, e.place, 
           l.latitude, l.longitude, p.properties
    FROM earthquakes e
    LEFT JOIN locations l ON e.location_id = l.location_id
    LEFT JOIN properties p ON e.property_id = p.property_id
    WHERE e.magnitude BETWEEN ? AND ?
"""
cursor.execute(query, (min_mag, max_mag))
results = cursor.fetchall()
conn.close()

# Display data in a table
if results:
    st.subheader(f"{len(results)} earthquakes found")
    st.dataframe(results)
else:
    st.write("No earthquakes found for the selected range.")

# Optional: Map visualization
if results:
    st.subheader("Map of Earthquakes")
    map_data = [{"lat": row["longitude"], "lon": row["latitude"]} for row in results]
    st.map(map_data)