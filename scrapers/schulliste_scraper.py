import requests
from settings.headers import Headers 

class SchullisteScraper:
    """
    schulliste.eu にアクセスし、html を取得するクラス
    """

    @staticmethod
    def scrape(page_no):
        """引数の page_no から URL を組み立てて schuliste.eu にアクセスし、レスポンスを返す
        @param page_no アクセスする学校の ID
        @return その URL のレスポンス
        """
        # 今回アクセスする url を作る
        # page_no をゼロ埋め5桁にしたものが、その学校に割り振られた ID(と、思われる)
        url = f"http://www.schulliste.eu/schule/{str(page_no + 1).zfill(5)}-freie-montessori-schule-mkk/"
        response = requests.get(url, headers=Headers.header)
        return response;