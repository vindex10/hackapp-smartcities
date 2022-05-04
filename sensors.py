#!/usr/bin/env python3
import json
from datetime import datetime

def open_json(filename='bad_hersfeld_merged.json'):
	with open(filename) as f:
		js = json.loads(f.read())
	return js['sensordata']

def to_datetime(timestamp):
	return datetime.strptime(timestamp.split('.')[0], "%Y-%m-%dT%H:%M:%S")

def get_sensors(jsdata, dts=('2018-01-25T00:00:00', '2018-04-25T00:00:00'), dp=(50.89, 9.6, 50.86, 9.8)):
	sensors = {}
	for s in jsdata:
		if (s['type'] == 'noise' and to_datetime(dts[0]) <= to_datetime(s['timestamp']) <= to_datetime(dts[1])
		 and dp[2] <= s['lat'] <= dp[0] and dp[1] <= s['lng'] <= dp[3]):
			sid = s['sensorId']
			if sid not in sensors:
				sensors[sid] = {'lng': s['lng'], 'lat': s['lat'], 'val': s['measurement'], 'n': 1}
			else:
				sensors[sid]['val'] += s['measurement']
				sensors[sid]['n'] += 1
	return sensors

# def merge_sensors(*sss):
# 	pass

def get_avr_sensors(*a, **kw):
	avr_sensors = {}
	for sid, sensor in get_sensors(*a, **kw).items():
		avr_sensors[sid] = {'lng': sensor['lng'], 'lat': sensor['lat'], 'val': sensor['val']/sensor['n']}
	return avr_sensors

def dump_sensors(sensors, filename):
	with open(filename, 'w') as f:
		f.write(str(sensors))

def load_dump(filename):
	with open(filename) as f:
		s = f.read()
	return eval(s)

from random import random
def gen_rand_sensors_loc(dp, n):
	lat0, lng0 = dp[0], dp[1]
	dlat, dlng = dp[2] - lat0, dp[3] - lng0
	return [(lat0 + random()*dlat, lng0 + random()*dlng) for i in range(n)]

def gen_sensors(locs):
	sensors = {}
	for lat, lng in locs:
		sensors[str(lat)+' '+str(lng)] = {'lng': lng, 'lat': lat, 'val': 40 + random()*50}
	return sensors

if __name__ == '__main__':
	# print(get_avr_sensors(open_json('test_datasample.json')))
	# dump_sensors(get_avr_sensors(open_json()), 'sensors.dmp')
	# print(load_dump('sensors.dmp'))
	sensors_loc = gen_rand_sensors_loc((50.8716958196109, 9.696314334869387, 50.86492479825324, 9.711334705352783), 25)
	sensors = gen_sensors(sensors_loc)
	dump_sensors(sensors, 'rand_sensors.dmp')