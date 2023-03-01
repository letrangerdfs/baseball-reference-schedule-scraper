import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

url = "https://www.baseball-reference.com/boxes/ANA/ANA202104010.shtml"

r = session.get(url)

r.html.render(timeout=20000)

tables = r.html.find('.sortable')

for i, table in enumerate(tables):
    table_html = table.html
    soup = BeautifulSoup(table_html, 'html.parser')
    rows = []
    for tr in soup.find_all('tr'):
        row = []
        for td in tr.find_all(['td', 'th']):
            row.append(td.text.strip())
        if row:
            rows.append(row)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df.dropna()
    df.to_csv(f'table_data_{i+1}.csv', index=False)