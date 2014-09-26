from flask import render_template, jsonify, request, redirect, url_for
from app import app
import pymysql as mdb
#import maps 
import folium as fo
import pandas as pd
import pdb
import pandas.io.sql as psql
import MySQLdb as mys
import numpy as np
import sys, os

db = mdb.connect(user="root", host="localhost", db="demo", charset='utf8')

@app.route('/')
def welcome():
	return render_template("welcome.html")
	
@app.route('/slides')
def slides():
	return render_template("slides.html")
	
@app.route('/index2')
def badtable():
  	with db:
 		cur = db.cursor()
    		cur.execute("SELECT fullname, city, pharmadollars, score, scoreptile FROM badt ORDER BY scoreptile DESC LIMIT 50;")
     	query_results = cur.fetchall()
     	cities = []
 	for result in query_results:
 			cities.append(dict(fullname=result[0],city=result[1], pharmadollars=result[2], score=result[3], scoreptile=result[4]))
	return render_template("index2.html", cities=cities)		

@app.route('/index')
def index():
	return render_template("index.html",user_selection='Flu')
	#return redirect(url_for('.makemap'),procedures='Flu')
	
@app.route('/contact')
def contact():
    return render_template("contact.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/drsearch')
def drsearch():
    return render_template("drsearch.html")    
    
# #make sure sql is up to date with correct csv to sql file		
 #@app.route('/db_fancy')
 #def cities_page_fancy():

#map from my python code
@app.route('/makemap', methods=['get'])
def map():
	user_selection = request.args.get('procedures')
	procedure={'Flu':"app/csv/flu.csv", 'CT Scan':"app/csv/ct.csv",
	'Chest Xray':"app/csv/xchest.csv", 'Lens':"app/csv/lens.csv",
 	'Colon':"app/csv/colon.csv",'Electrocardiogram':"app/csv/ekgc.csv", 'EKG':"app/csv/ekgr.csv",
 	'ED':"app/csv/ed.csv", 'Eyen':"app/csv/eyenew.csv", 'Eyeo':"app/csv/eyeexam.csv", 
 	'Hearing':"app/csv/hearing.csv", 'HDD':"app/csv/hdd.csv", 'Medic M':"app/csv/mm.csv", 
 	'NMR':"app/csv/nm.csv", 'Coccal':"app/csv/cocc.csv",'Psych':"app/csv/psych.csv", 
 	'PT':"app/csv/pt.csv", 'Ear Wax':"app/csv/earwax.csv",'Shoulder Surgery':"app/csv/asurg.csv", 
 	'Thera Ex':"app/csv/thex.csv", 'Tissue':"app/csv/tissue.csv", 'Allergy':"app/csv/triam.csv",
 	'Nails':"app/csv/nails.csv",'Ultrasounds':"app/csv/ultrasound.csv",'Urine':"app/csv/urine.csv",
 	'Routine Veni':"app/csv/veni.csv",'Xray ab':"app/csv/xab.csv",'Xray ankle':"app/csv/xankle.csv",
 	'Xray foot':"app/csv/xfoot.csv",'Xray spine':"app/csv/xspine.csv",'Xray shoulder':"app/csv/xshoulder.csv"}	

	fluimport = open(procedure[request.args["procedures"]])
	#print procedure[request.args["procedures"]]
	df = pd.read_csv(fluimport)
	#print df.latitude[1]
	#print df.score[1]
	mymap = fo.Map(location=[37.7341003,-122.114853], tiles='Stamen Toner',
                   zoom_start=10)	
 	for x in range(len(df.latitude)):
 		try:
 			lat=(df.latitude[x])
 			long=(df.longitude[x])
 			name=(df.fullname[x])
 			scale=(df.score[x])*30.0
 			bad=(df.bad[x])
			badscale=df.bad[x]*500
 			if np.isnan(scale):
 				continue
 			if bad==1:		
				mymap.circle_marker(location=[lat,long], popup=(name),radius=badscale, fill_color='#f00')
			else:
				mymap.circle_marker(location=[lat,long], popup=(name),radius=scale, fill_color='#0000FF')
 		except:
 			continue	
 	mymap.create_map(path='app/templates/test.html')
 		
#  to load sql tables with maps!
 	sqlproc={'Flu':"Admin influenza virus vac", 'CT Scan':"Ct head/brain w/o dye",
	'Chest Xray':"Chest x-ray", 'Lens':"Anesth lens surgery", 'Cancer Screen':"Cancer screen w pelvic of breast exam", 'Colon':"Colonoscopy and biopsy",'Electrocardiogram':"Electrocardiogram report", 'EKG':"Electrocardiogram complete",
 	'ED':"Emergency dept visit", 'Eyen':"Eye exam new patient", 'Eyeo':"Eye exam & treatment", 'Hearing':"Comprehensive hearing test", 'HDD':"Hospital discharge day", 'Medic M':"Medication management", 
 	'NMR':"Neuromuscular reeducation", 'Coccal':"Pneumococcal vaccine",'Psych':"Psy dx interview", 'PT':"Pt evaluation", 'Ear Wax':"Remove impacted ear wax",'Shoulder Surgery':"Shoulder arthroscopy/surgery", 
 	'Thera Ex':"Therapeutic exercises", 'Tissue':"Tissue exam by pathologist", 'Allergy':"Triamcinolone acet inj NOS",
 	'Nails':"Trim nail(s)",'Ultrasounds':"Ultrasound therapy",'Urine':"Urinalysis nonauto w/o scope",
 	'Routine Veni':"Routine venipuncture",'Xray ab':"X-ray exam of abdomen",'Xray ankle':"X-ray exam of ankle",
 	'Xray foot':"X-ray exam of foot",'Xray spine':"X-ray exam of lower spine",'Xray shoulder':"X-ray exam of shoulder"}	
 		
  	with db:
 		cur = db.cursor()
    		cur.execute("SELECT fullname, city, yearspracticing, services_count, pharmadollars, score, scoreptile FROM week3 WHERE proc='%s' ORDER BY score DESC LIMIT 30;"%(sqlproc[user_selection]))
     	query_results = cur.fetchall()
     	cities = []
 	for result in query_results:
 			cities.append(dict(fullname=result[0],city=result[1], yearspracticing=result[2], services_count=result[3], pharmadollars=result[4], score=result[5], scoreptile=result[6]))
	return render_template("index.html", user_selection=user_selection, cities=cities)	

@app.route('/makemap2')
def help():
	return render_template('test.html')
 		
 #to search!
@app.route('/search', methods=['get'])
def search():
	user_selection2 = request.args.get('docs')
	sqlsearch={'ak':"AMIR KAYKHA" ,'tjh':"THOMAS J. HONRATH",'jw':"JULIE WONG"}

	with db:
	    c=db.cursor()
        c.execute("SELECT fullname, city, yearspracticing, pharmadollars, services_count, score, scoreptile FROM week3 where fullname = '%s';"%(sqlsearch[user_selection2]))
        query_results = c.fetchall()
        #print query_results
        names=[]
	for result in query_results:
 			names.append(dict(fullname=result[0],city=result[1], yearspracticing=result[2], pharmadollars=result[3], services_count=result[4], score=result[5], scoreptile=result[6]))
	return render_template("drsearch.html", names=names)
