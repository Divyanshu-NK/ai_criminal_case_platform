import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://devgan.in/bns/section/103/', headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("Title:", soup.title.string)

# Let's find tables
tables = soup.find_all('table')
if len(tables) > 1:
    table1 = tables[1]
    rows = table1.find_all('tr')
    for r in rows:
        print(r.text.strip())
        print("---")



