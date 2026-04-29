import sys
import argparse
import tkinter as tk
from tkinter import messagebox

from step1_scrap_meteo import fetch_geocode_and_air_quality
from step2_excel_meteo import save_to_excel
from step3_db_meteo import init_db, save_to_db
from step4_telegram_meteo import send_telegram_notification

def run_pipeline(city: str):
    print("=" * 55)
    print("  Python Automation Pipeline")
    print("=" * 55)
    # STEP 1
    print("\n[STEP 1] Fetching air quality data...")
    data = fetch_geocode_and_air_quality(city)
    print("[INFO] Data fetched for:", city)
    # STEP 2
    print("\n[STEP 2] Saving to Excel...")
    excel_path = save_to_excel(data)
    print("[INFO] Saved to Excel:", excel_path)
    # STEP 3
    print("\n[STEP 3] Storing in database...")
    init_db()
    record = save_to_db(data)
    # STEP 4
    print("\n[STEP 4] Sending Telegram notification...")
    telegram_ok = send_telegram_notification(record)
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
    print(f"  Telegram   : {'Sent' if telegram_ok else 'Failed'}")
    print("=" * 55)
    return data, record, excel_path, telegram_ok

def run_all_gui(city: str):
    try:
        data, record, excel_path, telegram_ok = run_pipeline(city)
        messagebox.showinfo(
            "Success",
            f"City: {city}\nExcel: {excel_path}\nDB ID: {record['id']}\nDB Time: {record['created_at']}\nTelegram: {'Sent' if telegram_ok else 'Failed'}"
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
    root.geometry("350x180")
    label = tk.Label(root, text="Enter city name:", font=("Arial", 12))
    label.pack(pady=10)
    entry = tk.Entry(root, width=30, font=("Arial", 12))
    entry.pack()
    entry.focus_set()
    btn = tk.Button(root, text="Fetch & Save", command=on_submit, font=("Arial", 12))
    btn.pack(pady=14)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Air Quality Automation Pipeline")
    parser.add_argument(
        "--city",
        type=str,
        help="City name to fetch data for"
    )
    args = parser.parse_args()
    if args.city:
        run_pipeline(args.city)
    else:
        start_gui()