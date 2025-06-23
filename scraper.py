import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_sporting_life_tips():
    base_url = "https://www.sportinglife.com"
    cards_url = f"{base_url}/racing/racecards"

    response = requests.get(cards_url)
    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select("a.RaceCardLink__StyledRaceLink-sc-1e7dn4d-0")
    tip_list = []

    for card in cards:
        race_url = base_url + card["href"]
        race_resp = requests.get(race_url)
        race_soup = BeautifulSoup(race_resp.text, "html.parser")

        try:
            time = race_soup.select_one("span.RaceHeader__RaceTime-sc-1m4nlts-2").text.strip()
            course = race_soup.select_one("span.RaceHeader__RaceTitle-sc-1m4nlts-4").text.strip()
        except:
            continue

        runners = race_soup.select("div.RaceCardRunner")
        for runner in runners:
            try:
                horse = runner.select_one("span.RaceCardRunner__HorseName-sc-1e7dn4d-5").text.strip()
                form_el = runner.select_one("span.RaceCardRunner__RecentForm-sc-1e7dn4d-11")
                recent_form = form_el.text.strip() if form_el else ""

                if any(pos in recent_form[:3] for pos in ['1', '2', '3']):
                    tip_list.append(f"{time} {course} – **{horse}** (Form: {recent_form})")
            except:
                continue

        if len(tip_list) >= 5:
            break

    return tip_list[:5]
