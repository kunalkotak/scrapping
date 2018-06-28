#from gmplot import gmplot

# Place map
#gmap = gmplot.GoogleMapPlotter(19.15166821453314,72.97506942300494,12)

mum_links=lat_lgt(more_locations(search_results_google('Dmart Stores in Mumbai')))
mumbai=gps_lat_lgt(mum_links)


mumbai_lat=[float(i.split(',')[0]) for i in mumbai]
mumbai_lng=[float(i.split(',')[1]) for i in mumbai]
mumbai_coords=np.array([[i,j] for i,j in zip(mumbai_lat,mumbai_lng)])


test=[]

for a in mumbai_coords:
    for filename in os.listdir('C:\python wd\web scrapping\mumbai_try'):
        if filename.endswith('.kml'):
            #print(filename)
            s = BeautifulSoup(open(os.path.join('C:\python wd\web scrapping\mumbai_try', filename),'r'), 'xml')
            for coords in s.find_all('coordinates'):
                space_splits = coords.text.split(" ")
            lat = []
            lng=[]
            space_splits[0]=space_splits[0].split('\t')[-1]
            del space_splits[-1]
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
                test.append(filename)
            #print('-------------------------------------------------------------')
            #gmap.plot(lat, lng, 'cornflowerblue', edge_width=5)

test1=[i.split('.')[0] for i in test]


# =============================================================================
# 
# =============================================================================
input_file_1=pd.read_table('test1.txt',sep="\t")

df=pd.DataFrame([])

for index,row in input_file_1.iterrows():
    #print(row['Store'])
    temp=[]
    temp2=[]
    temp3=[]
    for i in more_locations(search_results_google('{0} Stores in {1}'.format(row['Store'],row['City']))):
        temp.append(i)
    for i in url_op(temp):
        temp2.append(i)
    for i in gps_lat_lgt(lat_lgt(temp)):
        temp3.append(i)
    for j,k,l,m in zip(temp,temp2,temp3,test1):
        df = df.append(pd.DataFrame({'Store': row['Store'], 'City': row['City'],'gps':j,'Address':k,'lat_lgt':l,'Block':m}, index=[0]), ignore_index=True)
    print('done')










# =============================================================================
# 
# =============================================================================

mum_links=lat_lgt(more_locations(search_results_google('Dmart Stores in Mumbai')))
mumbai=gps_lat_lgt(mum_links)


mumbai_lat=[float(i.split(',')[0]) for i in mumbai]
mumbai_lng=[float(i.split(',')[1]) for i in mumbai]

gmap.scatter(mumbai_lat, mumbai_lng, 'red', size=60, marker=False)


gmap.draw("mumbai.html")
