from enums.where import Where

class SchullisteParser:

    @staticmethod
    def is_elemental_school(html):
        """渡されたページ情報から、そのページが小学校のものかどうかを判定する
        
        Keyword arguments:
        html -- requests で取得した html
        """
        try:
            elements = html.xpath("//a[contains(@title, 'Zu Schulen im Fachbereich übergehen')]")
            for element in elements:
                # 取得した要素に Grund が含まれる文字列があれば true
                if "Grund" in element.text:
                    return True
        except IndexError:
            # そもそもカテゴリが見つからない場合
            return False
        return False
        

    @staticmethod
    def get_data_by_xpath(html, xpath, where):
        """データを xpath を用いて取得し、返却する
        
        Keyword arguments:
        html -- requests で取得した html
        xpath -- データがあると思われる xpath
        where -- xpath で取得したデータのどの部分が欲しいか
                ex: text -> Where.TEXT
        """
        try:
            element = html.xpath(xpath)[0]
        except IndexError:
            return ""
        if where is Where.TEXT:
            return element.text
        if where is Where.ATTRIBUTE:
            # attribute から取得するとき、element は配列ではない
            return element
        # where の指定が想定外の場合も空文字を返却
        return ""
