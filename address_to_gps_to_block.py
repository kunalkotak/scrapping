import os
os.getcwd()
os.chdir('C:\python wd\web scrapping\Vadodara Address')
#
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
import time 

# =============================================================================
from selenium import webdriver
chrome_path = r'C:\python wd\MRA\cromedriver\version 2.39\chromedriver.exe'
option = webdriver.ChromeOptions()
option.add_argument("--incognito")


def search_address_list(search_list):
    url='https://www.google.com/maps'
    t=[]
    for i in search_list:    
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
        driver.get(url)
        search_word=driver.find_element_by_id('searchboxinput')
        search_word.send_keys(i)
    #time.sleep(5)
        driver.find_element_by_class_name('searchbox-searchbutton').click()
        try:
            driver.find_element_by_class_name('section-result-content').click()
            time.sleep(5)
            t.append(driver.current_url)
            driver.close()
        except:
            time.sleep(5)
            t.append(driver.current_url)
            driver.close()
    #search_word.submit()
    #links=driver.find_elements_by_xpath("//div[@class='zkIadb']//div//a")
    #for link in links:
    #    href=link.get_attribute('href')
        #print(href)
    return t

# =============================================================================
# Input File--> input file should contain 'Address', 'Store name' and 'City' columns
# Only this 3 columns are important
#=============================================================================
address_input=pd.read_excel('Vadodara_address.xlsx')    #write the full location of input file

# =============================================================================
#Get the gps links for all addresses
# 
# =============================================================================
#new_try_mum=search_address_list(address_input['Address'])
#new_input1=new_input[:100]
#input_2=new_input[100:200]


# Edit Address=============================================================================
#to clean the address data
# so that google result is accurate

def edit_address(a):
    new_add=[]
    for i in a:
        if 'Address:-' in i:
            new_add.append(i.split(':-')[1])
        else:
            new_add.append(i)
    return new_add
# =============================================================================

#

# Edit Address- Part 2
#Remove the phone numbers as google is not showing goodresults if phone numbers are included
#=============================================================================
#delete=['PH','MB','Phone No.']
def edit_address_2(a):
    new_add2=[]
    for i in a:
        if 'PH' in i:
            new_add2.append(i.split('PH')[0])
        elif 'MB' in i:
            new_add2.append(i.split('MB')[0])
        elif 'Phone' in i:
            new_add2.append(i.split('Phone')[0])        
        else:
            new_add2.append(i)
    return new_add2




# Create New Column for final input=============================================================================
address_input['Address input']=address_input['Store name']+' '+edit_address_2(edit_address(address_input['Address']))



# Applying Function=============================================================================
address_links=search_address_list(address_input['Address input'])   #address gps links extracted from the address
# =============================================================================
# =============================================================================
#
# =============================================================================
def gps_lat_lgt_try(a):
    temp=[]
    for i in a:
        try:
            temp.append('{1},{0}'.format(i.split('d')[-1],i.split('!')[-2].split('d')[-1]))
        except:
            temp.append('nan')
    return temp


# =============================================================================
#Getting Lat Lng 
# =============================================================================
lat_lng_address=gps_lat_lgt_try(address_links)
lat_lng2=[]
for i in lat_lng_address:
    if i=='nan':
        lat_lng2.append(np.nan)       
    else:
        if '!' not in i:
            lat_lng2.append(i)
        else:
            lat_lng2.append(np.nan)
        
        
address_input['lat_lng']=lat_lng2
address_input['lat_lng'].isna().sum()
type(address_input['lat_lng'])

# =============================================================================
# 
# =============================================================================

block=[]


address_input2=address_input.dropna()
lat_all=[float(i.split(',')[0]) for i in address_input2['lat_lng']]
lng_all=[float(i.split(',')[1]) for i in address_input2['lat_lng']]
coords_all=np.array([[i,j] for i,j in zip(lat_all,lng_all)])


import zipfile
import os
os.getcwd()

zip_files_list=[f for f in os.listdir(r'C:\python wd\web scrapping\all_kmls') if f.endswith('.zip')] 

import shutil


os.chdir(r'C:\python wd\web scrapping\all_kmls')      #Set the working directory 
for a,b in zip(coords_all,address_input2['City']):
    found=False
    for i in zip_files_list:
        if i.split('_')[1].split(' ')[0].upper().lower() in b.upper().lower():
            #os.rmdir('C:/Users/koku8001/Desktop/renaming/unzipped')
            os.makedirs('C:/Users/koku8001/Desktop/renaming/unzipped')
            zip_ref = zipfile.ZipFile(i, 'r')
            zip_ref.extractall(r'C:/Users/koku8001/Desktop/renaming/unzipped')
            p=os.listdir(r'C:/Users/koku8001/Desktop/renaming/unzipped')
            q=[w for w in os.listdir(os.path.join(r'C:/Users/koku8001/Desktop/renaming/unzipped',p[0])) if w.split('_')[1]=='Block']            
            files=[f for f in os.listdir(os.path.join(r'C:/Users/koku8001/Desktop/renaming/unzipped',p[0],q[0])) if f.endswith('.kml')]
            for j in files:
                s = BeautifulSoup(open(os.path.join(r'C:/Users/koku8001/Desktop/renaming/unzipped',p[0],q[0], j),'r'), 'xml')
                
                try:
                    for coords in s.find_all('coordinates'):
                        space_splits = coords.text.split("\n")
                    lat=[]
                    lng=[]
                    tab_split=[]
                    del space_splits[0]
                    del space_splits[-1]
                    for t in space_splits:
                        tab_split.append(t.split('\t')[5])
                    for split in tab_split:
                        comma_split = split.split(',')
                        lat.append(comma_split[1])    # lat
                        lng.append(comma_split[0])    # lng
                except:
                    for coords in s.find_all('coordinates'):
                        space_splits = coords.text.split(' ')
                    lat=[]
                    lng=[]
                    #tab_split=[]
                    space_splits[0]=space_splits[0].split('\t')[-1]
                    del space_splits[-1]
                    #for t in space_splits:
                    #    tab_split.append(t.split('\t')[5])
                    for split in space_splits:
                        comma_split = split.split(',')
                        lat.append(comma_split[1])    # lat
                        lng.append(comma_split[0])    # lng


                lat=[float(i) for i in lat]
                lng=[float(i) for i in lng]
                #print(lat)
                coords=[[i,j] for i,j in zip(lat,lng)]
                coords2=np.array(coords)
                poly=Polygon(coords2,closed=True)
                if poly.get_path().contains_point(a):
                    found=True
                    block.append(j)
            if found==False:
                block.append(np.nan)
            shutil.rmtree(r'C:/Users/koku8001/Desktop/renaming/unzipped')
            zip_ref.close()    

#del address_input2['Block']    
address_input2['Block']=block    

address_input2.to_csv('C:\python wd\web scrapping\Vadodara Address/Vadodara Address_to_block.csv')
