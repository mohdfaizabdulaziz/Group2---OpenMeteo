# ============================================================
# step5_telegram.py
# WHAT  : Send a Telegram message notification via Bot API
#
# SETUP (do this once):
#   1. Open Telegram → search @BotFather → send /newbot
#   2. Follow prompts → copy the bot TOKEN it gives you
#   3. Start a chat with your new bot (send it any message)
#   4. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#   5. Find "chat" → "id" in the response → copy that number
#   6. Add both to your .env file (see keys below)
# ============================================================

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_notification(record: dict) -> bool:
    """
    Send a Telegram message with Air Quality record details.

    Args:
        record: dict with keys { id, data, created_at }

    Returns:
        True if sent successfully, False otherwise
    """

    weather    = record["data"]
    record_id  = record["id"]
    created_at = record["created_at"]

    message = (
        f"<b>Air Quality Saved</b>\n"
        f"Record ID : <code>{record_id}</code>\n"
        f"Saved At  : {created_at}\n\n"
        f"<b>City        :</b> {weather['city']}, {weather['country']}\n"
        f"<b>Temperature :</b> {weather['temperature_c']}C (Feels like {weather['feels_like_c']}C)\n"
        f"<b>Condition   :</b> {weather['weather_desc']}\n"
        f"<b>Humidity    :</b> {weather['humidity_percent']}%\n"
        f"<b>Wind Speed  :</b> {weather['wind_speed_kmph']} km/h\n\n"
        f"Excel report saved to: output/weather_report.xlsx"
    )

    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "HTML",
    }

    try:
        print("[TELEGRAM] Sending notification...")
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[TELEGRAM] Notification sent (chat_id: {TELEGRAM_CHAT_ID})")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"[TELEGRAM] HTTP error: {e} — Response: {response.text}")
        return False
    except Exception as e:
        print(f"[TELEGRAM] Failed to send notification: {e}")
        return False


# ── Run this file directly to test ───────────────────────────
if __name__ == "__main__":
    test_record = {
        "id": 99,
        "created_at": "2025-01-15 10:30:00",
        "data": {
            "city": "KualaLumpur",
            "country": "Malaysia",
            "temperature_c": 32,
            "feels_like_c": 38,
            "humidity_percent": 80,
            "wind_speed_kmph": 15,
            "weather_desc": "Partly Cloudy",
            "visibility_km": 10,
            "scraped_at": "2025-01-15 10:30:00",
        }
    }
    send_telegram_notification(test_record)
