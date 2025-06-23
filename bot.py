import requests
from scraper import fetch_sporting_life_tips

TELEGRAM_BOT_TOKEN = "8162763392:AAFF97mkCT08u9-jJ0Uu5HBS4f7N-Stc_UE"
CHAT_ID = "-1002833778838"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def main():
    tips = fetch_sporting_life_tips()
    if not tips:
        send_to_telegram("⚠️ No good tips found today.")
        return

    message = "🐎 *Top 5 UK Racing Tips Today*

"
    message += "

".join(tips)
    message += "

🏁 Filtered by form (1/2/3 placings). Auto-posted daily."

    with open("Tips.txt", "w") as f:
        f.write(message)

    send_to_telegram(message)

if __name__ == "__main__":
    main()
