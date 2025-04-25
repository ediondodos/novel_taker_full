# novel_tracker/anti_detect/user_agents.py
from fake_useragent import UserAgent

class UserAgentManager:
    def __init__(self):
        self.ua = UserAgent()
        
    def get_random(self):
        return self.ua.random