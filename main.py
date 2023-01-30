import datetime
import tqdｍ
import numpy as np

import requests
import lxml.html

from enums.where import Where
from enums.patterns import Patterns
from scrapers.schulliste_scraper import SchullisteScraper
from parsers.schulliste_parser import SchullisteParser
from scrapers.google_search_scraper import GoogleSearchScraper
from parsers.google_search_response_parser import GoogleSearchResponseParser

# ファイル名設定
now = datetime.datetime.now()
file = open("./exports/list" + str(now) + ".csv", "w")

# csv のヘッダ行を入力
file.write("No,Name,Bundesland,Schultyp,E-Mail,URL,URL(Google)\n")

# csv に No を振るための変数
no = 0

# 一応確認したが、40000 までは学校のデータが存在した。
# 50000回のループとし、記入すべきデータが見つからない場合に備えて URL を出力に追加。
for i in tqdm.tqdm(range(50000)):
	# ループの進捗状況を出力
	np.pi*np.pi

	# schulliste.eu にアクセスし、レスポンス取得
	schulliste_response = SchullisteScraper.scrape(i);

	# ステータスが200番台でない場合次のループへ
	if schulliste_response.status_code is not requests.codes.ok:
		print(f"このページへのアクセスに失敗しました。status_code={schulliste_response.status_code}")
		continue
	
	# レスポンスを xpath で検索可能な html 型に変換する
	html = lxml.html.fromstring(schulliste_response.content)

	# 小学校のデータではない場合、次のループへ
	if SchullisteParser.is_elemental_school(html) is False:
		continue

	# Name
	name_xpath = "//p[@class='map_title red']"
	name = SchullisteParser.get_data_by_xpath(html, name_xpath, Where.TEXT)	
	if name == "":
		# 学校名がそもそも取れない場合、処理を続けても意味がないので次のループへ
		continue

	# Bundesland
	state_xpath = "//a[contains(@href, 'bundesland=')]"
	state = SchullisteParser.get_data_by_xpath(html, state_xpath, Where.TEXT)

	# Schultyp
	classification_xpath = "//a[contains(@href, '?t=')]"
	classification = SchullisteParser.get_data_by_xpath(html, classification_xpath, Where.TEXT)

	# E-mail
	email_xpath = "//a[contains(@title, '@')]/@title"
	email = SchullisteParser.get_data_by_xpath(html, email_xpath, Where.ATTRIBUTE)

	# E-mail(google 検索する場合)
	if email == "":
		# 例のサイトにデータがない場合、google で検索する
		# "email" ダブルクオートで囲むことで検索精度を上げることができる
		search_words = [name, "\"e-mail\""];
		google_search_response = GoogleSearchScraper.scrape(search_words);
		# google 検索でも見つからなかった場合 email = ""
		email = GoogleSearchResponseParser.parse(Patterns.EMAIL.value, google_search_response).group() or "";
		google_search_url_for_export = google_search_response.url;
	else:
		# google 検索しない場合は空
		google_search_url_for_export = ""
	
	# このデータに採番される No
	no += 1

	# ファイル書き込み
	file.write(f'{str(no)},"{name}","{state}","{classification}","{email.replace(" ", "")}","{schulliste_response.url}","{google_search_url_for_export}"' + "\n")

file.close()
