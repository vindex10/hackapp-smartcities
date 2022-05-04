#!/usr/bin/env python3
import scipy as sp

g = 500000

def f_db(lat, lng, sensors):
	ret = 0
	for s in sensors.values():
		ret += s['val'] * sp.exp(- ((s['lat'] - lat)**2 + (s['lng'] - lng)**2) * g)
	return ret

def f(lat, lng, sensors):
	val = 0
	for s in sensors.values():
		val += s['val']
	return f_db(lat, lng, sensors) / val * sp.pi/g

def f_rgba(lat, lng, sensors):
	val = int(f_db(lat, lng, sensors))
	val = min(255, val)
	# print(val)
	if val < 50:
		return (0, 0, 0, 0)
	elif val < 90:
		return (255, 255, 0, 120)
	return (255, 0, 0, 120)
	# return (255, 0, 0)

def gen_heatmap_rgba(dp, wh, sensors):
	nw, nh = wh
	lat0, lng0 = dp[0], dp[1]
	dlat, dlng = dp[2] - lat0, dp[3] - lng0
	return [f_rgba(lat0 + dlat*j/nh, lng0 + dlng*i/nw, sensors) for j in range(nh) for i in range(nw)]
