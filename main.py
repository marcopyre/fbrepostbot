username = ''
password = ''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import platform

print(platform.system())

if platform.system() == 'Windows':
    ThisOS = 'chromedriver.exe'
elif platform.system() == 'Linux':
    ThisOS = 'chromedriver'

options = webdriver.ChromeOptions()
options.headless = True
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs" , prefs)

args = ["--lang=en-US","--disable-gpu","--disable-impl-side-painting","--disable-gpu-sandbox","--disable-accelerated-2d-canvas","--disable-accelerated-jpeg-decoding","--no-sandbox","--test-type=ui","--disable-dev-shm-usage"]
for arg in args:
    options.add_argument(arg)

driver = webdriver.Chrome(ThisOS,options=options)
driver.set_window_size(1920 , 1080)
chrome_options = webdriver.ChromeOptions()

# Wait for initialize, in seconds
shortwait = WebDriverWait(driver, 600)
wait = WebDriverWait(driver, 3600)

storage = 'https://docs.google.com/document/d/1u11Bn0wAwoelv4FhzYLUWM3FaylINbD7rb8FmjZMoWE/edit'
target = 'https://www.facebook.com/lahalle.com'
CounterStorage = 'https://docs.google.com/document/d/18qhHUoP2-nPtDDjG4tPtvbC-OADwFY1mOWzT53kUtv8/edit'

def connect():
    driver.get('https://facebook.com/')
    try:
        shortwait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-cookiebanner=\'accept_button\']"))).click()
    except:
        S=''

    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name=\'email\']"))).send_keys(username)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name=\'pass\']"))).send_keys(password)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@name=\'login\']"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//body")))

def repost():
    shares = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Share\')]")))
    shares[2].click()
    reshares = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Share now (Friends)\')]")))
    reshares[0].click()

def getID(clean):
    cleaning = clean.split('2Fposts%2F')
    cleaned = cleaning[1].split('&show_text=')
    return cleaned[0]

connect()

driver.get(target)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(storage)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[2])
driver.get(CounterStorage)

while True:
    # get google doc where link is stored
    driver.switch_to.window(driver.window_handles[1])
    if wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).text.replace('\n', '').replace('”','"').replace('\u200c','')[:-1] != "off":
        a = ActionChains(driver)

        #get link
        text = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).text

        #clean link
        lastpost = text.replace('\n','').replace('”','"').replace('\u200c','')[:-1]
        #get google doc where counter is stored
        driver.switch_to.window(driver.window_handles[2])


        #get counter
        counter = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class=\'kix-paragraphrenderer\']"))).text[0]

        #navigate to target
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        #click on the first post
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label=\'Actions for this post\']")))
        driver.find_elements_by_xpath("//div[@aria-label=\'Actions for this post\']")[0].click()

        #click on the embed option
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Embed\')]"))).click()

        #get embed link
        loop = True
        while loop == True:
            print('looping')
            newlink = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label=\'Sample code input\']"))).get_attribute('value')
            if newlink != '':
                loop = False
            else:
                time.sleep(1)
        newlink = getID(newlink)
        #debug printing
        print('\n\n\n\ncounter: ' + counter)
        print('-------')
        print(lastpost)
        print(newlink)
        print('-------')

        #check if the last post is new
        if lastpost != newlink:
            print('modified')

            repost()

            a = ActionChains(driver)

            #modify link
            count = 0
            driver.switch_to.window(driver.window_handles[1])
            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).text
            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).click

            while count < text.count('\n') + 1:
                count +=1
                a.key_down(Keys.SHIFT).send_keys(Keys.END, Keys.BACKSPACE).perform()
            a.key_up(Keys.SHIFT).send_keys(newlink).perform()
            time.sleep(30)

            a = ActionChains(driver)
            #modify counter
            driver.switch_to.window(driver.window_handles[2])
            try:
                driver.switch_to_alert().accept()
            except:
                S=''

            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).text
            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'kix-paragraphrenderer\']'))).click
            a.key_down(Keys.SHIFT).send_keys(Keys.END, Keys.BACKSPACE).perform()
            a.key_up(Keys.SHIFT).send_keys(str(int(counter)+1)).perform()
            time.sleep(30)

        else:
            print('same')


        driver.switch_to.window(driver.window_handles[0])
        try:
            driver.switch_to_alert().accept()
        except:
            S=''
    else:
        print('bot is off')
    time.sleep(600)
