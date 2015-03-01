# -*- coding: utf-8 -*-
import requests
import re


#Http Headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
          AppleWebKit/537.36 (KHTML, like Gecko) \
          Chrome/29.0.1535.0 Safari/537.36'}
#Retourne les urls Virgin Tonic de la page
reg_url_vt = re.compile('<a href=.(.*html).>.*(Virgin Tonic du [0-9]*/[0-9]*/[0-9]*)</a>')
#Retourne les url vers archive.org
reg_archive = re.compile('.*(archive.org.*mp3).*')
#Url des podcasts Virgin
url_virgin = "http://podcast-non-officiel.blogspot.fr/search/label/Virgin%20Tonic"

"""
Retourne l'url archive.org présent dans la page de l'url passée en param
"""
def get_archive_url(url):
	r = requests.get(url,headers=headers)
	return reg_archive.findall(r.text)[0]
"""
Retourne une liste de couple label,url virgin tonic
"""	
def get_virgin_tonic():
	list_vt = []
	r =  requests.get(url_virgin, headers=headers)	
	dico = reg_url_vt.findall(r.text)
	for url,label in dico:
		pod = [label,get_archive_url(url)]
		list_vt.append(pod)	
	return list_vt

if __name__ == "__main__":
	print get_virgin_tonic()
