import pandas.io.sql as psql
import MySQLdb as mys
import pandas as pd
import folium as fo
import pdb
import numpy as np

def pins():
	fluimport = open("/Users/lindsaypettingill/Desktop/flu.csv")
	df = pd.read_csv(fluimport)
      
	mymap = fo.Map(location=[37.7833, -122.4167], tiles='Stamen Toner',
                   zoom_start=11)

	for x in range(len(df.latitude)):
		try:
			lat=(df.latitude[x])
			long=(df.longitude[x])
			name=(df.fullname[x])
			scale=(df.est10[x])*30.0
			if np.isnan(scale):
				continue
			mymap.circle_marker(location=[lat,long], popup=(name),radius=scale, fill_color='#f00')
		except:
			continue
		mymap.create_map(path='/Users/lindsaypettingill/Desktop/app/flu.html')
