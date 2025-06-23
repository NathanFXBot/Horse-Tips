import requests
from datetime import date

# === TELEGRAM CONFIG ===
BOT_TOKEN = "8042508263:AAG1iFBEzqOh-fKz93sVxb8J0LDaQC-5cIk"
CHAT_ID = "-1002833778838"  # HorsesSignal supergroup

# === REAL TIPS ENDPOINT ===
TIPS_URL = "https://horses.realtips.gg/api/today"

# === FETCH TIPS ===
try:
    response = requests.get(TIPS_URL)
    response.raise_for_status()
    tips = response.json().get("tips", [])
except Exception as e:
    tips = []
    print("❌ Error fetching tips:", e)

# === FORMAT TELEGRAM MESSAGE ===
today_str = date.today().strftime('%-d %b %Y')
if not tips:
    message = f"❌ No horse racing tips available for {today_str}."
else:
    message = f"🐎 *Top 5 Horse Racing Tips – {today_str}*\n\n"
    for i, tip in enumerate(tips, 1):
        message += f"*{i}. {tip['time']} – {tip['horse']} – 🟨 {tip['type']}*\n"
        message += f"   ➤ Trainer: {tip['trainer']} | Form: {tip['form']}\n\n"

# === SEND TO TELEGRAM ===
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
}
res = requests.post(telegram_url, json=payload)

if res.status_code == 200:
    print("✅ Tips sent to Telegram!")
else:
    print("❌ Telegram error:", res.text)
