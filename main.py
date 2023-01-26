import datetime

from selenium import webdriver

from enums.where import Where
from scrapers.site_scraper import SiteScraper

# chromedriver はバックグラウンドで起動
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver.exe', options=options)  # Optional argument, if not specified will search path.

# ファイル名設定
now = datetime.datetime.now()
file = open("./exports/list" + str(now) + ".csv", "w")

# csv のヘッダ行を入力
file.write("No,Name,Bundesland,Schultyp,E-Mail,URL,URL(Google)\n")

no = 0
site_scraper = SiteScraper()
# 一応確認したが、40000 までは学校のデータが存在した。
# 50000回のループとし、記入すべきデータが見つからない場合に備えて URL を出力に追加。
for i in range(50000):
	page_no = str(i + 1).zfill(5)
	url = "http://www.schulliste.eu/schule/" + page_no + "-freie-montessori-schule-mkk/"
	driver.get(url)

	# 小学校のデータではない場合、次のループへ
	if site_scraper.is_elemental_school(driver) is False:
		continue
	
	# No
	no += 1

	# Name
	name_xpath = "//p[@class='map_title red']"
	name = site_scraper.get_data_by_xpath(driver, name_xpath, Where.TEXT, None)	
	if name == "":
		# 学校名がそもそも取れない場合、処理を続けても意味がないので次のループへ
		continue

	# Bundesland
	state_xpath = "//a[contains(@href, 'bundesland=')]"
	state = site_scraper.get_data_by_xpath(driver, state_xpath, Where.TEXT, None)

	# Schultyp
	classification_xpath = "//a[contains(@href, '?t=')]"
	classification = site_scraper.get_data_by_xpath(driver, classification_xpath, Where.TEXT, None)

	# E-mail
	email_xpath = "//a[contains(@title, '@')]"
	email = site_scraper.get_data_by_xpath(driver, email_xpath, Where.ATTRIBUTE, "title")
	if email == "":
		# 例のサイトにデータがない場合、google で検索する
		formatted_name = name.replace(" ", "+")
		google_search_url = f'https://www.google.com/search?q={formatted_name}+%22e-mail%22'
		email = site_scraper.google_search(driver, google_search_url)
	else:
		# google 検索しない場合は空
		google_search_url = ""

	# ファイル書き込み
	file.write(f'{str(no)},"{name}","{state}","{classification}","{email}","{url}","{google_search_url}"' + "\n")

driver.quit()
file.close()
