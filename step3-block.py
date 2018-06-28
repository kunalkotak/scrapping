# =============================================================================
# Block For Google Results
# =============================================================================
from bs4 import BeautifulSoup    
from selenium import webdriver
import pandas as pd
import numpy as np
from matplotlib.patches import Polygon
import time 



block=[]

lat_all=[float(i.split(',')[0]) for i in output_final_file['lat_lgt']]   #edit
lng_all=[float(i.split(',')[1]) for i in output_final_file['lat_lgt']]   #edit
coords_all=np.array([[i,j] for i,j in zip(lat_all,lng_all)])
#
#

import zipfile
import os
os.getcwd()
#file_name = "my_python_files.zip"
zip_files_list=[f for f in os.listdir(r'C:\python wd\web scrapping\all_kmls') if f.endswith('.zip')] 


import shutil

os.chdir(r'C:\python wd\web scrapping\all_kmls')      #Set the working directory 


for a,b in zip(coords_all,output_final_file['City']):
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
    
output_final_file['Block']=block    
