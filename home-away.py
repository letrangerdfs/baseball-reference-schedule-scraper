import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://www.baseball-reference.com/leagues/majors/2021-schedule.shtml"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

games = soup.select("p.game")

with open("team_names.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Date", "Away team", "Home team"])
    current_date = ""
    for game in games:
        date_element = game.find_previous("h3")
        date_string = date_element.text.strip() if date_element else current_date
        current_date = date_string
        date_object = datetime.strptime(date_string, "%A, %B %d, %Y")
        date_formatted = date_object.strftime("%Y-%m-%d")
        away_team = game.find_all("a")[0].text
        home_team = game.find_all("a")[1].text
        writer.writerow([date_formatted, away_team, home_team])
