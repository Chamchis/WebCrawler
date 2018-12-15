import getpass
import time
import sys
from selenium import webdriver

SCROLL_PAUSE_TIME = 1

def Load_driver():

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("disable-gpu")
	#Bypass user-agent
	options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
	#Bypass languageset
	#options.add_argument("lang=ko_KR")

	global driver 
	driver = webdriver.Chrome('./chromedriver', options=options)
	driver.implicitly_wait(3)

def Down_to_Bottom():

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	    # Wait to load page
	    time.sleep(SCROLL_PAUSE_TIME)

	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height

def Choose_What_to_Do():

	print ("")
	print ("------------ 작업 가능한 목록 -----------")
	print ("")
	print (" 1. 내 친구 목록 추출")
	print (" 2. 다른 사람 친구 목록 추출")
	print ("")
	print ("-----------------------------------------")

	choose = input(" 번호 입력 : ")

	if choose == "1" :
		print ("-----------------------------------------")
		Print_Friendlist()
		print ("-----------------------------------------")
		print ("")
	elif choose == "2" :
		print ("-----------------------------------------")
		ID_Login()
		print ("-----------------------------------------")
		print ("")
	else :
		print ("잘못된 입력")
		sys.exit()

def Account_Login():

	Load_driver()
	print ("")
	print ("Login to Facebook")
	uid = input("ID : ")
	upw = getpass.getpass("PW : ")

	print ("")
	print ("[-] 로그인 중...")

	try :
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

	except :
		print ("[*] 로그인 실패!")
		driver.quit()
		sys.exit()

	print ("[+] 로그인 성공")

	
	Choose_What_to_Do()

def ID_Login():

	print("")
	print("Input ID")
	print("예) https://facebook.com/seunghwan.yi.92 라면 seunghwan.yi.92 를 입력")
	uid = input("ID : ")

	try :
		#Bypass plugin
		driver.get('https://www.facebook.com/' + uid)
		driver.implicitly_wait(100)
		driver.get_screenshot_as_file('fb_main_headless.png')
		driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
		#driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
		Print_Friendlist()

	except :
		print ("[*] 찾을 수 없는 아이디!")
		driver.quit()
		sys.exit()

def Print_Friendlist():


	driver.find_element_by_xpath("//a[@data-tab-key='friends']").click()
	Down_to_Bottom()

	friends_elems = driver.find_elements_by_xpath("//div[@data-testid='friend_list_item']")
	friends_counts = len(friends_elems)

	print("총 친구 수 : " + str(friends_counts))
	friends_list=[]
	for i in friends_elems:
	    friends_list.append(i.text)

	for friends in friends_list:
	    print(str(friends.split()))

	#Make screenshot
	#driver.implicitly_wait(100)
	#driver.get_screenshot_as_file('fb_main_headless.png')
	driver.quit()

if __name__ == '__main__':

	print ("#########################################################################")
	print ("#########################################################################")
	print ("########################## Facebook Crawler 0.1 #########################")
	print ("														 lesh.tistory.com")
	print ("#########################################################################")
	print ("")
	print ("")
	Account_Login()
	

	

