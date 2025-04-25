# novel_tracker/scrapers/royalroad.py
from .base_scraper import BaseScraper

class RoyalRoadScraper(BaseScraper):
    def get_title(self):
        title_tag = self.soup.find('h1', {'property': 'name'})
        return title_tag.text.strip() if title_tag else None
    
    def get_chapters(self):
        stats = self.soup.find('span', {'title': 'Chapters'})
        if stats:
            return int(stats.find_next_sibling('span').text.strip())
        return 0
    
    def get_status(self):
        status_tag = self.soup.find('span', {'title': 'Publication Status'})
        return status_tag.find_next_sibling('span').text.strip() if status_tag else 'Unknown'