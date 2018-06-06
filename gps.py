#Scraped the gps addresses of any search which is given as input

#libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

#chrome path
chrome_path = r'C:\python wd\MRA\cromedriver\version 2.39\chromedriver.exe'

#openning in incognito mode
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

#this function returns the first link--which is link for more locations
def search_results_google(search):
    url='https://google.com/'
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
    driver.get(url)
    search_word=driver.find_element_by_id('lst-ib')
    search_word.send_keys(search)
    search_word.submit()
    links=driver.find_elements_by_xpath("//div[@class='zkIadb']//div//a")
    #print(links)
    #results=[]
    for link in links:
        href=link.get_attribute('href')
        print(href)
        #results.append(href)
        link=href
    #driver.close()
    return link

#this function uses the link by above function and returns list of gps links
def more_locations(result):
    url=result
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
    driver.get(url)
    links=driver.find_elements_by_xpath("//a[@class='yYlJEf VByer']")
    #print(links)
    gps=[]
    for link in links:
        href=link.get_attribute('href')
        print(href)
        gps.append(href)
        link=href
    #driver.close()
    return gps

#calling both the functions and storing the final list in gps_links
gps_links=more_locations(search_results_google('Dmart Stores in vadodara'))




