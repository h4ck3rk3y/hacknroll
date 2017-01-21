from pygeocoder import Geocoder
from pymongo import MongoClient

mongoclient = MongoClient('mongodb://localhost:27017/')
routerush = mongoclient.routerush

gplaces = routerush.gplaces
gphotos = routerush.gphotos
route_rome = routerush.rome2rio
geo = routerush.geo
