from flask import render_template, jsonify, request
from app import app
import pymysql as mdb
#import maps 
import folium as fo
import pandas as pd
import pdb
import pandas.io.sql as psql
import MySQLdb as mys
import numpy as np

db = mdb.connect(user="root", host="localhost", db="demo", charset='utf8')

@app.route('/')
def welcome():
	return render_template("welcome.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/slides')
def slides():
	return render_template("slides.html")

@app.route('/drsearch')
def drsearch():
    return render_template("drsearch.html")

@app.route('/index2')
def badtable():
  	with db:
 		cur = db.cursor()
    		cur.execute("SELECT fullname, city, proc, malp_word, pharmadollars, score, scoreptile FROM badt ORDER BY scoreptile DESC LIMIT 50;")
     	query_results = cur.fetchall()
     	cities = []
 	for result in query_results:
 			cities.append(dict(fullname=result[0],city=result[1],proc=result[2], pharmadollars=result[3], yelprating=result[4], malp_word=result[5]))
	return render_template("index2.html", cities=cities)

@app.route('/contact')
def contact():
    return render_template("contact.html")
    
@app.route('/about')
def about():
    return render_template("about.html")

# #make sure sql is up to date with correct csv to sql file		
 #@app.route('/db_fancy')
 #def cities_page_fancy():

#map from my python code
@app.route('/makemap', methods=['get'])
def map():
	user_selection = request.args.get('procedures')
	procedure={'Flu':"/Users/lindsaypettingill/Desktop/app/csv/flu.csv", 'NoGo':"/Users/lindsaypettingill/Desktop/app/csv/bad.csv",'CT Scan':"/Users/lindsaypettingill/Desktop/app/csv/ct.csv",
	'Chest Xray':"/Users/lindsaypettingill/Desktop/app/csv/xchest.csv", 'Lens':"/Users/lindsaypettingill/Desktop/app/csv/lens.csv", 'Cancer Screen':"/Users/lindsaypettingill/Desktop/app/csv/cancer.csv",
 	'Colon':"/Users/lindsaypettingill/Desktop/app/csv/colon.csv",'Electrocardiogram':"/Users/lindsaypettingill/Desktop/app/csv/ekgr.csv", 'EKG':"/Users/lindsaypettingill/Desktop/app/csv/ekgc.csv",
 	'ED':"/Users/lindsaypettingill/Desktop/app/csv/ed.csv", 'Eyen':"/Users/lindsaypettingill/Desktop/app/csv/eyenew.csv", 'Eyeo':"/Users/lindsaypettingill/Desktop/app/csv/eyeexam.csv", 
 	'Hearing':"/Users/lindsaypettingill/Desktop/app/csv/heartest.csv", 'HDD':"/Users/lindsaypettingill/Desktop/app/csv/hdd.csv", 'Medic M':"/Users/lindsaypettingill/Desktop/app/csv/mm.csv", 
 	'NMR':"/Users/lindsaypettingill/Desktop/app/csv/nm.csv", 'Coccal':"/Users/lindsaypettingill/Desktop/app/csv/cocc.csv",'Psych':"/Users/lindsaypettingill/Desktop/app/csv/psych.csv", 
 	'PT':"/Users/lindsaypettingill/Desktop/app/csv/pt.csv", 'Ear Wax':"/Users/lindsaypettingill/Desktop/app/csv/earwax.csv",'Shoulder Surgery':"/Users/lindsaypettingill/Desktop/app/csv/asurg.csv", 
 	'Thera Ex':"/Users/lindsaypettingill/Desktop/app/csv/thex.csv", 'Tissue':"/Users/lindsaypettingill/Desktop/app/csv/tissue.csv", 'Allergy':"/Users/lindsaypettingill/Desktop/app/csv/triam.csv",
 	'Nails':"/Users/lindsaypettingill/Desktop/app/csv/nails.csv",'Ultrasounds':"/Users/lindsaypettingill/Desktop/app/csv/ultrasound.csv",'Urine':"/Users/lindsaypettingill/Desktop/app/csv/urine.csv",
 	'Routine Veni':"/Users/lindsaypettingill/Desktop/app/csv/veni.csv",'Xray ab':"/Users/lindsaypettingill/Desktop/app/csv/xab.csv",'Xray ankle':"/Users/lindsaypettingill/Desktop/app/csv/xankle.csv",
 	'Xray foot':"/Users/lindsaypettingill/Desktop/app/csv/xfoot.csv",'Xray spine':"/Users/lindsaypettingill/Desktop/app/csv/xspine.csv",'Xray shoulder':"/Users/lindsaypettingill/Desktop/app/csv/xshoulder.csv"}	

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
 			if np.isnan(scale):
 				continue
 			mymap.circle_marker(location=[lat,long], popup=(name),radius=scale, fill_color='#3186cc')
 		except:
 			continue	
 		mymap.create_map(path='app/static/test.html')
 		
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
	return render_template("index.html", cities=cities)		
    
 		
# #to search!
@app.route('/search', methods=['get'])
def search():
	user_selection2 = request.args.get('docs')
	sqlsearch={'ljc':"LOUIS J. CUBBA",'jw':"JULIE WONG"}

	with db:
	    c=db.cursor()
        c.execute("SELECT fullname, city, yearspracticing, pharmadollars, services_count, score, scoreptile, lastlower FROM perc where fullname = '%s';"%(sqlsearch[user_selection2]))
        query_results = c.fetchall()
        #print query_results
        names=[]
	for result in query_results:
 			names.append(dict(fullname=result[0],city=result[1], yearspracticing=result[2], pharmadollars=result[3], countproc=result[4], score=result[5], scorereptile=result[6]))
	return render_template("search.html", names=names)


@app.route("/jquery")
def index_jquery():
    return render_template('index_js.html') 


