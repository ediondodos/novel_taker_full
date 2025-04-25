# novel_tracker/scrapers/base_scraper.py
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'lxml')
        
    @abstractmethod
    def get_title(self):
        pass
    
    @abstractmethod
    def get_chapters(self):
        pass
    
    @abstractmethod
    def get_status(self):
        pass
