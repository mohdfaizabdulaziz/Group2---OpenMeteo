# ============================================================
# step3_database.py
# WHAT  : Store weather data in a local SQLite database
# HOW   : Use Python's built-in sqlite3 module
#         Data is stored as JSON string in a single column
#
# Table schema:
#   id          INTEGER  - auto increment
#   data        TEXT     - JSON string of all weather fields
#   created_at  DATETIME - auto set to current timestamp
# ============================================================

import sqlite3
import json
import os
from datetime import datetime


DB_FILE = "Air_Quality.db"


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # allows accessing columns by name
    return conn


def init_db():
    """
    Create the 'records' table if it doesn't exist yet.
    Only runs once — safe to call every time the script runs.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            data       TEXT     NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized. Table 'records' is ready.")


def save_to_db(Air_Quality: dict) -> dict:
    """
    Insert a new record into the database.
    Returns a dict with { id, data, created_at } for use in email notification.
    """

    # Convert the weather data dictionary to a JSON string
    json_data = json.dumps(Air_Quality)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO records (data) VALUES (?)",
        (json_data,)
    )

    conn.commit()

    # Get the ID and timestamp of the newly inserted row
    record_id = cursor.lastrowid
    cursor.execute("SELECT created_at FROM records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    created_at = row["created_at"]

    conn.close()

    result = {
        "id": record_id,
        "data": Air_Quality,
        "created_at": created_at,
    }
    
        # data["city"],
        # data["country"],
        # data["air_quality"].get("pm10", [None])[0],
        # data["air_quality"].get("pm2_5", [None])[0],
        # data["air_quality"].get("carbon_monoxide", [None])[0],
        # data["air_quality"].get("carbon_dioxide", [None])[0],
        # data["air_quality"].get("scraped_at", None),

    print(f"[DB] Saved! Record ID: {record_id} | Created At: {created_at}")
    return result


def get_all_records():
    """Fetch all records from the database (for viewing/debugging)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, created_at FROM records ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    from step1_scrap_meteo import fetch_geocode_and_air_quality

    init_db()
    data = fetch_geocode_and_air_quality("Kuala Lumpur")
    record = save_to_db(data)

    print("\n── Saved Record ──")
    print(f"  ID         : {record['id']}")
    print(f"  Created At : {record['created_at']}")
    print(f"  Data       : {json.dumps(record['data'], indent=4)}")

    print("\n── All Records in DB ──")
    for row in get_all_records():
        print(f"  [{row['id']}] {row['created_at']} → {row['data'][:60]}...")