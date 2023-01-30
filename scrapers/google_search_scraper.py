import requests
from settings.headers import Headers 

class GoogleSearchScraper:
    """
    Google 検索し、html を取得するクラス
    """
    
    @staticmethod
    def scrape(search_words):
        """引数の検索ワードで google 検索し、レスポンスを返す
        @param search_words 検索ワードの配列
        @return 検索結果のレスポンス
        """
        google_search_url = "https://www.google.com/search";
        query_string = " ".join(search_words);
        # ex: search_words = ["Ameisenbergschule Grund- und Hauptschule", "\"e-mail\""]
        #       -> request to https://www.google.com/search?q=Ameisenbergschule+Grund-+und+HauptschuleA+%22e-mail%22
        return requests.get(google_search_url, headers=Headers.header, params={'q': f'{query_string}'});
