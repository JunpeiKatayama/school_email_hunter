from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
# chromedriver はバックグラウンドで起動
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
file = open('list.csv', 'w')

for i in range(9999):
	page_no = str(i + 1).zfill(4)
	url = "http://www.schulliste.eu/schule/" + page_no + "-freie-montessori-schule-mkk/"
	driver.get(url)
	try:
		# 学校名は p 要素かつ class =  map_title red
		name = driver.find_element(By.XPATH, "//p[@class='map_title red']").text
	except NoSuchElementException:
		# 学校名が見つからなかったら unknown と記録
		name = "unknown"
	try:
		# メールアドレスは a 要素かつ title に @ が含まれるものの title 属性
		email = driver.find_element(By.XPATH, "//a[contains(@title, '@')]").get_attribute("title")
	except NoSuchElementException:
		# メールアドレスが見つからなかったら unknown と記録
		email = "unknown"
	file.write(name + "," + email + "\n")

driver.quit()