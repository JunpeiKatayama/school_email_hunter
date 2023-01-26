import re

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from enums.where import Where

class SiteScraper:

    @staticmethod
    def is_elemental_school(driver):
        """渡されたページ情報から、そのページが小学校のものかどうかを判定する
        
        Keyword arguments:
        driver -- celenium の webdriver
        """
        try:
            elements = driver.find_elements(By.XPATH, "//a[contains(@title, 'Zu Schulen im Fachbereich übergehen')]")
            for element in elements:
                # 取得した要素に Grund が含まれる文字列があれば true
                if "Grund" in element.text:
                    return True
        except NoSuchElementException:
            # そもそもカテゴリが見つからない場合
            return False
        return False
        

    @staticmethod
    def get_data_by_xpath(driver, xpath, where, attribute_name):
        """データを xpath を用いて取得し、返却する
        
        Keyword arguments:
        driver -- celenium の webdriver
        xpath -- データがあると思われる xpath
        where -- xpath で取得したデータのどの部分が欲しいか
                ex: text -> Where.TEXT
        attribute_name -- Where.ATTRIBUTE が指定されている場合、どの attribute から取得するか
                ex: href の中身が欲しい -> href
        """
        try:
            element = driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            # データが見つからなかったら空
            return ""
        if where is Where.TEXT:
            return element.text
        if where is Where.ATTRIBUTE:
            return element.get_attribute(attribute_name)
        # where の指定が想定外の場合も空文字を返却
        return ""

    @staticmethod
    def google_search(driver, url):
        """学校名 + e-mail で google 検索し、検索結果からメールアドレスを探して返却する

        driver -- celenium の webdriver
        url -- 検索用 URL
        """
        driver.get(url)
        try:
            # 取得範囲は検索結果の全体
            element = driver.find_element(By.XPATH, "//div[@class='GyAeWb']").text
        except NoSuchElementException:
            # 検索結果が1件もない場合
            return ""
        # hogehoge@test.com. のように末尾に dot がつく場合がそこそこあるので末尾は必ず英数字とする正規表現
        pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z0-9])");
        result = re.search(pattern, element)
        if result is None:
            # 検索結果の1件目にメールアドレスの記載がない場合
            return ""
        return result.group()
