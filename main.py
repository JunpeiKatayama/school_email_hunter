import datetime
import re

import requests
import lxml.html

from enums.where import Where
from scrapers.site_scraper import SiteScraper

# ファイル名設定
now = datetime.datetime.now()
file = open("./exports/list" + str(now) + ".csv", "w")

# csv のヘッダ行を入力
file.write("No,Name,Bundesland,Schultyp,E-Mail,URL,URL(Google)\n")

# csv に No を振るための変数
no = 0
site_scraper = SiteScraper()
# 一応確認したが、40000 までは学校のデータが存在した。
# 50000回のループとし、記入すべきデータが見つからない場合に備えて URL を出力に追加。
for i in range(50000):
	page_no = str(i + 1).zfill(5)
	url = "http://www.schulliste.eu/schule/" + page_no + "-freie-montessori-schule-mkk/"
	
	# url にリクエストしてレスポンスを取得
	response = requests.get(url)
	
	# ステータスが200番台でない場合次のループへ
	if response.status_code is not requests.codes.ok:
		print(f"このページへのアクセスに失敗しました。status_code={response.status_code}")
		continue

	# レスポンスを xpath で検索可能な html 型に変換する
	html = lxml.html.fromstring(response.content)

	# 小学校のデータではない場合、次のループへ
	if site_scraper.is_elemental_school(html) is False:
		continue

	# Name
	name_xpath = "//p[@class='map_title red']"
	name = site_scraper.get_data_by_xpath(html, name_xpath, Where.TEXT)	
	if name == "":
		# 学校名がそもそも取れない場合、処理を続けても意味がないので次のループへ
		continue

	# Bundesland
	state_xpath = "//a[contains(@href, 'bundesland=')]"
	state = site_scraper.get_data_by_xpath(html, state_xpath, Where.TEXT)

	# Schultyp
	classification_xpath = "//a[contains(@href, '?t=')]"
	classification = site_scraper.get_data_by_xpath(html, classification_xpath, Where.TEXT)

	# E-mail
	email_xpath = "//a[contains(@title, '@')]/@title"
	email = site_scraper.get_data_by_xpath(html, email_xpath, Where.ATTRIBUTE)
	if email == "":
		# 例のサイトにデータがない場合、google で検索する
		formatted_name = name.replace(" ", "+")
		google_search_url = f'https://www.google.com/search?q={formatted_name}+%22e-mail%22'
		google_search_response = requests.get(url)
		# メールアドレスにマッチする正規表現
		pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z0-9])");
		# メールアドレスは、google 検索結果全体から探す
		result = re.search(pattern, google_search_response.content.decode())
		if result is None:
			# 検索結果にメールアドレスの記載がない場合
			email = ""
		email = result.group()
	else:
		# google 検索しない場合は空
		# このカラムにデータがある場合、メールアドレスが正確か疑った方が良い
		google_search_url = ""
	
	# このデータに採番される No
	no += 1

	# ファイル書き込み
	file.write(f'{str(no)},"{name}","{state}","{classification}","{email}","{url}","{google_search_url}"' + "\n")

file.close()
