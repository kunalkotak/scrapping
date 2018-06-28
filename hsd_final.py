import os
os.getcwd()
os.chdir('C:\python wd\web scrapping')
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
from matplotlib.patches import Polygon
import time 
chrome_path = r'C:\python wd\MRA\cromedriver\version 2.39\chromedriver.exe'
#phantomJS=r'C:\python wd\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe'

#driver = webdriver.PhantomJS()
option = webdriver.ChromeOptions()
option.add_argument("--incognito")

# =============================================================================
#import pandas as pd
#import os
os.getcwd()
os.chdir(r'C:\python wd\web scrapping\final run')

store=pd.read_csv('store_names.csv')
cities=pd.read_csv('city_names75.csv')
store_city=pd.DataFrame([])
for i in store['Store Name']:
    for j in cities['TOWNNAME']:
        store_city = store_city.append(pd.DataFrame({'Store':i,'City':j}, index=[0]), ignore_index=True)

store_city.to_csv('Store_city.csv')

input_final=store_city[:3000]
input_final2=store_city[3000:6000]
input_final3=store_city[6000:]




# =============================================================================
def search_results_google(search):
    url='https://www.google.com/'
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
    driver.get(url)
    search_word=driver.find_element_by_id('lst-ib')
    search_word.send_keys(search)
    search_word.submit()
    try:
        links=driver.find_elements_by_xpath("//div[@class='zkIadb']//div//a")
        for link in links:
            href=link.get_attribute('href')
        return href        
        #print(href)
    except:
        return None
    driver.close()
     



def more_locations(result):
    url=result
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
    driver.get(url)
    links=driver.find_elements_by_xpath("//a[@class='yYlJEf VByer']")
    gps=[]
    for link in links:
        href=link.get_attribute('href')
        if len(href.split('/'))>6:
            gps.append(href)
    driver.close()
    return gps

#gps_links_big=more_locations(search_results_google('Big Bazaar Stores in ahmedabad'))




def url_op(a):
    add=[]
    for i in a:
        try:
            add.append(i.split('/')[6].replace('+',' '))
        except:
            continue
    return add

#address_big=url_op(gps_links_big)



def lat_lgt(result):
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)
    t=[]
    for i in result:
        driver.get(i)
        time.sleep(5)
        t.append(driver.current_url)
    driver.close()
    return t


#trial=lat_lgt(gps_links_big)


def gps_lat_lgt(a):
    temp=[]
    for i in a:
        try:
            temp.append('{0},{1}'.format(i.split('d')[-1],i.split('!')[-2].split('d')[-1]))
        except:
            continue
    return temp

#ab=gps_lat_lgt(trial)

# =============================================================================
# 
# =============================================================================

input_file_1=pd.read_table('test.txt',sep="\t")


df_final1=pd.DataFrame([])

for index,row in input_final.iterrows():
    #print(row['Store'])
    tem=[]
    temp=[]
    temp2=[]
    temp3=[]
    tem.append(search_results_google('{0} Stores in {1}'.format(row['Store'],row['City'])))
    for a in tem:
        if a is None:
            continue
        else:
            for i in more_locations(a):
                temp.append(i)    
    for i in url_op(temp):
        temp2.append(i)
    for i in gps_lat_lgt(lat_lgt(temp)):
        temp3.append(i)
    for j,k,l in zip(temp,temp2,temp3):
        df_final1 = df_final1.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':j,'Address':k,'lat_lgt':l}, index=[0]), ignore_index=True)
    print('done')


df_final_edit=pd.DataFrame([])
for index,row in df_final1.iterrows():
    if row['Store'].split(' ')[0].upper().lower() in row['gps'].split('/')[6].upper().lower():
        df_final_edit=df_final_edit.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':row['gps'],'Address':row['Address'],'lat_lgt':row['lat_lgt']}, index=[0]), ignore_index=True)


df_final_edit.to_csv('Output1.csv')
# =============================================================================
#df_final_edit is the first output
# =============================================================================
 
# =============================================================================
#df_final2=pd.DataFrame([])
#for index,row in input_final2.iterrows():
#    #print(row['Store'])
#    tem=[]
#    temp=[]
#    temp2=[]
#    temp3=[]
#    tem.append(search_results_google('{0} Stores in {1}'.format(row['Store'],row['City'])))
#    for a in tem:
#        if a is None:
#            continue
#        else:
#            for i in more_locations(a):
#                temp.append(i)    
#    for i in url_op(temp):
#        temp2.append(i)
#    for i in gps_lat_lgt(lat_lgt(temp)):
#        temp3.append(i)
#    for j,k,l in zip(temp,temp2,temp3):
#        df_final2 = df_final2.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':j,'Address':k,'lat_lgt':l}, index=[0]), ignore_index=True)
#    print('done')
#
#
#
#df_final3=pd.DataFrame([])
#
#for index,row in input_final3.iterrows():
#    #print(row['Store'])
#    tem=[]
#    temp=[]
#    temp2=[]
#    temp3=[]
#    tem.append(search_results_google('{0} Stores in {1}'.format(row['Store'],row['City'])))
#    for a in tem:
#        if a is None:
#            continue
#        else:
#            for i in more_locations(a):
#                temp.append(i)    
#    for i in url_op(temp):
#        temp2.append(i)
#    for i in gps_lat_lgt(lat_lgt(temp)):
#        temp3.append(i)
#    for j,k,l in zip(temp,temp2,temp3):
#        df_final3 = df_final3.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':j,'Address':k,'lat_lgt':l}, index=[0]), ignore_index=True)
#    print('done')

# =============================================================================
#without lat_log

#df2=pd.DataFrame([])
#
#for index,row in input_file_1.iterrows():
#    print(row['Store'])
#    temp=[]
#    temp2=[]
#    temp3=[]
#    for i in more_locations(search_results_google('{0} Stores in {1}'.format(row['Store'],row['City']))):
#        temp.append(i)
#    for i in url_op(temp):
#        temp2.append(i)
#    for j,k in zip(temp,temp2):
#        df2 = df2.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':j,'Address':k}, index=[0]), ignore_index=True)



        
# =============================================================================

#
        #Do not run this. kml files not available    
    #
    

#block=[]
#
#
#
#lat_all=[float(i.split(',')[0]) for i in df_final['lat_lgt']]
#lng_all=[float(i.split(',')[1]) for i in df_final['lat_lgt']]
#coords_all=np.array([[i,j] for i,j in zip(lat_all,lng_all)])
#
#
#for a in coords_all:
#    found=False
#    for filename in os.listdir('C:\python wd\web scrapping\mumbai_try'):
#        if filename.endswith('.kml'):
#            #print(filename)
#            s = BeautifulSoup(open(os.path.join('C:\python wd\web scrapping\mumbai_try', filename),'r'), 'xml')
#            for coords in s.find_all('coordinates'):
#                space_splits = coords.text.split(" ")
#            lat=[]
#            lng=[]
#            space_splits[0]=space_splits[0].split('\t')[-1]
#            del space_splits[-1]
#            for split in space_splits:
#                comma_split = split.split(',')
#                lat.append(comma_split[1])    # lat
#                lng.append(comma_split[0])    # lng
#    
#            lat=[float(i) for i in lat]
#            lng=[float(i) for i in lng]
#            #print(lat)
#            coords=[[i,j] for i,j in zip(lat,lng)]
#            coords2=np.array(coords)
#            poly=Polygon(coords2,closed=True)
#            if poly.get_path().contains_point(a):
#                found=True
#                block.append(filename)
#    if found==False:
#        block.append(np.nan)
#            #print('-------------------------------------------------------------')
#            #gmap.plot(lat, lng, 'cornflowerblue', edge_width=5)
#
#
## =============================================================================
#df_final['block']=block
