from flask import Flask, request, jsonify
from flask import render_template, send_from_directory, make_response

from util import *
from connection import *
from pygeocoder import Geocoder
from keys import *

from places_to_visit import *

from rq import Queue
from rq.job import Job
from rq import get_current_job
from redis import Redis

from datetime import datetime as dt

import random

NUMER_OF_QUEUES = 8

queues = [Queue('r' + str(i), connection=Redis()) for i in range(8)]

app = Flask(__name__)
app.url_map.strict_slashes = False

qid=-1

def make_trip(location, money, country):
	money, errors = parse_money(money)

	job = get_current_job()

	price, first_dest, route = pick_cities(location, float(money), job, country)
	parsed_location = Geocoder(goo_key()).geocode(location)

	if first_dest:
		location_flight = Geocoder(goo_key()).geocode(first_dest)[0]

	places = go_nearby(parsed_location[0], location_flight, price, [], job, country, route)
	nearest_airport =dst_iata = getNearestAirport(parsed_location.latitude, parsed_location.longitude)['iata']

	data =  {
		'places_list': places[:-1],
		'origin': parsed_location.city,
		'return_trip': places[-1]
	}

	result = trips.insert_one({'user': 'gyani', 'trip': data, 'id': job.get_id(), 'edited': False, 'createdat': dt.now().strftime("%d-%m-%Y at %H:%M:%S")})

	return data


# A function to serve basic webpages
@app.route('/')
@app.route('/result/<queue_id>')
@app.route('/wait')
@app.route('/about')
@app.route('/mytrips')
def basic_pages(**kwargs):
	return make_response(open('templates/index.html').read())

# API end that takes in the GitHub url for processing
@app.route("/api/maketrip/", methods=["POST"])
def analyzer_api():
	global qid
	request_data = request.get_json(silent=True)
	if request_data and 'money' in request_data and 'location' in request_data:
		money = request_data['money']
		location = request_data['location']

		country = None
		if 'country' in request_data and request_data['country']:
			country = request_data['country']

		q = queues[((qid+1)%8)+1]
		qid+=1
		job = q.enqueue_call(func = 'app.make_trip', args=(location, money, country), result_ttl=5000, ttl=10000, timeout=10000)
		job.meta['current'] = 'Just Started'
		job.meta['phase'] = 'started'
		job.meta['money-left'] = money
		job.meta['country'] = country
		job.save()
		data = {}
		data['location'] = location
		data['money'] = money
		data['id'] = job.get_id()
		data['status'] = 'making-trip'

		return jsonify(**data)
	else:
		data = {'status': 'error'}
		return jsonify(**data)

@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static/img', 'favicon.ico')

# API end to query the status of the analysis
@app.route('/api/result/<queue_id>', methods=["GET"])
def result(queue_id):
	try:
		job = Job.fetch(queue_id, connection=Redis())
		data = {}

		if job.is_finished:
			data['trip'] = job.result
			data['status'] = 'success'

		elif job.is_failed:
			data['status'] = 'error'

		elif job.is_queued:
			data['status'] = 'queued'
		else:
			data['current'] = job.meta['current']
			data['status'] = 'processing'
			data['phase'] = job.meta['phase']
			data['money'] = job.meta['money-left']
			if 'from' in job.meta:
				data['from'] = job.meta['from']

		return jsonify(**data)
	except:
		trip = trips.find_one({'id': queue_id})
		data = {}
		data['status'] = 'success'
		data['trip'] = trip['trip']
		return jsonify(**data)

@app.route('/api/mytrips', methods=["GET"])
def mytrips():
	data = []
	trips_data = trips.find({'user': 'gyani'})

	for trip in trips_data:
		actual_trip = trip['trip']
		trip_cities = []
		image = actual_trip['places_list'][0]['photo']
		for place in actual_trip['places_list']:
			trip_cities.append(place['city'])

		trip_title = 'Trip to %s and %d other cities'%(', '.join(trip_cities[:min(4, len(trip_cities))]), len(trip_cities) -min(4,len(trip_cities)))
		creadedat = "21-01-2017 at 23:00:00"
		if 'creadedat' in trip:
			creadedat = trip["creadedat"]

		data.append({'title': trip_title, 'link': '/result/%s' %(trip['id']), 'createdat': creadedat, 'photo': image})

	response = {}
	response['data']  = data
	response['status'] = 'success'

	return jsonify(**response)

@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404

if __name__ == "__main__":
        app.debug = True
        app.run()