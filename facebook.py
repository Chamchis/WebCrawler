import getpass
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
#Bypass user-agent
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
#Bypass languageset
#options.add_argument("lang=ko_KR")

driver = webdriver.Chrome('./chromedriver', options=options)
driver.implicitly_wait(3)

print ("Login to Facebook")
uid = input("ID : ")
upw = getpass.getpass("PW : ")


#Bypass plugin
driver.get('https://www.facebook.com/login/device-based/regular/login/')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
#driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

#input id/pw
driver.find_element_by_name('email').send_keys(uid)
driver.find_element_by_name('pass').send_keys(upw)
fb_submit=driver.find_element_by_name('login')
fb_submit.click()

driver.implicitly_wait(10)
driver.find_element_by_xpath("//a[@title='프로필']").click()

driver.find_element_by_xpath("//a[@data-tab-key='friends']").click()

#Make screenshot
driver.implicitly_wait(100)
driver.get_screenshot_as_file('fb_main_headless.png')

driver.quit()
