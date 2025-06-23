import requests
from scraper_real import scrape_today_race_tips
from datetime import datetime

# Replace these with your actual bot details
TELEGRAM_BOT_TOKEN = "8042508263:AAG1iFBEzqOh-fKz93sVxb8J0LDaQC-5cIk"
TELEGRAM_CHAT_ID = "-1002833778838"

def format_tips_message(tips):
    today = datetime.utcnow().strftime("%-d %b %Y")
    message = f"🐎 Top 5 Horse Racing Tips – {today}\n\n"
    for i, tip in enumerate(tips, start=1):
        message += (
            f"{i}. {tip['race']} – {tip['horse']} – {tip['type']}\n"
            f"   ➤ Trainer: {tip['trainer']} | Form: {tip['form']}\n\n"
        )
    return message.strip()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Tips sent to Telegram!")
    else:
        print("❌ Failed to send:", response.text)

def main():
    tips = scrape_today_race_tips()
    if tips:
        message = format_tips_message(tips)
        send_telegram_message(message)
    else:
        send_telegram_message("❌ No racing tips found today.")

if __name__ == "__main__":
    main()
