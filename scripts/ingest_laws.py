import os
import sys
import json
import time
# pyrefly: ignore [missing-import]
from qdrant_client.http import models as rest
import uuid
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.qdrant import qdrant_manager
from app.rag.embedding.service import embedding_service

BNS_DATA_DIR = os.path.join("law_data", "bns")
SC_DATA_DIR = os.path.join("law_data", "supreme_court")

def fetch_bns_section(section_num):
    file_path = os.path.join(BNS_DATA_DIR, f"sec_{section_num}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"Scraping BNS Section {section_num}...")
    url = f"https://devgan.in/bns/section/{section_num}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            tables = soup.find_all('table')
            if len(tables) > 1:
                rows = tables[1].find_all('tr')
                if len(rows) >= 4:
                    title_raw = rows[1].text.strip()
                    text_raw = rows[3].text.strip()
                    
                    # Clean title: "S. 103 Punishment for murder." -> "Punishment for murder."
                    title = title_raw.split(" ", 2)[-1] if len(title_raw.split(" ")) >= 3 else title_raw
                    
                    data = {
                        "act_name": "BNS",
                        "section": str(section_num),
                        "title": title,
                        "text": text_raw,
                        "ingredients": [] 
                    }
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    time.sleep(0.5) # Polite delay
                    return data
    except Exception as e:
        print(f"Failed to fetch section {section_num}: {e}")
    return None

def fetch_supreme_court_cases():
    print("Scraping IndianKanoon for recent Supreme Court cases...")
    # Using a generic search to get latest supreme court criminal cases.
    url = 'https://indiankanoon.org/search/?formInput=criminal+doctypes:supremecourt'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('div', class_='headline')
        
        scraped_cases = []
        for i, res in enumerate(results[:10]): # Fetch top 10 recent cases
            a_tag = res.find('a')
            if not a_tag:
                continue
                
            case_id = a_tag['href'].split('/')[-2]
            file_path = os.path.join(SC_DATA_DIR, f"case_{case_id}.json")
            
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    scraped_cases.append(json.load(f))
                continue
                
            doc_url = "https://indiankanoon.org" + a_tag['href']
            print(f"Scraping Case: {a_tag.text.strip()}...")
            doc_r = requests.get(doc_url, headers=headers, timeout=10)
            doc_soup = BeautifulSoup(doc_r.text, 'html.parser')
            doc_text_div = doc_soup.find('div', class_='judgments')
            
            if doc_text_div:
                text_content = doc_text_div.text.strip()
            else:
                text_content = doc_soup.text.strip()[:1000] # Fallback
                
            data = {
                "court": "Supreme Court",
                "case_id": case_id,
                "title": a_tag.text.strip(),
                "text": text_content,
                "url": doc_url
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            scraped_cases.append(data)
            time.sleep(1) # Polite delay
        return scraped_cases
    except Exception as e:
        print(f"Failed to fetch supreme court cases: {e}")
        return []

def ingest_collection(collection_name, data, is_bns=True):
    print(f"Embedding and Upserting into Qdrant '{collection_name}'...")
    qdrant_manager.create_collection(collection_name)
    client = qdrant_manager.get_client()
    
    points = []
    for item in data:
        if is_bns:
            document = f"Act: {item['act_name']}, Section: {item['section']}. Title: {item['title']}. Text: {item['text']}"
        else:
            document = f"Court: {item['court']}, Case: {item['title']}. Text: {item['text'][:1500]}" # Truncate long cases for embedding
            
        vector = embedding_service.embed_text(document)
        point_id = str(uuid.uuid4())
        
        points.append(
            rest.PointStruct(
                id=point_id,
                vector=vector,
                payload=item
            )
        )
        
        if len(points) >= 20:
            client.upsert(collection_name=collection_name, points=points)
            points = []
            
    if points:
        client.upsert(collection_name=collection_name, points=points)
    print(f"Ingestion complete for '{collection_name}'.")

def run():
    os.makedirs(BNS_DATA_DIR, exist_ok=True)
    os.makedirs(SC_DATA_DIR, exist_ok=True)

    print("--- Stage 1: Data Scraping (Local Persistence) ---")
    bns_data = []
    
    from concurrent.futures import ThreadPoolExecutor
    # Scrape 1 to 358 concurrently with a limit of 5 workers to avoid IP bans
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_bns_section, range(1, 359))
        for res in results:
            if res:
                bns_data.append(res)
            
    sc_data = fetch_supreme_court_cases()

    print("\n--- Stage 2: Qdrant Vector Ingestion ---")
    if bns_data:
        ingest_collection("bns_laws", bns_data, is_bns=True)
    if sc_data:
        ingest_collection("supreme_court_cases", sc_data, is_bns=False)
        
    print("All data fully ingested and ready for Retrieval!")

if __name__ == "__main__":
    run()
