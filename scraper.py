import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_today_race_tips():
    base_url = "https://www.sportinglife.com/racing/racecards"
    tips = []

    try:
        res = requests.get(base_url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        races = soup.select("a.race-meeting-list__link")
        race_links = ["https://www.sportinglife.com" + a['href'] for a in races[:6]]  # Top 6 meetings max

        for link in race_links:
            race_page = requests.get(link)
            race_soup = BeautifulSoup(race_page.text, "html.parser")

            races_today = race_soup.select("div.rc-meeting-races a")

            for race in races_today[:2]:  # Max 2 races per meeting
                full_url = "https://www.sportinglife.com" + race['href']
                race_detail = requests.get(full_url)
                race_soup = BeautifulSoup(race_detail.text, "html.parser")

                time_tag = race_soup.select_one("span.rc-header__time")
                time_str = time_tag.text.strip() if time_tag else "N/A"
                course_tag = race_soup.select_one("span.rc-header__course")
                course = course_tag.text.strip() if course_tag else "N/A"

                horses = race_soup.select("div.rc-runner")
                for h in horses[:1]:  # Only top 1 runner per race
                    name = h.select_one("span.rc-runner__name").text.strip()
                    trainer = h.select_one("span.rc-runner__trainer-name")
                    form = h.select_one("span.rc-runner__form-figures")
                    tips.append({
                        "time": f"{time_str} {course}",
                        "horse": name,
                        "trainer": trainer.text.strip() if trainer else "Unknown",
                        "form": form.text.strip() if form else "-",
                        "type": "EW Value Pick"
                    })

    except Exception as e:
        print("Error scraping:", e)

    return tips[:5]  # Top 5 only
