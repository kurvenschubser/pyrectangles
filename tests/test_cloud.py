from __future__ import print_function

import sys
import math
import random

from rectangles import (
	Rectangle,
	RectangleCloud,
	INF,
	DIRECTION_UP,
	DIRECTION_DOWN,
	DIRECTION_LEFT,
	DIRECTION_RIGHT,
	partition,
)
R = Rectangle


RECTS = (R(10, 10, 10, 10), R(5, 10, 5, 10), R(25, 10, 10, 10),
			R(10, 25, 10, 10),
			R(10, 40, 10, 5))


CLOUDS = dict(
	checkers = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10), R(20, 20, 10, 10), R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	cross = RectangleCloud([
		R(0, 10, 10, 20), R(10, 0, 10, 40), R(20, 10, 10, 20)
	]),
	slash = RectangleCloud([
		R(5, 5, 10, 10), R(20, 20, 10, 10), R(35, 35, 10, 10)
	]),
	back_slash = RectangleCloud([
		R(5, 35, 10, 10), R(20, 20, 10, 10), R(35, 5, 10, 10)
	]),
	x = RectangleCloud([
		R(5, 5, 10, 10),                   R(35, 5, 10, 10),
		                 R(20, 20, 10, 10), 
		R(5,35, 10, 10),                   R(35, 35, 10, 10), 
	]),
	c = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10),
		R(5, 20, 10, 10),
		R(5,35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	mortar_left = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10),
											R(35, 20, 10, 10),
		R(5,35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	ring = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10),                  R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10)
	]),
	percent = RectangleCloud([
		R(5, 5, 10, 10),                                                       R(5, 65, 10, 10),
		                 R(20, 20, 10, 10),
		                                   R(35, 35, 10, 10),
		                                                     R(50, 50, 10, 10),
		R(5, 65, 10, 10),									                   R(65, 65, 10, 10)
	]),
	explode = RectangleCloud([
		R(5, 5, 10, 10),                     R(35, 5, 10, 10), 

		R(5, 35, 10, 10),                    R(35, 35, 10, 10)
	]),
	eight = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), 
		R(5, 20, 10, 10),                  R(35, 20, 10, 10),
		R(5, 35, 10, 10), R(20, 35, 10, 10), R(35, 35, 10, 10),
		R(5, 50, 10, 10),                    R(35, 50, 10, 10),
		R(5, 65, 10, 10), R(20, 65, 10, 10), R(35, 65, 10, 10)
	]),
	wheel = RectangleCloud([
		R(5, 5, 10, 10), R(20, 5, 10, 10), R(35, 5, 10, 10), R(50, 5, 10, 10), R(65, 5, 10, 10),
		R(5, 20, 10, 10),                                                      R(65, 20, 10, 10),
		R(5, 35, 10, 10),                    R(35, 35, 10, 10),                R(65, 35, 10, 10),
		R(5, 50, 10, 10),                                                      R(65, 50, 10, 10),
		R(5, 65, 10, 10), R(20, 65, 10, 10), R(35, 65, 10, 10), R(50, 65, 10, 10), R(65, 65, 10, 10)
	]),
)


def test_arrange():
	rects = r1, r2 = R(0, 0, 10, 30), R(10, 0, 20, 10)
	cloud = RectangleCloud(rects)
	cloud.arrange()

	assert r1.x == 20 and r2.x == 0 or r1.x == 0 and r2.x == 10
	assert r1.y == 0 and r2.y == 10
	assert r1.w == 10
	assert r1.h == 30

	assert r2.w == 20
	assert r2.h == 10


def test_ratio():
	cloud = RectangleCloud()
	cloud.add_rect(RECTS[0].clone())


class TestAddRect:
	def test_one(self):
		rects = r1, r2 = R(0, 0, 10, 30), R(10, 10, 20, 10)
		cloud = RectangleCloud(rects)

		# add a rect
		r = R(0, 0, 20, 10)
		cloud.add_rect(r)
		assert r == R(10, 20, 20, 10)

	def test_multiple(self):

		cloud = RectangleCloud()

		# add a rect
		r1 = RECTS[0].clone()

		cloud.add_rect(r1)
		assert r1 == R(0,0,10,10)

		# add next rect
		r2 = RECTS[1].clone()

		cloud.add_rect(r2)

		assert r1 == R(0,0,10,10)
		assert r2 == R(10,0,5,10)


def test_get_sorted_left():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)

	assert cloud._rects == rects
	assert (
		cloud.get_sorted_left()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test_get_sorted_lower():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_lower()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test_get_sorted_right():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_right()
		== [rects[1], rects[0], rects[3], rects[4], rects[2]]
	)


def test_get_sorted_upper():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_sorted_upper()
		== [rects[0], rects[1], rects[2], rects[3], rects[4]]
	)


def test_get_occupied_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	assert (
		cloud.get_occupied_rect()
		== R(5, 10, 30, 35)
	)


def test_get_selection_by_rect():
	rects = map(lambda o: R(*o), RECTS)

	cloud = RectangleCloud(rects)
	occ = cloud.get_occupied_rect()
	cp = occ.get_center()

	## sector 1, 1
	half1 = partition(occ, cp, DIRECTION_RIGHT)
	half2 = partition(occ, cp, DIRECTION_UP)
	sectorrect = half1.get_intersection(half2)
	assert (
		set(cloud.get_selection_by_rect(sectorrect))
		== set()
	)

	## sector 0, 1
	half1 = partition(occ, cp, DIRECTION_LEFT)
	half2 = partition(occ, cp, DIRECTION_UP)
	sectorrect = half1.get_intersection(half2)
	
	assert (
		set(cloud.get_selection_by_rect(sectorrect))
		== set([rects[3], rects[4]])
	)
	
	## sector 0, 0
	half1 = partition(occ, cp, DIRECTION_LEFT)
	half2 = partition(occ, cp, DIRECTION_DOWN)
	sectorrect = half1.get_intersection(half2)

	assert (
		set(cloud.get_selection_by_rect(sectorrect))
		== set([rects[0], rects[1], rects[3]])
	)

	## sector 1, 0
	half1 = partition(occ, cp, DIRECTION_RIGHT)
	half2 = partition(occ, cp, DIRECTION_DOWN)
	sectorrect = half1.get_intersection(half2)
	
	assert (
		set(cloud.get_selection_by_rect(sectorrect))
		== set([rects[2]])
	)


#############
## new try ##
#############

def test_make_candidates_data():
	r1 = R(5, 5, 10, 30)
	cloud = RectangleCloud([r1])

	## Make a spot facing down to infinity, i.e. without intersection
	occ = cloud.get_occupied_rect()
	spot = R(occ.x - INF, occ.y - INF, occ.w + 2 * INF, INF)
	intsec = occ.get_intersection(spot)
	assert not intsec

	rect = R(0, 0, 10, 10)
	data = cloud.make_candidates_data(spot, rect)

	cand = R(5, -5, 10, 10)
	assert data == [(cand, intsec, spot)]

	## test intersecting spot
	r2 = R(15, 20, 10, 10)
	cloud._rects.append(r2)
	cloud._invalidate()
	occ = cloud.get_occupied_rect()
	spot = R(r1.x + r1.w, r2.y + r2.h, occ.x + occ.w - (r2.x + r2.w) + INF, \
										occ.y + occ.h - (r2.y + r2.h) + INF)
	intsec = occ.get_intersection(spot)
	assert intsec

	data = cloud.make_candidates_data(spot, rect)

	cand = R(spot.x, spot.y, rect.w, rect.h)
	assert data == [(cand, intsec, spot)]


def test_rate_candidates():
	# r1, r2, r3 = R(0, 10, 10, 10), R(10, 0, 10, 30), R(20, 10, 10, 10)
	# cloud = RectangleCloud([r1, r2, r3], steps=12)
	# occ = cloud.get_occupied_rect()
	tobefit = R(0, 0, 20, 20)
	# spots = cloud.get_spots_for_rectangle(tobefit)

	# candidates_data = set()
	# for sp in spots:
		# data = cloud.make_candidates_data(sp, tobefit, occ)
		# candidates_data.update(data)

	# candidates_data = list(candidates_data)
	# rated = cloud.rate_candidates(candidates_data, occ)

	# expected_candidates = [
			# R(r2.x + r2.w, r3.y + r3.h, tobefit.w, tobefit.h),
			# R(r2.x - tobefit.w, r1.y + r1.h, tobefit.w, tobefit.h),
			# R(r2.x - tobefit.w, r1.y - tobefit.h, tobefit.w, tobefit.h),
			# R(r2.x + r2.w, r3.y - tobefit.h, tobefit.w, tobefit.h)
		# ]

	# assert (sorted([n[1] for n in sorted(rated, key=lambda t:t[0])][-4:], key=tuple)
		# == sorted(expected_candidates, key=tuple))


	## Try again with different coordinates.
	r1, r2, r3 = R(0, 15, 15, 10), R(15, 0, 10, 30), R(25, 10, 5, 10)
	cloud = RectangleCloud([r1, r2, r3])
	occ = cloud.get_occupied_rect()

	spots = cloud.get_spots_for_rectangle(tobefit)

	print("\n\n>>>>>>>>>>>>>>>>>>>>candidates_data>>>>>>>>>>>>>>>>>>>")
	print("spots", spots)
	
	candidates_data = set()
	for sp in spots:
		data = cloud.make_candidates_data(sp, tobefit)
		print("sp", sp)
		print("data", data)
		candidates_data.update(data)

	candidates_data = list(candidates_data)

	print(candidates_data)
	print("<<<<<<<<<<<<<<<<<<<<<candidates_data<<<<<<<<<<<<<<<<<<<")

	rated = cloud.rate_candidates(candidates_data)

	for i, (ratio, c) in enumerate(rated):
		print(i, ratio, c)
		print(c.debuginfo)
		print()
	print([n for n in sorted(rated, key=lambda t:t[0])])

	expected_candidates = [
		R(r2.x + r2.w, r3.y + r3.h, tobefit.w, tobefit.h),
		R(r2.x - tobefit.w, r1.y + r1.h, tobefit.w, tobefit.h),
		R(r2.x - tobefit.w, r1.y - tobefit.h, tobefit.w, tobefit.h),
		R(r2.x + r2.w, r3.y - tobefit.h, tobefit.w, tobefit.h)
	]

	print("\n", "spots", spots)
	print("expected_candidates", expected_candidates, len(expected_candidates))
	print("actual candidates", rated, len(rated))
	print()

	assert (sorted([n[1] for n in sorted(rated,
											key=lambda t:t[0])][-4:],
											key=tuple)
		== sorted(expected_candidates, key=tuple))


def test_get_spots_for_rectangle():
	r1, r2, r3 = R(0, 10, 10, 10), R(10, 0, 10, 30), R(20, 10, 10, 10)
	cloud = RectangleCloud([r1, r2, r3])
	occ = cloud.get_occupied_rect()
	
	tobefit = R(0, 0, 20, 20)
	
	spots = cloud.get_spots_for_rectangle(tobefit)
	
	expected_spots = [
		## inner spots
		R(r2.x + r2.w, r3.y + r3.h, 
			occ.x + occ.w - (r2.x + r2.w) + INF,
			occ.y + occ.h - (r3.y + r3.h) + INF),
		R(r2.x + r2.w, occ.y - INF, 
			occ.x + occ.w - (r2.x + r2.w) + INF,
			r3.y - occ.y + INF),
		R(occ.x - INF, occ.y - INF,
			r2.x - occ.x + INF,
			r1.y - occ.y + INF),
		R(occ.x - INF, r1.y + r1.h,
			r2.x - occ.x + INF,
			occ.y + occ.h - (r1.y + r1.h) + INF),
		## outer spots
		R(occ.x + occ.w, occ.y - INF,
			INF,
			occ.h + 2 * INF),
		R(occ.x - INF, occ.y + occ.h,
			occ.w + 2 * INF,
			INF),
		R(occ.x - INF, occ.y - INF,
			INF,
			occ.h + 2 * INF),
		R(occ.x - INF, occ.y - INF,
			occ.w + 2 * INF,
			INF)
	]
	
	print(len(spots), len(expected_spots))
	print(sorted(spots, key=tuple))
	print(sorted(expected_spots, key=tuple))

	assert sorted(spots, key=tuple) == sorted(expected_spots, key=tuple)


def test_clone():
	cloud = CLOUDS["x"].clone()
	expected_cloud = RectangleCloud(
		[r.clone() for r in CLOUDS["x"].get_rects()])
	assert cloud.get_rects() == expected_cloud.get_rects()


class TestGetSeedPoints:
	def test_get_seed_points(self):
		cloud = CLOUDS["cross"].clone()
		seeds = cloud._get_seed_points(DIRECTION_RIGHT)
		expected_seeds = [(30, 20), (20, 5), (20, 35)]
		print(seeds)
		print(expected_seeds)
		assert set(seeds) == set(expected_seeds)

		seeds = cloud._get_seed_points(DIRECTION_LEFT)
		expected_seeds = [(0, 20), (10, 5), (10, 35)]
		assert set(seeds) == set(expected_seeds)

		seeds = cloud._get_seed_points(DIRECTION_UP)
		expected_seeds = [(15, 40), (5, 30), (25, 30)]
		assert set(seeds) == set(expected_seeds)

		seeds = cloud._get_seed_points(DIRECTION_DOWN)
		expected_seeds = [(15, 0), (5, 10), (25, 10)]
		assert set(seeds) == set(expected_seeds)


class TestGetSpot:
	def test_corner(self):
		"""Find spots that intersect with occupied rect
		on one corner.
		"""

		cloud = CLOUDS["cross"].clone()
		occ = cloud.get_occupied_rect()
		r1, r2, r3 = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		seed = (20, 35)
		direction = DIRECTION_RIGHT
		spot = cloud._get_spot(rectangle, seed, direction)
		assert spot == R(r2.x + r2.w, r3.y + r3.h, 
							occ.x + occ.w - (r2.x + r2.w) + INF,
							occ.y + occ.h - (r3.y + r3.h) + INF)

		seed = (5, 10)
		direction = DIRECTION_DOWN
		spot = cloud._get_spot(rectangle, seed, direction)
		assert spot == R(occ.x - INF, occ.y - INF, 
							r2.x - occ.x + INF,
							r1.y - occ.y + INF)

	def test_strip(self):
		"""Find spots that run along one axis of occupied 
		rect, being framed by two beams of rects at the 
		side.
		"""
		cloud = CLOUDS["explode"]
		
		r1, r2, r3, r4 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()
		
		seed = (15, 40)
		direction = DIRECTION_RIGHT
		spot = cloud._get_spot(rectangle, seed, direction)
		
		expected_spot = R(r3.x + r3.w, occ.y - INF, 
							r4.x - (r3.x + r3.w), 
							occ.h + 2 * INF)
		assert spot == expected_spot
	
	def test_mortar(self):
		"""Find spots that are bordered by rects on three
		sides.
		"""
		cloud = CLOUDS["c"]
		r1, r2, r3, r4, r5, r6, r7 = cloud.get_rects()

		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()

		seed = (15, 25)
		direction = DIRECTION_RIGHT
		spot = cloud._get_spot(rectangle, seed, direction)

		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							occ.x + occ.w - (r4.x + r4.w) + INF, 
							r6.y - (r2.y + r2.h))

		assert spot == expected_spot
	
	def test_inside(self):
		"""Find spots that are surrounded by rects on all 
		sides.
		"""
		
		cloud = CLOUDS["ring"]

		r1, r2, r3, r4, r5, r6, r7, r8 = cloud.get_rects()
		rectangle = R(0, 0, 20, 20)
		occ = cloud.get_occupied_rect()

		seed = (15, 25)
		direction = DIRECTION_RIGHT
		spot = cloud._get_spot(rectangle, seed, direction)
		
		expected_spot = R(r4.x + r4.w, r2.y + r2.h, 
							r5.x - (r4.x + r4.w), 
							r7.y - (r2.y + r2.h))
							
		assert spot == expected_spot

	def test_outside(self):
		"""Find spots that point outward from occupied rect
		until INF.
		"""
		
		cloud = RectangleCloud([R(0, 0, 10, 10)])
		rectangle = R(0, 0, 10, 10)
		occ = cloud.get_occupied_rect()
		
		seed = (5, 10)
		direction = DIRECTION_UP
		spot = cloud._get_spot(rectangle, seed, direction)
		
		expected_spot = R(occ.x - INF, 10, 10 + 2 * INF, INF)
		