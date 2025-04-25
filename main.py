from search.google_cse import google_search
from scrapers import WuxiaWorldScraper, RoyalRoadScraper
from anti_detect.user_agents import UserAgentManager
from anti_detect.proxies import ProxyRotator
import requests
import random
import time

# Configuration
API_KEY = 'your_google_api_key'
CSE_ID = 'your_cse_id'
PROXIES = []  # Add your proxies here

def scrape_novel(novel_name):
    # Search for novel
    print(f"Searching for: {novel_name}")
    results = google_search(novel_name, API_KEY, CSE_ID)
    
    # Setup anti-detection
    ua_manager = UserAgentManager()
    proxy_rotator = ProxyRotator(PROXIES)
    
    for url in results:
        try:
            headers = {'User-Agent': ua_manager.get_random()}
            proxy = proxy_rotator.get()
            
            print(f"Scraping: {url}")
            response = requests.get(url, headers=headers, proxies=proxy)
            
            # Select appropriate scraper
            if 'wuxiaworld' in url:
                scraper = WuxiaWorldScraper(response.text)
            elif 'royalroad' in url:
                scraper = RoyalRoadScraper(response.text)
            else:
                continue
                
            # Extract and normalize data
            data = {
                'title': scraper.get_title(),
                'chapters': normalize_chapters(scraper.get_chapters()),
                'status': normalize_status(scraper.get_status())
            }
            
            print(f"Results: {data}")
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")

if __name__ == "__main__":
    scrape_novel("Shadow Slave")