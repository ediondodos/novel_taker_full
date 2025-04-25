# novel_tracker/anti_detect/proxies.py
import random

class ProxyRotator:
    def __init__(self, proxies=None):
        self.proxies = proxies or []
        self.current = 0
        
    def get(self):
        if not self.proxies:
            return None
        proxy = self.proxies[self.current]
        self.current = (self.current + 1) % len(self.proxies)
        return {'http': proxy, 'https': proxy}

# Example usage:
# proxy_rotator = ProxyRotator([
#     'http://proxy1:port',
#     'http://proxy2:port'
# ])