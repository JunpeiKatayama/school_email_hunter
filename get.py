import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
# chromedriver はバックグラウンドで起動
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
# ファイル名設定
now = datetime.datetime.now()
file = open("list" + str(now) + ".csv", "w")
# csv のヘッダ行を入力
file.write("No,Name,Bundesland,Schultyp,E-Mail,URL\n")

# 一応確認したが、40000 までは学校のデータが存在した。
# 50000回のループとし、記入すべきデータが見つからない場合に備えて URL を出力に追加。
for i in range(50000):
	page_no = str(i + 1).zfill(5)
	url = "http://www.schulliste.eu/schule/" + page_no + "-freie-montessori-schule-mkk/"
	driver.get(url)

	# No
	no = i + 1
	
	# Name
	try:
		# 学校名は p 要素かつ class =  map_title red
		name = driver.find_element(By.XPATH, "//p[@class='map_title red']").text
	except NoSuchElementException:
		# 学校名が見つからなかったら空
		name = ""
	
	# Bundesland
	try:
		# 州名の xpath は a 要素かつ href に bundesland= を含む
		state = driver.find_element(By.XPATH, "//a[contains(@href, 'bundesland=')]").text
	except NoSuchElementException:
		# 州名が見つからなかったら空
		state = ""
	
	# Schultyp
	try:
		# 区分の xpath は a 要素かつ href に ?t= を含む
		classification = driver.find_element(By.XPATH, "//a[contains(@href, '?t=')]").text
	except NoSuchElementException:
		# 区分が見つからなかったら空
		classification = ""
	
	# E-mail
	try:
		# メールアドレスは a 要素かつ title に @ が含まれるものの title 属性
		email = driver.find_element(By.XPATH, "//a[contains(@title, '@')]").get_attribute("title")
	except NoSuchElementException:
		# メールアドレスが見つからなかったら空
		email = ""
	
	file.write(f'{str(no)},"{name}","{state}","{classification}","{email}","{url}"' + "\n")
	print(str(no))

driver.quit()
file.close()