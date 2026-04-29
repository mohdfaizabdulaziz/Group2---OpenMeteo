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

    Air_Quality   = record["data"]
    record_id  = record["id"]
    created_at = record["created_at"]

    message = (
        f"<b>Air Quality Saved</b>\n"
        f"Record ID : <code>{record_id}</code>\n"
        f"Saved At  : {created_at}\n\n"
        f"<b>City        :</b> {Air_Quality['city']}, {Air_Quality['country']}\n"
        f"<b>PM10        :</b> {Air_Quality['air_quality'].get('pm10', [None])[0]}\n"
        f"<b>PM2.5       :</b> {Air_Quality['air_quality'].get('pm2_5', [None])[0]}\n"
        f"<b>CO          :</b> {Air_Quality['air_quality'].get('carbon_monoxide', [None])[0]}\n"
        f"<b>CO2         :</b> {Air_Quality['air_quality'].get('carbon_dioxide', [None])[0]}\n\n"
        f"Excel report saved to: output/Air_Quality.xlsx"
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
            "air_quality": {
                "pm10": [45.0],
                "pm2_5": [25.0],
                "carbon_monoxide": [0.5],
                "carbon_dioxide": [400.0],
                "scraped_at": "2025-01-15 10:30:00",
            }
        }
    }
    send_telegram_notification(test_record)
