import pandas.io.sql as psql
import MySQLdb as mys
import pandas as pd
import folium as fo
import pdb
import numpy as np

# import sql as df
# #con = MySQLdb.connect(host="localhost",
#                       port=3306,
#                       user="root",
#                       db="doctor_main")
# sql = """
#         select *
#             from main3
#       """
# sqltopandas = psql.frame_query(sql, con)
# con.close()
# #end of that import
# pandasdf=sqltopandas

fluimport = open("/Users/lindsaypettingill/Desktop/app/csv/flu.csv")
df = pd.read_csv(fluimport)
      
mymap = fo.Map(location=[37.7833, -122.4167], tiles='Stamen Toner',
                   zoom_start=11)
mymap.create_map(path='test.html')                  

for x in range(len(df.latitude)):
	try:
		lat=(df.latitude[x])
		long=(df.longitude[x])
		name=(df.fullname[x])
		scale=(df.score[x])*30
		if np.isnan(scale):		
			continue
		if scale<10:		
			mymap.circle_marker(location=[lat,long], popup=(name),radius=scale, fill_color='#f00')
		else:
			mymap.circle_marker(location=[lat,long], popup=(name),radius=scale, fill_color='#2ca25f')
	except:
		continue
mymap.create_map(path='flu.html')
