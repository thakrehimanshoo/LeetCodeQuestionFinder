import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

s = Service(ChromeDriverManager().install()) #will install chromedirver
driver = webdriver.Chrome(service=s)

heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"
index = 1
QDATA_FOLDER = "Questiondata"

#will copy filtered questions
def copyfilter():
    questionslink = [] 
    with open("filtered_problems.txt", "r") as file:
        for line in file:
            questionslink.append(line)
    return questionslink


def questionname(text):
    index_file_path = os.path.join(QDATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")


def questionlink(text):
    index_file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text)


def content(file_name, text):
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)


def getContent(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        time.sleep(1)
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)
        body = driver.find_element(By.CSS_SELECTOR, body_class)
        print(heading.text)
        if (heading.text):
            questionname(heading.text)
            questionlink(url)
            content(str(index), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False


arr = copyfilter()
for link in arr:
    success = getContent(link, index)
    if (success):
        index = index+1


driver.quit()
