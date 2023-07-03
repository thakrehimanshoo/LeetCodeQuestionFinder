from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


s = Service(ChromeDriverManager().install()) #will install chromedirver


driver = webdriver.Chrome(service=s)

# function to get a tags
def all_a_tags():
    # find tags by a
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    for i in links:
        try:
            # will only take with problem key
            if "/problems/" in i.get_attribute("href"):
                ans.append(i.get_attribute("href"))
        except:
            pass
    
    ans = list(set(ans)) #to remove duplicate, used list
    return ans

#final list 
my_ans = []

#for all pages
driver.get("https://leetcode.com/problemset/all/?page=1") #will open chrome with this link
time.sleep(7)
for i in range(1, 55):
    my_ans += all_a_tags()
    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='next']")
    next_button.click()
    time.sleep(7)

my_ans = list(set(my_ans))

#make txt of links
with open('questionrun1.txt', 'a') as f:
    for j in my_ans:
        f.write(j + '\n')
#no of questions will print on terminal
print(len(my_ans))

driver.quit()
