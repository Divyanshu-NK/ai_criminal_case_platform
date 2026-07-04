import requests
from bs4 import BeautifulSoup

url = 'https://indiankanoon.org/search/?formInput=criminal+doctypes:supremecourt'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

results = soup.find_all('div', class_='headline')
print(f"Found {len(results)} results")
for res in results[:3]:
    a_tag = res.find('a')
    if a_tag:
        doc_url = "https://indiankanoon.org" + a_tag['href']
        print(a_tag.text.strip(), "->", doc_url)
        # Fetch the document
        doc_r = requests.get(doc_url, headers=headers)
        doc_soup = BeautifulSoup(doc_r.text, 'html.parser')
        doc_text = doc_soup.find('div', class_='judgments')
        if doc_text:
            print(f"  Snippet: {doc_text.text[:200].strip().replace(chr(10), ' ')}")


