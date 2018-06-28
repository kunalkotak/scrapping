import os
os.getcwd()
os.chdir('C:\python wd\web scrapping\compairing address')

import pandas as pd
 #input address:
input_address=pd.read_excel('MT_ValidResponses_Details_v4.xlsx')    #mt response containing 'ResponseId' and Address Columns


compaire_address=pd.read_csv('Vadodara Address_to_block.csv') #Output of the google address after getting the blocks


# =============================================================================
# h try
# =============================================================================

from string import digits

#s = 'abc123def456ghi789zero0'
remove_digits = str.maketrans('', '', digits)
temp_MT=input_address.copy()
t_h=[]
for i in temp_MT['Address_2']:#edit this column name according to your input file. 
    t_h.append(i.translate(remove_digits))


temp_MT['Address3']=t_h
# =============================================================================

temp_google=compaire_address.copy()

#### Cleaning the data

t_h1=[]
for i in temp_google['Address']:
    t_h1.append(i.translate(remove_digits))

remove_coma = str.maketrans('', '',',')

t_h2=[]
for i in t_h1:
    t_h2.append(i.translate(remove_coma))    


t_h3=[]
for i in t_h2:
    t_h3.append(" ".join(i.split()))

temp_google['Address3']=t_h3
# =============================================================================
from fuzzywuzzy import fuzz
# =============================================================================
# 
# =============================================================================

temp_h2=pd.DataFrame([])

for index1,row1 in temp_MT.iterrows():
    for index2,row2 in temp_google.iterrows():
        if row1['CHAIN NAME']==row2['Store name']:
            #temp_temp = temp_temp.append(pd.DataFrame({'Store': row2['Store'], 'City': row2['City'],'gps':row2['gps'],'Address_google':row2['Address'],'lat_lgt':row2['lat_lgt'],'Similarity':a,'Address':row1['Address_2']}, index=[0]), ignore_index=True)
            temp_h2 = temp_h2.append(pd.DataFrame({'ResponseId':row1['RESPONSEID'],'Store': row2['Store name'], 'City': row2['City'],'Address_google':row2['Address'],'lat_lgt':row2['lat_lng'],'Similarity':fuzz.token_set_ratio(row1['Address3'], row2['Address3']),'Address':row1['Address_2']}, index=[0]), ignore_index=True)


temp_h2['Similarity'].unique()

delete_fun=temp_h2[temp_h2['Similarity']>=65]   #threshold value selection

# =============================================================================
# Selecting the best Row with Maximum Similarity.
# =============================================================================
delete_fun2=delete_fun.sort_values('Similarity', ascending=False).drop_duplicates('Address_google').sort_index()    


# =============================================================================
