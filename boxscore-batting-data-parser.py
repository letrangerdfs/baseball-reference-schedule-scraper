from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
import teams


# Set the path to the chromedriver.exe file
chromedriver_path = r'C:\Users\muhrs\Desktop\chromedriver.exe'

# Set up the webdriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Wait for the page to fully load
driver.implicitly_wait(10)

# Construct the URL for the game
url = 'https://www.baseball-reference.com/boxes/ANA/ANA202104010.shtml'

# Navigate to the webpage
driver.get(url)

# Loop through all the possible combinations of MLB teams
for team_combination in teams.mlb_batting_team_combinations:

    # Get the HTML code for the batting table
    try:
        batting_table = driver.find_element(By.XPATH, f'//table[@id="{team_combination}"]')
        batting_html_code = batting_table.get_attribute('outerHTML')
        batting_soup = BeautifulSoup(batting_html_code, 'lxml')

        # Extract the batting data
        batting_rows = batting_soup.find_all('tr')
        player_stats = []
        for row in batting_rows[1:]:
            cells = row.find_all(['th', 'td'])
            player_name = cells[0].text
            AB = cells[1].text
            R = cells[2].text
            H = cells[3].text
            RBI = cells[4].text
            BB = cells[5].text
            SO = cells[6].text
            PA = cells[7].text
            BA = cells[8].text
            OBP = cells[9].text
            SLG = cells[10].text
            OPS = cells[11].text
            Pit = cells[12].text
            Str = cells[13].text
            WPA = cells[14].text
            aLI = cells[15].text
            WPA_plus = cells[16].text
            WPA_minus = cells[17].text
            cWPA = cells[18].text
            acLI = cells[19].text
            RE24 = cells[20].text
            PO = cells[21].text
            A = cells[22].text
            player_stats.append(
                [player_name, AB, R, H, RBI, BB, SO, PA, BA, OBP, SLG, OPS, Pit, Str, WPA, aLI, WPA_plus, WPA_minus,
                 cWPA, acLI, RE24, PO, A])

        # Write the batting data to a CSV file
        with open(f'{team_combination}_batting_stats.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['Player Name', 'AB', 'R', 'H', 'RBI', 'BB', 'SO', 'PA', 'BA', 'OBP', 'SLG', 'OPS', 'Pit', 'Str', 'WPA',
                 'aLI', 'WPA+', 'WPA-', 'cWPA', 'acLI', 'RE24', 'PO', 'A'])
            writer.writerows(player_stats)
    except:
        print(f'No batting data found for {team_combination}')

# Close the webdriver
driver.quit()
