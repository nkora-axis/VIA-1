#!/usr/bin/python
import requests
import codecs
import sys
import json
import collections
import pycountry
import pymongo
from pymongo import MongoClient

url="https://in.via.com/apiv2/hotels/hotel-auto?gsjr=true&term=" + str(sys.argv[1]) + "&flowType=NODE&ajax=true&jsonData=false&authToken=553f5767-373f-4d98-9e6d-08fa87400a42&requestSource=NODE_B2C&__xreq__=true"
res = requests.get(url)
json_res = json.loads(res.text)
res = []		
res1 = []
f_res = []
F_ress = []
mapping = ['_id','city','state','country','country_code']
for i in range(len(json_res['locations']['Cities'])):
	res.append(((json_res['locations']['Cities'])[i]).values())
	res1.append([res[i][j] for j in range(1,len(res[i]))])
	for k in res1[i][((len(res1[i]))-1)].split(','): res1[i].append(k)
	del res1[i][1]
	f_res.append([{mapping[k]:res1[i][k]} if k!=4 else {mapping[k]:(pycountry.countries.get(name=res1[i][k-1])).alpha_3} for k in range(len(mapping))])
	f_res[i].append({'type':'city'})
	F_ress.append({ k:v for i in range(len(f_res)) for j in range(len(f_res[i])) for k,v in f_res[i][j].items() for i in range(len(f_res))})
		
for i in range(len(F_ress)):
	print(str(i) +" : "+str(F_ress[i]))
choice = int(input("Enter your choice"))
connection = MongoClient('localhost',27017)
db = connection.VA
loc_detail = db.locations

try:
    loc_detail.insert(F_ress[choice],continue_on_error=False)
except pymongo.errors.DuplicateKeyError:
	print 'Duplicate key Error  %s' % F_ress[choice]['_id']


