#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from pyroutelib3 import Router
from PIL import Image
import base64
from io import BytesIO

from sensors import open_json, load_dump, get_avr_sensors
from sensors import gen_rand_sensors_loc, gen_sensors
from heatmap import gen_heatmap_rgba, f

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = os.urandom(64)

@app.route("/")
def index():
	return render_template('index.html')

def get_args(convert, *args):
	return tuple(convert(request.args.get(a)) for a in args)

router_0 = Router('car', 'map')
router_avoid = Router('car', 'map')

# import scipy as sc
@app.route("/path/<string:avoid>")
def path(avoid):
	sensors = load_dump('rand_sensors.dmp')
	# print(sensors)
	# print('>>>>>>>>>', avoid)
	if avoid == 'avoid':
		router = router_avoid
		router.weights = lambda lat, lng: f(lat, lng, sensors)
	else:
		router = router_0
	# print('--------------', router.weights(1.00004276, 0.99926016))
	# print('>>>>>>>>>>>>>>>>', router.weights(sc.array([ 1.00004276, 1.,     0.99995724]), sc.array([ 0.99926016, 1.    ,      1.00073984])))
	# print(router.weights(50.8716958196109, 9.696314334869387))
	start = router.data.findNode(*get_args(float, 'startlat', 'startlng')) # Find start
	end = router.data.findNode(*get_args(float, 'endlat', 'endlng')) # Find end
	status, route = router.doRoute(start, end) # Find the route - a list of OSM nodes
	print('>>>>>', list(map(router.nodeLatLon, route))[:5])
	return jsonify(list(map(router.nodeLatLon, route)))

# sensors_loc = gen_rand_sensors_loc((50.8716958196109, 9.696314334869387, 50.86492479825324, 9.711334705352783), 30)

@app.route("/heatmap")
def heatmap():
	buffered = BytesIO()
	dp = get_args(float, 'lefttoplat', 'lefttoplng', 'rightbotlat', 'rightbotlng')
	# sensors = get_avr_sensors(open_json('test_datasample.json'), dp=dp)
	sensors = load_dump('rand_sensors.dmp')
	# sensors = gen_sensors(sensors_loc)
	imsize = get_args(int, 'width', 'height')
	imsize = tuple(int(s/8) for s in imsize)
	image = Image.new("RGBA", imsize)
	# rgba = [(255, g, b, int(r*0.6)) for r, g, b in gen_heatmap_rgb(dp, imsize, sensors)]
	# rgba = [(r, g, b, 100) for r, g, b in gen_heatmap_rgb(dp, imsize, sensors)]
	image.putdata(gen_heatmap_rgba(dp, imsize, sensors))
	image.save(buffered, format="PNG")
	return base64.b64encode(buffered.getvalue())

@app.route('/<path:path>')	# temp hack <<<<<<<<<<<<<<<<<<<<<<<
def send_js(path):
	return send_from_directory('.', path)

if __name__ == "__main__":
	app.run(debug=True)
	# app.run(host='0.0.0.0', port=8000)
	# from gevent.wsgi import WSGIServer
	# WSGIServer(('0.0.0.0', 8000), app).serve_forever()