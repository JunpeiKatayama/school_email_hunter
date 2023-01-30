import re

class GoogleSearchResponseParser:
    
    @staticmethod
    def parse(pattern, response):
        return re.search(pattern, response.content.decode());
