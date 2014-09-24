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

badscore = open("/Users/lindsaypettingill/Desktop/app/csv/badscore.csv")
df = pd.read_csv(badscore)
      
mymap = fo.Map(location=[37.7833, -122.4167], tiles='Stamen Toner',
                   zoom_start=11)
mymap.create_map(path='bad2.html')                  

for x in range(len(df.latitude)):
#	try:
	lat=(df.latitude[x])
	long=(df.longitude[x])
	name=(df.fullname[x])
#		scale=(df.badscore[x])*50.0
#		if np.isnan(scale):
#			continue
	mymap.circle_marker(location=[lat,long], popup=(name),radius=250, fill_color='#f00')
#	except:
#		continue
mymap.create_map(path='bad2.html')

