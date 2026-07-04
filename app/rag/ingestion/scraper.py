import requests
import logging
from typing import List, Dict

logger = logging.getLogger("agent_logger")

class BNSSCraper:
    def __init__(self):
        # We use the HuggingFace datasets server API which exposes the structured BNS definitions.
        self.base_url = "https://datasets-server.huggingface.co/rows"
        self.dataset = "navaneeth005/BNS_definitions"
        self.config = "default"
        self.split = "train"
        
    def fetch_laws(self, offset: int = 0, length: int = 100) -> List[Dict]:
        """
        Scrapes a batch of laws from the dataset API.
        """
        logger.info(f"Scraping BNS laws offset={offset}, length={length}...")
        params = {
            "dataset": self.dataset,
            "config": self.config,
            "split": self.split,
            "offset": offset,
            "length": length
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        rows = data.get("rows", [])
        
        results = []
        for row_item in rows:
            row_data = row_item.get("row", {})
            section_num = str(row_data.get("Section", ""))
            title = row_data.get("Title", "")
            text = row_data.get("Legal Definition", "")
            
            if section_num and title and text:
                results.append({
                    "act_name": "BNS",
                    "section": section_num,
                    "title": title,
                    "text": text
                })
                
        return results

    def fetch_all_laws(self) -> List[Dict]:
        """
        Paginates and scrapes the entire BNS dataset (358 sections).
        """
        all_laws = []
        offset = 0
        batch_size = 100
        
        while True:
            batch = self.fetch_laws(offset=offset, length=batch_size)
            if not batch:
                break
                
            all_laws.extend(batch)
            offset += batch_size
            
            # Since the dataset has 358 rows, it will break when offset exceeds it
            
        logger.info(f"Successfully scraped {len(all_laws)} BNS laws in total.")
        return all_laws

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scraper = BNSSCraper()
    laws = scraper.fetch_laws(offset=0, length=5)
    for law in laws:
        print(f"Section {law['section']}: {law['title']}")
