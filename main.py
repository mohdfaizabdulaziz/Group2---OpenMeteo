import sys
import argparse
import tkinter as tk
from tkinter import messagebox

from step1_scrap_meteo import fetch_geocode_and_air_quality
from step2_excel_meteo import save_to_excel
from step3_db_meteo import init_db, save_to_db
# Optionally import further steps, e.g. Telegram, Email

def run_pipeline(city: str):
    """Run the pipeline: fetch data, save to Excel & DB, print status."""
    print("=" * 55)
    print("  Python Automation Pipeline")
    print("=" * 55)
    # ── STEP 1: Scrape ──
    print("\n[STEP 1] Fetching air quality data...")
    data = fetch_geocode_and_air_quality(city)
    print("[INFO] Data fetched for:", city)
    # ── STEP 2: Excel ──
    print("\n[STEP 2] Saving to Excel...")
    excel_path = save_to_excel(data)
    print("[INFO] Saved to Excel:", excel_path)
    # ── STEP 3: Database ──
    print("\n[STEP 3] Storing in database...")
    init_db()
    record = save_to_db(data)
    # Add further steps here if needed
    print("\n" + "=" * 55)
    print("  Pipeline Complete!")
    print("=" * 55)
    print(f"  City       : {data['city']}, {data['country']}")
    aq = data['air_quality']
    print(f"  PM10       : {aq.get('pm10', [None])[0]}")
    print(f"  PM2.5      : {aq.get('pm2_5', [None])[0]}")
    print(f"  CO         : {aq.get('carbon_monoxide', [None])[0]}")
    print(f"  CO2        : {aq.get('carbon_dioxide', [None])[0]}")
    print(f"  Record ID  : {record['id']}")
    print(f"  Saved At   : {record['created_at']}")
    print(f"  Excel File : {excel_path}")
    print("=" * 55)
    # Return record for further notification, if needed
    return data, record, excel_path

def run_all_gui(city: str):
    try:
        data, record, excel_path = run_pipeline(city)
        messagebox.showinfo(
            "Success",
            f"City: {city}\nExcel: {excel_path}\nDB ID: {record['id']}\nDB Time: {record['created_at']}"
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_submit():
    city = entry.get().strip()
    if not city:
        messagebox.showwarning("Input required", "Please enter a city name.")
        return
    run_all_gui(city)

def start_gui():
    global entry
    root = tk.Tk()
    root.title("Air Quality Downloader")
    root.geometry("350x160")
    label = tk.Label(root, text="Enter city name:", font=("Arial", 12))
    label.pack(pady=10)
    entry = tk.Entry(root, width=30, font=("Arial", 12))
    entry.pack()
    entry.focus_set()
    btn = tk.Button(root, text="Fetch & Save", command=on_submit, font=("Arial", 12))
    btn.pack(pady=14)
    root.mainloop()

# ── Entry Point ──────────────────────────────────────────────
if __name__ == "__main__":
    # If run with arguments, use CLI mode; else launch GUI
    parser = argparse.ArgumentParser(description="Air Quality Automation Pipeline")
    parser.add_argument(
        "--city",
        type=str,
        help="City name to fetch data for"
    )
    args = parser.parse_args()
    if args.city:
        # Command-line mode
        run_pipeline(args.city)
    else:
        # No --city argument, launch GUI
        start_gui()