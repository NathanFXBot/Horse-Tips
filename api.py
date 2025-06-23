from flask import Flask, jsonify
from scraper_real import scrape_today_race_tips
from datetime import date

app = Flask(__name__)

@app.route("/api/tips", methods=["GET"])
def get_tips():
    tips = scrape_today_race_tips()
    return jsonify({
        "date": date.today().strftime('%-d %b %Y'),
        "tips": tips
    })

@app.route("/", methods=["GET"])
def index():
    return "✅ Horse Racing Tips API is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
