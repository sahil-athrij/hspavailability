import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','maps.settings')
import django
django.setup()
import requests, json
from home.models import Markers
import datetime
from pprint import pprint
import time
import numpy as np

lats=np.linspace(8,37,116)
lngs=np.linspace(68,97,116)
for lat in lats:
    for lng in lngs:
        print(lat,lng)
        url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(lng)+'&radius=110000&type=hospital&country=India&key=AIzaSyCZrW79d1U3pgQDJlaErgxHQIq-8MRst-c'
        loc=requests.get(url)
        print(loc.content)
        data = json.loads(loc.content.decode())
        for x in data['results']:
            print(x["name"])
            lname = x["name"]
            lnum = "0000000000"
            lsize = 2
            lcost = 0
            lcovid = 0
            lfin = 0
            lbed = 0
            lcare = 0
            loxy = 0
            lvent = 0
            loxya = 0
            licu = 0
            llat = x["geometry"]["location"]["lat"]
            llng = x["geometry"]["location"]["lng"]
            ldate = datetime.date.today()

            marker = Markers.objects.get_or_create(name=lname, Phone=lnum, size=lsize,
                                                   financial_rating=lfin, avg_cost=lcost,
                                                   covid_rating=lcovid, beds_available=lbed,
                                                   care_rating=lcare, oxygen_rating=loxy,
                                                   ventilator_availability=lvent, icu_availability=licu,
                                                   oxygen_availability=loxya, lat=llat,
                                                   lng=llng, datef=ldate)[0]
        # while 'next_page_token' in data:
        #     url=url+'&pagetoken='+data['next_page_token']
        #     time.sleep(2)
        #     loc = requests.get(url)
        #     print(loc.content)
        #     data = json.loads(loc.content.decode())
        #     for x in data['results']:
        #         print(x['name'])
# loc = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=hospitals+in+India&key=AIzaSyCZrW79d1U3pgQDJlaErgxHQIq-8MRst-c')
# data = json.loads(loc.content.decode())
# for x in data['results']:
#     print(x["name"])
# while 'next_page_token' in data:
#     url='https://maps.googleapis.com/maps/api/place/textsearch/json?query=hospitals+in+India&key=AIzaSyCZrW79d1U3pgQDJlaErgxHQIq-8MRst-c&pagetoken='+data['next_page_token']
#     time.sleep(2)
#     loc = requests.get(url)
#     data = json.loads(loc.content.decode())
#     # print(data['next_page_token'])
#     for x in data['results']:
#         print(x["name"])





