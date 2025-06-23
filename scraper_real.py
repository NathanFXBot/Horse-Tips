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

        meetings = soup.select("a.race-meeting-list__link")
        meeting_links = ["https://www.sportinglife.com" + a['href'] for a in meetings[:5]]  # Top 5 meetings

        for link in meeting_links:
            race_page = requests.get(link)
            race_soup = BeautifulSoup(race_page.text, "html.parser")

            races = race_soup.select("a.rc-meeting__race")
            for race in races[:2]:  # Limit to 2 races per meeting
                race_url = "https://www.sportinglife.com" + race['href']
                race_detail = requests.get(race_url)
                detail_soup = BeautifulSoup(race_detail.text, "html.parser")

                time_tag = detail_soup.select_one("span.rc-header__time")
                course_tag = detail_soup.select_one("span.rc-header__course")
                time_str = time_tag.text.strip() if time_tag else "N/A"
                course_str = course_tag.text.strip() if course_tag else "N/A"

                runners = detail_soup.select("div.rc-runner")
                if runners:
                    runner = runners[0]  # Top 1 runner per race
                    name = runner.select_one("span.rc-runner__name").text.strip()
                    trainer_tag = runner.select_one("span.rc-runner__trainer-name")
                    form_tag = runner.select_one("span.rc-runner__form-figures")
                    trainer = trainer_tag.text.strip() if trainer_tag else "Unknown"
                    form = form_tag.text.strip() if form_tag else "-"

                    tips.append({
                        "time": f"{time_str} {course_str}",
                        "horse": name,
                        "trainer": trainer,
                        "form": form,
                        "type": "EW Value Pick"
                    })
    except Exception as e:
        print("❌ Error scraping Sporting Life:", e)

    return tips[:5]  # Top 5 overall
