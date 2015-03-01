# -*- coding: utf-8 -*-
import bottle
from bottle import request, Bottle,redirect

from bottle.ext.mongo import MongoPlugin
from bson.json_util import dumps, loads
from pno_provider import get_virgin_tonic

app = Bottle()
plugin = MongoPlugin(uri="mongodb://127.0.0.1", db="podcast_cogimix")
app.install(plugin)

"""
Index
"""
@app.route('/')
def index(mongodb):
	#On retourne l'ensemble de la base
        podcast = mongodb['podcast'].find()
        return dumps(podcast)
"""
Refresh la base de donnée
"""
@app.route('/refresh')
def refresh(mongodb):
	vt = get_virgin_tonic()
	for title,url in vt:
		#On n'ajoute pas les url déja présentes
		in_base = mongodb['podcast'].find({"url":url}).count()
		if in_base == 0:
			#On insert le nouveau podcast
			objid = mongodb['podcast'].insert({"url":url,"title":title})
			#On extrait la partie increment de l'objectid
			inc = int(str(objid)[18:], 16)
			#On met à jour le podcast pour ajouter l'id (int)
			mongodb['podcast'].update({"_id":objid},{"$set" : { "id" : inc,"artist":"Podcast"}})

"""
Retourn un objet json id,title et artist pour les podcsats contenant la chaine de caractére de song_query
"""
@app.route('/search',method="POST")
def search(mongodb):
	try:
		#On récupére le body de la requête
		param = request.body.read()
		#Non mais sérieux @plfort c'est quoi cette requête...
		query = loads(param)['song_query']
        	res =  mongodb['podcast'].find({ "title" : {"$regex":query}},{ "_id" : False, 
										"id" : "$inc",
										"title" : 1,
										"artist":1})
		return dumps(res)
	except ValueError:
		return ""

@app.route('/ping')
def ping(mongodb):
        return mongodb['podcast'].find().count()

"""
Retourne une redirection sur l'url du podcast demandé
"""
@app.route('/get/<id>')
def get(mongodb,id):
	try:
		#On récupére le podcast
		res = mongodb['podcast'].find_one({"id":int(id)})
		#Oui ben voilà !
		url = "http://%s" % res['url']
        	return redirect(url)
	except TypeError:
		print "Id %s not found" % id

app.run(host='0.0.0.0', port=8000,debug=True,reloader=True)
