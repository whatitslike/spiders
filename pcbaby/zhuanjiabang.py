from selenium import webdriver


driver = webdriver.PhantomJS(
    executable_path='/usr/local/bin/phantomjs'
)
driver.get("http://kuaiwen.pcbaby.com.cn/zhuanjiabang/")

links = []

for link in driver.find_elements_by_xpath("//p[@class='aList-title']/a"):
    links.append(link.get_attribute("href"))

driver.quit()